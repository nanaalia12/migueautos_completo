from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render

from django.db.models import Sum
from django.db import models

from registro.views import usuario

from .forms import *
from .models import *
from registro.models import *


# Create your views here.

def factura(request):
    titulo_pag = 'Creando factura'
    usuarios= Usuario.objects.all()
    vehiculos = Vehículo.objects.all()
    facturas = Factura.objects.all()

    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if Factura.objects.filter(usuario_id= request.POST['usuario '],vehiculo_id= request.POST['vehiculo'],).exists():
            form = FacturaForm()
            messages.warning(request,f'Ya hay una factura creada de ese usuario')
            return redirect('generar')
        else:
            if form.is_valid():
               
                aux= Factura.objects.create(
                    vehiculo_id= request.POST['vehiculo'],
                    usuario_id= request.POST['usuario '],
                )
                messages.success(request,f'Factura agregada correctamente') 
                return redirect('detalle',aux.id)
    else:
        form = FacturaForm()
    context={
        'base_datos':facturas,
        'form':form,
        "usuario":usuarios,
        "vehiculos":vehiculos,
        'titulo_pag': titulo_pag,
    }
    return render(request,'app-factura/factura/crearFactura.html', context)


def detalle(request,pk):
    titulo_pagina="facturas"
    detalles= Detalle.objects.filter(factura_id=pk)
    factura_u=Factura.objects.get(id=pk)
    productos = Producto.objects.filter(estado='Activo')
    titulo_pag = f'Agregando productos a la factura #{factura_u.id}'
    valor = 0
    #Suma los precios y da un total
    if(Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))):
        total= Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))[0]["total_definitivo"]
    else:
        total=0
    
    
    if request.method == 'POST':
        form= DetalleForm(request.POST)
        if form.is_valid():    
            producto= Producto.objects.get(id=request.POST['producto'])
            valor = request.POST['cantidad_detalle'] * producto.precio
            if(producto.stock >= int(request.POST['cantidad_detalle'])):
                    existe= Detalle.objects.filter(factura_id=factura_u.id,producto=producto)
                    if len(existe) == 0: 
                        
                        factura= Detalle.objects.create(
                                cantidad_detalle= form.cleaned_data.get('cantidad_detalle'),
                                total= producto.precio_venta *  form.cleaned_data.get('cantidad_detalle'),                                                          
                                factura=factura_u,               
                                producto = producto,
                                precio= producto.precio_venta 
                        )
                        
                        
                        
                        Producto.objects.filter(id=producto.id).update(
                            stock=producto.stock - form.cleaned_data.get('cantidad_detalle')
                        
                        )
                        
                        if(Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))):
                            total= Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))[0]["total_definitivo"]
                            Factura.objects.filter(id=pk).update(
                            valor=total                
                        )
                        else:
                            total=0
                        
                        messages.success(request,f' se agregó {producto} a la factura correctamente')
                        return redirect('detalle', pk=pk)
                    else:
                        anterior=Detalle.objects.filter(factura_id=factura_u.id,producto=request.POST['producto'])
                        
                        anterior.update(
                            
                            cantidad_detalle=anterior[0].cantidad_detalle + form.cleaned_data.get('cantidad_detalle'),
                            total=anterior[0].total + producto.precio * form.cleaned_data.get('cantidad_detalle'),
                        )
                        Producto.objects.filter(id=producto.id).update(
                            stock=producto.stock - form.cleaned_data.get('cantidad_detalle')
                        )
                        if(Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))):
                            total= Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))[0]["total_definitivo"]
                            Factura.objects.filter(id=pk).update(
                            valor=total                
                        )
                        else:
                            total=0
            else:
                messages.warning (request,f' Solo hay stock de {producto.stock} {producto.nombre}/s')
        else:
            messages.warning (request,f'Error')
    else:
        form= DetalleForm()
                    

            

    context ={
        'total':total,
        'detalle':detalles,
        'factura':factura_u,
        'productos':productos,
        'servicios': form,
        "titulo_pag":titulo_pag,
        'valor': valor
    }
    return render(request, "app-factura/detalle/detallefactura.html", context)


def detalle_estado(request,pk,cantidad ):
    titulo_pagina='producto'
    u_detalles= Detalle.objects.get(id=pk)
    factura_u= u_detalles.factura
    detalles= Detalle.objects.filter(factura_id=factura_u.id)
    accion_txt= f"el detalle {u_detalles.id} "
   
    if request.method == 'POST':
        if (factura_u.tipofactura =="Venta"):
            form= DetalleForm(request.POST)
            Producto.objects.filter(id=u_detalles.producto_id).update(
                stock=Producto.objects.get(id=u_detalles.producto_id).stock + int(cantidad),
            )
            Factura.objects.filter(id=factura_u.id).update(
                        neto_pagar=0
                        
            )
            u_detalles.delete()
            messages.success(request,f'Detalle elminado correctamente ')
            return redirect('factura-detalle',factura_u.id)
        else:
            form= DetalleForm(request.POST)
            Producto.objects.filter(id=u_detalles.producto_id).update(
                stock=Producto.objects.get(id=u_detalles.producto_id).stock - int(cantidad),
            )
            Factura.objects.filter(id=factura_u.id).update(
                        neto_pagar=0          
            )
            u_detalles.delete()
            messages.success(request,f'Detalle eliminado correctamente ')
            return redirect('factura-detalle',factura_u.id)
        
    else:
        
        form=DetalleForm()
    context={
            "titulo_pagina": titulo_pagina,
            "accion_txt":accion_txt,
            "detalles": detalles,
            "factura":factura_u,
            "form":form,
    }
    return render(request, "app-factura/detalle/detalle-eliminar.html", context)


def ver_factura(request,pk):
    factura = Factura.objects.get(id=pk)
    detalles_factura = Factura.objects.filter(factura_id=pk)
    titulo_pag = f'Factura #{factura.id}'
    context = {
        'factura':factura,
        'detalles':detalles_factura,
        'titulo_pag':titulo_pag,
        }
    return render(request,"app-factura/factura/verfactura.html", context)
    
def factura_eliminar(request,pk):
    titulo_pagina='Factura'
    tfacturas= Factura.objects.all()
    tfactura= Factura.objects.get(id=pk)
    accion_txt= f" la factura {tfactura.id}"
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        Factura.objects.filter(id=pk).update(
                    decision='Inactivo'
                )
        tfactura_usuario=  tfactura.usuario
        messages.success(request,f'Factura {tfactura.id} anulada correctamente')
        return redirect('factura-tfactura')
                
    else:
        form:FacturaForm()
    context={
            "titulo_pagina": titulo_pagina,
            "accion_txt":accion_txt,
            "tfacturas": tfacturas,
            
    }
    return render(request, "app-factura/factura/facturaeliminar.html", context)    
    
def factura_estado(request,pk, estado):

    tfactura= Factura.objects.get(id=pk)
    eliminacion= Detalle.objects.filter(factura=tfactura)
    veridetalle= Detalle.objects.filter(factura=tfactura)
    titulo_pagina='Factura'
    estado_msj=""
    estado_txt=""
    if estado == "Abierta":
        if not eliminacion.exists():
            estado_txt= "Eliminar"
            estado_msj= f"factura {tfactura.id}?"
            if request.method == 'POST':
                form = FacturaForm(request.POST)
                
                tfactura.delete()
                messages.success(request,f'Factura {pk} eliminada correctamente')
                return redirect('generar')
            else:
                form=FacturaForm()
        else:
            messages.warning(request,f'La factura {pk} no se puede eliminar, tiene productos registrados')
            return redirect('generar')
    elif estado == "C0errada":
        estado_txt= "Anular"
        estado_msj= f"Factura {tfactura.id}, una vez anulada no se podrá restablecer."
        if request.method == 'POST':
            form = FacturaForm(request.POST)
            Factura.objects.filter(id=pk).update(
                        estado='Anulada'
                    )
            tfactura_usuario=  tfactura.usuario
            messages.success(request,f'Factura {tfactura.id} anulada correctamente')
            return redirect('generar')
        else:
            form=FacturaForm()
    else:
        if veridetalle.exists():
            estado_txt= "Cerrar"
            estado_msj= f"{estado_txt} La factura {tfactura.id}, una vez cerrada no se podrán agregar nuevos productos?"
            if request.method == 'POST':
                form = FacturaForm(request.POST)
                Factura.objects.filter(id=pk).update(
                            estado='Cerrada'
                        )
                tfactura_usuario=  tfactura.usuario
                messages.success(request,f'Factura {tfactura.id} cerrada correctamente')
                return redirect('factura-tfactura')
            else:
                form:FacturaForm()
        else:
            messages.warning(request,f'La factura {pk} no se puede cerrar porque esta vacia')
            return redirect('factura-detalle', pk)
    context={
        "titulo_pagina": titulo_pagina,
        "estado_msj":estado_msj,
        "estado_txt":estado_txt,
           
    }
    return render(request, "app-factura/factura/factura-est     ado.html", context)