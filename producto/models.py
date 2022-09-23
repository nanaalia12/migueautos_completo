from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Marca(models.Model):
    nombre=models.CharField(max_length=20, unique=True,verbose_name="Nombre")
    class Estado(models.TextChoices):
        ACTIVO='Activo', _('Activo')
        INACTIVO='Inactivo', _('Inactivo')
        ANULADO='Anulado', _('Anulado')
    estado= models.CharField(max_length=10, choices=Estado.choices, verbose_name="Estado", default=Estado.ACTIVO)
    def __str__(self) -> str:
        return '%s' % (self.nombre)
    def clean(self):  
        self.nombre= self.nombre.capitalize()
    class Meta:
        verbose_name="marca"
        verbose_name_plural="marcas"
        
class Producto(models.Model):
    class Servicio(models.TextChoices):
        LATONERIA='Latoneria',_('Latoneria')
        PINTURA='Pintura',_('Pintura')   
    categoria=models.CharField(max_length=10, choices=Servicio.choices, verbose_name="Categoría")
    nombre=models.CharField(max_length=50, verbose_name="Nombre del producto ")
    stock=models.IntegerField(verbose_name="Cantidad")
    precio= models.IntegerField(verbose_name="Precio")
    precio_venta= models.IntegerField(default=0,verbose_name="Precio venta")
    
    class Estado(models.TextChoices):
        ACTIVO='Activo', _('Activo')
        INACTIVO='Inactivo', _('Inactivo')
        ANULADO='Anulado', _('Anulado')
    estado= models.CharField(max_length=10, choices=Estado.choices, verbose_name="Estado", default=Estado.ACTIVO)
    marca= models.ForeignKey(Marca, on_delete=models.SET_NULL, null=True, verbose_name=u"Marca")
    def __str__(self)-> str:
        return 'N:%s / M:%s / T:%s / C:%s / S:%s' % (self.nombre,self.marca,self.stock)
    def clean(self):
        self.nombre= self.nombre.title()
        
       