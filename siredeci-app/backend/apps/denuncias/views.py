from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, Count
from .models import Denuncia, Ubicacion, Evidencia
from .serializers import (
    DenunciaListSerializer,
    DenunciaDetailSerializer,
    DenunciaCreateSerializer,
    DenunciaUpdateSerializer
)
from apps.ciudadanos.models import Ciudadano


class DenunciaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar denuncias
    
    Endpoints:
    - GET /api/denuncias/ - Listar denuncias
    - POST /api/denuncias/ - Crear denuncia
    - GET /api/denuncias/{id}/ - Detalle de denuncia
    - PUT/PATCH /api/denuncias/{id}/ - Actualizar denuncia
    - DELETE /api/denuncias/{id}/ - Eliminar denuncia (soft delete)
    - GET /api/denuncias/mis-denuncias/ - Denuncias del ciudadano autenticado
    - GET /api/denuncias/estadisticas/ - Estadísticas de denuncias
    """
    
    queryset = Denuncia.objects.select_related(
        'id_categoria', 'id_ubicacion', 'id_ciudadano'
    ).prefetch_related('evidencias').all()
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'prioridad', 'id_categoria', 'id_ciudadano']
    search_fields = ['codigo_denuncia', 'titulo', 'descripcion', 'numero_seguimiento']
    ordering_fields = ['fecha_registro', 'fecha_actualizacion', 'prioridad']
    ordering = ['-fecha_registro']  # Por defecto, más recientes primero
    
    def get_serializer_class(self):
        """Retornar el serializer apropiado según la acción"""
        if self.action == 'list' or self.action == 'mis_denuncias':
            return DenunciaListSerializer
        elif self.action == 'create':
            return DenunciaCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return DenunciaUpdateSerializer
        return DenunciaDetailSerializer
    
    def get_permissions(self):
        """
        Permisos personalizados por acción
        Todos los endpoints son AllowAny para ciudadanos
        La validación se hace por id_ciudadano, no por autenticación
        """
        return [AllowAny()]
    
    def create(self, request, *args, **kwargs):
        """
        Crear una nueva denuncia
        
        Body:
        {
            "titulo": "string",
            "descripcion": "string",
            "id_categoria": int,
            "id_ciudadano": int (opcional si es_anonima=true),
            "es_anonima": boolean,
            "prioridad": "Baja|Media|Alta|Urgente",
            "ubicacion": {
                "latitud": decimal,
                "longitud": decimal,
                "direccion": "string",
                "referencia": "string" (opcional),
                "distrito": "string",
                "codigo_postal": "string" (opcional)
            }
        }
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        denuncia = serializer.save()
        
        # Usar el DetailSerializer para la respuesta
        response_serializer = DenunciaDetailSerializer(denuncia)
        
        return Response(
            {
                'mensaje': 'Denuncia registrada exitosamente',
                'denuncia': response_serializer.data
            },
            status=status.HTTP_201_CREATED
        )
    
    @action(detail=False, methods=['get'], url_path='mis-denuncias')
    def mis_denuncias(self, request):
        """
        Obtener las denuncias del ciudadano autenticado
        
        GET /api/denuncias/mis-denuncias/
        Query params:
        - estado: filtrar por estado
        - search: buscar por título/código
        - id_ciudadano: ID del ciudadano (requerido si no hay autenticación tradicional)
        """
        # Intentar obtener el ciudadano del usuario autenticado
        ciudadano = None
        
        # Opción 1: Usuario autenticado con modelo User
        if request.user and request.user.is_authenticated and hasattr(request.user, 'id'):
            try:
                ciudadano = Ciudadano.objects.get(id_usuario__id=request.user.id)
            except Ciudadano.DoesNotExist:
                pass
        
        # Opción 2: Ciudadano autenticado con token simple (desde custom authentication)
        if not ciudadano and hasattr(request.user, 'ciudadano') and request.user.ciudadano:
            ciudadano = request.user.ciudadano
        
        # Opción 3: id_ciudadano desde localStorage (para desarrollo)
        if not ciudadano:
            id_ciudadano = request.query_params.get('id_ciudadano') or request.GET.get('id_ciudadano')
            if id_ciudadano:
                try:
                    ciudadano = Ciudadano.objects.get(id_ciudadano=id_ciudadano, estado_cuenta='Activo')
                except Ciudadano.DoesNotExist:
                    pass
        
        # Si no se pudo obtener el ciudadano, retornar lista vacía
        if not ciudadano:
            return Response([], status=status.HTTP_200_OK)
        
        # Filtrar denuncias del ciudadano
        queryset = self.filter_queryset(
            self.get_queryset().filter(id_ciudadano=ciudadano)
        )
        
        # Paginación
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Obtener estadísticas de denuncias
        
        GET /api/denuncias/estadisticas/
        Query params:
        - id_ciudadano: filtrar por ciudadano
        """
        queryset = self.get_queryset()
        
        # Filtrar por ciudadano si se especifica
        id_ciudadano = request.query_params.get('id_ciudadano')
        if id_ciudadano:
            queryset = queryset.filter(id_ciudadano=id_ciudadano)
        
        # Calcular estadísticas
        total = queryset.count()
        por_estado = queryset.values('estado').annotate(
            cantidad=Count('id_denuncia')
        ).order_by('estado')
        
        por_prioridad = queryset.values('prioridad').annotate(
            cantidad=Count('id_denuncia')
        ).order_by('prioridad')
        
        por_categoria = queryset.values(
            'id_categoria__nombre'
        ).annotate(
            cantidad=Count('id_denuncia')
        ).order_by('-cantidad')[:5]  # Top 5 categorías
        
        return Response({
            'total': total,
            'por_estado': list(por_estado),
            'por_prioridad': list(por_prioridad),
            'top_categorias': list(por_categoria)
        })
    
    @action(detail=True, methods=['get'], url_path='seguimiento')
    def consultar_seguimiento(self, request, pk=None):
        """
        Consultar denuncia por número de seguimiento (público)
        
        GET /api/denuncias/{numero_seguimiento}/seguimiento/
        """
        denuncia = self.get_object()
        serializer = DenunciaDetailSerializer(denuncia)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Soft delete: cambiar estado a 'Cerrada' en lugar de eliminar
        """
        instance = self.get_object()
        
        if instance.estado in ['Cerrada', 'Rechazada']:
            return Response(
                {'error': 'La denuncia ya está cerrada o rechazada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        instance.estado = 'Cerrada'
        instance.save()
        
        return Response(
            {'mensaje': 'Denuncia cerrada exitosamente'},
            status=status.HTTP_200_OK
        )


class DenunciaPublicaViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para consultas públicas de denuncias (sin autenticación)
    
    Endpoints:
    - GET /api/publico/denuncias/ - Listar denuncias públicas
    - GET /api/publico/denuncias/{codigo}/ - Detalle por código
    - GET /api/publico/denuncias/seguimiento/{numero}/ - Consulta por seguimiento
    - GET /api/publico/denuncias/buscar/?codigo=XXX - Buscar por código o seguimiento
    """
    
    queryset = Denuncia.objects.all().select_related('id_categoria', 'id_ubicacion')
    
    serializer_class = DenunciaListSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['estado', 'id_categoria']
    search_fields = ['codigo_denuncia', 'titulo', 'numero_seguimiento']
    
    @action(detail=False, methods=['get'], url_path='seguimiento/(?P<numero_seguimiento>[^/.]+)')
    def por_seguimiento(self, request, numero_seguimiento=None):
        """
        Consultar denuncia por número de seguimiento
        
        GET /api/publico/denuncias/seguimiento/{numero_seguimiento}/
        """
        try:
            denuncia = Denuncia.objects.get(numero_seguimiento=numero_seguimiento)
            serializer = DenunciaDetailSerializer(denuncia)
            return Response(serializer.data)
        except Denuncia.DoesNotExist:
            return Response(
                {'error': 'No se encontró una denuncia con ese número de seguimiento'},
                status=status.HTTP_404_NOT_FOUND
            )
