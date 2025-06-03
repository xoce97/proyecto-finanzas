from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Módulo Finanzas funcionando.")


from django.shortcuts import render, redirect, get_object_or_404
from .models import Periodo, CuentaContable, MovimientoFinanciero
from .forms import PeriodoForm, CuentaContableForm, MovimientoFinancieroForm

# Listar periodos
def periodos_list(request):
    periodos = Periodo.objects.all()
    return render(request, 'finanzas/periodos_list.html', {'periodos': periodos})

# Crear periodo
def periodo_create(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('finanzas:periodos_list')
    else:
        form = PeriodoForm()
    return render(request, 'finanzas/periodo_form.html', {'form': form})

# Editar periodo
def periodo_edit(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    if request.method == 'POST':
        form = PeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            form.save()
            return redirect('finanzas:periodos_list')
    else:
        form = PeriodoForm(instance=periodo)
    return render(request, 'finanzas/periodo_form.html', {'form': form})
