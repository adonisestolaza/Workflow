from django.shortcuts import render, redirect
from django.db import connection
from datetime import date
from datetime import datetime
from .models import *
from core.ejecucion.models import *
from core.mainwork.views import *
from core.login.models import Usuario
from core.mainwork.models import *
from django.contrib import messages
import cx_Oracle

# Create your views here.


def procesos(request):
    data = {
        'empresas': listar_empresas(),
    }
    if request.method == 'POST':
        id_proceso = request.POST.get('id_proceso')
        fecha_ejecucion = request.POST.get('fecha_ejecucion')
        idresponsable = request.user.id
        estadoproceso = '1'
        salida = ejecutarproceso(
            id_proceso, fecha_ejecucion, idresponsable, estadoproceso)
        if salida == 1:
            messages.success(request, 'Proceso Ejecutado')
            try:
                proceso = obtener_procesoejecutado(id_proceso)
                request.session['ProcesoEjecutado'] = proceso

            except ObjectDoesNotExist as e:
                proceso = None
                request.session['ProcesoEjecutado'] = None

            return redirect(asignar_proceso_ejecutado)
        else:
            messages.success(request, 'Proceso no Ejecutado')
    return render(request, 'Ejecucion/ejecutar_proceso_tarea_tipo_jefe.html', data)


def asignar_responsable(request, idtarea):
    tarea = Tareaejecutada.objects.get(idtareaejecutada=idtarea)
    idproceso = tarea.idprocesoejecutado.idprocesoejecutado

    request.session['TareaNombre'] = tarea.nombre
    request.session['TareaProceso'] = idproceso

    data = {
        'empresas': listar_empresas(),
    }

    if request.method == 'POST':

        idresponsable = request.POST.get("responsableid")
        estado = '1'
        salida = actualizar_responsable(idtarea, idresponsable)
        salida2 = insertar_notificacion(idtarea, tarea.nombre, estado)

        if salida == 1:
            data['mensaje'] = 'Asignado correctamente'
        else:
            data['mensaje'] = 'No se pudo asignar responsable'
        return redirect('proceso_asignar')

    return render(request, 'Ejecucion/asignar_responsable.html', data)


def asignar_responsable_proceso_ejecutado(request, idtarea):
    tarea = Tareaejecutada.objects.get(idtareaejecutada=idtarea)
    idproceso = tarea.idprocesoejecutado.idprocesoejecutado

    request.session['TareaNombre'] = tarea.nombre
    request.session['TareaProceso'] = idproceso

    data = {
        'empresas': listar_empresas(),
    }

    if request.method == 'POST':

        idresponsable = request.POST.get("responsableid")
        estado = '1'
        salida = actualizar_responsable(idtarea, idresponsable)
        salida2 = insertar_notificacion(idtarea, tarea.nombre, estado)
        if salida == 1:
            data['mensaje'] = 'Asignado correctamente'
        else:
            data['mensaje'] = 'No se pudo asignar responsable'
        return redirect('asignar_proceso_ejecutado')

    return render(request, 'Ejecucion/responsable_usuario_proceso_ejecutado.html', data)


def terminar_tareas(request, idtarea):
    tarea = Tareaejecutada.objects.get(idtareaejecutada=idtarea)
    idproceso = tarea.idprocesoejecutado.idprocesoejecutado

    request.session['TareaNombre'] = tarea.nombre
    request.session['TareaDescripcion'] = tarea.descripcion
    request.session['TareaAvance'] = tarea.avance
    request.session['TareaDuracion'] = tarea.duracion_dias
    request.session['TareaOrden'] = tarea.orden_tarea

    data = {
        'empresas': listar_empresas()
    }

    if request.method == 'POST':

        # llamada procedimientos
        salida = terminar_tarea(idtarea)

        salida1 = activar_tarea(idproceso, idtarea)
        salida3 = recalcular_tarea(idproceso)
        salida2 = recalcular_proceso(idproceso)

        if salida == 1:
            messages.success(request, 'Tarea Terminada')

        else:
            messages.success(request, 'Tarea no terminada')
        return redirect('tareas')

    return render(request, 'Ejecucion/detalletarea.html', data)


def detalle_tarea(request, idtarea):
    tarea = Tareaejecutada.objects.get(idtareaejecutada=idtarea)
    idproceso = tarea.idprocesoejecutado.idprocesoejecutado

    request.session['TareaNombre'] = tarea.nombre
    request.session['TareaDescripcion'] = tarea.descripcion
    request.session['TareaAvance'] = tarea.avance
    request.session['TareaDuracion'] = tarea.duracion_dias
    request.session['TareaOrden'] = tarea.orden_tarea

    fecha = datetime.now()
    usuario = request.user.id
    nombre = request.user.nombres
    apellido = request.user.apellidos

    data = {
        'mensajes': listar_mensajes_tarea(idtarea),
        'tarea': tarea_por_id(idtarea)
    }
    if request.POST.get('action') == 'mensaje':
        # llamada procedimientos
        asunto = request.POST.get("asunto")
        mensaje = request.POST.get("idmensaje")
        estado = "1"

        salida = insertar_mensaje(
            asunto, mensaje, idtarea, estado, fecha, usuario, nombre, apellido)

        if salida == 1:
            messages.success(request, 'Mensaje agregado correctamente')
        else:
            messages.success(request, 'Mensaje no insertado')
        return redirect('detalle_tarea', idtarea)

    elif request.POST.get('action') == 'tareaterminada':
        print("entro al post de la tarea terminada")
        # llamada procedimientos
        salida = terminar_tarea(idtarea)

        activar_tarea(idproceso, idtarea)
        recalcular_tarea(idproceso)
        recalcular_proceso(idproceso)
        cant_tareas = cant_tareas_proceso(idproceso)
        if cant_tareas == 0:
            terminar_proceso(idproceso, fecha)

        if salida == 1:
            messages.success(request, 'La Tarea Ha sido Terminada')
        else:
            messages.success(request, 'La Tarea NO se ha terminado')

        return redirect('tareas')

    return render(request, 'Ejecucion/detalletarea.html', data)


def agregar_mensaje(request, idtarea):
    tarea = Tareaejecutada.objects.get(idtareaejecutada=idtarea)
    request.session['TareaNombre'] = tarea.nombre
    fecha = datetime.now()
    usuario = request.user.id
    nombre = request.user.nombres
    apellido = request.user.apellidos

    print(nombre)
    print(request.user.apellidos)
    if request.method == 'POST':
        # llamada procedimientos
        asunto = request.POST.get("asunto")
        mensaje = request.POST.get("mensaje")
        estado = "1"

        salida = insertar_mensaje(
            asunto, mensaje, idtarea, estado, fecha, usuario, nombre, apellido)

        if salida == 1:
            messages.success(request, 'Mensaje insertado')
        else:
            messages.success(request, 'Mensaje no insertado')

    return render(request, 'Ejecucion/insertarmensaje.html')


def mensajes_tareas(request, idtarea):

    data = {
        'mensaje': sp_mensaje_tareas(idtarea)
    }

    return render(request, 'Ejecucion/mensajes_tareas.html', data)


def tareas_ejecutadas_jefe(request, idproceso):

    if request.method == 'GET':
        data = {
            'tareas_ejecutadas_jefe': sp_tareas_ejecutadas(idproceso)
        }

    return render(request, 'Ejecucion/tareas_ejecutadas.html', data)


def notificacion_leida(request, idnotificacion):

    # llamada procedimientos
    salida = actualizar_notificacion(idnotificacion)

    if salida == 1:
        messages.success(request, 'Notificacion leida')

    else:
        messages.success(request, 'Notificacion no leida')

    return redirect('tareas')
    return render(request, 'menuPrincipal.html')


def mensaje_leido(request, idmensaje):

    # llamada procedimientos
    salida = actualizar_mensaje(idmensaje)

    if salida == 1:
        messages.success(request, 'Mensaje leido')

    else:
        messages.success(request, 'Mensaje no leido')
    return redirect('tareas')

    return render(request, 'menuPrincipal.html')


def editar_proceso(request, idprocesotipo):

    data = {
        'procesos_tarea': listar_procesos_tareas_tipo(idprocesotipo),
    }
    return render(request, 'Ejecucion/editar_proceso_tarea_tipo.html', data)


# Metodos que llaman Procedures y envian a template

def listar_procesos_tarea_tipo(request):
    data = {
        'empresas': listar_empresas(),
    }
    return render(request, 'Ejecucion/listar_procesos_tarea_tipo.html', data)


def tareas(request):

    return render(request, 'Ejecucion/terminar_tarea.html')


def historial_tareas_usuario(request):

    return render(request, 'Ejecucion/historial_usuario.html')


def asignar_proceso(request):

    return render(request, 'Ejecucion/proceso_ejecutado.html')


def asignar_proceso_ejecutado(request):
    idproceso = request.session['ProcesoEjecutado']

    proceso = Procesoejecutado.objects.get(idprocesoejecutado=idproceso)

    return render(request, 'Ejecucion/asignar_responsable_ejecutado.html', {'proceso': proceso})


def tareas_usuario(request):
    idusuario = request.GET.get('id_usuario')
    data = {
        'tareas_usuario': listar_tareas_usuario(idusuario)
    }
    return render(request, 'Ejecucion/tarea_usuario.html', data)


def listar_historial_usuario_tareas(request):
    idusuario = request.GET.get('id_usuario')
    data = {
        'historial_usuario': listar_historial_usuario(idusuario)
    }
    return render(request, 'Ejecucion/listar_historial_usuario.html', data)


def listar_notificacion_usuario(request):
    idusuario = request.user.id

    data = {
        'notificacion_user': notificacion_usuario(idusuario)
    }
    return render(request, 'Ejecucion/listar_notificacion_usuario.html', data)


def listar_mensaje_notificacion(request):

    idusuario = request.user.id
    data = {
        'mensaje_notificacion': sp_listar_mensajes_notificacion(idusuario)
    }
    return render(request, 'Ejecucion/listar_notificacion_mensaje.html', data)


def empresa_unidades_proceso(request):
    empresa_id = request.GET.get('empresa_id')
    data = {
        'unidades': listar_unidades(empresa_id)
    }
    return render(request, 'Ejecucion/unidades_empresas.html', data)


def unidades_proceso(request):
    unidad_id = request.GET.get('unidadId')
    data = {
        'procesos_tipo': listar_procesos_tipo(unidad_id)
    }
    return render(request, 'Ejecucion/unidades_procesos.html', data)


def tareas_ejecutadas_asignacion(request):
    proceso_e = request.GET.get('id_proceso')
    data = {
        'lista_tareas': listar_tareas_ejecutadas(proceso_e)
    }
    return render(request, 'Ejecucion/listar_tareas_ejecutadas.html', data)


def tareas_ejecutadas_asignacion_proceso_ejecutado(request):
    proceso_e = request.GET.get('id_proceso')
    data = {
        'lista_tareas': listar_tareas_ejecutadas(proceso_e)
    }
    return render(request, 'Ejecucion/listar_tareas_proceso_ejecutado.html', data)


def responsables_tareas(request):
    unidad_id = request.GET.get('unidad_id')
    data = {
        'listar_responsable': listar_responsable_tareas(unidad_id)
    }
    return render(request, 'Ejecucion/responsable_tarea.html', data)


def procesos_tarea(request):
    proceso_id = request.GET.get('procesoid')

    data = {
        'procesos_tarea': listar_procesos_tareas_tipo(proceso_id),
        'usuarios': listar_usuarios_de_empresa(proceso_id)
    }
    return render(request, 'Ejecucion/procesos_tareas.html', data)


def usuarios_responsables(request):
    proceso_id = request.GET.get('procesoid')
    data = {
        'usuarios': listar_usuarios_de_empresa(proceso_id),
    }
    return render(request, 'Ejecucion/usuarios_responsables.html', data)


def tareas_ejecutadas(request):
    proceso_id = request.GET.get('procesoid')
    data = {
        'usuarios': listar_tareas_ejecutadas(proceso_id),
    }
    return render(request, 'Ejecucion/tareas_ejecutadas.html', data)


def procesos_ejecutados(request):
    unidad_id = request.GET.get('unidadid')
    data = {
        'procesos_ejecutados': listar_procesos_ejecutados(unidad_id)
    }
    return render(request, 'Ejecucion/procesos_ejecutados.html', data)


def procesos_tarea_ejecutadas(request):
    proceso_e = request.GET.get('procesos_e')
    data = {
        'procesos_tarea_ejecutada': listar_procesos_tareas_ejecutadas(proceso_e)
    }
    return render(request, 'Ejecucion/procesos_tareas_ejecutadas.html', data)


# metodos procedimientos almacenados


def recalcular_proceso(id_proceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_RECALCULAR_PROCESO', [id_proceso, salida])
    return salida.getvalue()


def insertar_notificacion(id_tarea, nombre, estado):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_INSERTAR_NOTIFICACION', [
                    id_tarea, nombre, estado, salida])
    return salida.getvalue()


def recalcular_tarea(id_proceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_RECALCULAR_TAREA', [id_proceso, salida])
    return salida.getvalue()


def terminar_tarea(idtarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_TERMINAR_TAREA', [idtarea, salida])
    return salida.getvalue()


def activar_tarea(idproceso, idtarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTIVARTAREA', [idproceso, idtarea, salida])
    return salida.getvalue()


def actualizar_responsable(idtarea, idresponsable):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTUALIZAR_RESPONSABLE', [
                    idtarea, idresponsable, salida])
    return salida.getvalue()


def actualizar_notificacion(idnotificacion):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTUALIZAR_NOTIFICACION', [idnotificacion, salida])
    return salida.getvalue()


def actualizar_mensaje(idmensaje):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTUALIZAR_MENSAJE', [idmensaje, salida])
    return salida.getvalue()


def terminar_proceso(idproceso, fecha_termino):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTUALIZAR_PROCESO', [
                    idproceso, fecha_termino, salida])
    return salida.getvalue()

# funcion que ejecuta el proceso


def ejecutarproceso(id_proceso, fecha_ejecucion, idresponsable, idestadoproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_ACTIVAR_PROCESO', [
                    id_proceso, fecha_ejecucion, idresponsable, idestadoproceso, salida])
    return salida.getvalue()


def obtener_procesoejecutado(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_obtener_proceso_ejecutado', [idproceso, salida])
    return salida.getvalue()


def cant_tareas_proceso(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('sp_cant_tareas_por_proceso', [idproceso, salida])
    return salida.getvalue()


def insertar_mensaje(asunto, mensaje, idtarea, estado, fecha, idusuario, nombre, apellido):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_INSERTAR_MENSAJE', [
                    asunto, mensaje, idtarea, estado, fecha, idusuario, nombre, apellido, salida])
    return salida.getvalue()


def listar_unidades(idempresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_UNIDADES', [out_cursor, idempresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_procesos_tipo(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_PROCESOS_UNIDADES', [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_procesos_tareas_tipo(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()
    cursor.callproc('SP_LISTAR_PROCESOS_TAREAS_TIPO', [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_usuarios_de_empresa(idProcedimientoTipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_USUARIOS_DE_EMPRESA', [
                    idProcedimientoTipo, out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def listar_procesos():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_PROCESOS_EJECUTADOS', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_responsable_tareas(idunidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_CARGOS_RESPONSABLES', [out_cursor, idunidad])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_empresas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_EMPRESAS', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def listar_procesos_tareas_ejecutadas(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_PROCESOS_TAREAS_EJECUTADAS',
                    [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_procesos_ejecutados(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_UNIDAD_PROCESOS_EJECUTADOS',
                    [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_tareas_usuario(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_TAREAS_USUARIO', [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def listar_historial_usuario(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_HISTORIAL_TAREAS_USUARIO', [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def notificacion_usuario(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_notificacion_usuario', [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def sp_mensaje_tareas(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_MENSAJES', [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def sp_tareas_ejecutadas(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_TAREAS_EJECUTADAS_JEFE',
                    [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def sp_listar_mensajes_notificacion(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_MENSAJES_NOTIFICACION',
                    [out_cursor, idusuario])
    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def listar_tareas_ejecutadas(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_TAREAS_EJECUTADAS', [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def listar_usuarios_segun_cargo(idcargo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('listar_usuarios_segun_cargo', [out_cursor, idcargo])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def listar_mensajes_tarea(idtarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_listar_mensajes_tarea', [out_cursor, idtarea])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista

# Muestra el detalle de una tarea por id


def tarea_por_id(idtarea):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_tarea_por_id', [out_cursor, idtarea])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista
