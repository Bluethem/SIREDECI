from rest_framework import status, viewsets, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models.functions import TruncDate
from django.db.models import Count
from apps.personal.serializers import (
    LoginAdminSerializer,
    PersonalMunicipalSerializer,
    PersonalMunicipalAdminSerializer,
)
from apps.personal.models import PersonalMunicipal, Asignacion
from apps.usuarios.models import Usuario
from apps.usuarios.utils import get_codigos_roles, get_codigos_permisos
from apps.usuarios.permissions import IsStaffLike
from django.shortcuts import get_object_or_404
from apps.denuncias.models import Denuncia, Resolucion, Seguimiento
from apps.categorias.models import AreaResponsable
from apps.denuncias.serializers import DenunciaListSerializer, DenunciaUpdateSerializer


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


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaffLike])
def asignar_denuncia_pendiente(request, id_denuncia: int):
    """Asigna una denuncia pendiente al personal municipal autenticado.

    POST /api/municipal/pendientes-asignar/<id_denuncia>/asignar/

    - Verifica que la denuncia pertenece al área del personal.
    - Verifica que no tenga una asignación activa.
    - Crea una Asignacion con id_personal_asignado = personal autenticado.
    - Opcionalmente actualiza el estado a 'Asignado' si no lo está.
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

    denuncia = get_object_or_404(
        Denuncia.objects.select_related('id_categoria'),
        id_denuncia=id_denuncia,
        id_categoria__id_area_responsable=area,
    )

    # Verificar que no exista asignación activa
    if Asignacion.objects.filter(id_denuncia=denuncia, es_activa=True).exists():
        return Response(
            {
                'error': 'Ya asignada',
                'message': 'La denuncia ya cuenta con una asignación activa.'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Crear asignación
    motivo = request.data.get('motivo', '')
    asignacion = Asignacion.objects.create(
        motivo_asignacion=motivo,
        id_denuncia=denuncia,
        id_personal_asignado=personal,
        id_personal_asignador=personal,
    )

    # Actualizar estado a 'Asignado' si corresponde
    if denuncia.estado != 'Asignado':
        try:
            serializer = DenunciaUpdateSerializer(denuncia, data={'estado': 'Asignado'}, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        except Exception:
            # Si por alguna razón la transición no es válida, dejamos el estado como está
            pass

    return Response(
        {
            'mensaje': 'Denuncia asignada correctamente',
            'id_denuncia': denuncia.id_denuncia,
            'codigo_asignacion': asignacion.codigo_asignacion,
        },
        status=status.HTTP_201_CREATED,
    )


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
def dashboard_area_flujo(request):
    """Flujo operativo de denuncias del área en los últimos 30 días.

    GET /api/municipal/dashboard/flujo/
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

    hoy = timezone.now().date()
    hace_30 = hoy - timezone.timedelta(days=29)

    qs = (
        Denuncia.objects
        .filter(
            id_categoria__id_area_responsable=area,
            fecha_registro__date__gte=hace_30,
            fecha_registro__date__lte=hoy,
        )
    )

    agrupado = (
        qs.annotate(dia=TruncDate('fecha_registro'))
        .values('dia', 'estado')
        .annotate(total=Count('id_denuncia'))
        .order_by('dia')
    )

    # Reorganizar a estructura por día
    dias_map = {}
    for fila in agrupado:
        dia = fila['dia']
        estado = fila['estado']
        total = fila['total']
        if dia not in dias_map:
            dias_map[dia] = {
                'fecha': dia.isoformat(),
                'total': 0,
                'por_estado': {},
            }
        dias_map[dia]['total'] += total
        dias_map[dia]['por_estado'][estado] = total

    # Asegurar que todos los días del rango estén presentes (aunque sea con total 0)
    resultado = []
    for i in range(30):
        dia = hace_30 + timezone.timedelta(days=i)
        if dia in dias_map:
            resultado.append(dias_map[dia])
        else:
            resultado.append({
                'fecha': dia.isoformat(),
                'total': 0,
                'por_estado': {},
            })

    return Response(resultado, status=status.HTTP_200_OK)


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


@api_view(['PATCH'])
@permission_classes([IsAuthenticated, IsStaffLike])
def cambiar_estado_mis_denuncias(request, id_denuncia: int):
    """Permite al personal cambiar el estado de una denuncia que tiene asignada.

    PATCH /api/municipal/mis-denuncias/<id_denuncia>/cambiar-estado/
    Body JSON: {"estado": "En proceso" | "Resuelta" | ...}
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

    denuncia = get_object_or_404(Denuncia, id_denuncia=id_denuncia)

    # Verificar que exista una asignación activa de esa denuncia al personal
    tiene_asignacion = Asignacion.objects.filter(
        id_denuncia=denuncia,
        id_personal_asignado=personal,
        es_activa=True,
    ).exists()

    if not tiene_asignacion:
        return Response(
            {
                'error': 'Sin permiso sobre la denuncia',
                'message': 'La denuncia no está asignada actualmente al personal autenticado.'
            },
            status=status.HTTP_403_FORBIDDEN,
        )

    nuevo_estado = request.data.get('estado')
    if not nuevo_estado:
        return Response(
            {'error': 'Estado requerido', 'message': 'Debe especificar el nuevo estado.'},
            status=status.HTTP_400_BAD_REQUEST,
        )

    estado_anterior = denuncia.estado

    serializer = DenunciaUpdateSerializer(denuncia, data={'estado': nuevo_estado}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    # Registrar seguimiento del cambio de estado
    try:
      Seguimiento.objects.create(
          estado_anterior=estado_anterior,
          estado_nuevo=denuncia.estado,
          comentario=request.data.get('comentario', ''),
          id_denuncia=denuncia,
          id_usuario=user,
      )
    except Exception:
      # No bloquear el flujo si falla el registro de seguimiento
      pass

    return Response({'id_denuncia': denuncia.id_denuncia, 'estado': denuncia.estado}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStaffLike])
def reasignar_denuncia_area(request, id_denuncia: int):
    """Reasigna una denuncia a otra área responsable creando una nueva asignación.

    POST /api/municipal/mis-denuncias/<id_denuncia>/reasignar-area/

    Body JSON: {
      "area_destino": "Nombre del área destino",
      "motivo": "Texto opcional"
    }
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

    denuncia = get_object_or_404(Denuncia, id_denuncia=id_denuncia)

    # Asignación activa actual del personal autenticado
    asignacion_actual = (
        Asignacion.objects
        .select_related('id_personal_asignado__id_area_responsable')
        .filter(id_denuncia=denuncia, es_activa=True)
        .first()
    )

    if asignacion_actual is None:
        return Response(
            {
                'error': 'Sin asignación activa',
                'message': 'La denuncia no tiene una asignación activa que pueda reasignarse.'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    area_destino_nombre = request.data.get('area_destino')
    if not area_destino_nombre:
        return Response(
            {
                'error': 'Área requerida',
                'message': 'Debe especificar el nombre del área destino.'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    area_destino = get_object_or_404(AreaResponsable, nombre=area_destino_nombre)

    # Evitar reasignar a la misma área
    area_actual = getattr(asignacion_actual.id_personal_asignado, 'id_area_responsable', None)
    if area_actual and area_actual.id_area_responsable == area_destino.id_area_responsable:
        return Response(
            {
                'error': 'Misma área',
                'message': 'La denuncia ya está asignada a esa área.'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Buscar un personal activo en el área destino
    personal_destino = (
        PersonalMunicipal.objects
        .filter(id_area_responsable=area_destino, estado_laboral='Activo')
        .order_by('id_personal')
        .first()
    )

    if personal_destino is None:
        return Response(
            {
                'error': 'Sin personal destino',
                'message': 'No se encontró personal activo en el área destino.'
            },
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Cerrar asignación actual
    asignacion_actual.es_activa = False
    asignacion_actual.fecha_finalizacion = timezone.now()
    asignacion_actual.save()

    # Crear nueva asignación
    motivo = request.data.get('motivo', '')
    nueva_asignacion = Asignacion.objects.create(
        motivo_asignacion=motivo,
        id_denuncia=denuncia,
        id_personal_asignado=personal_destino,
        id_personal_asignador=personal,
    )

    return Response(
        {
            'mensaje': 'Denuncia reasignada correctamente',
            'id_denuncia': denuncia.id_denuncia,
            'asignacion_actual': asignacion_actual.codigo_asignacion,
            'nueva_asignacion': nueva_asignacion.codigo_asignacion,
            'area_destino': area_destino.nombre,
            'personal_destino': f"{personal_destino.nombre} {personal_destino.apellido}",
        },
        status=status.HTTP_200_OK,
    )
