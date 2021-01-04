from django.shortcuts import render
from django.db import connection
import cx_Oracle
from django.core.exceptions import ObjectDoesNotExist
from core.mainwork.models import *
from core.ejecucion.views import *
from core.ejecucion.models import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template
from django.views.generic import View
from django.conf import settings
from datetime import date
from datetime import datetime

from .utils import render_to_pdf  # created in step 4


# Create your views here.
def procesos(request):
    perfil = request.user.rol_id
    empresa = request.session['EmpresaUsuario']
    unidad = request.session['UnidadUsuario']
    cargo = request.session['CargoUsuario']

    data = {
        'procesos': listar_procesos_ejecutados(),
        'tareatipo': listar_tareas_tipo(),
        'cantareas': cantidad_de_tareas(),
        'terminadas': tareas_terminadas(),
        'en_curso': tareas_en_curso(),
        'detenidas': tareas_detenidas(),

    }

    return render(request, 'DashboardCliente/dashboard.html', data)


def procesos_Gerente(request):

    unidades = Unidad.objects.all().filter(
        empresa_idempresa=request.user.empresa_id)

    data = {
        'procesos': listar_procesos_unidad(request.user.unidad_id),
        'tareas': listar_tareas_unidad(request.user.unidad_id),
        'cantidad_tareas': listar_cantidad_tareas_empresa(request.user.empresa_id),
        'cantidad_tareasEstado': listar_cantidad_tareas_empresa_segunEstado(request.user.empresa_id),
        'cantareas': cantidad_de_tareas(),
        'terminadas': tareas_terminadas(),
        'en_curso': tareas_en_curso(),
        'detenidas': tareas_detenidas(),
        'procesos_ejecutados': sp_procesos_ejecutados_empresa(request.user.empresa_id),
        'procesos_ejecutados_sinasignar': sp_procesos_ejecutados_sinasignar_empresa(request.user.empresa_id),
        'mensajes': sp_listar_mensajes_usuario(request.user.id),
        'mensajes_notificacion': sp_listar_mensajes_notificacion(request.user.id),
        'funcionario_responsables': sp_lista_tareas_activas_empresa(request.user.empresa_id),
        'funcionario_responsables_atrasadas': sp_lista_tareas_atrasadas_empresa(request.user.empresa_id),
        'unidades': unidades,

    }

    return render(request, 'DashboardCliente/dashboard_gerente.html', data)


def procesos_Jefe(request):
    data = {
        'procesos': listar_procesos_unidad(request.user.unidad_id),
        'tareas': listar_tareas_unidad(request.user.unidad_id),
        'cantidad_tareas': listar_cantidad_tareas_unidad(request.user.unidad_id),
        'cantidad_tareasEstado': listar_cantidad_tareas_unidad_segunEstado(request.user.unidad_id),
        'cantareas': cantidad_de_tareas(),
        'terminadas': tareas_terminadas(),
        'en_curso': tareas_en_curso(),
        'detenidas': tareas_detenidas(),
        'procesos_ejecutados': sp_procesos_ejecutados(request.user.id),
        'tareas_sin_asignar': sp_tareas_sin_asignar_proceso(request.user.id),
        'mensajes': sp_listar_mensajes_usuario(request.user.id),
        'mensajes_notificacion': sp_listar_mensajes_notificacion(request.user.id),
        'funcionario_responsables': sp_lista_funcionarios_tareas_activas_unidad(request.user.unidad_id),
        'funcionarios_top_tareas': sp_lista_top_tareas_funcionario(request.user.unidad_id)
    }

    return render(request, 'DashboardCliente/dashboard_jefe.html', data)


def procesos_Process(request):
    data = {
        'empresas': listar_cantidad_empresa(),
        'cantidad_unidades': listar_cantidad_unidades(),
        'unidades': unidades(),
        'lista_empresas': listar_empresas(),
        'lista_empresas_atencion': sp_lista_empresas_atrasadas_process(),
        'lista_empresas_optimizables': sp_lista_empresas_optimizables_process(),
        'procesos_ejecutados': sp_procesos_ejecutados_process(),
        'funcionario_responsables': sp_lista_tareas_atrasadas_process(),
        'optimizables_barra': sp_optimizables_barra_process(),
        'empresas_pendientes': listar_cantidad_empresas_pendientes(),
        'empresas_pendientes_s': listar_empresas_pendientes(),
        'procesos_ejecutados_sinasignar': sp_procesos_ejecutados_sinasignar_empresa(2),
        'unidades': unidades,
        'procesos_atrasados': sp_lista_procesos_atrasados_process(),
        'procesos_optimizables': sp_lista_procesos_optimizables_process(),
        'cantidad_procesos_atrasados': sp_cantidad_procesos_atrasados_process(),
        'cantidad_procesos_optmizables': sp_cantidad_procesos_optimizables_process(),

    }
    return render(request, 'DashboardCliente/dashboard_process.html', data)


def procesos_comparativos(request, idprocesotipo):
    data = {
        'empresas': listar_cantidad_empresa(),
        'diferencia_proceso': sp_diferencia_procesos(idprocesotipo),
        'porcentaje_efectividad': sp_obtener_porcentaje(idprocesotipo),
        'porcentaje_ahorrado': sp_obtener_porcentaje_tiempo_ahorrado(idprocesotipo),
        'probabilidad_ejecucion': sp_probabilidad_ejecucion(idprocesotipo),
        'cant_procesos': sp_cant_procesos(idprocesotipo),
        'procesos_ejecutados': sp_procesos_ejecutados_tipo(idprocesotipo),
        'procesos_tareas': sp_procesos_tipo_tareas_tipo(idprocesotipo),
        'promedio_tareas': sp_promedio_tareas(idprocesotipo)
    }
    return render(request, 'DashboardCliente/dashboard_procesos_comparativos.html', data)


def procesos_Funcionario(request):
    data = {
        'mensajes_notificacion': sp_listar_mensajes_notificacion(request.user.id),
        'mensajes': sp_listar_mensajes_usuario(request.user.id),
        'tareas_encurso': sp_cant_tarea_funcionario(request.user.id),
        'total_tareas': sp_total_tareas_funcionario(request.user.id),
        'tareas_amarillo': sp_tareas_semaforo_amarillo(request.user.id),
        'top_tareas': sp_top_5_tareas_funcionario(request.user.id),
        'cant_semaforo': sp_cant_tareas_por_semaforo(request.user.id),
        'tareas_pendientes': sp_tareas_pendientes_funcionario(request.user.id)
    }
    return render(request, 'DashboardCliente/dashboard_funcionario.html', data)


def listar_procesos_ejecutados():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_PROCESO_EJECUTADO', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_procesos_empresa(idempresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_procesos_empresa', [out_cursor, idempresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_procesos_unidad(idunidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_procesos_unidad', [out_cursor, idunidad])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_tareas_unidad(idunidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_tareas_unidad', [out_cursor, idunidad])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_tareas_empresa(idempresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_tareas_empresa', [out_cursor, idempresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_tareas_empresa(idempresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_tareas_empresa', [out_cursor, idempresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_tareas_unidad(idunidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_tareas_unidad', [out_cursor, idunidad])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_tareas_empresa_segunEstado(idempresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_tareas_empresa_estado',
                    [out_cursor, idempresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_tareas_unidad_segunEstado(unidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_tareas_unidad_estado',
                    [out_cursor, unidad])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_tareas_tipo():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_TAREA_TIPO', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def cantidad_de_tareas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_CANTIDAD_TAREAS', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def tareas_terminadas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_CANTAREAS_TERMINO', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def tareas_en_curso():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_CANTAREAS_ENCURSO', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def tareas_detenidas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_CANTAREAS_DETENIDAS', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_procesos_ejecutados(idresponsable):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_PROCESOS_EJECUTADOS_RESPONSABLE', [
                    out_cursor, idresponsable])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def sp_tareas_sin_asignar_proceso(idresponsable):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_TAREAS_PROCESOS_SIN_ASIGNAR', [
                    out_cursor, idresponsable])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def get_grafico_cantidad(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['dashboard'] = 'dashboard'
    context['cantidad_de_tareas'] = self.cantidad_de_tareas()
    return context


def sp_listar_mensajes_usuario(idUsuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_mensajes_usuario', [out_cursor, idUsuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_listar_mensajes_notificacion(idUsuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_mensajes_notificacion', [out_cursor, idUsuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_funcionarios_tareas_activas_unidad(idUnidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_funcionarios_tareas_activas_unidad', [
                    out_cursor, idUnidad])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_top_tareas_funcionario(idUnidad):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTA_TOP_TAREAS_FUNCIONARIO', [out_cursor, idUnidad])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


# NUEVAS FUNCIONES LEO

def listar_cantidad_tareas_empresa(empresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_tareas_empresa', [out_cursor, empresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_empresa():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_empresa', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_tareas_empresa_segunEstado(empresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_tareas_empresa_estado',
                    [out_cursor, empresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_procesos_ejecutados_empresa(empresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_procesos_ejecutados_empresa',
                    [out_cursor, empresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def sp_procesos_ejecutados_sinasignar_empresa(empresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_procesos_ejecutados_sinasignar_empresa', [
                    out_cursor, empresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista


def sp_lista_tareas_activas_empresa(idempresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_tareas_activas_empresa', [out_cursor, idempresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_tareas_atrasadas_empresa(idempresa):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_tareas_atrasadas_empresa',
                    [out_cursor, idempresa])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista

# metodos Dashboard Funcionario


def sp_cant_tarea_funcionario(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_CANT_TAREAS_FUNCIONARIO',
                    [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_total_tareas_funcionario(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_TOTAL_TAREAS_FUNCIONARIO',
                    [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_tareas_semaforo_amarillo(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_TAREAS_SEMAFORO_AMARILLO',
                    [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_top_5_tareas_funcionario(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_TOP_5_TAREAS_FUNCIONARIO', [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_cant_tareas_por_semaforo(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_CANT_TAREAS_SEMAFORO_FUNCIONARIO',
                    [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_tareas_pendientes_funcionario(idusuario):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_TAREAS_PENDIENTES_FUNCIONARIO',
                    [out_cursor, idusuario])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_diferencia_procesos(idprocesotipo):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_PROCESOS_DIFERENCIA', [out_cursor, idprocesotipo])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_procesos_ejecutados_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_procesos_ejecutados_process', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)
    return lista

# 01-12


def listar_empresas():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_empresas_process', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def unidades():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_unidades_sinfiltro', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_unidades():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_unidades', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_tareas_atrasadas_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_tareas_atrasadas_process',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_cantidad_empresas_pendientes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_cant_empresas_pendientes', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def listar_empresas_pendientes():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_listar_empresas_pendientes', [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_empresas_atrasadas_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_empresas_atrasadas',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_empresas_optimizables_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_empresas_optimizables',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_procesos_atrasados_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_procesos_atrasados_process',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_lista_procesos_optimizables_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_lista_procesos_optimizables_process',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_cantidad_procesos_atrasados_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_cantidad_procesos_atrasados_process',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_cantidad_procesos_optimizables_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_cantidad_procesos_optimizables_process',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_optimizables_barra_process():
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('sp_optimizables_barra_process',
                    [out_cursor])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


# procesos comparativos
def sp_obtener_porcentaje(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_PORCENTAJE_EFECTIVIDAD', [idproceso, salida])
    return salida.getvalue()


def sp_obtener_porcentaje_tiempo_ahorrado(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_TIEMPO_AHORRADO_MES', [idproceso, salida])
    return salida.getvalue()


def sp_probabilidad_ejecucion(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    salida = cursor.var(cx_Oracle.NUMBER)
    cursor.callproc('SP_PROBABILIDAD_EJECUCION', [idproceso, salida])
    return salida.getvalue()


def sp_cant_procesos(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_CANT_PROCESOS', [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_procesos_ejecutados_tipo(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_PROCESOS_EJECUTADOS_TIPO',
                    [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_procesos_tipo_tareas_tipo(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_LISTAR_PROCESOS_TIPO_TAREAS_TIPO',
                    [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


def sp_promedio_tareas(idproceso):
    django_cursor = connection.cursor()
    cursor = django_cursor.connection.cursor()
    out_cursor = django_cursor.connection.cursor()

    cursor.callproc('SP_PROMEDIO_TAREAS', [out_cursor, idproceso])

    lista = []
    for fila in out_cursor:
        lista.append(fila)

    return lista


class GeneratePDF_funcionario(View):

    def get(self, request, *args, **kwargs):
        template = get_template('PDF/reporte_funcionario.html')
        context = {
            "invoice_id": "",
            'nombre': request.user.nombres,
            'apellido': request.user.apellidos,
            'fecha': datetime.now(),
            'mensajes_notificacion': sp_listar_mensajes_notificacion(request.user.id),
            'mensajes': sp_listar_mensajes_usuario(request.user.id),
            'tareas_encurso': sp_cant_tarea_funcionario(request.user.id),
            'total_tareas': sp_total_tareas_funcionario(request.user.id),
            'tareas_amarillo': sp_tareas_semaforo_amarillo(request.user.id),
            'top_tareas': sp_top_5_tareas_funcionario(request.user.id),
            'cant_semaforo': sp_cant_tareas_por_semaforo(request.user.id),
            'tareas_pendientes': sp_tareas_pendientes_funcionario(request.user.id)
        }
        html = template.render(context)
        pdf = render_to_pdf('PDF/reporte_funcionario.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Invoice_%s.pdf" % ("12341231")
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")


class GeneratePDF_proceso(View):

    def get(self, request, idprocesotipo, *args, **kwargs):
        template = get_template('PDF/reporte_proccess.html')
        context = {
            'nombre': request.user.nombres,
            'apellido': request.user.apellidos,
            'fecha': datetime.now(),
            'empresas': listar_cantidad_empresa(),
            'diferencia_proceso': sp_diferencia_procesos(idprocesotipo),
            'porcentaje_efectividad': sp_obtener_porcentaje(idprocesotipo),
            'porcentaje_ahorrado': sp_obtener_porcentaje_tiempo_ahorrado(idprocesotipo),
            'probabilidad_ejecucion': sp_probabilidad_ejecucion(idprocesotipo),
            'cant_procesos': sp_cant_procesos(idprocesotipo),
            'procesos_ejecutados': sp_procesos_ejecutados_tipo(idprocesotipo),
            'procesos_tareas': sp_procesos_tipo_tareas_tipo(idprocesotipo),
            'promedio_tareas': sp_promedio_tareas(idprocesotipo)
        }
        html = template.render(context)
        pdf = render_to_pdf('PDF/reporte_proccess.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Reporte_%s.pdf" % ('123')
            content = "inline; filename='%s'" % (filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
