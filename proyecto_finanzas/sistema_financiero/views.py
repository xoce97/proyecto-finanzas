from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Empresa, PeriodoContable, BalanceGeneral, EstadoResultados
from .forms import EmpresaForm, PeriodoForm, BalanceForm, EstadoResultadosForm
from decimal import Decimal
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors



def lista_empresas(request):
    empresas = Empresa.objects.all()
    return render(request, 'sistema_financiero/empresas/lista.html', {'empresas': empresas})

def crear_empresa(request):
    if request.method == 'POST':
        form = EmpresaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Empresa creada exitosamente')
            return redirect('lista_empresas')
    else:
        form = EmpresaForm()
    return render(request, 'sistema_financiero/empresas/crear.html', {'form': form})

def detalle_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    periodos = empresa.periodocontable_set.all().order_by('-fecha_fin')
    
    # Obtener el último balance si existe
    ultimo_balance = None
    ultimo_estado = None
    if periodos.exists():
        ultimo_periodo = periodos.first()
        ultimo_balance = BalanceGeneral.objects.filter(periodo=ultimo_periodo).first()
        ultimo_estado = EstadoResultados.objects.filter(periodo=ultimo_periodo).first()
    
    return render(request, 'sistema_financiero/empresas/detalle.html', {
        'empresa': empresa,
        'periodos': periodos,
        'ultimo_balance': ultimo_balance,
        'ultimo_estado': ultimo_estado
    })


def crear_periodo(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            periodo = form.save(commit=False)
            periodo.empresa = empresa
            periodo.save()
            messages.success(request, 'Periodo contable creado exitosamente')
            return redirect('detalle_empresa', empresa_id=empresa.id)
    else:
        form = PeriodoForm()
    return render(request, 'sistema_financiero/periodos/crear.html', {
        'form': form,
        'empresa': empresa
    })


def detalle_periodo(request, periodo_id):
    periodo = get_object_or_404(PeriodoContable, pk=periodo_id)
    balance = BalanceGeneral.objects.filter(periodo=periodo).first()
    estado_resultados = EstadoResultados.objects.filter(periodo=periodo).first()
    
    # Cálculo de razones financieras básicas
    razones = {}
    if balance and estado_resultados:
        # Razones de liquidez
        if balance.pasivo_corriente != 0:
            razones['corriente'] = balance.activo_corriente / balance.pasivo_corriente
            razones['acida'] = (balance.activo_corriente) / balance.pasivo_corriente  # Asumiendo que no hay inventario separado
        
        # Razones de rentabilidad
        if estado_resultados.ingresos != 0:
            razones['margen_bruto'] = (estado_resultados.utilidad_bruta / estado_resultados.ingresos) * 100
            razones['margen_neto'] = (estado_resultados.utilidad_neta / estado_resultados.ingresos) * 100
    
    return render(request, 'sistema_financiero/periodos/detalle.html', {
        'periodo': periodo,
        'balance': balance,
        'estado_resultados': estado_resultados,
        'razones': razones,
        'empresa': periodo.empresa
    })

def crear_balance(request, periodo_id):
    periodo = get_object_or_404(PeriodoContable, pk=periodo_id)
    if request.method == 'POST':
        form = BalanceForm(request.POST)
        if form.is_valid():
            balance = form.save(commit=False)
            balance.periodo = periodo
            balance.save()
            messages.success(request, 'Balance general creado exitosamente')
            return redirect('detalle_periodo', periodo_id=periodo.id)
    else:
        form = BalanceForm()
    return render(request, 'sistema_financiero/balances/crear.html', {
        'form': form,
        'periodo': periodo
    })

def crear_estado_resultados(request, periodo_id):
    periodo = get_object_or_404(PeriodoContable, pk=periodo_id)
    if request.method == 'POST':
        form = EstadoResultadosForm(request.POST)
        if form.is_valid():
            estado = form.save(commit=False)
            estado.periodo = periodo
            estado.save()
            messages.success(request, 'Estado de resultados creado exitosamente')
            return redirect('detalle_periodo', periodo_id=periodo.id)
    else:
        form = EstadoResultadosForm()
    return render(request, 'sistema_financiero/estados/crear.html', {
        'form': form,
        'periodo': periodo
    })



def analisis_financiero(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    periodos = PeriodoContable.objects.filter(empresa=empresa).order_by('fecha_inicio')
    
    # Obtener balances y estados de resultados para cada período
    datos = []
    for periodo in periodos:
        try:
            balance = BalanceGeneral.objects.get(periodo=periodo)
            estado = EstadoResultados.objects.get(periodo=periodo)
            
            # Cálculo de razones financieras
            razon_corriente = balance.activo_corriente / balance.pasivo_corriente if balance.pasivo_corriente != 0 else 0
            prueba_acida = (balance.activo_corriente - 0) / balance.pasivo_corriente if balance.pasivo_corriente != 0 else 0  # Asumiendo que no tenemos inventario separado
            margen_bruto = estado.utilidad_bruta / estado.ingresos if estado.ingresos != 0 else 0
            margen_operacional = estado.utilidad_operacional / estado.ingresos if estado.ingresos != 0 else 0
            margen_neto = estado.utilidad_neta / estado.ingresos if estado.ingresos != 0 else 0
            
            datos.append({
                'periodo': periodo,
                'balance': balance,
                'estado': estado,
                'razon_corriente': razon_corriente,
                'prueba_acida': prueba_acida,
                'margen_bruto': margen_bruto * 100,  # Convertir a porcentaje
                'margen_operacional': margen_operacional * 100,
                'margen_neto': margen_neto * 100,
                'capital_neto_trabajo': balance.capital_neto_trabajo,
            })
        except (BalanceGeneral.DoesNotExist, EstadoResultados.DoesNotExist):
            continue
    
    return render(request, 'sistema_financiero/analisis/analisis.html', {
        'empresa': empresa,
        'datos': datos,
    })

def gestion_capital_trabajo(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    periodos = PeriodoContable.objects.filter(empresa=empresa).order_by('fecha_inicio')
    
    datos = []
    for periodo in periodos:
        try:
            balance = BalanceGeneral.objects.get(periodo=periodo)
            datos.append({
                'periodo': periodo,
                'capital_neto': balance.capital_neto_trabajo,
                'activo_corriente': balance.activo_corriente,
                'pasivo_corriente': balance.pasivo_corriente,
            })
        except BalanceGeneral.DoesNotExist:
            continue
    
    return render(request, 'sistema_financiero/capital/gestion.html', {
        'empresa': empresa,
        'datos': datos,
    })


def simulacion_capital_trabajo(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    ultimo_periodo = PeriodoContable.objects.filter(empresa=empresa).order_by('-fecha_fin').first()
    
    if not ultimo_periodo:
        messages.warning(request, 'No hay períodos contables para esta empresa')
        return redirect('detalle_empresa', empresa_id=empresa.id)
    
    try:
        ultimo_balance = BalanceGeneral.objects.get(periodo=ultimo_periodo)
        ultimo_estado = EstadoResultados.objects.get(periodo=ultimo_periodo)
    except (BalanceGeneral.DoesNotExist, EstadoResultados.DoesNotExist):
        messages.warning(request, 'No hay datos financieros para el último período')
        return redirect('detalle_empresa', empresa_id=empresa.id)
    
    # Valores iniciales del formulario
    initial_data = {
        'activo_corriente': ultimo_balance.activo_corriente,
        'pasivo_corriente': ultimo_balance.pasivo_corriente,
        'ingresos': ultimo_estado.ingresos,
    }
    
    if request.method == 'POST':
        # Procesar la simulación
        activo_corriente = Decimal(request.POST.get('activo_corriente', ultimo_balance.activo_corriente))
        pasivo_corriente = Decimal(request.POST.get('pasivo_corriente', ultimo_balance.pasivo_corriente))
        ingresos = Decimal(request.POST.get('ingresos', ultimo_estado.ingresos))
        
        # Calcular resultados de la simulación
        capital_neto = activo_corriente - pasivo_corriente
        razon_corriente = activo_corriente / pasivo_corriente if pasivo_corriente != 0 else 0
        
        return render(request, 'sistema_financiero/simulacion/resultado.html', {
            'empresa': empresa,
            'periodo': ultimo_periodo,
            'activo_corriente': activo_corriente,
            'pasivo_corriente': pasivo_corriente,
            'ingresos': ingresos,
            'capital_neto': capital_neto,
            'razon_corriente': razon_corriente,
            'variacion_capital': capital_neto - ultimo_balance.capital_neto_trabajo,
            'variacion_razon': razon_corriente - (ultimo_balance.activo_corriente / ultimo_balance.pasivo_corriente if ultimo_balance.pasivo_corriente != 0 else 0),
        })
    
    return render(request, 'sistema_financiero/simulacion/formulario.html', {
        'empresa': empresa,
        'periodo': ultimo_periodo,
        'initial_data': initial_data,
    })


def exportar_analisis_pdf(request, empresa_id):
    empresa = get_object_or_404(Empresa, pk=empresa_id)
    periodos = PeriodoContable.objects.filter(empresa=empresa).order_by('fecha_inicio')
    
    # Crear el objeto HttpResponse con las cabeceras PDF correctas.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="analisis_{empresa.nombre}.pdf"'
    
    # Crear el objeto PDF, usando el objeto response como su "archivo".
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    elements.append(Paragraph(f"Análisis Financiero - {empresa.nombre}", styles['Title']))
    elements.append(Paragraph("Resumen de indicadores financieros", styles['Heading2']))
    
    # Preparar datos para la tabla
    data = [['Período', 'Razón Corriente', 'Prueba Ácida', 'Margen Bruto', 'Margen Operacional', 'Margen Neto', 'Capital Neto']]
    
    for periodo in periodos:
        try:
            balance = BalanceGeneral.objects.get(periodo=periodo)
            estado = EstadoResultados.objects.get(periodo=periodo)
            
            razon_corriente = balance.activo_corriente / balance.pasivo_corriente if balance.pasivo_corriente != 0 else 0
            prueba_acida = (balance.activo_corriente - 0) / balance.pasivo_corriente if balance.pasivo_corriente != 0 else 0
            margen_bruto = (estado.utilidad_bruta / estado.ingresos * 100) if estado.ingresos != 0 else 0
            margen_operacional = (estado.utilidad_operacional / estado.ingresos * 100) if estado.ingresos != 0 else 0
            margen_neto = (estado.utilidad_neta / estado.ingresos * 100) if estado.ingresos != 0 else 0
            
            data.append([
                periodo.nombre,
                f"{razon_corriente:.2f}",
                f"{prueba_acida:.2f}",
                f"{margen_bruto:.2f}%",
                f"{margen_operacional:.2f}%",
                f"{margen_neto:.2f}%",
                f"${balance.capital_neto_trabajo:,.2f}",
            ])
        except (BalanceGeneral.DoesNotExist, EstadoResultados.DoesNotExist):
            continue
    
    # Crear la tabla y aplicar estilos
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    
    elements.append(table)
    
    # Generar el PDF
    doc.build(elements)
    
    return response