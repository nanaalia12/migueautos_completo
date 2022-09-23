

from django.shortcuts import render, redirect
from registro.forms import usuarioForm, vehiculoForm
from registro.models import Usuario, Vehículo
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

# Registrar Usuario y vehiculo
@login_required(login_url='/login/')
def usuario(request): # se define la funcion para ver los usuarios
    usuario_db = Usuario.objects.all() #Se carga la base de datos
    formulario = usuarioForm(request.POST or None, request.FILES or None) # se carga el formulario
    if formulario.is_valid(): # si el formulario es valido
        nombre = request.POST.get('nombre')
        formulario.save() # se guarda el formulario
        messages.success(request, '¡Cliente %s ha sido registrado exitosamente!' %nombre) # se muestra un mensaje de exito
        return redirect('vehiculo') # se redirecciona a la url
    # se redirecciona a la url
    context = { # se define el contexto
        'usuario_db': usuario_db,	
        'formulario': formulario,
    }
    return render (request, 'registro/usuario.html', context) # se renderiza la pagina


@login_required(login_url='/login/') # se define la funcion para ver los vehiculos
def vehiculo(request): # se define la funcion para ver los vehiculos
    vehiculo_db = Vehículo.objects.all() # se carga la base de datos para ver los vehiculos
    usuario_db = Usuario.objects.all() # se carga la base de datos para el select de usuario # se carga el formulario
    vehiculo = vehiculoForm(request.POST or None)
    if vehiculo.is_valid(): # si el formulario es valido
        placa = request.POST.get('placa') 
        vehiculo.save() # se guarda el formulario
        messages.success(request,'¡Vehiculo %s ha sido registrado exitosamente!'%placa) # se muestra un mensaje de exito
        return redirect('insumo') # se redirecciona a la url
    else:
        print ('no entra')
    context = { # se define el contexto
        'vehiculo_db': vehiculo_db,
        'vehiculo': vehiculo,
        'usuario_db': usuario_db,
    }
    return render (request, 'registro/vehiculo.html', context) # se renderiza la pagina


#Eliminar usuario o vehiculo
@login_required(login_url='/login/')
def usuariodelete(request,id): # se define la funcion para eliminar un usuario
    delete_user = Usuario.objects.get(id=id) # se obtiene el usuario
    usuario_db = Usuario.objects.all() # se carga la base de datos
    formulario = usuarioForm() # se carga el formulario
    txt_action = 'este usuario'
    if request.method == 'POST' and 'aceptar' in request.POST: # si el metodo es post y el formulario es form1
        Usuario.objects.filter(id=id).update(
                   estado='Inactivo',
            ) #se elimina el usuario
        messages.success(request,'El Usuario %s esta inactivo' %delete_user.nombre) # se muestra un mensaje de exito
        return redirect ('usuario') # se redirecciona a la url
    if request.method == 'POST' and 'cancelar' in request.POST: # si el metodo es post y el formulario es form2
        return redirect ('usuario') # se redirecciona a la url
    context = {
        'usuario_db': usuario_db,
        'formulario': formulario,
        'txt_action':txt_action,
        } # se define el contexto
    return render (request,'registro/eliminar/eliminarusuario.html', context ) # se renderiza la pagina
@login_required(login_url='/login/')
def activarusuario(request,id): # se define la funcion para eliminar un usuario
    delete_user = Usuario.objects.get(id=id) # se obtiene el usuario
    usuario_db = Usuario.objects.all() # se carga la base de datos
    formulario = usuarioForm() # se carga el formulario
    txt_action = 'este usuario'
    if request.method == 'POST' and 'aceptar' in request.POST: # si el metodo es post y el formulario es form1
        Usuario.objects.filter(id=id).update(
                   estado='Activo',
            ) #se elimina el usuario
        messages.success(request,'El usuario %s esta activo' %delete_user.nombre) # se muestra un mensaje de exito
        return redirect ('usuario') # se redirecciona a la url
    if request.method == 'POST' and 'cancelar' in request.POST: # si el metodo es post y el formulario es form2
        return redirect ('usuario') # se redirecciona a la url
    context = {
        'usuario_db': usuario_db,
        'formulario': formulario,
        'txt_action':txt_action,
        } # se define el contexto
    return render (request,'registro/activar/activarusuario.html', context )
@login_required(login_url='/login/')
def vehiculoDelete(request,id):
    vehiculo_d = Vehículo.objects.get(id=id) # se obtiene el vehiculo
    vehiculo_db = Vehículo.objects.all() # se carga la base de datos para ver los vehiculos
    txt_action = 'Este vehículo' # se define el texto de la accion
    formulario = vehiculoForm() # se carga el formulario
    if request.method == 'POST' and 'aceptar' in request.POST: # si el metodo es post y el formulario es
        Vehículo.objects.filter(id=id).update(
                   estado='Inactivo',
             ) 
        messages.success(request,'El vehículo %s esta inactivo' %vehiculo_d.placa) # se muestra un mensaje de exito
        return redirect ('vehiculo') # se redirecciona a la url
    if request.method == 'POST' and 'cancelar' in request.POST: # si el metodo es post y el formulario es form2
        #no se realiza ninguna accion por que el cliente decidio no eliminar el vehiculo
        return redirect ('vehiculo') # se redirecciona a la url
    context = {
        'vehiculo_db': vehiculo_db,
        'formulario': formulario,
        'txt_action': txt_action
        }
    return render (request,'registro/eliminar/eliminarvehiculo.html', context )
@login_required(login_url='/login/')
def activarvehiculo(request,id): # se define la funcion para eliminar un usuario
    vehiculo_d = Vehículo.objects.get(id=id) # se obtiene el vehiculo
    vehiculo_db = Vehículo.objects.all() # se carga la base de datos para ver los vehiculos
    txt_action = 'este vehiculo' # se define el texto de la accion
    formulario = vehiculoForm()
    if request.method == 'POST' and 'aceptar' in request.POST: # si el metodo es post y el formulario es
        Vehículo.objects.filter(id=id).update(
                   estado='Activo',
             ) 
        messages.success(request,'El vehículo %s esta activo' %vehiculo_d.placa) # se muestra un mensaje de exito
        return redirect ('vehiculo') # se redirecciona a la url
    if request.method == 'POST' and 'cancelar' in request.POST: # si el metodo es post y el formulario es form2
        #no se realiza ninguna accion por que el cliente decidio no eliminar el vehiculo
        return redirect ('vehiculo') # se redirecciona a la url
    context = {
        'vehiculo_db': vehiculo_db,
        'formulario': formulario,
        'txt_action': txt_action
        }
        # se define el contexto
    return render (request,'registro/activar/activarvehiculo.html', context )
#Editar usuario o vehiculo
@login_required(login_url='/login/')
def editarUsuario(request,id): # se define la funcion para editar un usuario
    edit_user = Usuario.objects.get(id=id) # se obtiene el usuario

    formulario = usuarioForm(request.POST or None, request.FILES or None, instance=edit_user) # se carga el formulario
    if formulario.is_valid() and request.method == 'POST': # si el formulario es valido y el metodo es post
        formulario.save() # se guarda el formulario
        messages.success(request, '¡Usuario %s ha sido editado exitosamente!' %edit_user.nombre) # se muestra un mensaje de exito
        return redirect('usuario') # se redirecciona a la url
    context = { # se define el contexto
        'formulario': formulario,
        'edit': edit_user,
    }
    return render (request, 'registro/usuario.html', context)  # se renderiza la pagina
     

# LOGICA DE VEHICULO (EDITAR, ELIMINAR  Y OTRAS FUNCIONES)

@login_required(login_url='/login/')
def editarVehiculo(request,id): # se define la funcion para
    edit_vehiculo = Vehículo.objects.get(id=id) # se obtiene el vehiculo
    formulario_vehiculo = vehiculoForm(request.POST or None, instance=edit_vehiculo) # se carga el formulario
    usuario_db = Usuario.objects.all() # se carga la base de datos para el select de usuario 

    if formulario_vehiculo.is_valid() and request.method == 'POST': # si el formulario es valido y el metodo es post
        formulario_vehiculo.save() # se guarda el formulario
        messages.success(request, '¡Vehiculo %s ha sido editado exitosamente!' %edit_vehiculo.placa) # se muestra un mensaje de exito
        return redirect('vehiculo') # se redirecciona a la url
    context={ # se define el contexto
        'vehiculo': formulario_vehiculo,
        'edit': edit_vehiculo,
        'usuario_db': usuario_db
    }
    return render (request, 'registro/vehiculo.html', context)  # se renderiza la pagina 
