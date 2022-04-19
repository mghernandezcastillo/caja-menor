from django.db import models
from .user import User


class cajaMenor(models.Model):

    nombre = models.CharField(
        'nombre_empresa', max_length=50, primary_key=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    direccion = models.CharField('direccion', max_length=50)
    ciudad = models.CharField('ciudad', max_length=50)
    celular = models.CharField('celular', max_length=50)

    def __str__(self):
        return self.nombre + ' ' + self.empresa.nombre + ' ' + self.direccion + ' ' + self.ciudad + ' ' + self.celular
