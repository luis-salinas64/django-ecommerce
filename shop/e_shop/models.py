from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Categoria(models.Model):

    id = models.BigAutoField(db_column='ID', primary_key=True)
    
    categoria = models.CharField(verbose_name='categorias', max_length=20, default='')

    class Meta:
        db_table = 'e_shop_categoria'

    def __str__(self):
        return f'{self.categoria}'


class Talle(models.Model):

    id = models.BigAutoField(db_column='ID',primary_key=True)
    
    talle = models.CharField(verbose_name='talles', max_length=5, default='', blank=True)

    class Meta:
        db_table = 'e_shop_talle'

    def __str__(self):
        return f'{self.talle}'

class Articulo(models.Model):
    '''
    Esta clase hereda de Django models.Model y crea una tabla llamada
    Articulos. Las columnas toman el nombre especificado de cada objeto.
    '''
    id = models.BigAutoField(db_column='ID', primary_key=True)

    art_id = models.PositiveIntegerField(verbose_name='codigo_art', default='', unique=True)

    categoria_id = models.ForeignKey(Categoria,on_delete=models.DO_NOTHING,
                                    verbose_name='categoria', max_length=5,blank=True)

    nombre = models.CharField(verbose_name='nombre', max_length=80, default='')

    talle_id = models.ForeignKey(Talle,on_delete=models.DO_NOTHING,
                                verbose_name='talle',max_length=3, blank=True)

    color = models.CharField(verbose_name='color', max_length=20, default='')
    
    precio = models.FloatField(verbose_name='precio', max_length=10, default=0.00)

    stock_qty = models.PositiveIntegerField(verbose_name='stock qty', default=0)
    
    picture = models.ImageField(null=True, blank=True)

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

class WishList(models.Model):
    id = models.BigAutoField(db_column='ID', primary_key=True)
    user_id = models.ForeignKey(User,
                                verbose_name='User',
                                on_delete=models.DO_NOTHING,
                                default=1, blank=True
                                )
    art_id = models.ForeignKey(Articulo,
                                 verbose_name='Articulo',
                                 on_delete=models.CASCADE,
                                 default=0, blank=True
                                 )
    favorite = models.BooleanField(
        verbose_name='Favorite', default=False)
    cart = models.BooleanField(
        verbose_name='carts', default=False)
    wished_qty = models.PositiveIntegerField(
        verbose_name='wished qty', default=0)
    buied_qty = models.PositiveIntegerField(
        verbose_name='buied qty', default=0)

    class Meta:
        db_table = 'e_shop_wish_list'

    def __str__(self):
        return f'{self.id}'




