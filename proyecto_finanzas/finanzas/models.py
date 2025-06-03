from django.db import models

# Periodo contable
class Periodo(models.Model):
    nombre = models.CharField(max_length=50)  # Ej: "2024 Q1", "2023", etc.
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre

# Catálogo de cuentas contables
class CuentaContable(models.Model):
    CLASE_CUENTA = [
        ('ACTIVO', 'Activo'),
        ('PASIVO', 'Pasivo'),
        ('CAPITAL', 'Capital Contable'),
        ('INGRESO', 'Ingreso'),
        ('EGRESO', 'Egreso'),
    ]

    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10, unique=True)
    clase = models.CharField(max_length=10, choices=CLASE_CUENTA)
    nivel = models.PositiveIntegerField(default=1)  # Para jerarquía
    padre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='subcuentas')

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"

# Valores de una cuenta en un periodo específico
class MovimientoFinanciero(models.Model):
    cuenta = models.ForeignKey(CuentaContable, on_delete=models.CASCADE)
    periodo = models.ForeignKey(Periodo, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        unique_together = ('cuenta', 'periodo')

    def __str__(self):
        return f"{self.cuenta} | {self.periodo} | ${self.monto}"

