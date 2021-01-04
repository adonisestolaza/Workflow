from django.urls import path
from .views import *
from core.login.views import *



urlpatterns = [
    path('', index, name="index"),
    path('logged_in/', logged_in),
    path('menuPrincipal/', menuPrincipal, name="menuPrincipal"),
    path("logout/", logout_request, name="logout"),
    path('usuarios/', usuarios, name="lista_usuarios"),
    path('empresa/', empresa, name="empresa"),
    path('cargos/', cargo, name="cargos"),
    path('cargo/', cargos, name="lista_cargo"),
    path('unidad/', unidad, name="unidad"),
    path('proceso/', proceso, name="proceso"),
    path('tareas/', tarea, name="tarea"),
    path('comuna_region/', regiones_comunas , name="comuna_region"),
    path('listaempresa/', empresas, name="lista_empresa"),
    path('cargosfunc/', unidades_cargos , name="unidades_cargos"),
    path('eliminar_empresa/<int:idempresa>',deshabilitarEmpresa, name = 'eliminar_empresa'),
    path('editar_empresa/<int:idempresa>', editarEmpresa, name = 'editar_empresa'),
    path('listaunidades/', unidades, name="lista_unidad"),
    path('editar_tarea/<int:idtareatipo>', editarTarea, name = 'editar_tarea'),
    
]
