from rest_framework import serializers
from cajaMenorApp.models.tipoServicio import TipoServicio


class TipoServicioSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoServicio
        fields = ['nombre']

    def to_representation(self, obj):
        tipoServicio = TipoServicio.objects.get(nombre=obj.nombre)
        return {
            'nombre': tipoServicio.nombre
        }    