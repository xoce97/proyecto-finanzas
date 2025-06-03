from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponse
from .models import Periodo, CuentaContable, MovimientoFinanciero
from .forms import PeriodoForm, CuentaContableForm, MovimientoFinancieroForm, MovimientoFinancieroFormSet, ImportarMovimientosForm, ImportarMovimientosXMLForm
import csv
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib import messages
import xml.etree.ElementTree as ET

# Create your views here.
def home(request):
    return render(request, 'finanzas/home.html')

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


class CuentaContableListView(ListView):
    model = CuentaContable
    template_name = 'finanzas/cuenta_list.html'
    context_object_name = 'cuentas'

class CuentaContableCreateView(CreateView):
    model = CuentaContable
    form_class = CuentaContableForm
    template_name = 'finanzas/cuenta_form.html'
    success_url = reverse_lazy('finanzas:cuenta_list')

class CuentaContableUpdateView(UpdateView):
    model = CuentaContable
    form_class = CuentaContableForm
    template_name = 'finanzas/cuenta_form.html'
    success_url = reverse_lazy('finanzas:cuenta_list')

class CuentaContableDeleteView(DeleteView):
    model = CuentaContable
    template_name = 'finanzas/cuenta_confirm_delete.html'
    success_url = reverse_lazy('finanzas:cuenta_list')


class MovimientoFinancieroCreateView(CreateView):
    model = MovimientoFinanciero
    form_class = MovimientoFinancieroForm
    template_name = 'finanzas/movimiento_form.html'
    success_url = reverse_lazy('finanzas:movimiento_list')

class MovimientoFinancieroListView(ListView):
    model = MovimientoFinanciero
    template_name = 'finanzas/movimiento_list.html'
    context_object_name = 'movimientos'




def captura_masiva_movimientos(request, periodo_id):
    periodo = Periodo.objects.get(pk=periodo_id)
    cuentas = CuentaContable.objects.all()
    movimientos = []
    for cuenta in cuentas:
        obj, created = MovimientoFinanciero.objects.get_or_create(periodo=periodo, cuenta=cuenta)
        movimientos.append(obj)

    MovimientoFormSet = MovimientoFinancieroFormSet(queryset=MovimientoFinanciero.objects.filter(periodo=periodo))

    if request.method == 'POST':
        formset = MovimientoFinancieroFormSet(request.POST, queryset=MovimientoFinanciero.objects.filter(periodo=periodo))
        if formset.is_valid():
            formset.save()
            return redirect('finanzas:movimiento_list')
    else:
        formset = MovimientoFinancieroFormSet(queryset=MovimientoFinanciero.objects.filter(periodo=periodo))

    cuentas_info = [mov.cuenta for mov in movimientos]
    return render(request, 'finanzas/captura_masiva_movimientos.html', {
        'formset': formset,
        'periodo': periodo,
        'cuentas': cuentas_info,
    })


def importar_movimientos_csv(request):
    if request.method == 'POST':
        form = ImportarMovimientosForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo']
            decoded_file = archivo.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)
            errores = []
            for i, row in enumerate(reader, start=2):
                try:
                    periodo = Periodo.objects.get(nombre=row['periodo'])
                    cuenta = CuentaContable.objects.get(codigo=row['codigo_cuenta'])
                    monto = float(row['monto'])
                    MovimientoFinanciero.objects.update_or_create(
                        periodo=periodo,
                        cuenta=cuenta,
                        defaults={'monto': monto}
                    )
                except Exception as e:
                    errores.append(f"Error en la fila {i}: {e}")
            if errores:
                messages.warning(request, "Algunos datos no se importaron:\n" + "\n".join(errores))
            else:
                messages.success(request, "Importación exitosa")
            return redirect('finanzas:movimiento_list')
    else:
        form = ImportarMovimientosForm()
    return render(request, 'finanzas/importar_movimientos.html', {'form': form})


def importar_movimientos_xml(request):
    if request.method == 'POST':
        form = ImportarMovimientosXMLForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = form.cleaned_data['archivo']
            errores = []
            try:
                tree = ET.parse(archivo)
                root = tree.getroot()
                for i, movimiento in enumerate(root.findall('movimiento'), start=1):
                    periodo_nombre = movimiento.find('periodo').text
                    codigo_cuenta = movimiento.find('codigo_cuenta').text
                    monto = movimiento.find('monto').text
                    try:
                        periodo = Periodo.objects.get(nombre=periodo_nombre)
                        cuenta = CuentaContable.objects.get(codigo=codigo_cuenta)
                        MovimientoFinanciero.objects.update_or_create(
                            periodo=periodo,
                            cuenta=cuenta,
                            defaults={'monto': monto}
                        )
                    except Exception as e:
                        errores.append(f"Error en movimiento {i}: {e}")
                if errores:
                    messages.warning(request, "Algunos datos no se importaron correctamente:\n" + "\n".join(errores))
                else:
                    messages.success(request, "Importación exitosa")
            except Exception as e:
                messages.error(request, f"Error al procesar el archivo XML: {e}")
            return redirect('finanzas:movimiento_list')
    else:
        form = ImportarMovimientosXMLForm()
    return render(request, 'finanzas/importar_movimientos_xml.html', {'form': form})