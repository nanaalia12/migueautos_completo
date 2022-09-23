from tkinter.ttk import Widget
from django import forms
from .models import Usuario, Vehículo

class usuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre','apellido','identificacion','telefono']        
class vehiculoForm(forms.ModelForm):
    class Meta:
        model = Vehículo
        fields = ['placa','modelo','color','condición','usuario']

             
            
    

    