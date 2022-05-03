from django.contrib import admin
from django.utils.html import format_html
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

@admin.register(Color)
class ColorAdmin(admin.ModelAdmin):
    
    
    list_display = ('id','color')
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



@admin.register(Articulo)
class ArticuloAdmin(admin.ModelAdmin):
   

# NOTE: Para seleccionar los campos en la tabla de registros
    list_display = ('id','art_id','nombre','color_id','categoria_id')

    # NOTE: Filtro lateral de elementos:
    list_filter= ('nombre','art_id','categoria_id')
    
    # NOTE: Buscador de elementos en la columna:
    search_fields = ['nombre']

    
    # NOTE: Genera un campo desplegable con los registros seleccionados.
    fieldsets = (
        (None, {
            'fields': ('art_id','categoria_id','nombre')
        }),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('color_id','talle_xs','talle_s','talle_m','talle_l','talle_xl','precio','picture','picture_1','picture_2','picture_3'),
        }),
    )
    def imagen(self,obj):
        return format_html('<img src={} width="50" height="100" /> ', obj.picture.url, obj.picture_1.url,
                            obj.picture_2.url, obj.picture_3.url)
        