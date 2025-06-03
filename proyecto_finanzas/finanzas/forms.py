from django import forms
from .models import Periodo, CuentaContable, MovimientoFinanciero

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['nombre', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

class CuentaContableForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = ['nombre', 'codigo', 'clase', 'nivel', 'padre']

class MovimientoFinancieroForm(forms.ModelForm):
    class Meta:
        model = MovimientoFinanciero
        fields = ['cuenta', 'periodo', 'monto']
