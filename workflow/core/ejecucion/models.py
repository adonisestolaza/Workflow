# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from core.mainwork.models import Estadotarea, ProcesoTipo, Semaforo
from core.login.models import Usuario

class Procesoejecutado(models.Model):
    idprocesoejecutado = models.BigIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    fechaejecucion = models.DateField(blank=True, null=True)
    fechatermino = models.DateField(blank=True, null=True)
    idprocesotipo = models.ForeignKey(ProcesoTipo, models.DO_NOTHING, db_column='idprocesotipo')

    class Meta:
        managed = False
        db_table = 'procesoejecutado'

class Tareaejecutada(models.Model):
    idtareaejecutada = models.BigIntegerField(primary_key=True)
    idprocesoejecutado = models.ForeignKey(Procesoejecutado, models.DO_NOTHING, db_column='idprocesoejecutado')
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=250, blank=True, null=True)
    avance = models.BigIntegerField(blank=True, null=True)
    duracion_dias = models.BigIntegerField(blank=True, null=True)
    orden_tarea = models.BigIntegerField(blank=True, null=True)
    idestadotarea = models.ForeignKey(Estadotarea, models.DO_NOTHING,db_column='idestadotarea' )
    semaforo_idsemaforo = models.ForeignKey(Semaforo, models.DO_NOTHING, db_column='semaforo_idsemaforo')

    class Meta:
        managed = False
        db_table = 'tareaejecutada'


class Responsabletarea(models.Model):
    idresponsabletareausuario = models.BigIntegerField(primary_key=True)
    idtareaejecutada = models.ForeignKey(Tareaejecutada, models.DO_NOTHING, db_column='idtareaejecutada')
    usuario_idusuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='usuario_idusuario')
    asignador = models.BigIntegerField()

    class Meta:
        managed = False
        db_table = 'responsabletarea'


class Documento(models.Model):
    iddocumento = models.BigIntegerField(primary_key=True)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    archivo = models.BinaryField()
    idtareaejecutada = models.ForeignKey(Tareaejecutada, models.DO_NOTHING, db_column='idtareaejecutada')
    estado = models.FloatField()

    class Meta:
        managed = False
        db_table = 'documento'        
