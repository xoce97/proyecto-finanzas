from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import ReporteGenerado
from .forms import ReporteGeneradoForm




def lista_reportes(request):
    reportes = ReporteGenerado.objects.all()
    return render(request, 'reportes/lista_reportes.html', {'reportes': reportes})

def subir_reporte(request):
    if request.method == 'POST':
        form = ReporteGeneradoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_reportes')
    else:
        form = ReporteGeneradoForm()
    return render(request, 'reportes/form_reporte.html', {'form': form})
