from django.urls import path
from insumo.views import *


urlpatterns = [

    path ('insumo/', insumos, name='insumo'),
    path('marca/', marca, name='marca'),

     #marca MARCA
    path ('marca/editarMarca/<int:id>', editarmarca, name='editarmarca'),
    
    #Insumo
    path ('insumo/eliminarInsumo/<int:id>', eliminarInsumo, name='eliminarInsumo'),
    path ('insumo/editarInsumo/<int:id>', editarInsumo, name='editarInsumo'),
    
    # TESTING
    path('testing/',testing, name='testing'),
]