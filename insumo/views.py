from django.shortcuts import render,redirect
from insumo.forms import  InsumoForm, MarcaForm, ServicioForm
from .models import Insumo, Marca, Servicio
from django.contrib.auth.decorators import login_required
from django.contrib import messages


    
# Create your views here.


# lOGICA DE insumo (EDITAR ELIMINAR Y OTRAS FUNCIONES)




@login_required(login_url='/login/')
def insumos(request):
    db_insumo = Insumo.objects.all()

    form = InsumoForm()
    if request.method == 'POST':
        form = InsumoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            marca = form.cleaned_data['marca']
            precio = form.cleaned_data['precio']
            print(str(precio))
            print(marca)
            if Insumo.objects.filter(nombre=nombre,marca=marca,precio=precio).exists():
                messages.success(request,'El insumo %s es existente' %nombre)
                
            if not Insumo.objects.filter(nombre=nombre, precio=precio,marca=marca).exists():
                Insumo.objects.create(nombre=nombre, precio=precio,marca=marca)
                messages.success(request,'El insumo %s ha registrado correctamente' %nombre)
                return redirect('insumo')
            else:
                form = InsumoForm()
    else:
        form = InsumoForm()
    context = {
        'insumos' : db_insumo,
        'form': form,
    } 
    return render (request, 'insumo/insumo.html', context)

@login_required(login_url='/login/')
def editarInsumo(request,id):   
    editar = Insumo.objects.get(id=id)
    marcas = Marca.objects.all()

    
    form = InsumoForm()
    if request.method == 'POST':
        form = InsumoForm(request.POST, instance=editar)
        if form.is_valid():
            insumo = form.cleaned_data['nombre']
            valor = form.cleaned_data['precio']
            marca = request.POST['marca']
            print(marca)
                
            if Insumo.objects.filter(nombre=insumo, precio=valor,marca=marca).exists():
                messages.warning(request,'Insumo ya registrado')
                return redirect('insumo')
            
            else:
                aux = form.save()
                Insumo.objects.filter(id=aux.id).update(nombre=aux.nombre,marca=aux.marca,precio=aux.precio)

                messages.success(request,'Insumo %s ha sido editado correctamente' % aux.nombre)
                return redirect('insumo')
    else:
        form = InsumoForm()
        
    context = {
         'insumo': form,
         'edit': editar,
         'marcas': marcas,
    }
    return render (request, 'insumo/editar.html', context) 
    
    
@login_required(login_url='/login/')
def eliminarInsumo(request,id):
    delete_insumo = Insumo.objects.get(id=id)
    url_back = 'insumo'
    txt_action = 'insumo'
    context = {
        'url_back': url_back,
        'txt_action': txt_action,
    }
    if request.method == 'POST' and 'eliminar' in request.POST: # si el metodo es post y el formulario es
        delete_insumo.delete() # se elimina el vehiculo
        messages.success(request,'Vehiculo %s  ha sido eliminado exitosamente' %delete_insumo.nombre) # se muestra un mensaje de exito
        return redirect ('insumo') # se redirecciona a la url
    if request.method == 'POST' and 'cancelar' in request.POST: # si el metodo es post y el formulario es form2
        #no se realiza ninguna accion por que el cliente decidio no eliminar el vehiculo
        return redirect ('insumo') 
    return render (request, 'insumo/eliminar/eliminar.html',context)

# LOGICA DE marca (EDITAR, ELIMINAR  Y OTRAS FUNCIONES)

@login_required(login_url='/login/')
def marca(request):
    db_insumo = Marca.objects.all()
    form = MarcaForm()
    if request.method == 'POST': 
        form = MarcaForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            
            if Insumo.objects.filter(nombre=nombre).exists():
                messages.success(request,'La marca %s ya existe'%nombre)
                return redirect ('insumo')
            else:
                form = MarcaForm(request.POST)
                s = form.save()
                s.save()
                messages.success(request,'La marca %s ha sido registrada exitosamente'%nombre)
                return redirect('insumo')
    context = {
        'marcas' :db_insumo,
        'form': form,
    }
    return render (request,'insumo/marca.html', context)

@login_required(login_url='/login/')
def editarmarca(request,id):
    editar = Marca.objects.get(id=id)
    marca = Marca.objects.all()
    if request.method == "POST" and 'cancelar':
        form = MarcaForm(request.POST,instance=editar)
        if form.is_valid():
            marca = request.POST['nombre'] #nose que quieres editar solo es un ejemplo
            if Marca.objects.filter(nombre=marca):
                messages.success(request,'Esta marca ya existe')
                return redirect ('insumo')
            else:
                form.save()
                messages.success(request,'La marca %s ha sido editada' %marca)
                return redirect ('insumo')
        else : 
            form = MarcaForm(instance=editar)
    if request.method == 'POST' and 'cancelar' in request.POST: 
        return redirect ('insumo')    
    else:
        form = MarcaForm(instance=editar)
    context={
        'formulario': form,
        'marca': editar,
        'marcas':marca,
    }
    return render (request, 'insumo/editar/editarmarca.html', context)  


@login_required(login_url='/login/')
def eliminarMarca(request,id):
    vehiculo_d = Marca.objects.get(id=id) # se obtiene el vehiculo
    vehiculo_db = Marca.objects.all() # se carga la base de datos para ver los vehiculos
    txt_action = 'este marca' # se define el texto de la accion
    if request.method == 'POST' and 'eliminar' in request.POST: # si el metodo es post y el formulario es
        vehiculo_d.delete() # se elimina el vehiculo
        messages.success(request,'Marca %s ha sido eliminada exitosamente' %vehiculo_d.nombre) # se muestra un mensaje de exito
        return redirect ('insumo') # se redirecciona a la url
    if request.method == 'POST' and 'cancelar' in request.POST: # si el metodo es post y el formulario es form2
        #no se realiza ninguna accion por que el cliente decidio no eliminar el vehiculo
        return redirect ('insumo') # se redirecciona a la url
    context = {
        'vehiculo_db': vehiculo_db,
        'txt_action': txt_action,  
    }
    return render (request, 'insumo/eliminar/eliminar.html',context)

def testing(request):

    return render(request, 'insumo/editar.html')