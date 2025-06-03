from django import forms
from .models import Periodo, CuentaContable, MovimientoFinanciero

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['nombre', 'fecha_inicio', 'fecha_fin']

class CuentaContableForm(forms.ModelForm):
    class Meta:
        model = CuentaContable
        fields = ['nombre', 'codigo', 'clase', 'nivel', 'padre']

class MovimientoFinancieroForm(forms.ModelForm):
    class Meta:
        model = MovimientoFinanciero
        fields = ['cuenta', 'periodo', 'monto']
