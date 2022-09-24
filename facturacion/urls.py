
from django.urls import path
from .views import factura

urlpatterns = [
    path('generar/', factura, name='generar')
]