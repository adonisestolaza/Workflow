from django.db import models

# Create your models here.

class Region(models.Model):
    idregion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'region'

    def __str__(self):
        return self.nombre

class Comuna(models.Model):
    id_comuna = models.AutoField(primary_key=True)
    nombre_comuna = models.CharField(max_length=50)
    id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='id_region')

    class Meta:
        managed = False
        db_table = 'comuna'

    def __str__(self):
        return self.nombre_comuna  


class Empresa(models.Model):
    idempresa = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    razonsocial = models.CharField(max_length=100, blank=True, null=True)
    direccion = models.CharField(max_length=100, blank=True, null=True)
    fechacreacion = models.DateField(blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    telefono = models.BigIntegerField(blank=True, null=True)
    logo = models.BinaryField(blank=True, null=True)
    estado = models.BooleanField(('Estado'), default=True)
    comuna_idcomuna = models.ForeignKey(Comuna, models.DO_NOTHING, db_column='comuna_idcomuna')

    class Meta:
        managed = False
        db_table = 'empresa'
        unique_together = (('idempresa', 'rut'),)

    def __str__(self):
        return self.nombre 

class Unidad(models.Model):
    idunidad = models.AutoField(primary_key=True)
    empresa_idempresa = models.ForeignKey(Empresa, models.DO_NOTHING, db_column='empresa_idempresa')
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    estado = models.BooleanField(('Estado'), default=True)

    class Meta:
        managed = False
        db_table = 'unidad'

    def __str__(self):
        return self.nombre    

class Cargo(models.Model):
    idcargo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)
    unidad_idunidad = models.ForeignKey('Unidad', models.DO_NOTHING, db_column='unidad_idunidad')
    estado = models.BooleanField(('Estado'), default=True)

    class Meta:
        managed = False
        db_table = 'cargo'
    

    def __str__(self):
        return self.nombre               


class Semaforo(models.Model):
    idsemaforo = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'semaforo'

class Estadotarea(models.Model):
    idestadotarea = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'estadotarea'


        

class Rol(models.Model):
    idrol = models.IntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=100)
    estado = models.BooleanField(('Estado'), default=True)

    class Meta:
        managed = False
        db_table = 'rol'
        ordering = ['idrol']

    def __str__(self):
        return self.nombre

class ProcesoTipo(models.Model):
    idprocesotipo = models.AutoField(primary_key=True)  
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    unidad_idunidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, db_column='unidad_idunidad')

    class Meta:
        managed = False
        db_table = 'procesotipo'

    def __str__(self):
        return self.nombre        


class TareaTipo(models.Model):
    idtareatipo = models.AutoField(primary_key=True) 
    nombre = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=50)
    duraciondias = models.IntegerField()
    orden_tarea = models.IntegerField()
    cargo_idcargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, db_column='cargo_idcargo')
    idprocesotipo = models.ForeignKey(ProcesoTipo, on_delete=models.CASCADE, db_column='idprocesotipo')


    class Meta:
        managed = False
        db_table = 'tareatipo'
        


    def __str__(self):
        return self.nombre





     


       





	


