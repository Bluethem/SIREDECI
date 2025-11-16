from django.urls import path
from apps.personal import views

app_name = 'personal'

urlpatterns = [
    path('admin/login/', views.login_admin, name='admin-login'),
]

