from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Talle(models.Model):

    id_talle = models.BigAutoField(db_column='ID',primary_key=True)
    
    talle = models.CharField(verbose_name='talles', max_length=5, default='')

    class Meta:
        db_table = 'e_shop_talle'

    def __str__(self):
        return f'{self.id_talle}'


class Categoria(models.Model):

    id_categ = models.BigAutoField(db_column='ID', primary_key=True)
    
    categorias = models.CharField(verbose_name='categorias', max_length=5, default='')

    class Meta:
        db_table = 'e_shop_categorias'

    def __str__(self):
        return f'{self.id_categ}'

class Articulo(models.Model):
    '''
    Esta clase hereda de Django models.Model y crea una tabla llamada
    Articulos. Las columnas toman el nombre especificado de cada objeto.
    '''
    id = models.BigAutoField(db_column='ID', primary_key=True)

    art_id = models.PositiveIntegerField(
        verbose_name='art ids', default=0, unique=True)

    categoria = models.ForeignKey(Categoria,on_delete=models.DO_NOTHING,
                                verbose_name='categoria', max_length=5)

    nombre = models.CharField(verbose_name='nombre', max_length=80, default='')

    talle = models.ForeignKey(Talle,on_delete=models.DO_NOTHING,
                                verbose_name='talle',max_length=5)

    color = models.CharField(
        verbose_name='color', max_length=20, default='')
    
    precio = models.FloatField(verbose_name='precio', max_length=5, default=0.00)

    stock_qty = models.PositiveIntegerField(
        verbose_name='stock qty', default=0)
    
    picture = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None,
                                verbose_name='picture', default='')

    class Meta:
        '''
        Con "class Meta" podemos definir atributos de nuestras entidades como el nombre de la tabla.
        '''
        db_table = 'e_shop_articulo'

    def __str__(self):
        '''
        La función __str__ cumple la misma función que __repr__ en SQL Alchemy, 
        es lo que retorna cuando llamamos al objeto.
        '''
        return f'{self.id}'


