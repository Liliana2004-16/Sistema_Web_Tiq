from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from .services import FincaService
from .forms import FincaForm

service = FincaService()

def finca_list(request):
    fincas = service.listar_fincas()
    return render(request, 'finca/list.html', {'fincas': fincas})

def finca_create(request):
    if request.method == 'POST':
        form = FincaForm(request.POST)
        if form.is_valid():
            service.crear_finca(form.cleaned_data)
            messages.success(request, "Finca creada correctamente.")
            return redirect('finca:list')
    else:
        form = FincaForm()
    return render(request, 'finca/form.html', {'form': form, 'titulo': 'Registrar Finca'})

def finca_update(request, id):
    finca = get_object_or_404(service.listar_fincas(), id=id)

    if request.method == 'POST':
        form = FincaForm(request.POST, instance=finca)
        if form.is_valid():
            service.actualizar_finca(id, form.cleaned_data)
            messages.success(request, "Finca actualizada.")
            return redirect('finca:list')

    else:
        form = FincaForm(instance=finca)

    return render(request, 'finca/form.html', {'form': form, 'titulo': 'Editar Finca'})

def finca_delete(request, id):
    finca = get_object_or_404(service.listar_fincas(), id=id)

    if request.method == "POST":
        service.eliminar_finca(id)
        messages.success(request, "Finca eliminada.")
        return redirect('finca:list')

    return render(request, 'finca/delete.html', {'finca': finca})


