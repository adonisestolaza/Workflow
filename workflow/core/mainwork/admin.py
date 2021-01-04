from django.contrib import admin
from .models import Cargo, Region, Comuna, Empresa, Unidad, ProcesoTipo, TareaTipo

# Register your models here.

admin.site.register(Cargo)
admin.site.register(Empresa)
admin.site.register(Unidad)
admin.site.register(Region)
admin.site.register(Comuna)
admin.site.register(TareaTipo)
admin.site.register(ProcesoTipo)