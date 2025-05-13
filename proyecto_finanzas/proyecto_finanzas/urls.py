"""
URL configuration for proyecto_finanzas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from sistema_financiero import views

app_name = 'sistema_financiero'

urlpatterns = [
    # Gestión de empresas
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('empresas/crear/', views.crear_empresa, name='crear_empresa'),
    path('empresas/<int:empresa_id>/', views.detalle_empresa, name='detalle_empresa'),
    
    # Gestión de períodos
    path('empresas/<int:empresa_id>/periodos/crear/', views.crear_periodo, name='crear_periodo'),
    path('periodos/<int:periodo_id>/', views.detalle_periodo, name='detalle_periodo'),
    
    # Estados financieros
    path('periodos/<int:periodo_id>/balance/crear/', views.crear_balance, name='crear_balance'),
    path('periodos/<int:periodo_id>/estado/crear/', views.crear_estado_resultados, name='crear_estado'),
    
    # Análisis
    path('empresas/<int:empresa_id>/analisis/', views.analisis_financiero, name='analisis_financiero'),
    
    # Capital de trabajo
    path('empresas/<int:empresa_id>/capital/', views.gestion_capital_trabajo, name='gestion_capital'),
    
    # Simulación
    path('empresas/<int:empresa_id>/simular/', views.simulacion_capital_trabajo, name='simulacion_capital'),
]