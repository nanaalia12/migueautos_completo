
from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render


from .forms import *
from .models import *
from registro.models import *
# Create your views here.
def marca(request):

    """ En esta funcion se carga formulario y se guarda en la base de datos, y tambien imprime esta 
    informacion en el mismo HTML en una tabla
    """
    titulo_pagina="Productos"
    marcas= Marca.objects.all()
    if request.method == 'POST':
        form= MarcaForm(request.POST)
        if form.is_valid():
            form.save()
            marca_nombre= form.cleaned_data.get('nombre')
            messages.success(request,f'Marca {marca_nombre} agregada correctamente')
        else:
            nombre = request.POST.get('nombre')
            messages.warning(request,f'La marca {nombre} ya existente')
        return redirect('producto-marca')
    else:
        form = MarcaForm()
    context={
        "titulo_pagina": titulo_pagina,
        "marcas": marcas,
        "form":form
    }
    return render(request, "app-producto/marca/crearmarca.html", context)

def marca_eliminar(request,pk):

    """
    Tiene como funcionamiento eliminar por id la marca de la base de datos
    """

    marcas= Marca.objects.all()
    marca= Marca.objects.get(id=pk)
    producto= Producto.objects.filter(marca_id = pk)
    form = MarcaForm()
    txt_action= f"la marca {marca.nombre}"
    if request.method == 'POST' and 'aceptar' in request.POST:
        form = MarcaForm(request.POST)
        if len(producto) == 0:
            Marca.objects.filter(id=pk).delete()
            marca_nombre= marca.nombre
            messages.success(request,f'La marca {marca_nombre} ha eliminada correctamente')
            return redirect('producto-marca')
        else:
            messages.warning(request,f'Marca no se puede eliminar porque se esta usando')
            return redirect('producto-marca')
    if request.method == 'POST' and 'cancelar' in request.POST: # si el metodo es post y el formulario es form2
        #no se realiza ninguna accion por que el cliente decidio no eliminar el vehiculo
        return redirect ('producto-marca') # se redirecciona a la url
    else:
        form:MarcaForm()
    context={
            "txt_action":txt_action,
            "marcas": marcas,
            'form': form
            
    }
    return render(request, "app-producto/marca/marca-eliminar.html", context)

def Editarmarca(request,pk):
    titulo_pagina="Producto"
    marcas= Marca.objects.get(id=pk)
    if request.method == 'POST':
        form= MarcaForm(request.POST, instance=marcas)
        if form.is_valid():
            form.save()
        return redirect('producto-marca')
    else:
        form= MarcaForm(instance=marcas)
        
        context={
        "marcas": marcas,
        "titulo_pagina": titulo_pagina,
        'form':form
    }
    return render(request, "app-producto/marca/editarmarca.html", context)





def mostrarProducto(request,pk):
    producto = Producto.objects.get(id=pk)
    titulo_pag = f'Producto {producto.nombre}'
    context = {
        'producto': producto,
        'titulo_pag': titulo_pag,
    }
    return render(request, "app-producto/producto/verproducto.html")


def editarproducto(request,pk):
    producto = Producto.objects.get(id=pk)
    titulo_pag = f'Editando producto {producto.nombre}'
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        nombre_producto = request.POST['nombre']
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            marca = form.cleaned_data['marca']
            categoria = form.cleaned_data['categoria']
        if Producto.objects.filter(nombre=nombre,marca=marca,categoria=categoria).exists():
            messages.success(request,f'El producto {nombre_producto} coincide con los mismos datos de otro producto')
            return redirect('producto-crearproducto')
        else:
            aux = form.save()
            messages.success(request,f'Producto {nombre_producto} agregado correctamente')
            return redirect('producto-crearproducto')
        
    else:
        form = ProductoForm(instance=producto)
        context={
        "producto": producto,
        "titulo_pagina":titulo_pag,
        'form': form,
    }
    return render(request,'app-producto/producto/editarproducto.html', context)

def producto_eliminar(request,pk):
    titulo_pagina='producto'
    productoTs= Producto.objects.all()
    productoT= Producto.objects.get(id=pk)
    accion_txt= f"producto {productoT.id}"
    if request.method == 'POST' and 'aceptar' in request.POST:
        form = ProductoForm(request.POST)
        Producto.objects.filter(id=pk).update(
                    estado='Inactivo'
                )
        productoT_nombre= productoT.nombre
        messages.success(request,f'Producto {productoT_nombre} eliminado correctamente')
        return redirect('producto-crearproducto')
    if request.method == 'POST' and 'cancelar' in request.POST:
        return redirect ('producto-crearproducto')
    else:
        form:ProductoForm()
    context={
            "titulo_pagina": titulo_pagina,
            "accion_txt":accion_txt,
            "productoTs": productoTs,
            
    }
    return render(request, "app-producto/producto/eliminar-producto.html", context)

def productoInactivo (request):
    """
    Se imprime la informacion de todos los productos guardados
    en la base de datos 
    """
    titulo_pagina="Producto"
    productoTs= Producto.objects.all() 
    context= {
        "productoTs": productoTs,
        "titulo_pagina":titulo_pagina
    }
    return render(request,"app-producto/producto/productoInactivo.html", context)

def producto(request):
    usuario_c= Usuario.objects.exclude(estado="Inactivo")
    titulo_pagina="Agregar Producto"
    productt = Producto.objects.filter()

    if request.method == 'POST':
        form = ProductoForm(request.POST)    
        producto_nombres= request.POST['nombre']
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            marca = form.cleaned_data['marca']

            if Producto.objects.filter(nombre=nombre, marca=marca).exists():
                messages.warning(request,f'Ya hay un producto registrado con esas caracteristicas')
                return redirect('producto-crearproducto')
            else:
                aux= form.save()
                Producto.objects.filter(id=aux.id).update(
                    precio_venta=aux.precio,
                    
                )
                messages.success(request,f'Producto {producto_nombres} agregado correctamente')
                return redirect('producto-crearproducto')
        else:
            messages.warning(request,f'Producto {producto_nombres} no se pudo agregar')
    else:
        form = ProductoForm()
    context={
        'base_datos':productt, 
        'form':form,  
        "titulo_pagina":titulo_pagina,
        "usuario":usuario_c
        }
    
    return render(request,'app-producto/producto/crearproducto.html', context)