from django.db import models
import os
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model




def validate_file_extension(value):
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.sql']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Archivo no válido')
class Backup(models.Model):
    nombre = models.CharField(max_length = 200,default="Copia de Seguridad", blank=True)
    archivo = models.FileField(upload_to = "backup",validators=[validate_file_extension])
    fecha = models.DateTimeField(auto_now = True)
    
    
class BaseModel(models.Model):
    user_created = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,null=True, blank=True, related_name="user_created%(app_label)s_%(class)s_related")
    date_created = models.DateTimeField(auto_now_add=True,null=True, blank=True)
    
    user_updated = models.ForeignKey(get_user_model(),on_delete=models.CASCADE,null=True, blank=True,  related_name="user_updated%(app_label)s_%(class)s_related")
    date_updated = models.DateTimeField(auto_now=True,null=True, blank=True)
    
    class Meta:
        abstract = True