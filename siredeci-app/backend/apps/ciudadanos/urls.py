from django.urls import path
from .views import (
    CiudadanoLoginView,
    CiudadanoRegistroView,
    CiudadanoNotificacionesView,
    CiudadanoNotificacionMarcarLeidaView,
    CiudadanoConfiguracionNotificacionesView,
)

urlpatterns = [
    path('login/', CiudadanoLoginView.as_view(), name='ciudadano-login'),
    path('registro/', CiudadanoRegistroView.as_view(), name='ciudadano-registro'),
    path('notificaciones/', CiudadanoNotificacionesView.as_view(), name='ciudadano-notificaciones'),
    path('notificaciones/marcar-leida/', CiudadanoNotificacionMarcarLeidaView.as_view(), name='ciudadano-notificaciones-marcar-leida'),
    path('notificaciones/config/', CiudadanoConfiguracionNotificacionesView.as_view(), name='ciudadano-notificaciones-config'),
]
