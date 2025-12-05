from rest_framework import serializers

from .models import Categoria


class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = [
            'id_categoria',
            'codigo_categoria',
            'nombre',
            'descripcion',
            'color',
            'icono',
            'tiempo_respuesta_promedio',
            'id_area_responsable',
        ]
