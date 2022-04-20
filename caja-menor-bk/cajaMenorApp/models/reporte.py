from django.db import models
from .tipoServicio import TipoServicio
from .cajaMenor import CajaMenor

from datetime import date 


class Reporte(models.Model):

    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField('fecha', blank=True, default=date.today())
    tipoServicio = models.ForeignKey(TipoServicio, on_delete=models.CASCADE)
    caja_menor = models.ForeignKey(CajaMenor, on_delete=models.CASCADE)
    nombre_usuario = models.CharField('Nombre Usuario',max_length= 50)
    detalle = models.TextField('Observacion',max_length= 500)
    valor = models.IntegerField('Valor',default=0)
    evidence = models.ImageField(upload_to='firmas', null=True , blank=True)


    def __str__(self):
        return self.id + ' ' + self.fecha.strftime('%d/%m/%Y') + ' ' + self.tipoServicio.nombre + ' ' + self.caja_menor.nombre + ' ' + self.nombre_usuario + ' ' + self.detalle + ' ' + str(self.valor)