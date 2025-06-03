from django.contrib import admin
from .models import ReporteGenerado

@admin.register(ReporteGenerado)
class ReporteGeneradoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_generado', 'usuario', 'archivo')
    list_filter = ('fecha_generado', 'usuario')

