
from django.urls import path
from .views import marca,marca_eliminar,Editarmarca,producto,mostrarProducto,editarproducto,producto_eliminar
# marca_eliminar,marca, productoT, producto, Verproducto, Editarproducto,Editarmarca, producto_eliminar, productoInactivo

urlpatterns = [
   
    path('marca/', marca, name='producto-marca'),
    path('editarmarca/<int:pk>', Editarmarca, name='producto-editarmarca'),
    path('crearmarca/eliminar/<int:pk>/', marca_eliminar, name='producto-marca-eliminar'),
   
    
    path('crearproducto/', producto, name='producto-crearproducto'),
    path('', mostrarProducto, name='producto-producto'),
    path('editarproducto/<int:pk>', editarproducto, name='producto-editarproducto'),
    path('eliminar/<int:pk>/', producto_eliminar, name='producto-producto-eliminar'),
    
    # path('productoi/', productoInactivo, name='producto-productoI'),
    # path('verproducto/<int:pk>', Verproducto, name='producto-verproducto'),
]