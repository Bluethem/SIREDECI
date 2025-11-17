from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
import secrets
from .models import Ciudadano


class CiudadanoLoginView(APIView):
    """
    Vista para login de ciudadanos usando DNI + Fecha de Emisión
    No requiere autenticación previa
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        dni = request.data.get('dni')
        fecha_emision = request.data.get('fecha_emision')
        
        if not dni or not fecha_emision:
            return Response({
                'error': 'DNI y fecha de emisión son requeridos'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Buscar ciudadano por DNI y fecha de emisión
            ciudadano = Ciudadano.objects.get(
                dni=dni,
                fecha_emision_dni=fecha_emision,
                estado_cuenta='Activo'
            )
            
            # Generar token simple (no JWT, solo identificador de sesión)
            session_token = secrets.token_urlsafe(32)
            
            # Datos del ciudadano para la sesión
            ciudadano_data = {
                'id_ciudadano': ciudadano.id_ciudadano,
                'codigo_ciudadano': ciudadano.codigo_ciudadano,
                'dni': ciudadano.dni,
                'nombre': ciudadano.nombre,
                'apellido': ciudadano.apellido,
                'email': ciudadano.email,
                'id_usuario': ciudadano.id_usuario.id_usuario if ciudadano.id_usuario else None,
                'session_token': session_token
            }
            
            return Response({
                'mensaje': 'Login exitoso',
                'ciudadano': ciudadano_data,
                'tipo_usuario': 'ciudadano'
            }, status=status.HTTP_200_OK)
            
        except Ciudadano.DoesNotExist:
            return Response({
                'error': 'DNI o fecha de emisión incorrectos, o cuenta inactiva'
            }, status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'error': f'Error en el login: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CiudadanoRegistroView(APIView):
    """
    Vista para registro de nuevos ciudadanos
    """
    permission_classes = [AllowAny]
    
    def post(self, request):
        """
        Registrar un nuevo ciudadano
        """
        try:
            # Validar datos requeridos
            required_fields = ['dni', 'nombre', 'apellido', 'fecha_emision_dni']
            for field in required_fields:
                if not request.data.get(field):
                    return Response({
                        'error': f'El campo {field} es requerido'
                    }, status=status.HTTP_400_BAD_REQUEST)
            
            # Verificar si el DNI ya existe
            if Ciudadano.objects.filter(dni=request.data['dni']).exists():
                return Response({
                    'error': 'El DNI ya está registrado'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            # Crear ciudadano
            ciudadano = Ciudadano.objects.create(
                dni=request.data['dni'],
                nombre=request.data['nombre'],
                apellido=request.data['apellido'],
                fecha_emision_dni=request.data['fecha_emision_dni'],
                email=request.data.get('email'),
                direccion=request.data.get('direccion'),
                estado_cuenta='Activo'
            )
            
            return Response({
                'mensaje': 'Ciudadano registrado exitosamente',
                'ciudadano': {
                    'id_ciudadano': ciudadano.id_ciudadano,
                    'codigo_ciudadano': ciudadano.codigo_ciudadano,
                    'dni': ciudadano.dni,
                    'nombre': ciudadano.nombre,
                    'apellido': ciudadano.apellido
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'Error al registrar ciudadano: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
