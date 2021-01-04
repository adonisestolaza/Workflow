from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from core.mainwork.models import Rol, Cargo, Empresa, Unidad
         
class ManejadorUsuario(BaseUserManager):
    def create_user(self, correo, password=None):
        if not correo:
            raise ValueError('Usuarios deben tener correo')

        usuario = self.model(
            correo=self.normalize_email(correo),
        )

        usuario.set_password(password)
        usuario.save(using=self.db)
        return usuario

    def create_superuser(self, correo, password):
            
            usuario = self.create_user(
                correo,
                password=password,
            )
            usuario.staff = True
            usuario.admin = True
            usuario.save(using=self.db)
            return usuario

class Usuario(AbstractBaseUser):
    rut = models.CharField(max_length=10)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    telefono =  models.IntegerField()
    direccion =  models.CharField(max_length=50)
    correo = models.EmailField(verbose_name='correo electronico', max_length=100, unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE ,blank=True, null = True)
    unidad = models.ForeignKey(Unidad, on_delete=models.CASCADE, blank=True, null = True)
    cargo = models.ForeignKey(Cargo, on_delete=models.CASCADE, blank=True, null = True)
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    
    activo = models.BooleanField(('Activo'), default=True)
    staff = models.BooleanField(default= False)
    admin = models.BooleanField(default= False)
    
    objects = ManejadorUsuario()

    USERNAME_FIELD = 'correo'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name= ('usuario')
        verbose_name_plural = ('usuarios')
        db_table = 'usuario'
  
    def get_full_name(self):
        return self.nombres + ' ' + self.apellidos   

    def get_short_name(self):
        return self.nombres

    def has_perm(self, perm, obj=None):
        "El usuario cuenta con permiso?"
        return True

    def has_module_perms(self, app_label):
        "El usuario cuenta con permiso para el modulo?"
        return True 
     
    def es_admin(self, app_label):
        
        if self.rol == 1:
            return True

        return False  

    @property 
    def is_staff(self):
        "El usuario es staff (no super usuario)"
        return self.staff  

    @property 
    def is_admin(self):
        "El usuario es un administrador (super usuario)"
        return self.admin 

    @property 
    def is_active(self):
        "El usuario esta activo "
        return self.activo                   






