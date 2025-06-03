from django import forms
from .models import Periodo, CuentaContable, MovimientoFinanciero
from .models import CuentaContable
from django.forms import modelformset_factory

CUENTA_CHOICES = [
    # ---- ACTIVO ----
    ('A', 'Activo'),
    ('AC', 'Activo a corto plazo'),
    ('CA', 'Caja'),
    ('CAEF', 'Caja y efectivo'),
    ('BAN', 'Bancos'),
    ('INV', 'Inventarios'),
    ('ACTD', 'Activo a corto plazo disponible'),
    ('ACTR', 'Activo a corto plazo realizable'),
    ('ACC', 'Activo a corto plazo circulante'),
    ('ALP', 'Activo a largo plazo'),
    ('INM', 'Inmuebles'),
    ('MAQ', 'Maquinaria'),
    ('EQ', 'Equipo'),
    ('DEP', 'Depreciación acumulada'),
    ('AA', 'Activo a largo plazo'),
    ('OTOA', 'Otros activos'),

    # ---- PASIVO ----
    ('P', 'Pasivo'),
    ('PC', 'Pasivo a corto plazo'),
    ('PCCP', 'Cuentas por pagar'),
    ('PCCPB', 'Cuentas por pagar bancarias'),
    ('PCP', 'Préstamos a corto plazo'),
    ('PP', 'Provisiones'),
    ('PLP', 'Pasivo a largo plazo'),
    ('PLPP', 'Préstamos a largo plazo'),
    ('PLPO', 'Otros pasivos a largo plazo'),

    # ---- CAPITAL ----
    ('C', 'Capital'),
    ('CRS', 'Reservas'),
    ('CAG', 'Aportaciones de los socios'),
    ('CGN', 'Ganancias retenidas'),
    ('COT', 'Otros conceptos de capital'),

    # ---- INGRESOS ----
    ('I', 'Ingresos'),
    ('IV', 'Ventas'),
    ('IOD', 'Otros ingresos'),
    
    # ---- EGRESOS ----
    ('E', 'Egresos'),
    ('ECV', 'Costo de ventas'),
    ('EG', 'Gastos generales'),
    ('EGA', 'Gastos administrativos'),
    ('EGV', 'Gastos de ventas'),
    ('EF', 'Gastos financieros'),
    ('EO', 'Otros egresos'),

    # ---- RESULTADO ----
    ('UO', 'Utilidad operativa'),
    ('UN', 'Utilidad neta'),
]

class PeriodoForm(forms.ModelForm):
    class Meta:
        model = Periodo
        fields = ['nombre', 'fecha_inicio', 'fecha_fin']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }


class MovimientoFinancieroForm(forms.ModelForm):
    class Meta:
        model = MovimientoFinanciero
        fields = ['periodo', 'cuenta', 'monto']
        widgets = {
            'periodo': forms.Select(attrs={'class': 'form-select'}),
            'cuenta': forms.Select(attrs={'class': 'form-select'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class CuentaContableForm(forms.ModelForm):
    codigo = forms.ChoiceField(
        choices=CUENTA_CHOICES,
        label="Código de Cuenta",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    class Meta:
        model = CuentaContable
        fields = ['codigo', 'nombre', 'clase', 'nivel', 'padre']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'clase': forms.Select(attrs={'class': 'form-select'}),
            'nivel': forms.NumberInput(attrs={'class': 'form-control'}),
            'padre': forms.Select(attrs={'class': 'form-select'}),
        }


MovimientoFinancieroFormSet = modelformset_factory(
    MovimientoFinanciero,
    form=MovimientoFinancieroForm,
    extra=0,  # No formularios extra, solo los que quieres mostrar
)

class ImportarMovimientosForm(forms.Form):
    archivo = forms.FileField(label="Archivo CSV")


class ImportarMovimientosXMLForm(forms.Form):
    archivo = forms.FileField(label="Archivo XML")