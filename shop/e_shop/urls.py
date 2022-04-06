from django.contrib import admin
from django.urls import path, include
from django.views.generic import base
from django.views.generic.base import View
from e_shop.views import *

# Librerías para el manejo de sesión.
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

INDEX_LIST = ['inicio/', 'inicio/#', '']
INDEX_PATTERNS = [path(x, InicioView.as_view()) for x in INDEX_LIST]

urlpatterns = [

    path('base',BaseView.as_view(), name = 'base'),
    path('inicio',InicioView.as_view(), name = 'inicio'),

    # NOTE: Manejo de sesión:
    path('login', auth_views.LoginView.as_view(template_name='e_shop/bootstrap-login.html', redirect_authenticated_user=True, redirect_field_name='index'), name='login'
         ),

    path('logout', auth_views.LogoutView.as_view(next_page='/e-shop/inicio', redirect_field_name='inicio'),
         ),
    path('signup', register, name='register'),

    # NOTE: Páginas del sitio:
    path('detail', DetailsView.as_view(), name='detail'),
    path('detail1', Detail1View.as_view(), name='detail1'),
    path('index1', IndexView.as_view(), name='index1'),
    path('camisas', CamisasView.as_view(), name='camisas'),
    path('remeras', RemerasView.as_view(), name='remeras'),
    path('vestidos', VestidosView.as_view(), name='vestidos'),
    path('camperas', CamperasView.as_view(), name='camperas'),
    path('jeans', JeansView.as_view(), name='jeans'),
    path('pantalones', PantalonesView.as_view(), name='pantalones'),
    path('gracias', ThanksView.as_view(), name='gracias'),
    path('update-user', UpdateUserView.as_view(), name= 'update'),
    path('user', login_required(UserView.as_view()), name= 'user'),
    path('wish', login_required(WishView.as_view()), name='wish'),
    path('cart', login_required(CartView.as_view()), name='cart'),
    # NOTE: Ejemplos de Plotly en HTML:
    path('graph', GraphView.as_view(), name='graph'),
    

    # NOTE: Formularios ocultos
    path('checkbutton', check_button, name='checkbutton'),
    path('check_talle', check_talle,name='check_talle'),
    path('gracias', gracias_compra, name='gracias'),
    

    # NOTE: Ejemplos de Bootstrap HTML:
    path('bootstrap-login', BootstrapLoginUserView.as_view(), name='loginbootstrap'),
    path('bootstrap-signup', BootstrapSignupView.as_view(), name='signupbootstrap'),

    

]
