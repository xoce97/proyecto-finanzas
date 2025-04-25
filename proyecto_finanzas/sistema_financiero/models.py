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
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE)
    activo_corriente = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    activo_no_corriente = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    pasivo_corriente = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    pasivo_no_corriente = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    patrimonio = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    @property
    def activo_total(self):
        return self.activo_corriente + self.activo_no_corriente
    
    @property
    def pasivo_total(self):
        return self.pasivo_corriente + self.pasivo_no_corriente
    
    @property
    def capital_neto_trabajo(self):
        return self.activo_corriente - self.pasivo_corriente

class EstadoResultados(models.Model):
    periodo = models.ForeignKey(PeriodoContable, on_delete=models.CASCADE)
    ingresos = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    costo_ventas = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    gastos_operacionales = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    gastos_no_operacionales = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    impuestos = models.DecimalField(max_digits=15, decimal_places=2, validators=[MinValueValidator(0)])
    
    @property
    def utilidad_bruta(self):
        return self.ingresos - self.costo_ventas
    
    @property
    def utilidad_operacional(self):
        return self.utilidad_bruta - self.gastos_operacionales
    
    @property
    def utilidad_neta(self):
        return self.utilidad_operacional - self.gastos_no_operacionales - self.impuestos
