from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='finanzas_index'),
]