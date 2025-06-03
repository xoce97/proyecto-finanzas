from django import forms
from .models import IndicadorCapitalTrabajo, ResultadoIndicador

class IndicadorCapitalTrabajoForm(forms.ModelForm):
    class Meta:
        model = IndicadorCapitalTrabajo
        fields = ['nombre', 'descripcion']

class ResultadoIndicadorForm(forms.ModelForm):
    class Meta:
        model = ResultadoIndicador
        fields = ['indicador', 'periodo', 'valor']
