from django import forms
from .models import ReporteGenerado

class ReporteGeneradoForm(forms.ModelForm):
    class Meta:
        model = ReporteGenerado
        fields = ['nombre', 'usuario', 'archivo']
