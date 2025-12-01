from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from apps.personal.serializers import (
    LoginAdminSerializer,
    PersonalMunicipalSerializer
)
from apps.usuarios.models import Usuario
from apps.usuarios.utils import get_codigos_roles, get_codigos_permisos


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

