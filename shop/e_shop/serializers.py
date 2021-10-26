from e_shop.models import Categoria,Talle,Articulo
from django.contrib.auth.models import User
# Luego importamos todos los serializadores de django rest framework.
from rest_framework import serializers

class CategoriaSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Categoria
        fields = ("__all__")    

class TalleSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Talle
        fields = ("__all__")    
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields= ("__all__")

class ArticuloSerializer(serializers.ModelSerializer):
    
    categoria_id = serializers.PrimaryKeyRelatedField(write_only=True,
            queryset=Categoria.objects.all())
    
    talle_id = serializers.PrimaryKeyRelatedField(write_only=True,
            queryset=Talle.objects.all())
    
    class Meta:
        model = Articulo
        fields = ("__all__")

