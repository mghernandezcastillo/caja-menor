from rest_framework import serializers
from cajaMenorApp.models.reporte import Reporte
from drf_extra_fields.fields import Base64ImageField


class ReporteSerializer(serializers.ModelSerializer):
    evidence = Base64ImageField(required=False)
    class Meta:
        model = Reporte
        fields = ['id', 'fecha', 'tipoServicio', 'caja_menor', 'nombre_usuario', 'detalle', 'valor', 'evidence']
