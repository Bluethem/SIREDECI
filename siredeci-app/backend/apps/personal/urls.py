from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.personal import views

app_name = 'personal'

router = DefaultRouter()
router.register(r'personal', views.PersonalMunicipalViewSet, basename='personal-municipal')

urlpatterns = [
    path('admin/login/', views.login_admin, name='admin-login'),
    path('municipal/mis-denuncias/', views.mis_denuncias_personal, name='municipal-mis-denuncias'),
    path('municipal/mis-denuncias/<int:id_denuncia>/cambiar-estado/', views.cambiar_estado_mis_denuncias, name='municipal-mis-denuncias-cambiar-estado'),
    path('municipal/mis-denuncias/<int:id_denuncia>/reasignar-area/', views.reasignar_denuncia_area, name='municipal-mis-denuncias-reasignar-area'),
    path('municipal/pendientes-asignar/', views.pendientes_asignar_area, name='municipal-pendientes-asignar'),
    path('municipal/pendientes-asignar/<int:id_denuncia>/asignar/', views.asignar_denuncia_pendiente, name='municipal-pendientes-asignar-asignar'),
    path('municipal/mi-area/denuncias/', views.denuncias_area_personal, name='municipal-mi-area-denuncias'),
    path('municipal/dashboard/summary/', views.dashboard_area_summary, name='municipal-dashboard-summary'),
    path('municipal/dashboard/flujo/', views.dashboard_area_flujo, name='municipal-dashboard-flujo'),
    path('municipal/duplicadas/', views.denuncias_duplicadas_area, name='municipal-duplicadas'),
    path('', include(router.urls)),
]

