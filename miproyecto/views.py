import datetime
import os
from time import strftime
from django.shortcuts import render,redirect
from datetime import date
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from miproyecto.forms import BackupForm
from miproyecto.models import Backup


def index(request):
    day  = timezone.now()
    hour = timezone.now()
    #prueba numero a
    #formatedHour = hour.strftime("%Y/%m/%d %H:%M:%S")
    formatedDay  = strftime("%d/%m/%Y")
    formatedHour = strftime("%r")
    # today = date.today()
    # fecha = today.strftime("%B %d, %Y")
    # hora = datetime.time(datetime.datetime.now().hour, datetime.datetime.now().minute, datetime.datetime.now().second)
    context = {
    'fecha': formatedDay,
    'hora': formatedHour,
    }
    return render(request, 'index.html', context)

@login_required(login_url='/login/')
def exportar_datos():
    fecha=date.today()
    os.system(f"mysqldump --add-drop-table --column-statistics=0 -u root --password=0000 migueautos> static/backup/BKP_{fecha}.sql")
   
@login_required(login_url='/login/')
def importar_datos(archivo):
    try:
        os.system(f"mysql -u root password=0000 migueautos< {archivo[1:]}")
    except:
        print("Problemas al importar")
       
@login_required(login_url='/login/')            
def backup(request,tipo):
   
    ejemplo_dir = 'static/backup/'
    with os.scandir(ejemplo_dir) as ficheros:
        ficheros = [fichero.name for fichero in ficheros if fichero.is_file()]
    print(ficheros)
    filtrado=[]
    backups = Backup.objects.all()
    if request.method == 'POST' and tipo== "U":
        # Fetching the form data
        
        form = BackupForm(request.POST, request.FILES)
        if form.is_valid():
            nombre= request.POST['nombre']
            archivo = request.FILES['archivo']
            
            insert = Backup(nombre=nombre, archivo=archivo)
            insert.save()
            
            importar_datos(insert.archivo.url)
            
            insert = Backup(nombre=nombre, archivo=archivo)
            insert.save()
            
            return redirect('backup','A')
        else:
            print( "Error al procesar el formulario")
              
    elif request.method == 'POST' and tipo== "D":
        exportar_datos()
        return redirect('backup','A')
    
    else:
        form = BackupForm()
      
        
    context ={
        "ficheros":ficheros,
        "form":form,
        "backups":backups
    }
    return render(request, 'backup.html',context)  