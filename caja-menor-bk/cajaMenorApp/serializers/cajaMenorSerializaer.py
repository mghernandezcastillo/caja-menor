from rest_framework import serializers
from cajaMenorApp.models.cajaMenor import CajaMenor


class CajaMenorSerializer(serializers.ModelSerializer):
    class Meta:
        model = CajaMenor
        fields = ['id', 'user', 'gastos', 'saldo']
    def to_representation(self, obj):
        cajaMenor = CajaMenor.objects.get(id=obj.id)
        return {
            'id': cajaMenor.id,
            'user': cajaMenor.user.name,
            'gastos': cajaMenor.gastos,
            'saldo': cajaMenor.saldo
        }