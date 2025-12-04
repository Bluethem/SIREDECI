from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from apps.personal.serializers import (
    LoginAdminSerializer,
    PersonalMunicipalSerializer,
    PersonalMunicipalAdminSerializer,
)
from apps.personal.models import PersonalMunicipal, Asignacion
from apps.usuarios.models import Usuario
from apps.usuarios.utils import get_codigos_roles, get_codigos_permisos
from apps.usuarios.permissions import IsStaffLike
from apps.denuncias.models import Denuncia, Resolucion
from apps.denuncias.serializers import DenunciaListSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_admin(request):
    """
    Endpoint para el login de administradores (Personal Municipal)
    
    POST /api/admin/login/
    Body: {
        "email": "admin@example.com",
        "password": "password123"
    }
    """
    serializer = LoginAdminSerializer(data=request.data)
    
    if serializer.is_valid():
        usuario = serializer.validated_data['usuario']
        personal = serializer.validated_data.get('personal')

        # Generar tokens JWT
        refresh = RefreshToken.for_user(usuario)
        access_token = refresh.access_token

        # Preparar datos del usuario
        roles = list(get_codigos_roles(usuario))
        permisos = list(get_codigos_permisos(usuario))

        user_data = {
            'id_usuario': usuario.id_usuario,
            'codigo_usuario': usuario.codigo_usuario,
            'nombre_usuario': usuario.nombre_usuario,
            'email': usuario.email,
            'estado_cuenta': usuario.estado_cuenta,
            'roles': roles,
            'permisos': permisos,
        }

        # Serializar datos del personal si aplica
        personal_serializer = PersonalMunicipalSerializer(personal) if personal is not None else None

        return Response({
            'access': str(access_token),
            'refresh': str(refresh),
            'user': user_data,
            'personal': personal_serializer.data if personal_serializer else None,
            'message': 'Login exitoso'
        }, status=status.HTTP_200_OK)
    
    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )


class PersonalMunicipalViewSet(viewsets.ModelViewSet):
    queryset = PersonalMunicipal.objects.select_related('id_area_responsable', 'id_usuario').all()
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['id_area_responsable', 'estado_laboral']
    search_fields = ['codigo_personal', 'dni', 'nombre', 'apellido', 'email']
    ordering_fields = ['fecha_ingreso', 'nombre', 'apellido']
    ordering = ['apellido', 'nombre']

    def get_permissions(self):
        # Por ahora restringimos a usuarios internos (no ciudadanos).
        # Más adelante se pueden añadir HasRol/HasPermiso para control más fino.
        if self.action in ['list', 'retrieve', 'create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsStaffLike()]
        return [IsAuthenticated(), IsStaffLike()]

    def get_serializer_class(self):
        return PersonalMunicipalAdminSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def mis_denuncias_personal(request):
    """Denuncias asignadas al personal municipal autenticado.

    GET /api/municipal/mis-denuncias/
    """
    user = request.user

    personal = getattr(user, 'personal', None)
    if personal is None or personal.estado_laboral != 'Activo':
        return Response(
            {
                'error': 'Personal no válido',
                'message': 'El usuario autenticado no tiene un registro de personal municipal activo.'
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    asignaciones_qs = (
        Asignacion.objects
        .select_related('id_denuncia')
        .filter(id_personal_asignado=personal, es_activa=True)
    )

    denuncias = [a.id_denuncia for a in asignaciones_qs]

    serializer = DenunciaListSerializer(denuncias, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def pendientes_asignar_area(request):
    """Denuncias de la(s) categoría(s) de mi área que aún no tienen asignación activa.

    GET /api/municipal/pendientes-asignar/
    """
    user = request.user

    personal = getattr(user, 'personal', None)
    if personal is None or personal.estado_laboral != 'Activo':
        return Response(
            {
                'error': 'Personal no válido',
                'message': 'El usuario autenticado no tiene un registro de personal municipal activo.'
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    area = personal.id_area_responsable

    qs = (
        Denuncia.objects
        .select_related('id_categoria', 'id_ubicacion')
        .filter(id_categoria__id_area_responsable=area)
        .exclude(asignaciones__es_activa=True)
    )

    estado = request.query_params.get('estado')
    if estado:
        qs = qs.filter(estado=estado)

    serializer = DenunciaListSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def denuncias_area_personal(request):
    """Denuncias asociadas al área responsable del personal autenticado.

    GET /api/municipal/mi-area/denuncias/
    """
    user = request.user

    personal = getattr(user, 'personal', None)
    if personal is None or personal.estado_laboral != 'Activo':
        return Response(
            {
                'error': 'Personal no válido',
                'message': 'El usuario autenticado no tiene un registro de personal municipal activo.'
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    area = personal.id_area_responsable

    qs = (
        Denuncia.objects
        .select_related('id_categoria', 'id_ubicacion')
        .filter(id_categoria__id_area_responsable=area)
    )

    estado = request.query_params.get('estado')
    if estado:
        qs = qs.filter(estado=estado)

    serializer = DenunciaListSerializer(qs, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def dashboard_area_summary(request):
    """Resumen de métricas para el dashboard del área del personal.

    GET /api/municipal/dashboard/summary/
    """
    user = request.user

    personal = getattr(user, 'personal', None)
    if personal is None or personal.estado_laboral != 'Activo':
        return Response(
            {
                'error': 'Personal no válido',
                'message': 'El usuario autenticado no tiene un registro de personal municipal activo.'
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    area = personal.id_area_responsable

    qs = Denuncia.objects.filter(id_categoria__id_area_responsable=area)

    total = qs.count()
    por_estado = (
        qs.values('estado')
        .order_by('estado')
    )
    por_prioridad = (
        qs.values('prioridad')
        .order_by('prioridad')
    )

    return Response(
        {
            'area': area.nombre if area else None,
            'total_denuncias': total,
            'por_estado': list(por_estado),
            'por_prioridad': list(por_prioridad),
        },
        status=status.HTTP_200_OK,
    )


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStaffLike])
def denuncias_duplicadas_area(request):
    """Denuncias del área cuya resolución final es de tipo 'Duplicada'.

    Basado en el modelo relacional: Resolucion(tipo_resolucion='Duplicada') -> Tramitacion -> Asignacion -> Denuncia.

    GET /api/municipal/duplicadas/
    """
    user = request.user

    personal = getattr(user, 'personal', None)
    if personal is None or personal.estado_laboral != 'Activo':
        return Response(
            {
                'error': 'Personal no válido',
                'message': 'El usuario autenticado no tiene un registro de personal municipal activo.'
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    area = personal.id_area_responsable

    resoluciones = (
        Resolucion.objects
        .select_related('id_tramitacion__id_asignacion__id_denuncia__id_categoria')
        .filter(
            tipo_resolucion='Duplicada',
            id_tramitacion__id_asignacion__id_denuncia__id_categoria__id_area_responsable=area,
        )
    )

    denuncias_set = []
    vistos = set()
    for res in resoluciones:
        denuncia = getattr(res.id_tramitacion.id_asignacion, 'id_denuncia', None)
        if denuncia and denuncia.id_denuncia not in vistos:
            vistos.add(denuncia.id_denuncia)
            denuncias_set.append(denuncia)

    serializer = DenunciaListSerializer(denuncias_set, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
