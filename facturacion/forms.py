from django import forms
from .models import Factura
# Detalle


class FacturaForm(forms.ModelForm):
    class Meta: 
        model = Factura
        fields = ['usuario', 'vehiculo']
    