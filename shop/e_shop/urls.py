from django.contrib import admin
from django.urls import path, include
from django.views.generic import base
from django.views.generic.base import View
from e_shop.views import *

# Librerías para el manejo de sesión.
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required


urlpatterns = [

path('base',BaseView.as_view(), name = 'base'),

]
