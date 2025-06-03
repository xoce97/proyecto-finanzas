from django.contrib import admin
from .models import IndicadorCapitalTrabajo, ResultadoIndicador

@admin.register(IndicadorCapitalTrabajo)
class IndicadorCapitalTrabajoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')

@admin.register(ResultadoIndicador)
class ResultadoIndicadorAdmin(admin.ModelAdmin):
    list_display = ('indicador', 'periodo', 'valor')
    list_filter = ('indicador', 'periodo')
