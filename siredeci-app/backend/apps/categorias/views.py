from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Categoria
from .serializers import CategoriaSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def categorias_list(request):
    """Lista pública de categorías activas para el registro de denuncias."""
    categorias = Categoria.objects.filter(esta_activo=True).order_by('id_categoria')
    serializer = CategoriaSerializer(categorias, many=True)
    return Response(serializer.data)
