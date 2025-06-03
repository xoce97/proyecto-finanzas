from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_escenarios, name='lista_escenarios'),
    path('nuevo/', views.crear_escenario, name='crear_escenario'),
    path('variable/nuevo/<int:escenario_id>/', views.crear_variable, name='crear_variable'),
]
