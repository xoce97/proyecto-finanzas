from django.db import models
from finanzas.models import Periodo

class IndicadorCapitalTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class ResultadoIndicador(models.Model):
    indicador = models.ForeignKey(IndicadorCapitalTrabajo, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    valor = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        unique_together = ('indicador', 'periodo')

