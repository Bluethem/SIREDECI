from django.urls import path
from apps.reportes import views

app_name = 'reportes'

urlpatterns = [
    path('dashboard/summary/', views.dashboard_summary, name='dashboard-summary'),
    path('dashboard/categorias/', views.dashboard_categorias, name='dashboard-categorias'),
    path('dashboard/temporal/', views.dashboard_temporal, name='dashboard-temporal'),
    path('dashboard/prioridades/', views.dashboard_prioridades, name='dashboard-prioridades'),
    path('dashboard/alerts/', views.dashboard_alerts, name='dashboard-alerts'),
    path('geo/points/', views.geo_points, name='geo-points'),
    path('geo/top-zonas/', views.geo_top_zonas, name='geo-top-zonas'),
    path('geo/evolucion/', views.geo_evolucion, name='geo-evolucion'),
    path('indicators/', views.indicators_list, name='indicators-list'),
    path('desempeno/ranking/', views.ranking_desempeno, name='ranking-desempeno'),
    # Gestión de reportes para administradores
    path('reportes/', views.admin_reportes_list, name='admin-reportes-list'),
    path('reportes/generar/', views.admin_reportes_generate, name='admin-reportes-generate'),
    path('reportes/<str:codigo_reporte>/download/', views.admin_reportes_download, name='admin-reportes-download'),
]
