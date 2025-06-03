from django import forms
from .models import EscenarioSimulacion, VariableEscenario

class EscenarioSimulacionForm(forms.ModelForm):
    class Meta:
        model = EscenarioSimulacion
        fields = ['nombre', 'descripcion']

class VariableEscenarioForm(forms.ModelForm):
    class Meta:
        model = VariableEscenario
        fields = ['nombre', 'valor_original', 'valor_modificado']
