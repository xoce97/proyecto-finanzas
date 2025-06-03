from django.contrib import admin
from .models import EscenarioSimulacion, VariableEscenario, ResultadoProyeccion

class VariableEscenarioInline(admin.TabularInline):
    model = VariableEscenario
    extra = 1

@admin.register(EscenarioSimulacion)
class EscenarioSimulacionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion')
    inlines = [VariableEscenarioInline]

@admin.register(ResultadoProyeccion)
class ResultadoProyeccionAdmin(admin.ModelAdmin):
    list_display = ('escenario', 'periodo', 'descripcion', 'valor_proyectado')
    list_filter = ('escenario', 'periodo')
