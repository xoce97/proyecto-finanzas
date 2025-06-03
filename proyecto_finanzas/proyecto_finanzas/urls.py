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
from django.urls import path , include
from finanzas.views import home
from django.contrib import admin

urlpatterns = [
    #panel administracion
    path('admin/', admin.site.urls),
    path('finanzas/', include('finanzas.urls')),
    path('analisis/', include('analisis.urls')),
    path('capital/', include('capital_trabajo.urls')),
    path('simulacion/', include('simulacion.urls')),
    path('reportes/', include('reportes.urls')),
]