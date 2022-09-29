
from django.urls import path
from .views import *

urlpatterns = [
    path('generar/', factura, name='generar'),
    path('estado/<int:pk>/<str:estado>/', factura_estado, name='factura_estado'),
    
    
    path('detalle/<int:pk>/generada',detalle, name='detalle'),
    path('detalle-estado/eliminar/<int:pk>/<str:cantidad>', detalle_estado, name='detalle_eliminar_estado'),
]