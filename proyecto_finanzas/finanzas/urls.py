from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('periodos/', views.periodos_list, name='periodos_list'),
    path('periodos/nuevo/', views.periodo_create, name='periodo_create'),
    path('periodos/<int:pk>/editar/', views.periodo_edit, name='periodo_edit'),
    # Añadir rutas para CuentaContable y MovimientoFinanciero
]
