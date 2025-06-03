from django.db import models
from finanzas.models import Periodo

class EscenarioSimulacion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre

class VariableEscenario(models.Model):
    escenario = models.ForeignKey(EscenarioSimulacion, on_delete=models.CASCADE, related_name='variables')
    nombre = models.CharField(max_length=100)
    valor_original = models.DecimalField(max_digits=12, decimal_places=2)
    valor_modificado = models.DecimalField(max_digits=12, decimal_places=2)

class ResultadoProyeccion(models.Model):
    escenario = models.ForeignKey(EscenarioSimulacion, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    descripcion = models.CharField(max_length=200)
    valor_proyectado = models.DecimalField(max_digits=12, decimal_places=2)
