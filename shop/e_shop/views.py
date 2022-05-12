
from re import template
from textwrap import indent
from unicodedata import name
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Importo vistas genericas:
from django.db.models.query import QuerySet
from django.db.models import Count

# from django.db import filters
from django.views.generic import TemplateView, ListView, CreateView,DeleteView,UpdateView
import io

# Importamos los modelos que vamos a usar:
from django.contrib.auth.models import User

from matplotlib.style import context
from e_shop.models import *
# Graficos
import plotly.graph_objs as go
from plotly.offline import plot

# Formulario de registro:
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm

from e_shop.forms import *
#from shop.e_shop.api.api_views import *

class BaseView(TemplateView):
    '''
    Template base que vamos a extender para el resto de las páginas del sitio.
    '''
    template_name = 'e_shop/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Hacer un query que obtenga todas las categorias registradas en la tabla
        categorias = Categoria.objects.all()

        
        context["categorias"] = categorias

        return context


class InicioView(TemplateView):
    '''
    Template de Inicio.
    '''
    template_name = 'e_shop/inicio.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Hacer un query que obtenga todas las categorias registradas en la tabla
        categorias = Categoria.objects.all()

        id_categoria = {}


        context["categorias"] = categorias
        return context


class LoginUserView(TemplateView):
    '''
    Formulario de inicio de sesión.
    '''
    template_name = 'e_shop/login.html'


class UserForm(UserCreationForm):
    '''
    Formulario de creación de usuario.
    Utilizamos un formulario que viene por defecto en Django y que cumple con todos los
    requisitos para agregar un nuevo usuario a la base de datos.
    También tiene los métodos para validar todos sus campos.
    '''
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()



    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','password1','password2')


def register(request):
    '''
    Función que complementa el formulario de registro de usuario.
    Al completar el formulario, se envía la información a esta función que espera
    una petición de tipo `POST`, si la información enviada no es valida o la petición no es POST,
    se redirige nuevamente a la página de registro. Si el registro fue exitoso,
    el usuario será redirigido a la página de logueo.
    '''
    if request.method == 'POST':
        # Si la petición es de tipo POST, analizamos los datos del formulario:
        # Creamos un objeto de tipo UserForm (la clase que creamos mas arriba)
        # Pasandole los datos del request:
        form = UserForm(request.POST)
        # Luego, utilizamos el método que viene en en la clase UserCreationForm
        # para validar los datos del formulario:
        [print('',item) for item in form] # NOTE: Imprimimos para ver el contenido del formulario COMPLETO
        if form.is_valid():
            # Si los datos son validos, el formulario guarda los datos en la base de datos.
            # Al heredar de UserCreationForm, aplica las codificaciónes en el password y todo
            # lo necesario:
            form.save()
            # Con todo terminado, redirigimos a la página de inicio de sesión,
            # porque por defecto, registrar un usuario no es iniciar una sesión.
            return redirect('/e-shop/bootstrap-login')
    else:
        # Si el método no es de tipo POST, se crea un objeto de tipo formulario
        # Y luego se envía al contexto de renderización.
        form = UserForm()
    # Si los datos del POST son invalidos o si el método es distinto a POST
    # retornamos el render de la página de registro, con el formulario de registro en el contexto.
    [print('',item) for item in form] # NOTE: Imprimimos para ver el contenido del formulario vacío
    return render(request, 'e_shop/bootstrap-signup.html', {'form': form})

# ---------------------------- OPERACIONES DE ADMINISTRADOR --------------------------------

# Listado de Articulos

class ListadoView(ListView):

    model = Articulo
    template_name='e_shop/listado_art.html'

    queryset = Articulo.objects.all().order_by('art_id')

# Listado de Categorias
class ListadoCatView(ListView):

    model = Categoria
    template_name='e_shop/listado_cat.html'

    queryset = Categoria.objects.all().order_by('id')

# Listado de Colores
class ListadoColorView(ListView):

    model = Color
    template_name='e_shop/listado_color.html'

    queryset = Color.objects.all().order_by('id')

# Menu Administrador
class AdminView(TemplateView):
    model = Articulo
    template_name='e_shop/admin.html'


# Confirmacion de carga correcta
class OkCargaView(TemplateView):
    template_name = 'e_shop/ok.html'


# Registrar nueva Categoria
def register_cat(request):

    if request.method == 'POST':
        # Si la petición es de tipo POST, analizamos los datos del formulario:
        # Creamos un objeto de tipo Form
        # Pasandole los datos del request:
        form = CategoriaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()


            return redirect('/e-shop/ok')

    else:
        # Si el método no es de tipo POST, se crea un objeto de tipo formulario
        # Y luego se envía al contexto de renderización.
        form = CategoriaForm()

    return render(request,'e_shop/carga_form.html', {'form':form})

# Registrar nuevo Color
def register_color(request):

    if request.method == 'POST':
        # Si la petición es de tipo POST, analizamos los datos del formulario:
        # Creamos un objeto de tipo Form
        # Pasandole los datos del request:
        form = ColorForm(request.POST)

        if form.is_valid():
            form.save()


            return redirect('/e-shop/ok')

    else:
        # Si el método no es de tipo POST, se crea un objeto de tipo formulario
        # Y luego se envía al contexto de renderización.
        form = ColorForm()

    return render(request,'e_shop/carga_form.html', {'form':form})

# Registrar nuevo articulo
def register_art(request):
    '''
    Función que complementa el formulario de registro de articulo.
    Al completar el formulario, se envía la información a esta función que espera
    una petición de tipo `POST`, si la información enviada no es valida o la petición no es POST,
    se redirige nuevamente a la página de carga. Si el registro fue exitoso,
    el usuario notificado.
    '''

    if request.method == 'POST':
        # Si la petición es de tipo POST, analizamos los datos del formulario:
        # Creamos un objeto de tipo Form
        # Pasandole los datos del request:
        form = ArticuloForm(request.POST,request.FILES)



        if form.is_valid():
            form.save()
            print("valido")


            return redirect('/e-shop/ok')

    else:
        # Si el método no es de tipo POST, se crea un objeto de tipo formulario
        # Y luego se envía al contexto de renderización.
        form = ArticuloForm()

    return render(request,'e_shop/carga_form.html', {'form':form})

# Borrar categoria
def cat_delete (request,id):

    categoria = Categoria.objects.get(id=id)
    if request.method=="POST":

        categoria.delete()
        return redirect('/e-shop/listado_cat')

    return render(request,'e_shop/cat_delete.html',{'categoria':categoria})

# Borrar color
def color_delete (request,id):

    color = Color.objects.get(id=id)
    if request.method=="POST":

        color.delete()
        return redirect('/e-shop/listado_color')

    return render(request,'e_shop/color_delete.html',{'color':color})


# Borrar articulo
def art_delete (request,art_id):

    articulo = Articulo.objects.get(art_id=art_id)
    if request.method=="POST":

        articulo.delete()
        return redirect('/e-shop/listado_art')

    return render(request,'e_shop/art_delete.html',{'articulo':articulo})


# Editar Articulo

def edit_articulo(request,art_id):
    form = None

    articulo = Articulo.objects.get(art_id=art_id)

    if request.method == 'GET':
        form = ArticuloForm(instance=articulo)

    else:
        form = ArticuloForm(request.POST,instance=articulo)


        if form.is_valid():
            form.save()
            print("valido")

            return redirect('/e-shop/ok')
    return render (request, 'e_shop/carga_form.html', {'form':form})


# Editar Categoria
def edit_categoria(request,id):
    form = None

    categoria = Categoria.objects.get(id=id)

    if request.method == 'GET':
        form = CategoriaForm(instance=categoria)

    else:
        form = CategoriaForm(request.POST,instance=categoria)


        if form.is_valid():
            form.save()
            print("valido")

            return redirect('/e-shop/ok')
    return render (request, 'e_shop/carga_form.html', {'form':form})

# Editar Color
def edit_color(request,id):
    form = None

    color = Color.objects.get(id=id)

    if request.method == 'GET':
        form = ColorForm(instance=color)

    else:
        form = ColorForm(request.POST,instance=color)


        if form.is_valid():
            form.save()
            print("valido")

            return redirect('/e-shop/ok')
    return render (request, 'e_shop/carga_form.html', {'form':form})


# -----------------------------

class IndexView(ListView):
    '''
    Página principal del sitio.
    Utilizamos `ListView` para poder aprovechar sus funciones de paginado.
    Para ello tenemos que utilizar sus atributos:
    \n'''

    queryset = Articulo.objects.all().order_by('art_id')


    # NOTE: Este queryset incorporará una lista de elementos a la que le asignará
    # Automáticamente el nombre de articulo_list


    template_name = 'e_shop/index1.html'
    paginate_by = 12


    # NOTE: Examinamos qué incluye nuestro contexto:
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        # Hacer un query que obtenga todas las categorias registradas en la tabla
        categorias = Categoria.objects.all()

        context["categorias"] = categorias

        return context



class DetailView(TemplateView):
    template_name = 'e_shop/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Buscar el articulo en la base de datos TUYA, usas la funcion Articulo.objects.get y le
            # mandas la id del articulo, por eso art_id=self.request.GET.get('art_id')
            # eso te devuelve el artículo que esté en la db que coincida con el id

            # el art_id llega por url
            articulo_obj = Articulo.objects.get(art_id=self.request.GET.get('art_id'))

            # context es lo que muestra el articulo al usuario, le tenemos que dar todos los valores
            # que necesita

            context["articulo"] = articulo_obj

            # Agrego un diccionario talles para que sea mas facil realizar la impresión
            context["talle"] = {
                'xs': articulo_obj.talle_xs,
                's': articulo_obj.talle_s,
                'm': articulo_obj.talle_m,
                'l': articulo_obj.talle_l,
                'xl': articulo_obj.talle_xl,
            }

            # Procedimiento para cuando un usuario NO está logueado
            username = self.request.user
            if username is not None:
                user_obj = User.objects.filter(username = username)
                if user_obj.first() is not None:
                    wish_obj = WishList.objects.filter(user_id=user_obj[0].id, art_id = articulo_obj)

                    if wish_obj.first() is not None:
                        context["favorite"] = wish_obj.first().favorite
                        context["cart"] = wish_obj.first().cart
                        context["wished_qty"] = 1
                    else:
                        context["favorite"] = False
                        context["cart"] = False
                        context["wished_qty"] = 0

            return context

        except:
            return context


def check_button(request):
    '''
    Esta función tiene como objetivo el cambio de estado de los botones de favoritos y carrito.
    '''
    if request.method == 'POST':

        # NOTE: Obtenemos los datos necesarios:
        username = request.POST.get('username')
        art_id = request.POST.get('art_id')
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        color_id = request.POST.get('color_id')
        talle = request.POST.get('talle')
        user_authenticated = request.POST.get('user_authenticated')
        type_button = request.POST.get('type_button')
        actual_value = request.POST.get('actual_value')
        path = request.POST.get('path')

        # Validamos los datos y les damos formato:
        username = username if username != '' else None
        art_id = art_id if art_id != '' else None
        nombre =nombre if nombre != '' else None
        color_id = color_id if color_id != '' else None
        precio = precio if precio != '' else None
        talle = talle if talle != '' else None
        user_authenticated = True if user_authenticated == 'True' else False
        type_button = type_button if type_button != '' else None
        actual_value = True if actual_value == 'True' else False
        path = path if path != None else 'index1'



        if user_authenticated and username != None:
            # Si el usuario está autenticado, traemos su "wishlist"
            user_obj = User.objects.get(username=username)

            # Buscamos el art_id pasado en el request
            art_obj = Articulo.objects.get(art_id=art_id)
            
            wish_obj = WishList.objects.filter(
                user_id=user_obj, art_id=art_obj).first()
            if not wish_obj:
                # Si no tiene "wishlist" creamos una
                wish_obj = WishList.objects.create(
                    user_id=user_obj, art_id=art_obj, talle_elegido=talle)

            # Remplazamos el estado del botón seleccionado:
            if type_button == "cart":
                wish_obj.cart = not actual_value
                wish_obj.save()
                print('wish_obj.cart :', wish_obj.cart)
            elif type_button == "favorite":
                wish_obj.favorite = not actual_value
                print('wish_obj.favorite :', wish_obj.favorite)
                wish_obj.save()

            else:
                pass
            # Componemos los endpoints segun la página:
            if 'detail' in path:
                path += f'?art_id={art_id}'

            # Una vez terminada la modificación, volvemos a la misma página.
            return redirect(path)

        else:
            # Si el usuario no está autenticado, lo redirigimos a la página de logueo.
            return redirect('login')
    else:
        # Si por error quisieron acceder al recurso con otro método que no sea POST, lo redirigimos al index
        return redirect('index1')


class CartView(TemplateView):
    '''
    Vista de carrito de compras.
    Aquí se listará el total de elementos del carrito del usuario,
    luego en el template se colocará un formulario en cada elemento del carrito
    para darlo de baja, y un boton general para concretar el pedido.
    '''

    template_name = 'e_shop/cart.html'

    def get_context_data(self, **kwargs):
        '''
        En el contexto, devolvemos la lista total de elementos en el carrito de compras,
        y el precio total calculado para la compra.
        '''

        context = super().get_context_data(**kwargs)
        # Obtenemos el usuario del request
        username = self.request.user
        # Creamos el objeto del usuario pasando el username
        user_obj = User.objects.get(username=username)
        # Creamos un objeto obteniendo del usuario lo que puso en su carrito (check_button)
        wish_obj = WishList.objects.filter(user_id=user_obj, cart=True)
        # Creamos una lista de objetos
        cart_items = [obj.art_id for obj in wish_obj]
        
        # Pasamos al contexto la lista de art deseados (wish_list)
        context['cart_items'] = wish_obj

        
        context['precio_total'] = round((sum([float(articulo.precio) for articulo in cart_items])),2)

        return context

class ThanksView(TemplateView):
    template_name = 'e_shop/thanks.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        username = self.request.user
        # Creamos el objeto del usuario pasando el username
        user_obj = User.objects.get(username=username)
        # Creamos un objeto obteniendo del usuario lo que puso en su carrito (check_button)
        wish_obj = WishList.objects.filter(user_id=user_obj, cart=True)
        # Creamos una lista de objetos

        for articulo in wish_obj:

            art_buscado = Articulo.objects.filter(art_id=articulo.art_id.art_id).first()
            
            if articulo.talle_elegido == 'xs':
                art_buscado.talle_xs -= 1
            elif articulo.talle_elegido == 's':
                art_buscado.talle_s -= 1
            elif articulo.talle_elegido == 'm':
                art_buscado.talle_m -= 1
            elif articulo.talle_elegido == 'l':
                art_buscado.talle_l -= 1
            elif articulo.talle_elegido == 'xl':
                art_buscado.talle_xl -= 1
            

            art_buscado.save()
            articulo.delete()
            

        cart_items = [obj.art_id for obj in wish_obj]
            
        # Pasamos al contexto la lista de art deseados (wish_list)
        context['cart_items'] = wish_obj        

        context['articulo'] = self.request.POST

        

        return context


class WishView(TemplateView):
    '''
    En esta vista vamos a traer todos los articulos favoritos de un usuario en particular.
    Luego en el Template vamos a colocar un formulario por cada favorito,
    para eliminarlo de la lista de favoritos.
    '''

    template_name = 'e_shop/wish.html'

    def get_context_data(self, **kwargs):

        # Preparamos en nuestro contexto la lista de articulos del usuario registrado.

        context = super().get_context_data(**kwargs)
        # Obtenemos el username del request
        username = self.request.user
        # Creamos un objeto a partir del usuario
        user_obj = User.objects.get(username=username)
        wish_obj = WishList.objects.filter(user_id=user_obj, favorite=True)
        #cart_items = [obj.art_id for obj in wish_obj]
        context['fav_items'] = wish_obj

        return context



class UpdateUserView(TemplateView):

    # Esta vista tiene como objetivo, proporcionar un formulario de actualización de los campos de usuario.

    template_name = 'e_shop/update-user.html'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)




class UserView(TemplateView):
    '''
    Vista con el detalle de los datos personales del usuario
    '''

    template_name = 'e_shop/user.html'

    # Preparamos en nuestro contexto la lista de articulos del usuario registrado.
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)




# ------------------------------- NOTE: Categorias --------------------------

class CategoriasView(ListView):

    template_name = 'e_shop/categorias.html'


    queryset = Articulo.objects.all()


    def get_context_data(self, **kwargs):

        categoria_id = self.request.GET.get("categoria_id")

        # Filtrar articulos por categoria
        articulo_obj = Articulo.objects.all().filter(categoria_id=categoria_id)


        context = super().get_context_data(**kwargs)
        categorias = Categoria.objects.all()

        context["categorias"] = categorias
        # Agregar lista de articulos al contexto para que lo use el template
        context["articulos"] = articulo_obj

        return context


# NOTE: Vistas con Bootstrap:

class BootstrapLoginUserView(TemplateView):

   # Vista para Template de login con estilo de bootstrap.

    template_name = 'e_shop/bootstrap-login.html'

class BootstrapSignupView(TemplateView):

    # Vista para Template de registro de usuario con estilo de bootstrap.

    template_name = 'e_shop/bootstrap-signup.html'

# --------------------------------------Grafico de precios ------------------------------

class GraphView(TemplateView):
    '''
    Vista para Template de registro de usuario con estilo de bootstrap.
    '''
    template_name = 'e_shop/graph.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtenemos la lista de comics:
        articulos = Articulo.objects.all()

        # Obtenemos los nombres y precios en dos listas:
        nombres = [articulo.nombre for articulo in articulos]
        precios = [articulo.precio for articulo in articulos]

        # Gráfico scatter tipo bar (idem plt.bar)
        # Le pasamos como parámetros de X e Y los títulos y precios:
        trace1 = go.Bar(
            x=nombres,
            y=precios,
            name='ploty bar',
            orientation='v',
        )
        data = [trace1]
        layout = go.Layout(
            xaxis=dict(
                autorange=True,
                linewidth=3,
                categoryorder='total descending',
                rangeslider=dict(visible=True),
            ),
            yaxis=dict(
                autorange=True,
                linewidth=3,
            ),
            template='plotly_dark',
            showlegend=True
        )
        fig = go.Figure(data=data, layout=layout)
        plot_div = plot(fig, output_type='div', include_plotlyjs=True)
        context['graph'] = plot_div
        return context