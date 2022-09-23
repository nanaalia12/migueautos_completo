from django.db import models
from django.utils.translation import gettext_lazy as _

class Marca(models.Model):
    nombre = models.CharField(max_length=45, unique=False)
    class Estado(models.TextChoices):
        ACTIVO='Activo', _('Activo')
        INACTIVO='Inactivo', _('Inactivo')
        ANULADO='Anulado', _('Anulado')
    estado= models.CharField(max_length=10, choices=Estado.choices, verbose_name="Estado", default=Estado.ACTIVO)
    def __str__(self):
        return f'{self.nombre}'  


class Insumo(models.Model):
    nombre = models.CharField(max_length=45, unique=False )
    precio = models.PositiveIntegerField()
    marca =  models.ForeignKey(Marca,on_delete=models.CASCADE ,related_name="insumos_db")
    class Estado(models.TextChoices):
        ACTIVO='Activo', _('Activo')
        INACTIVO='Inactivo', _('Inactivo')
        ANULADO='Anulado', _('Anulado')
    estado= models.CharField(max_length=10, choices=Estado.choices, verbose_name="Estado", default=Estado.ACTIVO)   
    def __str__(self):
        return f'{self.nombre} $ {self.precio}., {self.marca}' 

class Servicio(models.Model):
    valor = models.IntegerField()
    def str(self):
        return self.valor
    
        