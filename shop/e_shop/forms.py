from random import choices
from turtle import color
from django import forms
from e_shop.models import *



# --------------- FORMULARIO DE CARGA ARTICULO -------------------------

class CategoriaForm(forms.ModelForm):

    categoria = forms.CharField(label="Categoria", max_length=20, required=True)

    class Meta:
        model = Categoria
        fields = ('categoria',)

class ColorForm(forms.ModelForm):

    color = forms.CharField(label="Color", max_length=20, required=True)

    class Meta:
        model = Color
        fields = ('color',)


class ArticuloForm(forms.ModelForm):


    art_id = forms.FloatField(label= "articulo", required=True)
    nombre = forms.CharField(label="Nombre", max_length=20, required=True)
    categoria_id = forms.ModelChoiceField(label="Categoria", queryset=Categoria.objects.all(),initial=0)
    color_id = forms.ModelChoiceField(label="Color", queryset=Color.objects.all(),initial=0)
    talle_xs = forms.FloatField(label= "Talle xs")
    talle_s = forms.FloatField(label="Talle s")
    talle_m = forms.FloatField(label= "Talle m")
    talle_l = forms.FloatField(label= "Talle l")
    talle_xl = forms.FloatField(label= "Talle xl")
    precio = forms.FloatField(label="Precio", min_value=0.01)
    picture = forms.ImageField(label="Foto Principal")
    picture_1 = forms.ImageField(label="Foto Secundaria")
    picture_2 = forms.ImageField(label="Foto Secundaria")
    picture_3 = forms.ImageField(label="Foto Secundaria")


    class Meta:
        model = Articulo
        fields = ('art_id','nombre','categoria_id','color_id','talle_xs',
                    'talle_s','talle_m','talle_l','talle_xl','precio','picture','picture_1','picture_2','picture_3')


