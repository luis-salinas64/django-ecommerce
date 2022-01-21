from django.contrib import admin
from django.urls import path, include
from django.views.generic import base
from django.views.generic.base import View
from e_shop.views import *

# Librerías para el manejo de sesión.
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

INDEX_LIST = ['index/', 'index/#', '']
INDEX_PATTERNS = [path(x, IndexView.as_view()) for x in INDEX_LIST]

urlpatterns = [

    path('base',BaseView.as_view(), name = 'base'),

    # NOTE: Manejo de sesión:
    path('login', auth_views.LoginView.as_view(template_name='e_shop/bootstrap-login.html', redirect_authenticated_user=True, redirect_field_name='index'), name='login'
         ),

    path('logout', auth_views.LogoutView.as_view(next_page='/e-shop/index', redirect_field_name='index'),
         ),
    path('signup', register, name='register'),

    # NOTE: Páginas del sitio:
    path('detail', DetailsView.as_view(), name='detail'),
    path('index', IndexView.as_view(), name='index'),
    path('gracias', ThanksView.as_view(), name='gracias'),
    path('update-user', UpdateUserView.as_view(), name= 'update'),
    path('user', login_required(UserView.as_view()), name= 'user'),
    path('wish', login_required(WishView.as_view()), name='wish'),
    path('cart', login_required(CartView.as_view()), name='cart'),

    # NOTE: Formularios ocultos
    path('checkbutton', check_button, name='checkbutton'),

    # NOTE: Ejemplos de Bootstrap HTML:
    path('bootstrap-login', BootstrapLoginUserView.as_view(), name='loginbootstrap'),
    path('bootstrap-signup', BootstrapSignupView.as_view(), name='signupbootstrap'),
]
