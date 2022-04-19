"""cajaMenorProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from rest_framework_simplejwt.views import (TokenObtainPairView, TokenRefreshView)
from cajaMenorApp import views


urlpatterns = [
    path('login', TokenObtainPairView.as_view()),
    path('refresh', TokenRefreshView.as_view()),
    path('register', views.UserCreateView.as_view()),

    #URLS de usuario
    path('user/<int:pk>', views.UserDetailView.as_view()),

    #URLS de caja menor
    path('cajaMenor/<int:user>', views.CajaMenorCreateView.as_view()),
    path('cajaMenor/<int:user>/<int:pk>', views.CajaMenorDetailView.as_view()),
    path('cajaMenor/<int:user>/list', views.CajaMenorListView.as_view()),
    path('cajaMenor/<int:user>/<int:pk>/update', views.CajaMenorUpdateView.as_view()),
    path('cajaMenor/<int:user>/<int:pk>/delete', views.CajaMenorDeleteView.as_view()),
    

    #URLS de tipo de servicio
    path('tipoServicio/<int:user>', views.TipoServicioCreateView.as_view()),
    path('tipoServicio/<int:user>/list', views.TipoServicioListView.as_view()),

    #URLS de reporte
    path('reporte/<int:user>', views.ReporteCreateView.as_view()),
    path('reporte/<int:user>/list', views.ReporteListView.as_view()),

]

