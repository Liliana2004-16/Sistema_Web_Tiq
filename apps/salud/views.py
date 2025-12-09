from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.decorators import login_required
from apps.users.decorators import role_required
from .models import EventoSanitario, Inseminacion, ConfirmacionGestacion
from .forms import EventoSanitarioForm, InseminacionForm, ConfirmacionGestacionForm
from apps.ganaderia.models import Animal
from apps.ganaderia.services import AnimalService
import openpyxl
from datetime import date
from .services import EventoSanitarioService, InseminacionService, GestacionService


def evento_sanitario_list(request):
    mes = request.GET.get("mes")
    eventos = EventoSanitario.objects.all()

    if mes:
        eventos = eventos.filter(fecha__month=mes)

    return render(request, "salud/evento_sanitario_list.html", {
        "eventos": eventos
    })


@login_required
@role_required("Gerente", "Auxiliar administrativa", "Administrador Finca")
def evento_sanitario_create(request):

    if request.method == "POST":
        form = EventoSanitarioForm(request.POST)
        if form.is_valid():

            EventoSanitarioService.registrar_evento_sanitario(
                fecha=form.cleaned_data["fecha"],
                animal=form.cleaned_data["animal"],
                diagnostico=form.cleaned_data["diagnostico"],
                tratamiento=form.cleaned_data["tratamiento"],
                responsable=form.cleaned_data["responsable"],
                sintomas=form.cleaned_data.get("sintomas")
            )

            messages.success(request, "Evento sanitario registrado exitosamente.")
            return redirect("salud:evento_sanitario_list")
    else:
        form = EventoSanitarioForm()

    return render(request, "salud/evento_sanitario_form.html", {"form": form})

def buscar_animal(request):
    arete = request.GET.get("arete") or request.GET.get("numero_arete")

    try:
        animal = AnimalService.get_by_arete(arete)
        edad = (date.today() - animal.fecha_nacimiento).days
        
        return JsonResponse({
            "id": animal.id,
            "nombre": animal.nombre,
            "edad": edad,
            "estado": animal.estado
        })
    except Exception:
        return JsonResponse({"error": "No encontrado"}, status=404)



def export_eventos_excel(request):
    mes = request.GET.get("mes")

    eventos = EventoSanitario.objects.all()
    if mes:
        eventos = eventos.filter(fecha__month=mes)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Eventos Sanitarios"

    ws.append(["Fecha", "Arete", "Animal", "Diagnóstico", "Tratamiento", "Responsable", "Sintomas"])

    for e in eventos:
        ws.append([
            e.fecha,
            e.animal.numero_arete,
            e.animal.nombre,
            e.diagnostico,
            e.tratamiento,
            e.responsable,
            e.sintomas or "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = "attachment; filename=eventos_sanitarios.xlsx"
    wb.save(response)
    return response
@login_required
@role_required("Gerente", "Auxiliar administrativa", "Administrador Finca")
def evento_sanitario_edit(request, pk):
    evento = get_object_or_404(EventoSanitario, pk=pk)

    if request.method == "POST":
        form = EventoSanitarioForm(request.POST, instance=evento)

        if form.is_valid():
            form.save()
            messages.success(request, "Evento sanitario actualizado correctamente.")
            return redirect("salud:evento_sanitario_list")

    else:
        form = EventoSanitarioForm(instance=evento)

    return render(request, "salud/evento_sanitario_form.html", {
        "form": form,
        "edit": True
    })
@login_required
@role_required("Gerente", "Auxiliar administrativa", "Administrador Finca")
def evento_sanitario_delete(request, pk):
    evento = get_object_or_404(EventoSanitario, pk=pk)

    if request.method == "POST":
        evento.delete()
        messages.success(request, "Evento sanitario eliminado exitosamente.")
        return redirect("salud:evento_sanitario_list")

    return render(request, "salud/evento_sanitario_confirm_delete.html", {
        "evento": evento
    })

@login_required
@role_required("Gerente", "Administrador finca")
def inseminacion_create(request):
    form = InseminacionForm()

    if request.method == "POST":
        form = InseminacionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            numero_arete = request.POST.get("numero_arete")

            try:
                animal = AnimalService.get_by_arete(numero_arete)

                InseminacionService.registrar_inseminacion(
                    fecha=data['fecha'],
                    tipo_semen=data['tipo_semen'],
                    animal=animal,
                    inseminador=data['inseminador'],
                    usuario_responsable=request.user
                )

                messages.success(request, "Registro de inseminación guardado correctamente.")
                return redirect("salud:inseminacion_list")

            except Exception as e:
                messages.error(request, str(e))

    return render(request, "salud/inseminacion_form.html", {"form": form})


@login_required
def inseminacion_list(request):
    registros = Inseminacion.objects.select_related("responsable").order_by('-fecha')
    return render(request, "salud/inseminacion_list.html", {"registros": registros})

@login_required
@role_required("Gerente", "Administrador finca")
def inseminacion_edit(request, pk):
    inseminacion = get_object_or_404(Inseminacion, pk=pk)
    form = InseminacionForm(instance=inseminacion)

    if request.method == "POST":
        form = InseminacionForm(request.POST, instance=inseminacion)
        if form.is_valid():
            form.save()
            messages.success(request, "Inseminación actualizada correctamente.")
            return redirect("salud:inseminacion_list")

    return render(request, "salud/inseminacion_form.html", {"form": form})

@login_required
@role_required("Gerente", "Administrador finca")
def inseminacion_delete(request, pk):
    inseminacion = get_object_or_404(Inseminacion, pk=pk)
    inseminacion.delete()
    messages.success(request, "Registro eliminado correctamente.")
    return redirect("salud:inseminacion_list")


@login_required
@role_required("Gerente", "Administrador finca")
def gestacion_pendientes(request):
    pendientes = GestacionService.obtener_inseminaciones_pendientes()

    return render(request, "salud/gestacion_pendientes.html", {
        "pendientes": pendientes
    })

@login_required
@role_required("Gerente", "Administrador finca")
def confirmar_gestacion(request, id_inseminacion):
    inseminacion = get_object_or_404(Inseminacion, id=id_inseminacion)
    form = ConfirmacionGestacionForm()

    if request.method == "POST":
        form = ConfirmacionGestacionForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data

            try:
                GestacionService.confirmar_gestacion(
                    inseminacion=inseminacion,
                    fecha_confirmacion=data['fecha_confirmacion'],
                    metodo_diagnostico=data['metodo_diagnostico'],
                    resultado=data['resultado'],
                    responsable=data['responsable'],
                    observaciones=data.get('observaciones')
                )

                messages.success(request, "Confirmación de gestación registrada exitosamente.")
                return redirect("salud:gestacion_pendientes")

            except ValidationError as e:
                messages.error(request, str(e))

    return render(request, "salud/confirmar_gestacion_form.html", {
        "form": form,
        "inseminacion": inseminacion
    })

@login_required
@role_required("Gerente", "Administrador finca")
def gestacion_historial(request):

    historial = ConfirmacionGestacion.objects.all()
    mes = request.GET.get("mes", "")
    estado = request.GET.get("estado", "")
    finca = request.GET.get("finca", "")
    
    if mes and mes.strip():
        try:
            mes_int = int(mes)
            historial = historial.filter(fecha_confirmacion__month=mes_int)
        except ValueError:
            mes = "" 

    if estado and estado.strip():
        historial = historial.filter(resultado=estado)

    if finca and finca.strip():
        historial = historial.filter(inseminacion__animal__finca_id=finca)

    historial = historial.select_related(
        'inseminacion__animal'
    ).order_by('-fecha_confirmacion')

    return render(request, "salud/historial_confirmaciones.html", {
        "historial": historial,
        "mes_seleccionado": mes,
        "estado_seleccionado": estado,
        "finca_seleccionada": finca,
    })