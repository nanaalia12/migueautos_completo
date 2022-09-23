from django import forms
from insumo.models import Insumo, Marca,Servicio

class ServicioForm(forms.ModelForm):
    class Meta:
        model= Servicio
        fields='__all__' 
        #fields= '__all__'
        
class InsumoForm(forms.ModelForm):
    class Meta:
        model = Insumo
        fields= ['nombre','precio','marca']
    def clean(self): 
            nombre = self.cleaned_data['nombre']
            precio = self.cleaned_data['precio']
            if Insumo.objects.filter(nombre=nombre,precio=precio).exists():
                raise forms.ValidationError('Registro existente.') 
            #fields = '__all__'
        
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields=['nombre'] 
        #fields = '__all__'    
    def clean(self):
        nombre = self.cleaned_data['nombre']
        if Marca.objects.filter(nombre=nombre).exists():
            raise forms.ValidationError('La marca ya existe.')        