from django.db import models
from finanzas.models import Periodo
from finanzas.models import CuentaContable

# Opcional: categorías para organización de razones
RAZONES_CATEGORIA = [
    ('LIQUIDEZ', 'Liquidez'),
    ('ACTIVIDAD', 'Actividad'),
    ('ENDEUDAMIENTO', 'Endeudamiento'),
    ('RENTABILIDAD', 'Rentabilidad'),
]

class RazonFinanciera(models.Model):
    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=RAZONES_CATEGORIA)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class ResultadoRazon(models.Model):
    razon = models.ForeignKey(RazonFinanciera, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('razon', 'periodo')



class AnalisisVertical(models.Model):
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    porcentaje = models.DecimalField(max_digits=7, decimal_places=2)  # ej. 35.24%

    class Meta:
        unique_together = ('cuenta', 'periodo')

class AnalisisHorizontal(models.Model):
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.CASCADE)
    periodo_base = models.ForeignKey(Periodo, related_name='base_h', on_delete=models.CASCADE)
    periodo_comparado = models.ForeignKey(Periodo, related_name='comparado_h', on_delete=models.CASCADE)
    variacion_absoluta = models.DecimalField(max_digits=15, decimal_places=2)
    variacion_porcentual = models.DecimalField(max_digits=7, decimal_places=2)

    class Meta:
        unique_together = ('cuenta', 'periodo_base', 'periodo_comparado')


