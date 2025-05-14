from django import forms
from .models import Empresa, PeriodoContable, BalanceGeneral, EstadoResultados
from django.core.exceptions import ValidationError
from django.utils import timezone

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={
                'rows': 3,
                'class': 'form-control',
                'placeholder': 'Descripción de la empresa'
            }),
        }
        labels = {
            'nombre': 'Nombre de la Empresa',
            'descripcion': 'Descripción'
        }

class PeriodoContableForm(forms.ModelForm):
    class Meta:
        model = PeriodoContable
        fields = ['nombre', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej. Enero-Diciembre 2023'
            }),
            'fecha_inicio': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
            'fecha_fin': forms.DateInput(attrs={
                'type': 'date',
                'class': 'form-control'
            }),
        }
        labels = {
            'nombre': 'Nombre del Período',
            'fecha_inicio': 'Fecha de Inicio',
            'fecha_fin': 'Fecha de Fin'
        }

    def clean(self):
        cleaned_data = super().clean()
        fecha_inicio = cleaned_data.get('fecha_inicio')
        fecha_fin = cleaned_data.get('fecha_fin')
        
        if fecha_inicio and fecha_fin:
            if fecha_fin < fecha_inicio:
                raise ValidationError('La fecha de fin no puede ser anterior a la fecha de inicio')
            
            if fecha_fin > timezone.now().date():
                raise ValidationError('La fecha de fin no puede ser en el futuro')

class BalanceGeneralForm(forms.ModelForm):
    class Meta:
        model = BalanceGeneral
        exclude = ['periodo']
        widgets = {
            # Activo a Corto Plazo
            'caja_efectivo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'bancos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'inversiones_temporales': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'clientes_nacionales': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'documentos_por_cobrar_corto_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'deudores_diversos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'estimacion_cuentas_incobrables': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'pagos_anticipados': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'inventario': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'antecipo_proveedores': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'otros_activos_corto_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            
            # Activo a Largo Plazo
            'terrenos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'edificios': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'maquinaria_equipo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'vehiculos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'mobiliario_equipo_oficina': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'equipo_computo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'equipo_comunicacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'otros_activos_fijos': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'activos_intangibles': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gastos_organizacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gastos_instalacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'documentos_por_cobrar_largo_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            
            # Pasivo a Corto Plazo
            'cuentas_por_pagar_corto_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'documentos_por_pagar_corto_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'cobros_anticipados_corto_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'iva_trasladado': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'otros_pasivos_corto_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            
            # Pasivo a Largo Plazo
            'cuentas_por_pagar_largo_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'documentos_por_pagar_largo_plazo': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            
            # Capital Contable
            'capital_social': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'capital_variable': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'aportacion_patrimonial': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'reserva_legal': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'utilidad_ejercicios_anteriores': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'perdida_ejercicios_anteriores': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class EstadoResultadosForm(forms.ModelForm):
    class Meta:
        model = EstadoResultados
        exclude = ['periodo']
        widgets = {
            'ventas_netas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'costo_ventas': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gastos_operacion': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'gastos_financieros': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'productos_financieros': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'fluctuacion_cambiaria': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'impuesto_utilidad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'utilidad_ejercicio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'perdida_ejercicio': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }

class BalanceGeneralSimplificadoForm(forms.ModelForm):
    """Formulario simplificado para vista rápida"""
    class Meta:
        model = BalanceGeneral
        fields = [
            'caja_efectivo', 'bancos', 'clientes_nacionales', 'inventario',
            'cuentas_por_pagar_corto_plazo', 'documentos_por_pagar_corto_plazo',
            'capital_social'
        ]
        widgets = {
            field: forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
            for field in fields
        }

class EstadoResultadosSimplificadoForm(forms.ModelForm):
    """Formulario simplificado para vista rápida"""
    class Meta:
        model = EstadoResultados
        fields = ['ventas_netas', 'costo_ventas', 'gastos_operacion', 'impuesto_utilidad']
        widgets = {
            field: forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
            for field in fields
        }