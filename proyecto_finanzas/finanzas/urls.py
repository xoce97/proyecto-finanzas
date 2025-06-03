from django.urls import path
from . import views

app_name = 'finanzas'

urlpatterns = [
    path('', views.home, name='home'),
    path('periodos/', views.periodos_list, name='periodos_list'),
    path('periodos/nuevo/', views.periodo_create, name='periodo_create'),
    path('periodos/<int:pk>/editar/', views.periodo_edit, name='periodo_edit'),
    # Añadir rutas para CuentaContable
    path('cuentas/', views.CuentaContableListView.as_view(), name='cuenta_list'),
    path('cuentas/nueva/', views.CuentaContableCreateView.as_view(), name='cuenta_create'),
    path('cuentas/<int:pk>/editar/', views.CuentaContableUpdateView.as_view(), name='cuenta_update'),
    path('cuentas/<int:pk>/eliminar/', views.CuentaContableDeleteView.as_view(), name='cuenta_delete'),
    path('movimientos/', views.MovimientoFinancieroListView.as_view(), name='movimiento_list'),
    path('movimientos/nuevo/', views.MovimientoFinancieroCreateView.as_view(), name='movimiento_create'),
    path('movimientos/captura/<int:periodo_id>/', views.captura_masiva_movimientos, name='captura_masiva_movimientos'),
    # Ruta para importar los datos de cuentas.
    path('movimientos/importar/', views.importar_movimientos_csv, name='importar_movimientos'),
    path('movimientos/importar-xml/', views.importar_movimientos_xml, name='importar_movimientos_xml'),
]

