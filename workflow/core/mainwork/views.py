from django.shortcuts import render, redirect
from django.db import connection
import cx_Oracle
from django.contrib import messages
from .models import *
from django.contrib.auth import logout
from core.cliente.views import *
from core.ejecucion.views import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.
def index(request):
	return render(request, 'index.html')


def logged_in(request):

	return render(request, 'menuPrincipal.html')


def menuPrincipal(request):
    #Rol del Usuario (admin, diseñador, gerente, jefe, funcionario)
    perfil = request.user.rol_id
    empresa = Empresa.objects.get(idempresa = request.user.empresa_id)
    request.session['EmpresaUsuario'] = empresa.nombre

    try:
        unidad = Unidad.objects.get(idunidad = request.user.unidad_id)
        request.session['UnidadUsuario'] = unidad.nombre 
        
    except ObjectDoesNotExist as e:
        unidad = None
        request.session['UnidadUsuario'] = None

    try:
        cargo = Cargo.objects.get(idcargo = request.user.cargo_id)
        request.session['CargoUsuario'] = cargo.nombre
    except ObjectDoesNotExist:
        cargo = None  
        request.session['CargoUsuario'] = None

    
    #Si el perfil es Admin o Diseñador 
    if perfil == 1 :
        return redirect(procesos_Process)
    elif perfil == 2:
        return redirect(procesos_Process)
    elif perfil == 3:
        return redirect(procesos_Gerente)
    elif perfil == 4:
        return redirect(procesos_Jefe)
    elif perfil == 5:
        return redirect(procesos_Funcionario)

  
    return render(request, 'menuPrincipal.html')



def empresas(request):
    data = {
        'empresas':listar_empresas()
        }

    return render(request, 'Empresa/listarEmpresa.html', data)


def proceso(request):

    data = {
        'unidades':listar_unidades(),
        'empresas':listar_empresas(),
        'cargos':listar_cargos()
    }
    
    if request.method == 'POST':

        nombre = request.POST.get('nombre_proceso')
        descripcion =  request.POST.get('descripcion')
        unidad = request.POST.get('unidad')
        request.session['UnidadWF'] = unidad

          
        salida = agregar_procesotipo(nombre, descripcion, unidad)
        if salida == 1:
            messages.success(request, 'Proceso Creado correctamente')
            
            try:
                proceso = obtener_procesotipo(unidad)
                request.session['Proceso'] = proceso
                
            except ObjectDoesNotExist as e:
                proceso = None
                request.session['Proceso'] = None
            
            return redirect(tarea)    
                          
        else:
            messages.success(request, 'Proceso no creado')

    return render(request, 'Procesos/CrearProceso.html', data)

def cargo(request):

    data = {

        'unidades': listar_unidades(),
        'empresas': listar_empresas()

    }

    if request.method == 'POST':

        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        unidad = request.POST.get('unidad')
        estado = '1'

        salida = agregar_cargo(nombre, descripcion, estado, unidad)

        print(salida)
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
            messages.success(request, 'Servicio editado correctamente')

        else:
            data['mensaje'] = 'No se pudo agregar'
            messages.success(request, 'Servicio NO editado correctamente')

    return render(request, 'Cargos/crearCargo.html', data)


def cargos(request):

    data = {

        'cargos': listar_cargos()

    }

    return render(request, 'Cargos/listarCargo.html', data)


def tarea(request):
    print('ENTRE ACA')
    unidad_id = request.session['UnidadWF']
    procesotipo_session = request.session['Proceso']

    try:
        proceso = ProcesoTipo.objects.get(idprocesotipo = procesotipo_session)
        request.session['NombreProceso'] = proceso.nombre
                
    except ObjectDoesNotExist as e:
        proceso = None
        request.session['NombreProceso'] = None

    print(proceso)
    data = {
        #'unidades':listar_unidades(),
        #'empresas':listar_empresas(),
        'cargos':listar_unidades_cargos(unidad_id),
        #'procesos':listar_procesostipo()
    }
    
    if request.method == 'POST':
      
        nombre = request.POST.get('tarea')
        descripcion =  request.POST.get('descripcionTarea')
        dias = request.POST.get('tiempo')
        orden = request.POST.get('orden')
        cargo = request.POST.get('cargo')
        #procesotipo = request.POST.get('proceso')
        procesotipo = proceso.idprocesotipo
        
        salida = agregar_tareatipo(nombre, descripcion, dias, orden, cargo, procesotipo)
        if salida == 1:
            messages.success(request, 'Tarea Creada Correctamente')
                               
        else:
            messages.success(request, 'Tarea No Creada')

    return render(request, 'Tareas/CrearTareas.html', data)

def unidad(request):

    data = {
        
        'empresas':listar_empresas()
        
    }
    
    if request.method == 'POST':
      
        nombre = request.POST.get('nombre')
        descripcion =  request.POST.get('descripcion')
        empresa = request.POST.get('empresa')
        estado = '1'

        salida = agregar_unidad(nombre, descripcion, estado, empresa)

        print(salida)
        if salida == 1:
            data['mensaje'] = 'Agregado correctamente'
            messages.success(request, 'Servicio editado correctamente')
                               
        else:
            data['mensaje'] = 'No se pudo agregar'
            messages.success(request, 'Servicio NO editado correctamente')

    return render(request, 'Unidades/crearUnidad.html', data)
    

def unidades(request):

    data = {
        
        'unidades':listar_unidades_empresa()
        
    }
    

    return render(request, 'Unidades/listarUnidades.html', data)    



def empresa(request):
    data = {
        'regiones':listar_regiones(),
        'comunas':listar_comunas()
       
    }
    

    if request.method == 'POST':
        rut = request.POST.get('rut')
        nombre =  request.POST.get('nombre')
        rubro =  request.POST.get('rubro')
        comuna = request.POST.get('comuna')
        direccion = request.POST.get('direccion')
        correo = request.POST.get('correo')
        estado = '1'
        telefono = request.POST.get('telefono')

       
        salida = agregar_empresa(rut, nombre, rubro, comuna, direccion, telefono, correo, estado)
        
        if salida == 1:
            messages.success(request, 'Empresa creada correctamente')
                                 
        else:
            messages.success(request, 'Empresa no creada ')
      
    return render(request, 'Empresa/crearEmpresa.html', data)



def editarTarea(request, idtareatipo):
    
    if request.method == 'GET':
        
        tarea = TareaTipo.objects.get(idtareatipo = idtareatipo)
        procesotipo = ProcesoTipo.objects.get(idprocesotipo = tarea.idprocesotipo.idprocesotipo)
        request.session['NombreProceso'] = procesotipo.nombre
        request.session['NombreTarea'] = tarea.nombre
        request.session['DescripcionTarea'] = tarea.descripcion
        request.session['DuracionTarea'] = tarea.duraciondias
        request.session['OrdenTarea'] = tarea.orden_tarea

        cargos= listar_unidades_cargos(procesotipo.unidad_idunidad.idunidad)

    else:
        nombre = request.POST.get('tarea')
        descripcion =  request.POST.get('descripcionTarea')
        dias = request.POST.get('tiempo')
        orden = request.POST.get('orden')
        cargo = request.POST.get('cargo')
        #procesotipo = request.POST.get('proceso')
        
        tarea = TareaTipo.objects.get(idtareatipo = idtareatipo)
        procesotipo = ProcesoTipo.objects.get(idprocesotipo = tarea.idprocesotipo.idprocesotipo)
        idprocesotipo = procesotipo.idprocesotipo
    

        
        salida = editar_tareatipo(str(idtareatipo), nombre, descripcion, dias, orden, cargo)
        
        if salida == 1:
            messages.success(request, 'Tarea Modificada Correctamente')
                                 
        else:
            messages.success(request, 'Tarea no Modificada ')
            
        return redirect('editar_proceso', idprocesotipo = idprocesotipo )
        

    return render(request,'Tareas/editarTarea.html',{'tarea':tarea, 'procesotipo':procesotipo , 'cargos': cargos}  )        


def editar_tareatipo(idtareatipo, nombre, descripcion, duracion, orden, cargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_editar_tareatipo', [idtareatipo,
                    nombre, descripcion, duracion, orden, cargo, salida])
    
    return salida.getvalue()
	

def usuarios(request):
    data = {
       'usuarios':listar_usuarios()
    }
    

    return render(request, 'Usuarios/ListarUsuarios.html', data)

def listar_usuarios():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()


    cursor.callproc('sp_listar_usuarios', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista    

def listar_empresas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()


    cursor.callproc('sp_listar_empresas', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista 

def editarEmpresa(request, idempresa):
    
    

    if request.method == 'GET':
        regiones = listar_regiones()  
        empresa = Empresa.objects.get(idempresa = idempresa)

        comuna = Comuna.objects.get(nombre_comuna = empresa.comuna_idcomuna)
        region = Region.objects.get(nombre = comuna.id_region)
    else:
        rut = request.POST.get('rut')
        nombre =  request.POST.get('nombre')
        rubro =  request.POST.get('rubro')
        comuna = request.POST.get('comuna')
        direccion = request.POST.get('direccion')
        correo = request.POST.get('correo')
        telefono = request.POST.get('telefono')

        salida = editar_empresa(idempresa, rut, nombre, rubro, comuna, direccion, telefono, correo)
        
        if salida == 1:
            messages.success(request, 'Empresa Modificada Correctamente')
                                 
        else:
            messages.success(request, 'Empresa no Modificada ')
            
        return redirect('lista_empresa')
        
    return render(request,'Empresa/crearEmpresa.html', {'empresa':empresa,'comuna':comuna, 'regiones':regiones,  'region':region } )      

def deshabilitarEmpresa(request, idempresa):
 
    empresa = Empresa.objects.get(idempresa = idempresa)
 
    if request.method =='POST':

        salida = deshabilitar_empresa(idempresa)
        
        if salida == 1:
            messages.success(request, 'Empresa deshabilitada correctamente')
                                 
        else:
            messages.success(request, 'Empresa no deshabilitada ')

        return redirect('lista_empresa')
    return render (request, 'Empresa/eliminarEmpresa.html', {'empresa':empresa})    

def listar_unidades():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_unidades_sinfiltro', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista  

def listar_unidades_empresa():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_unidades_empresa', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista      

def listar_procesostipo():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_procesostipo', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista       

def listar_cargos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cargos', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista      

def listar_regiones():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_regiones', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista   

def listar_comuna_region(regionid):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_comunas_region', [out_cursor, regionid])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista      

def regiones_comunas(request):
    regionid = request.GET.get('region_id')
 
    data = {
           'region_comuna':listar_comuna_region(regionid)
        }   
     
    return render(request, 'Empresa/regiones_comuna.html',data)    

def listar_comunas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_comunas', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista         



def agregar_empresa(rut, nombre, rubro, comuna, direccion, telefono, correo, estado):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_agregar_empresa',[rut, nombre, rubro, comuna, direccion, telefono, correo, estado, salida])
    
    return salida.getvalue()

def editar_empresa(idempresa, rut, nombre, rubro, comuna, direccion, telefono, correo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_editar_empresa',[idempresa, rut, nombre, rubro, comuna, direccion, telefono, correo, salida])
    
    return salida.getvalue()

def deshabilitar_empresa(id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_deshabilitar_empresa',[id, salida])
    
    return salida.getvalue()



def agregar_procesotipo(nombre, descripcion, unidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_agregar_procesotipo',[nombre, descripcion, unidad, salida])
    return salida.getvalue()

def obtener_procesotipo(unidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_obtener_proceso',[unidad, salida])
    return salida.getvalue()    

def agregar_unidad(nombre, descripcion, estado, empresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_agregar_unidad',[nombre, descripcion, estado, empresa, salida])

    return salida.getvalue()


def agregar_tareatipo(nombre, descripcion, dias, orden, cargo, procesotipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_agregar_tareatipo',[nombre, descripcion, dias, orden, cargo, procesotipo, salida])
    return salida.getvalue()   

def unidades_cargos(request):
    
    unidad_id =request.GET.get('unidad')
    data = {
           'cargos':listar_unidades_cargos(unidad_id)
        }  
        
    return render(request, 'Ejecucion/unidades_cargos.html',data)    


def listar_unidades_cargos(unidad_id):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()


    cursor.callproc('SP_LISTAR_UNIDADES_CARGOS',[out_cursor, unidad_id])
   
    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista    

def agregar_cargo(nombre, descripcion, estado, unidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_AGREGAR_CARGO', [
                    nombre, descripcion, estado, unidad, salida])

    return salida.getvalue()     




