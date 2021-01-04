from django.urls import path
from .views import *


urlpatterns = [
    path('control/',procesos, name="lista_procesos"),
    path('controlger/',procesos_Gerente, name="lista_procesos_gerente"),
    path('controljef/',procesos_Jefe, name="lista_procesos_jefe"),
    path('controlpro/',procesos_Process, name="lista_procesos_process"),
    path('controlcompa/<int:idprocesotipo>',procesos_comparativos, name="lista_procesos_comparativos"),
    path('controlfun/',procesos_Funcionario, name="lista_procesos_funcionario"),
    path('reporte_funcionario/',GeneratePDF_funcionario.as_view(), name="reporte_funcionario"),
    path('reporte_process/<int:idprocesotipo>',GeneratePDF_proceso.as_view(), name="reporte_process")


]

  
    
 