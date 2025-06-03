from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import IndicadorCapitalTrabajo, ResultadoIndicador
from .forms import IndicadorCapitalTrabajoForm, ResultadoIndicadorForm


def index(request):
    return HttpResponse("Módulo Capital de Trabajo funcionando.")



def lista_indicadores(request):
    indicadores = IndicadorCapitalTrabajo.objects.all()
    return render(request, 'capital_trabajo/lista_indicadores.html', {'indicadores': indicadores})

def crear_indicador(request):
    if request.method == 'POST':
        form = IndicadorCapitalTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_indicadores')
    else:
        form = IndicadorCapitalTrabajoForm()
    return render(request, 'capital_trabajo/form_indicador.html', {'form': form})

def crear_resultado(request):
    if request.method == 'POST':
        form = ResultadoIndicadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_indicadores')
    else:
        form = ResultadoIndicadorForm()
    return render(request, 'capital_trabajo/form_resultado.html', {'form': form})
