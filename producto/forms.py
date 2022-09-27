from django.forms import ModelForm
from .models import Marca,Producto
from django import forms

class MarcaForm(ModelForm):
    class Meta:
        model = Marca
        fields= ['nombre']
        
class ProductoForm(ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(ProductoForm, self).__init__(*args, **kwargs)
        self.fields['precio'].widget.attrs['min'] = 1
        self.fields['stock'].widget.attrs['min'] = 1
        # self.fields['marca'].widget.attrs['min'] = 1
    def clean(self):
        nombre = self.cleaned_data['nombre']
        # marca = self.cleaned_data['marca']
        categoria = self.cleaned_data['categoria']
        if Producto.objects.filter(nombre=nombre).exists():
            pass
    class Meta:
        model= Producto
        fields= ['image','categoria','nombre','precio', 'stock'] 
        
class DetalleForm(forms.Form):
    cantidad_stock = forms.IntegerField(label='cantidad_stock')
    def __init__(self, *args, **kwargs):
        super(DetalleForm, self).__init__(*args, **kwargs)
        self.fields['cantidad_stock'].widget.attrs['min'] = 1
        
    def clean_price(self):
        price = self.cleaned_data['price']
        if price < 1:
            raise forms.ValidationError("Price cannot be less than 0.01")
        return price

