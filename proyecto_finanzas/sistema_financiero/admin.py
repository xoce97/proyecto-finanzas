from django.contrib import admin
from .models import Empresa, PeriodoContable, BalanceGeneral, EstadoResultados

class PeriodoContableInline(admin.TabularInline):
    model = PeriodoContable
    extra = 0
    fields = ('nombre', 'fecha_inicio', 'fecha_fin')
    readonly_fields = ('nombre', 'fecha_inicio', 'fecha_fin')
    show_change_link = True

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_creacion', 'total_periodos')
    search_fields = ('nombre', 'descripcion')
    list_filter = ('fecha_creacion',)
    inlines = [PeriodoContableInline]
    
    def total_periodos(self, obj):
        return obj.periodocontable_set.count()
    total_periodos.short_description = 'Periodos'

class BalanceGeneralInline(admin.StackedInline):
    model = BalanceGeneral
    extra = 0
    fieldsets = (
        ('Activo Corriente', {
            'fields': (
                ('caja_efectivo', 'bancos'),
                ('clientes_nacionales', 'inventario'),
            )
        }),
        ('Activo No Corriente', {
            'fields': (
                ('terrenos', 'edificios'),
                ('maquinaria_equipo', 'vehiculos'),
            )
        }),
    )
    readonly_fields = ('activo_total', 'pasivo_total', 'capital_neto_trabajo')

class EstadoResultadosInline(admin.StackedInline):
    model = EstadoResultados
    extra = 0
    fieldsets = (
        ('Ingresos', {
            'fields': ('ventas_netas',)
        }),
        ('Costos y Gastos', {
            'fields': (
                ('costo_ventas', 'gastos_operacion'),
                ('gastos_financieros', 'productos_financieros'),
            )
        }),
        ('Resultados', {
            'fields': (
                ('utilidad_bruta', 'utilidad_operacional'),
                ('utilidad_antes_impuestos', 'utilidad_neta'),
            )
        }),
    )
    readonly_fields = ('utilidad_bruta', 'utilidad_operacional', 'utilidad_antes_impuestos', 'utilidad_neta')

@admin.register(PeriodoContable)
class PeriodoContableAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'empresa', 'fecha_inicio', 'fecha_fin', 'dias_periodo')
    list_filter = ('empresa', 'fecha_inicio', 'fecha_fin')
    search_fields = ('nombre', 'empresa__nombre')
    date_hierarchy = 'fecha_inicio'
    inlines = [BalanceGeneralInline, EstadoResultadosInline]
    
    def dias_periodo(self, obj):
        return (obj.fecha_fin - obj.fecha_inicio).days
    dias_periodo.short_description = 'Días'

@admin.register(BalanceGeneral)
class BalanceGeneralAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'activo_total', 'pasivo_total', 'capital_neto_trabajo')
    list_filter = ('periodo__empresa', 'periodo__nombre')
    search_fields = ('periodo__nombre',)
    readonly_fields = ('activo_total', 'pasivo_total', 'capital_neto_trabajo')
    
    fieldsets = (
        ('Activo', {
            'fields': (
                ('activo_corriente', 'activo_no_corriente'),
                ('activo_total',),
            )
        }),
        ('Pasivo', {
            'fields': (
                ('pasivo_corriente', 'pasivo_no_corriente'),
                ('pasivo_total',),
            )
        }),
        ('Capital Contable', {
            'fields': (
                ('capital_social', 'capital_variable'),
                ('patrimonio', 'capital_neto_trabajo'),
            )
        }),
    )

@admin.register(EstadoResultados)
class EstadoResultadosAdmin(admin.ModelAdmin):
    list_display = ('periodo', 'ventas_netas', 'utilidad_bruta', 'utilidad_neta', 'margen_neto')
    list_filter = ('periodo__empresa', 'periodo__nombre')
    search_fields = ('periodo__nombre',)
    readonly_fields = ('utilidad_bruta', 'utilidad_operacional', 'utilidad_antes_impuestos', 'utilidad_neta')
    
    def margen_neto(self, obj):
        return f"{(obj.utilidad_neta / obj.ventas_netas * 100 if obj.ventas_netas != 0 else 0):.2f}%"
    margen_neto.short_description = 'Margen Neto'