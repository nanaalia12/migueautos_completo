from django.contrib import messages
from django.shortcuts import render, redirect
from django.shortcuts import render

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