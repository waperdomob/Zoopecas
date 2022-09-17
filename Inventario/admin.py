from django.contrib import admin
from Inventario import *
from import_export.admin import ImportExportModelAdmin

from Inventario.models import Categorias, Productos, Proveedores
# Register your models here.

class categoriasAdmin(admin.ModelAdmin):
    list_display=("categoria",)

class proveedoresAdmin(admin.ModelAdmin):
    list_display= ("proveedor","telefono","nombreEmpleado",)

class productosAdmin(ImportExportModelAdmin):
    list_display=("producto","descripcion","cantidad_total","precio_compra","precio_venta","imagen","categoria",)

admin.site.register(Categorias,categoriasAdmin)
admin.site.register(Proveedores,proveedoresAdmin)
admin.site.register(Productos,productosAdmin)
