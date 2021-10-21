from django.contrib import admin
from e_shop.models import *
# Register your models here.

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    
    
    list_display = ('id','categoria')
    '''
    fieldsets = (
        (None, {
            'fields': ('id','categoria')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
)
    '''

@admin.register(Talle)
class TalleAdmin(admin.ModelAdmin):
    
    
    list_display = ('id','talle')
    '''
    fieldsets = (
        (None, {
            'fields': ('id','talle')
        }),
    
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
    '''

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
            'fields': ('art_id','categoria_id','nombre')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('talle_id','color','precio','stock_qty','picture'),
        }),
    )
    