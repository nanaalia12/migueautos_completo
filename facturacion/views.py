from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render

from django.db.models import Sum
from django.db import models

from .forms import *
from .models import *
from registro.models import *


# Create your views here.

def factura(request):
    titulo_pag = 'Creando factura'
    usuarios=Usuario.objects.all()
    vehiculos = Vehículo.objects.all()
    facturas = Factura.objects.all()
    
    if request.method == 'POST':
        form = FacturaForm(request.POST)
        if Factura.objects.filter(usuario=request.POST['usuario'],vehiculo=request.POST['vehiculo'],estado="Abierta").exists():
            form = FacturaForm()
            messages.warning(request,f'Ya hay una factura creada de ese usuario')
            return redirect('generar')
        
        else:
            if form.is_valid():
                usuario= Usuario.objects.get(id=request.POST['usuario']),
                vehiculo = Vehículo.objects.get(id = request.POST['vehiculo'])
                aux= Factura.objects.create(
                    vehiculo=vehiculo,
                    usuario= usuario[0],
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
    #Suma los precios y da un total
    if(Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))):
        total= Detalle.objects.filter(factura_id=factura_u.id).values("factura").annotate(total_definitivo=Sum(('total'),output_field=models.IntegerField()))[0]["total_definitivo"]
    else:
        total=0
    
    
    if request.method == 'POST':
        form= DetalleForm(request.POST)
        if form.is_valid():    
            producto= Producto.objects.get(id=request.POST['producto'])
            if(producto.stock >= int(request.POST['cantidad_detalle'])):
                    existe= Detalle.objects.filter(factura_id=factura_u.id,producto=producto)
                    if len(existe) == 0: 
                        
                        factura= Detalle.objects.create(
                                cantidad_detalle= form.cleaned_data.get('cantidad_detalle'),
                                total= producto.precio_venta *  form.cleaned_data.get('cantidad_detalle'),                                                          
                                factura=factura_u,               
                                producto = producto,
                                precioX= producto.precio_venta 
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
                        return redirect('factura-detalle', pk=pk)
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
    }
    return render(request, "app-factura/detalle/detallefactura.html", context)