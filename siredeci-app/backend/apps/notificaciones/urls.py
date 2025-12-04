from django.urls import path

from apps.notificaciones import views

app_name = 'notificaciones'

urlpatterns = [
    path('usuario/', views.UsuarioNotificacionesView.as_view(), name='usuario-notificaciones'),
    path('usuario/marcar-leida/', views.UsuarioNotificacionMarcarLeidaView.as_view(), name='usuario-notificaciones-marcar-leida'),
    path('usuario/config/', views.UsuarioConfiguracionNotificacionesView.as_view(), name='usuario-notificaciones-config'),
]
