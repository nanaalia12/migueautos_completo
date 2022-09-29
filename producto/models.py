from django.db import models
from django.utils.translation import gettext_lazy as _
from miproyecto.settings import MEDIA_URL,STATIC_URL
from miproyecto.models import BaseModel
from crum import get_current_user
# Create your models here.
class Marca(BaseModel):
    nombre=models.CharField(max_length=20, unique=True,verbose_name="Nombre")
    class Estado(models.TextChoices):
        ACTIVO='Activo', _('Activo')
        INACTIVO='Inactivo', _('Inactivo')
        ANULADO='Anulado', _('Anulado')
    estado= models.CharField(max_length=10, choices=Estado.choices, verbose_name="Estado", default=Estado.ACTIVO)
    
    def __str__(self) -> str:
        return '%s' % (self.nombre)
    
    def save(self):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_created = user
            else:
                self.user_updated = user
        return super(Marca,self).save()
    
    def clean(self):  
        self.nombre= self.nombre.capitalize()
    class Meta:
        verbose_name="marca"
        verbose_name_plural="marcas"
        
class Producto(BaseModel):
    class Servicio(models.TextChoices):
        LATONERIA='Latoneria',_('Latoneria')
        PINTURA='Pintura',_('Pintura')
    image = models.ImageField(upload_to='producto/%y/%m/%d',null=True, blank=True)
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
        return '%s - %s - %s - %s' % (self.nombre,self.marca,self.stock,self.categoria)
    
    
    def clean(self):
        self.nombre = self.nombre.title()
    
    def save(self):
        user = get_current_user()
        if user is not None:
            if not self.pk:
                self.user_created = user
            else:
                self.user_updated = user
        return super(Producto,self).save()
        
    def get_image(self):
        if self.image:
            return '{}{}'.format(MEDIA_URL, self.image)
        return '{}{}'.format(STATIC_URL, 'img/logomigueautos.png')