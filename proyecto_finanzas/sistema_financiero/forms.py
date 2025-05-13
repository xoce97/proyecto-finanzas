from django import forms
from .models import Empresa, PeriodoContable, BalanceGeneral, EstadoResultados
from django.core.exceptions import ValidationError
from django.utils import timezone

class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'descripcion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = PeriodoContable
        fields = ['nombre', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
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

class BalanceForm(forms.ModelForm):
    class Meta:
        model = BalanceGeneral
        fields = ['activo_corriente', 'activo_no_corriente', 'pasivo_corriente', 'pasivo_no_corriente', 'patrimonio']
        widgets = {
            'activo_corriente': forms.NumberInput(attrs={'step': '0.01'}),
            'activo_no_corriente': forms.NumberInput(attrs={'step': '0.01'}),
            'pasivo_corriente': forms.NumberInput(attrs={'step': '0.01'}),
            'pasivo_no_corriente': forms.NumberInput(attrs={'step': '0.01'}),
            'patrimonio': forms.NumberInput(attrs={'step': '0.01'}),
        }

class EstadoResultadosForm(forms.ModelForm):
    class Meta:
        model = EstadoResultados
        fields = ['ingresos', 'costo_ventas', 'gastos_operacionales', 'gastos_no_operacionales', 'impuestos']
        widgets = {
            'ingresos': forms.NumberInput(attrs={'step': '0.01'}),
            'costo_ventas': forms.NumberInput(attrs={'step': '0.01'}),
            'gastos_operacionales': forms.NumberInput(attrs={'step': '0.01'}),
            'gastos_no_operacionales': forms.NumberInput(attrs={'step': '0.01'}),
            'impuestos': forms.NumberInput(attrs={'step': '0.01'}),
        }