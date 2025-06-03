from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_reportes, name='lista_reportes'),
    path('subir/', views.subir_reporte, name='subir_reporte'),
]
