from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DenunciaViewSet, DenunciaPublicaViewSet

# Router para endpoints RESTful
router = DefaultRouter()
router.register(r'denuncias', DenunciaViewSet, basename='denuncia')
router.register(r'publico/denuncias', DenunciaPublicaViewSet, basename='denuncia-publica')

urlpatterns = [
    path('', include(router.urls)),
]
