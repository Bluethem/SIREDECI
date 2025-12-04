from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.utils import timezone
from datetime import timedelta
import secrets
from .models import Ciudadano
from apps.notificaciones.models import Notificacion, ConfiguracionNotificacion


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


class CiudadanoNotificacionesView(APIView):
    """Listar notificaciones internas de un ciudadano por id_usuario.

    GET /api/ciudadano/notificaciones/?id_usuario=ID
    """

    permission_classes = [AllowAny]

    def get(self, request):
        id_usuario = request.query_params.get('id_usuario') or request.GET.get('id_usuario')
        if not id_usuario:
            return Response({'detail': 'id_usuario es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        notificaciones = (
            Notificacion.objects
            .filter(id_usuario_id=id_usuario, canal_envio='Interno')
            .select_related('id_denuncia')
            .order_by('-fecha_creacion')[:100]
        )

        data = []
        for n in notificaciones:
            denuncia = n.id_denuncia
            data.append({
                'id_notificacion': n.id_notificacion,
                'codigo_notificacion': n.codigo_notificacion,
                'tipo_notificacion': n.tipo_notificacion,
                'mensaje': n.mensaje_personalizado,
                'fecha_creacion': n.fecha_creacion.isoformat() if n.fecha_creacion else None,
                'fecha_envio': n.fecha_envio.isoformat() if n.fecha_envio else None,
                'canal_envio': n.canal_envio,
                'estado_envio': n.estado_envio,
                'denuncia': {
                    'id_denuncia': getattr(denuncia, 'id_denuncia', None),
                    'codigo_denuncia': getattr(denuncia, 'codigo_denuncia', None),
                    'numero_seguimiento': getattr(denuncia, 'numero_seguimiento', None),
                    'titulo': getattr(denuncia, 'titulo', None),
                } if denuncia else None,
            })

        return Response({'results': data}, status=status.HTTP_200_OK)


class CiudadanoNotificacionMarcarLeidaView(APIView):
    """Marcar una notificación como leída para un ciudadano.

    POST /api/ciudadano/notificaciones/marcar-leida/
    Body: {"id_notificacion": int, "id_usuario": int}
    """

    permission_classes = [AllowAny]

    def post(self, request):
        id_notificacion = request.data.get('id_notificacion')
        id_usuario = request.data.get('id_usuario')

        if not id_notificacion or not id_usuario:
            return Response(
                {'detail': 'id_notificacion e id_usuario son requeridos'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            notificacion = Notificacion.objects.get(
                id_notificacion=id_notificacion,
                id_usuario_id=id_usuario,
            )
        except Notificacion.DoesNotExist:
            return Response(
                {'detail': 'Notificación no encontrada para este usuario'},
                status=status.HTTP_404_NOT_FOUND,
            )

        notificacion.estado_envio = 'Leído'
        notificacion.save(update_fields=['estado_envio'])

        return Response({'detail': 'Notificación marcada como leída'}, status=status.HTTP_200_OK)


class CiudadanoConfiguracionNotificacionesView(APIView):
    """Obtener y actualizar la configuración de notificaciones del ciudadano.

    GET /api/ciudadano/notificaciones/config/?id_usuario=ID
    PUT /api/ciudadano/notificaciones/config/?id_usuario=ID
    """

    permission_classes = [AllowAny]

    def get_obj(self, id_usuario):
        config, _ = ConfiguracionNotificacion.objects.get_or_create(id_usuario_id=id_usuario)
        return config

    def get(self, request):
        id_usuario = request.query_params.get('id_usuario') or request.GET.get('id_usuario')
        if not id_usuario:
            return Response({'detail': 'id_usuario es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        config = self.get_obj(id_usuario)
        data = {
            'recibir_email': config.recibir_email,
            'recibir_sms': config.recibir_sms,
            'recibir_push': config.recibir_push,
            'frecuencia_resumen': config.frecuencia_resumen,
            'horario_preferido': config.horario_preferido,
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        id_usuario = request.query_params.get('id_usuario') or request.GET.get('id_usuario')
        if not id_usuario:
            return Response({'detail': 'id_usuario es requerido'}, status=status.HTTP_400_BAD_REQUEST)

        config = self.get_obj(id_usuario)

        config.recibir_email = bool(request.data.get('recibir_email', config.recibir_email))
        config.recibir_sms = bool(request.data.get('recibir_sms', config.recibir_sms))
        config.recibir_push = bool(request.data.get('recibir_push', config.recibir_push))

        frecuencia = request.data.get('frecuencia_resumen')
        if frecuencia:
            config.frecuencia_resumen = frecuencia

        horario = request.data.get('horario_preferido')
        if horario is not None:
            config.horario_preferido = horario

        config.save()

        data = {
            'recibir_email': config.recibir_email,
            'recibir_sms': config.recibir_sms,
            'recibir_push': config.recibir_push,
            'frecuencia_resumen': config.frecuencia_resumen,
            'horario_preferido': config.horario_preferido,
        }
        return Response(data, status=status.HTTP_200_OK)
