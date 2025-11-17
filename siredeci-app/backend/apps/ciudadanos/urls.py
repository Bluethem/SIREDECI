from django.urls import path
from .views import CiudadanoLoginView, CiudadanoRegistroView

urlpatterns = [
    path('login/', CiudadanoLoginView.as_view(), name='ciudadano-login'),
    path('registro/', CiudadanoRegistroView.as_view(), name='ciudadano-registro'),
]
