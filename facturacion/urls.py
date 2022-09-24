
from django.urls import path
from .views import *

urlpatterns = [
    path('generar/', factura, name='generar'),
    path('detalle/<int:pk>/generada',detalle, name='detalle'),
]