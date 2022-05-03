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
    
    path('detail_nuevo', DetailNuevoView.as_view(), name='detail_nuevo'),
    path('index1', IndexView.as_view(), name='index1'),
    #path('camisas', CamisasView.as_view(), name='camisas'),
    path('categorias', CategoriasView.as_view(), name='categorias'),
    #path('remeras', RemerasView.as_view(), name='remeras'),
    #path('vestidos', VestidosView.as_view(), name='vestidos'),
    #path('camperas', CamperasView.as_view(), name='camperas'),
    #path('jeans', JeansView.as_view(), name='jeans'),
    #path('pantalones', PantalonesView.as_view(), name='pantalones'),
    
    path('gracias', ThanksView.as_view(), name='gracias'),
    path('update-user', UpdateUserView.as_view(), name= 'update'),
    path('user', login_required(UserView.as_view()), name= 'user'),
    path('wish', login_required(WishView.as_view()), name='wish'),
    path('cart', login_required(CartView.as_view()), name='cart'),

    path('admin', login_required(AdminView.as_view()), name='admin'),
    path('ok', login_required(OkCargaView.as_view()), name='ok'),

    path('listado_art', login_required(ListadoView.as_view()), name='listado_art'),
    path('listado_cat', login_required(ListadoCatView.as_view()), name='listado_cat'),
    path('listado_color', login_required(ListadoColorView.as_view()), name='listado_color'),
    
    path('color', login_required(register_color), name='color'),
    path('categoria',login_required(register_cat), name='categoria'),
    path('carga_form',login_required(register_art), name='carga_form'),

    path('art_delete/<int:art_id>',login_required(art_delete),name='art_delete'),
    path('cat_delete/<int:id>',login_required(cat_delete),name='cat_delete'),
    path('color_delete/<int:id>',login_required(color_delete),name='color_delete'),

    path('edit_articulo/<int:art_id>',login_required(edit_articulo),name='edit_articulo'),
    path('edit_categoria/<int:id>',login_required(edit_categoria),name='edit_categoria'),
    path('edit_color/<int:id>',login_required(edit_color),name='edit_color'),

    # NOTE: Grafico en Plotly en HTML:
    path('graph', GraphView.as_view(), name='graph'),
    

    # NOTE: Formularios ocultos
    path('check_button', check_button, name='check_button'),
    #path('check_talle', check_talle,name='check_talle'),
    path('gracias', gracias_compra, name='gracias'),
    
    

    # NOTE: Formularios para DB por usuarios autorizados

    #path('carga_form', login_required(register_art), name='carga_form'),
    

    # NOTE: Ejemplos de Bootstrap HTML:
    path('bootstrap-login', BootstrapLoginUserView.as_view(), name='loginbootstrap'),
    path('bootstrap-signup', BootstrapSignupView.as_view(), name='signupbootstrap'),

     
    

]

