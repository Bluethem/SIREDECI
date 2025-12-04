from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from apps.notificaciones.models import Notificacion, ConfiguracionNotificacion
from apps.usuarios.permissions import IsStaffLike


class UsuarioNotificacionesView(APIView):
    """Listar notificaciones internas del usuario autenticado (admin o personal municipal).

    GET /api/notificaciones/usuario/
    """

    permission_classes = [IsAuthenticated, IsStaffLike]

    def get(self, request):
        user = request.user

        notificaciones = (
            Notificacion.objects
            .filter(id_usuario=user, canal_envio='Interno')
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


class UsuarioNotificacionMarcarLeidaView(APIView):
    """Marcar una notificación interna como leída para el usuario autenticado.

    POST /api/notificaciones/usuario/marcar-leida/
    Body: {"id_notificacion": int}
    """

    permission_classes = [IsAuthenticated, IsStaffLike]

    def post(self, request):
        user = request.user
        id_notificacion = request.data.get('id_notificacion')

        if not id_notificacion:
            return Response(
                {'detail': 'id_notificacion es requerido'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            notificacion = Notificacion.objects.get(
                id_notificacion=id_notificacion,
                id_usuario=user,
            )
        except Notificacion.DoesNotExist:
            return Response(
                {'detail': 'Notificación no encontrada para este usuario'},
                status=status.HTTP_404_NOT_FOUND,
            )

        notificacion.estado_envio = 'Leído'
        notificacion.save(update_fields=['estado_envio'])

        return Response({'detail': 'Notificación marcada como leída'}, status=status.HTTP_200_OK)


class UsuarioConfiguracionNotificacionesView(APIView):
    """Obtener y actualizar configuración de notificaciones del usuario autenticado.

    GET /api/notificaciones/usuario/config/
    PUT /api/notificaciones/usuario/config/
    """

    permission_classes = [IsAuthenticated, IsStaffLike]

    def get_obj(self, user):
        config, _ = ConfiguracionNotificacion.objects.get_or_create(id_usuario=user)
        return config

    def get(self, request):
        user = request.user
        config = self.get_obj(user)
        data = {
            'recibir_email': config.recibir_email,
            'recibir_sms': config.recibir_sms,
            'recibir_push': config.recibir_push,
            'frecuencia_resumen': config.frecuencia_resumen,
            'horario_preferido': config.horario_preferido,
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        config = self.get_obj(user)

        # Usar get con fallback al valor actual para no resetear si no viene en la request
        if 'recibir_email' in request.data:
            config.recibir_email = bool(request.data.get('recibir_email'))
        if 'recibir_sms' in request.data:
            config.recibir_sms = bool(request.data.get('recibir_sms'))
        if 'recibir_push' in request.data:
            config.recibir_push = bool(request.data.get('recibir_push'))

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
