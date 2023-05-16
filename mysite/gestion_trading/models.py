from django.db import models



class Trade(models.Model):
    id_trade = models.AutoField(primary_key=True)
    activo = models.CharField(max_length=100)
    orden = models.CharField(max_length=100)
    stoploss = models.FloatField()
    takeprofit = models.FloatField()
    lotaje = models.FloatField(2)
    ratio =  models.CharField(max_length=100)
    beneficio_esperado = models.CharField(max_length=100)
    utilidad_proyectada = models.CharField(max_length=100)

    objects = models.Manager() # Administrador de objetos por defecto
    def __str__(self):
        return f"{self.id_trade}: {self.activo}"
    
trades = Trade.objects.all() # pylint: disable=E1101