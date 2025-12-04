from django.urls import path

from apps.reportes import views

app_name = 'reportes_publicos'

urlpatterns = [
    # Reportes generados (metadatos)
    path('reportes/', views.public_reportes_list, name='public-reportes-list'),
    path('reportes/<str:codigo_reporte>/', views.public_reporte_detail, name='public-reporte-detail'),

    # Dashboards y sus indicadores
    path('dashboards/', views.public_dashboards_list, name='public-dashboards-list'),
    path('dashboards/<str:codigo_dashboard>/', views.public_dashboard_detail, name='public-dashboard-detail'),

    # Indicadores y series de estadísticas
    path('indicadores/<str:codigo_indicador>/', views.public_indicador_detail, name='public-indicador-detail'),
    path('indicadores/<str:codigo_indicador>/serie/', views.public_indicador_serie, name='public-indicador-serie'),

    # Tendencias geográficas y ranking de áreas
    path('tendencias-geograficas/', views.public_tendencias_geograficas, name='public-tendencias-geograficas'),
    path('ranking-areas/', views.public_ranking_areas, name='public-ranking-areas'),

    # Resumen público de estadísticas de denuncias
    path('estadisticas/denuncias-resumen/', views.public_estadisticas_denuncias_resumen, name='public-estadisticas-denuncias-resumen'),
]
