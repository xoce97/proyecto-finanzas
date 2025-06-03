from django.shortcuts import render, redirect
from .models import EscenarioSimulacion, VariableEscenario
from .forms import EscenarioSimulacionForm, VariableEscenarioForm
from django.http import HttpResponse
# Create your views here.




def lista_escenarios(request):
    escenarios = EscenarioSimulacion.objects.all()
    return render(request, 'simulacion/lista_escenarios.html', {'escenarios': escenarios})

def crear_escenario(request):
    if request.method == 'POST':
        form = EscenarioSimulacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_escenarios')
    else:
        form = EscenarioSimulacionForm()
    return render(request, 'simulacion/form_escenario.html', {'form': form})

def crear_variable(request, escenario_id):
    escenario = EscenarioSimulacion.objects.get(pk=escenario_id)
    if request.method == 'POST':
        form = VariableEscenarioForm(request.POST)
        if form.is_valid():
            variable = form.save(commit=False)
            variable.escenario = escenario
            variable.save()
            return redirect('lista_escenarios')
    else:
        form = VariableEscenarioForm()
    return render(request, 'simulacion/form_variable.html', {'form': form, 'escenario': escenario})
