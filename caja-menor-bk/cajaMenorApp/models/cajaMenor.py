from django.db import models
from .user import User


class CajaMenor(models.Model):

    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    gastos = models.IntegerField(default=0)
    saldo = models.IntegerField(default=0)

    def __str__(self):
        return str(self.id) + ' ' + self.user.name + ' ' + self.user.id + ' ' + str(self.gastos) + ' ' + str(self.saldo)
