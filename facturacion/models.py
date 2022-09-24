from django.db import models
from django.utils.translation import gettext_lazy as _
from registro.models import *
from producto.models import *
# Create your models here.

class Factura(models.Model):
    usuario = models.ForeignKey(Usuario,on_delete=models.CASCADE, verbose_name='usuario')
    vehiculo = models.ForeignKey(Vehículo, on_delete=models.CASCADE, verbose_name='vehiculo')
    valor = models.IntegerField(default=0, null=True, verbose_name='valor')
    class Estado(models.TextChoices):
        ABIERTA = 'Abierta', _('Abierta')
        CERRADA = 'Cerrada', _('Cerrada')
        ANULADA = 'Anulada', _('Anulada')
    estado =models.CharField(max_length=10,choices=Estado.choices,verbose_name='estado',default=Estado.ABIERTA)
    class Decision(models.TextChoices):
        ACTIVA = 'Activa', _('Activa')
        INACTIVA = 'Inactiva', _('Inactiva')
    decision = models.CharField(max_length=10,choices=Decision.choices,verbose_name='decision',default=Decision.ACTIVA)
    class META:
        db_table = "facturas_factura"
        verbose_name = "factura"
        verbose_plural = "facturas"
        

class Detalle(models.Model):
    factura = models.ForeignKey(Factura,on_delete=models.SET_NULL,null=True, verbose_name='Factura')
    producto = models.ForeignKey(Producto, on_delete=models.SET,verbose_name='Producto',null=True)
    class Estado(models.TextChoices):
        ABIERTA = 'Abierta', _('Abierta')
        CERRADA = 'Cerrada', _('Cerrada')
        ANULADA = 'Anulada', _('Anulada')
    estado = models.CharField(max_length=10,choices=Estado.choices,verbose_name='Estado',default=Estado.ABIERTA)
    cantidad_detalle = models.IntegerField(default=0)
    total = models.IntegerField(default=0)
    precio = models.IntegerField(default=0)
    
    def __str__(self) -> str:
        return '%s'%(self.factura)
    
    class Meta:
        db_table = 'Detalles_factura'
        verbose_name = 'Detalle'
    
        
class Servicio(models.Model):
    class Servi(models.TextChoices):
        LATONERIA = 'Latoneria', _('Latoneria')
        PINTURA = 'Pintura', _('Pintura')
    servicio = models.CharField(max_length=10,choices=Servi.choices)
    