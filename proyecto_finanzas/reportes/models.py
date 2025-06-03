from django.db import models
from django.contrib.auth.models import User

class ReporteGenerado(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_generado = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    archivo = models.FileField(upload_to='reportes/')

    def __str__(self):
        return f"{self.nombre} ({self.fecha_generado.date()})"
