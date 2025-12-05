from django.urls import path

from . import views

app_name = 'categorias'

urlpatterns = [
    path('categorias/', views.categorias_list, name='categorias-list'),
]
