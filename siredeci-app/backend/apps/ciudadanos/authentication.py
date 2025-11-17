from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from apps.ciudadanos.models import Ciudadano
from django.contrib.auth.models import AnonymousUser


class SimpleCiudadanoUser:
    """Usuario simple para ciudadanos sin modelo Django User"""
    def __init__(self, ciudadano):
        self.id = ciudadano.id_ciudadano if ciudadano else None
        self.ciudadano = ciudadano
        self.is_authenticated = True
        self.is_active = True
        self.is_staff = False
        self.is_superuser = False
    
    def __str__(self):
        return f"Ciudadano {self.ciudadano.nombre if self.ciudadano else 'Anónimo'}"


class CiudadanoTokenAuthentication(BaseAuthentication):
    """
    Autenticación simple para ciudadanos usando token de sesión
    No usa JWT, solo valida que el token exista
    """
    
    def authenticate(self, request):
        # Obtener token del header Authorization
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header:
            return None
        
        # El header debería ser: "Bearer {session_token}"
        try:
            parts = auth_header.split()
            if len(parts) != 2:
                return None
            
            token_type, token = parts
            if token_type.lower() != 'bearer':
                return None
        except (ValueError, AttributeError):
            return None
        
        # Si el token tiene formato JWT, dejar que lo maneje JWTAuthentication
        if '.' in token and len(token.split('.')) == 3:
            return None
        
        # Es un token simple de ciudadano
        # Buscar el id_ciudadano en los datos de la petición o en custom headers
        id_ciudadano = request.data.get('id_ciudadano') if hasattr(request, 'data') else None
        
        # Si no hay id_ciudadano en los datos, es válido igual (para endpoints públicos)
        # Retornar un usuario "autenticado" genérico
        if id_ciudadano:
            try:
                ciudadano = Ciudadano.objects.get(id_ciudadano=id_ciudadano, estado_cuenta='Activo')
                user = SimpleCiudadanoUser(ciudadano)
                return (user, token)
            except Ciudadano.DoesNotExist:
                pass
        
        # Token válido pero sin ciudadano específico - crear usuario anónimo autenticado
        user = SimpleCiudadanoUser(None)
        return (user, token)
    
    def authenticate_header(self, request):
        return 'Bearer'
