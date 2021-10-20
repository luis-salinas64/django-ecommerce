from django.contrib import admin
from e_shop.models import *
# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass
    '''
    list_display = ('categ_id','categoria')
    fieldsets = (
        (None, {
            'fields': ('categ_id','categoria')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
)
    '''

@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    
    list_display = ('id_talle','talle')
    fieldsets = (
        (None, {
            'fields': ('id_talle','talle')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
    

@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
    

# NOTE: Para seleccionar los campos en la tabla de registros
    list_display = ('art_id','nombre', 'precio','stock_qty')

    # NOTE: Filtro lateral de elementos:
    list_filter= ('nombre','art_id')
    
    # NOTE: Buscador de elementos en la columna:
    search_fields = ['nombre']

    
    # NOTE: Genera un campo desplegable con los registros seleccionados.
    fieldsets = (
        (None, {
            'fields': ('art_id','nombre', 'stock_qty')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('precio','color','picture'),
        }),
    )
