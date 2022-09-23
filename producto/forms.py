from django.forms import ModelForm
from .models import Marca,Producto


class MarcaForm(ModelForm):
    class Meta:
        model = Marca
        fields= ['nombre']
        
class ProductoForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['precio'].widget.attrs['min'] = 1
        self.fields['stock'].widget.attrs['min'] = 1
        self.fields['marca'].widget.attrs['min'] = 1
    def clean(self):
        nombre = self.cleaned_data['nombre']
        marca = self.cleaned_data['marca']
        categoria = self.cleaned_data['categoria']
        if Producto.objects.filter(nombre=nombre, marca=marca, ).exists():
            pass
    class Meta:
        model= Producto
        fields= ['categoria','nombre','precio', 'stock','marca'] 