# apps/ganaderia/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Animal, Pesaje, Parto, ProduccionLeche, EventoSalida
from .forms import PesajeForm, PartoForm, ProduccionForm, EventoSalidaForm, TrasladoForm
from .services import AnimalService
from apps.users.decorators import role_required  # vamos a crear este decorador en users
from django.core.paginator import Paginator
from openpyxl import Workbook
from django.http import HttpResponse
from apps.ganaderia.models import Finca

@login_required
def animales_list(request):
    q = request.GET.get('q')
    if q:
        animales = Animal.objects.filter(numero_arete__icontains=q) | Animal.objects.filter(nombre__icontains=q)
    else:
        animales = Animal.objects.all()
    return render(request, 'ganaderia/animales_list.html', {'animales': animales})

@login_required
def animal_detail(request, pk):
    animal = get_object_or_404(Animal, pk=pk)
    return render(request, 'ganaderia/animal_detail.html', {'animal': animal})

@login_required
@role_required("Gerente", "Administrador Finca")

def registrar_pesaje_view(request):
    if request.method == 'POST':
        form = PesajeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            try:
                pesaje = AnimalService.registrar_pesaje(
                    numero_arete=data['numero_arete'],
                    fecha=data['fecha'],
                    peso=data['peso'],
                    finca=data['finca'],
                    usuario=request.user
                )
                messages.success(request, "Pesaje registrado exitosamente")
                return redirect('ganaderia:registrar_pesaje')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = PesajeForm()
    return render(request, 'ganaderia/registrar_pesaje.html', {'form': form})

@login_required
@role_required("Gerente", "Administrador Finca")
def partos_list(request):

    madre_filter = request.GET.get('madre', '')

    partos = Parto.objects.select_related("madre", "cria", "finca")

    if madre_filter:
        partos = partos.filter(madre__numero_arete__icontains=madre_filter)

    paginator = Paginator(partos.order_by('-fecha_nacimiento'), 10)
    page = request.GET.get('page')
    partos_page = paginator.get_page(page)

    context = {
        "partos": partos_page,
        "madre_filter": madre_filter
    }

    return render(request, "ganaderia/partos_list.html", context)


@login_required
@role_required("Gerente", "Administrador Finca")
def registrar_parto_view(request):

    if request.method == 'POST':

        madre_arete = request.POST.get("madre")
        fecha = request.POST.get("fecha_nacimiento")
        cria_arete = request.POST.get("numero_arete_cria")
        nombre_cria = request.POST.get("nombre_cria")
        sexo = request.POST.get("sexo")
        raza = request.POST.get("raza")
        peso = request.POST.get("peso")
        finca_id = request.POST.get("finca")

        # Validación madre
        try:
            madre = Animal.objects.get(numero_arete=madre_arete)
        except Animal.DoesNotExist:
            messages.error(request, "La madre no existe.")
            return redirect("ganaderia:registrar_parto")

        # Validación cría duplicada
        if Animal.objects.filter(numero_arete=cria_arete).exists():
            messages.error(request, "Ya existe un animal con ese número de arete.")
            return redirect("ganaderia:registrar_parto")

        # Crear cría
        cria = Animal.objects.create(
            numero_arete=cria_arete,
            nombre=nombre_cria,
            fecha_nacimiento=fecha,
            sexo=sexo,
            raza=raza,
            madre=madre,
            finca_id=finca_id,
            estado="activo"
        )

        # Registrar parto
        Parto.objects.create(
            fecha_nacimiento=fecha,
            madre=madre,
            cria=cria,
            finca_id=finca_id,
            peso=float(peso) if peso else None,
            raza=raza,
            sexo=sexo,
            created_by=request.user
        )

        messages.success(request, "Parto registrado exitosamente.")
        return redirect("ganaderia:partos_list")

    # GET → Mostrar formulario
    fincas = Finca.objects.all()
    madres = Animal.objects.filter(sexo="F")

    return render(request, "ganaderia/registrar_parto.html", {
        "fincas": fincas,
        "madres": madres
    })

@login_required
@role_required("Gerente", "Administrador Finca")
def partos_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Partos"

    # Encabezados
    ws.append([
        "Madre", "Fecha Nacimiento Cría", "Nombre Cría",
        "Arete Cría", "Finca", "Raza", "Sexo", "Peso (kg)"
    ])

    # Datos
    for p in Parto.objects.select_related("madre", "cria", "finca"):
        ws.append([
            p.madre.numero_arete,
            p.fecha_nacimiento.strftime("%d/%m/%Y"),
            p.cria.nombre,
            p.cria.numero_arete,
            p.finca.nombre,
            p.raza,
            p.sexo,
            p.peso,
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="partos.xlsx"'
    wb.save(response)
    return response

@login_required
@role_required("Gerente", "Administrador Finca")
def registrar_produccion_view(request, turno=None):
    if request.method == 'POST':
        form = ProduccionForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                prod = AnimalService.registrar_produccion(
                    numero_arete=cd['numero_arete'],
                    fecha=cd['fecha'],
                    peso_am=cd.get('peso_am'),
                    peso_pm=cd.get('peso_pm'),
                    usuario=request.user
                )
                messages.success(request, "Producción registrada exitosamente")
                return redirect('ganaderia:registrar_produccion')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = ProduccionForm()
    return render(request, 'ganaderia/registrar_produccion.html', {'form': form})

@login_required
@role_required("Gerente", "Administrador Finca")
def registrar_evento_salida_view(request):
    if request.method == 'POST':
        form = EventoSalidaForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            try:
                evento = AnimalService.registrar_evento_salida(
                    numero_arete=cd['numero_arete'],
                    fecha=cd['fecha'],
                    tipo_evento=cd['tipo_evento'],
                    usuario=request.user,
                    observaciones=cd.get('observaciones','')
                )
                messages.success(request, "Evento de salida registrado exitosamente")
                return redirect('ganaderia:eventos_salida')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = EventoSalidaForm()
    return render(request, 'ganaderia/evento_salida.html', {'form': form})

@login_required
def traslados_view(request):
    if request.method == 'POST':
        form = TrasladoForm(request.POST)
        if form.is_valid():
            aretes = form.cleaned_data['lista_aretes']
            finca_dest = form.cleaned_data['finca_destino']
            try:
                traslados = AnimalService.trasladar_animales(aretes, finca_dest, usuario=request.user)
                messages.success(request, "Traslado(s) realizado(s) exitosamente")
                return redirect('ganaderia:traslados')
            except Exception as e:
                form.add_error(None, str(e))
    else:
        form = TrasladoForm()
    return render(request, 'ganaderia/traslados.html', {'form': form})
