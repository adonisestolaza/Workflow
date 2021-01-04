from django.contrib import admin
from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path('procesos/', procesos, name="procesos"),
    path('unidades/', empresa_unidades_proceso , name="unidades_empresa"),
    path('procesos_tipo/', unidades_proceso , name="unidades_proceso"),
    path('procesos_tarea/',procesos_tarea , name="procesos_tareas"),
    path('ejecutarproceso/', procesos, name="ejecutar_proceso"),
    path('tareas_usuario/',tareas_usuario, name="tareas_usuario"),
    path('listar_historial_usuario/',listar_historial_usuario_tareas, name="listar_historial_usuario"),
    path('historial_usuario/',historial_tareas_usuario, name="historial_tareas_usuario"),
    path('tareas/',tareas, name="tareas"),
    path('proceso_asignar/',asignar_proceso, name="proceso_asignar"),
    path('asignar_proceso_ejecutado/',asignar_proceso_ejecutado, name="asignar_proceso_ejecutado"),
    path('listar_tareas/',tareas_ejecutadas_asignacion, name="listar_tareas"),
    path('listar_tareas_proceso_ejecutado/',tareas_ejecutadas_asignacion_proceso_ejecutado, name="listar_tareas_ejecutadas"),
    path('responsable/',responsables_tareas, name="responsable"),
    path('notificacion/',listar_notificacion_usuario, name="notificacion"),
    path('mensaje/',listar_mensaje_notificacion, name="mensaje"),
    path('detalle_tarea/<int:idtarea>', detalle_tarea, name="detalle_tarea"),
    path('tareas_ejecutadas_jefe/<int:idproceso>',tareas_ejecutadas_jefe , name="tareas_ejecutadas_jefe"),
    path('agregar_mensaje/<int:idtarea>',agregar_mensaje , name="agregar_mensaje"),
    path('mensajes_tareas/<int:idtarea>',mensajes_tareas , name="mensajes_tareas"),
    path('notificacion_leida/<int:idnotificacion>',notificacion_leida , name="notificacion_leida"),
    path('mensaje_leido/<int:idmensaje>',mensaje_leido , name="mensaje_leido"),
    path('asignar_responsable/<int:idtarea>',asignar_responsable , name="asignar_responsable"),
    path('asignar_responsable_ejecutado/<int:idtarea>',asignar_responsable_proceso_ejecutado , name="asignar_responsable_ejecutado"),
    path('procesos_ejecutados/',procesos_ejecutados , name="procesos_ejecutados"),
    path('procesos_tarea/',procesos_tarea , name="procesos_tareas"),
    path('procesos_tarea_ejecutada/',procesos_tarea_ejecutadas , name="procesos_tarea_ejecutada"),
    path('usuarios_responsables/', usuarios_responsables , name="usuarios_responsables"),
    path('listar_procesos_tarea_tipo/',listar_procesos_tarea_tipo , name="listar_procesos_tarea_tipo"),
    path('editar_proceso/<int:idprocesotipo>',editar_proceso , name="editar_proceso"),
]