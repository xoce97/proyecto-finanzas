from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_indicadores, name='lista_indicadores'),
    path('nuevo/', views.crear_indicador, name='crear_indicador'),
    path('resultado/nuevo/', views.crear_resultado, name='crear_resultado'),
]
