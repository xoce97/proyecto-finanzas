from django.db import models
from django.core.validators import MinValueValidator


class Empresa(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    fecha_creacion = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.nombre

class PeriodoContable(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    
    def __str__(self):
        return f"{self.nombre} - {self.empresa}"

class BalanceGeneral(models.Model):
    periodo = models.OneToOneField(PeriodoContable, on_delete=models.CASCADE, primary_key=True)
    
    # Activo a Corto Plazo
    caja_efectivo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    bancos = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    inversiones_temporales = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    clientes_nacionales = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    documentos_por_cobrar_corto_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    deudores_diversos = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    estimacion_cuentas_incobrables = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    pagos_anticipados = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    inventario = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    anticipo_proveedores = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    otros_activos_corto_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Activo a Largo Plazo
    terrenos = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    edificios = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    maquinaria_equipo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    vehiculos = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    mobiliario_equipo_oficina = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    equipo_computo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    equipo_comunicacion = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    otros_activos_fijos = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    activos_intangibles = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gastos_organizacion = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    gastos_instalacion = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    documentos_por_cobrar_largo_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Pasivo a Corto Plazo
    cuentas_por_pagar_corto_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    documentos_por_pagar_corto_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    cobros_anticipados_corto_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    iva_trasladado = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    otros_pasivos_corto_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Pasivo a Largo Plazo
    cuentas_por_pagar_largo_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    documentos_por_pagar_largo_plazo = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Capital Contable
    capital_social = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    capital_variable = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    aportacion_patrimonial = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    reserva_legal = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    utilidad_ejercicios_anteriores = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    perdida_ejercicios_anteriores = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    @property
    def activo_corriente(self):
        return (self.caja_efectivo + self.bancos + self.inversiones_temporales + 
                self.clientes_nacionales + self.documentos_por_cobrar_corto_plazo + 
                self.deudores_diversos - self.estimacion_cuentas_incobrables + 
                self.pagos_anticipados + self.inventario + 
                self.antecipo_proveedores + self.otros_activos_corto_plazo)
    
    @property
    def activo_no_corriente(self):
        return (self.terrenos + self.edificios + self.maquinaria_equipo + 
                self.vehiculos + self.mobiliario_equipo_oficina + 
                self.equipo_computo + self.equipo_comunicacion + 
                self.otros_activos_fijos + self.activos_intangibles + 
                self.gastos_organizacion + self.gastos_instalacion + 
                self.documentos_por_cobrar_largo_plazo)
    
    @property
    def pasivo_corriente(self):
        return (self.cuentas_por_pagar_corto_plazo + 
                self.documentos_por_pagar_corto_plazo + 
                self.cobros_anticipados_corto_plazo + 
                self.iva_trasladado + 
                self.otros_pasivos_corto_plazo)
    
    @property
    def pasivo_no_corriente(self):
        return (self.cuentas_por_pagar_largo_plazo + 
                self.documentos_por_pagar_largo_plazo)
    
    @property
    def patrimonio(self):
        return (self.capital_social + self.capital_variable + 
                self.aportacion_patrimonial + self.reserva_legal + 
                (self.utilidad_ejercicios_anteriores - self.perdida_ejercicios_anteriores) + 
                self.utilidad_ejercicio)
    
    @property
    def activo_total(self):
        return self.activo_corriente + self.activo_no_corriente
    
    @property
    def pasivo_total(self):
        return self.pasivo_corriente + self.pasivo_no_corriente
    
    @property
    def capital_neto_trabajo(self):
        return self.activo_corriente - self.pasivo_corriente
    
    class Meta:
        verbose_name_plural = "Balances Generales"

class EstadoResultados(models.Model):
    periodo = models.OneToOneField(PeriodoContable, on_delete=models.CASCADE, primary_key=True)
    
    # Ingresos
    ventas_netas = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Costos
    costo_ventas = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Gastos de Operación
    gastos_operacion = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Gastos Financieros
    gastos_financieros = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    productos_financieros = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    fluctuacion_cambiaria = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    
    # Impuestos
    impuesto_utilidad = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    # Resultados
    utilidad_ejercicio = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    perdida_ejercicio = models.DecimalField(max_digits=15, decimal_places=2, default=0, validators=[MinValueValidator(0)])
    
    @property
    def utilidad_bruta(self):
        return self.ventas_netas - self.costo_ventas
    
    @property
    def utilidad_operacional(self):
        return self.utilidad_bruta - self.gastos_operacion
    
    @property
    def resultado_financiamiento(self):
        return (self.gastos_financieros - self.productos_financieros + 
                self.fluctuacion_cambiaria)
    
    @property
    def utilidad_antes_impuestos(self):
        return self.utilidad_operacional - self.resultado_financiamiento
    
    @property
    def utilidad_neta(self):
        return self.utilidad_antes_impuestos - self.impuesto_utilidad
    
    @property
    def utilidad_ejercicio_final(self):
        return self.utilidad_neta if self.utilidad_neta > 0 else 0
    
    @property
    def perdida_ejercicio_final(self):
        return abs(self.utilidad_neta) if self.utilidad_neta < 0 else 0
    
    class Meta:
        verbose_name_plural = "Estados de Resultados"