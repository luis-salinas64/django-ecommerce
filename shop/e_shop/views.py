from re import template
from unicodedata import name
from django.shortcuts import render
# Create your views here.
# Importo vistas genericas:
from django.db.models.query import QuerySet
from django.db.models import Count
# from django.db import filters
from django.views.generic import TemplateView, ListView

# Importamos los modelos que vamos a usar:
from django.contrib.auth.models import User
from matplotlib.style import context
from e_shop.models import *


# Formulario de registro:
from django import forms
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm

class BaseView(TemplateView):
    '''
    Template base que vamos a extender para el resto de las páginas del sitio.
    '''
    template_name = 'e_shop/base.html'



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

class IndexView(ListView):
    '''
    Página principal del sitio.
    Utilizamos `ListView` para poder aprovechar sus funciones de paginado.
    Para ello tenemos que utilizar sus atributos:
    \n'''


    queryset = Articulo.objects.all().order_by('art_id')
    # NOTE: Este queryset incorporará una lista de elementos a la que le asignará
    # Automáticamente el nombre de articulo_list


    template_name = 'e_shop/index.html'
    paginate_by = 9


    # NOTE: Examinamos qué incluye nuestro contexto:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context




class DetailsView(TemplateView):
    template_name = 'e_shop/detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            # Buscar el articulo en la base de datos TUYA, usas la funcion Articulo.objects.get y le
            # mandas la id del articulo, por eso art_id=self.request.GET.get('art_id')
            # eso te devuelve el artículo que esté en la db que coincida con el id

            articulo_obj = Articulo.objects.get(art_id=self.request.GET.get('art_id'))

            # A partir de acá, articulo_obj es un objeto articulo con todos los datos del articulo

            # context es lo que muestra el articulo al usuario, le tenemos que dar todos los valores
            # que necesita


            if articulo_obj.talle_xs > 0:
                articulo_obj.talle_xs = 'xs'
            if articulo_obj.talle_s > 0:
                articulo_obj.talle_s = 's'    
            if articulo_obj.talle_m > 0:
                articulo_obj.talle_m = 'm'
            if articulo_obj.talle_l > 0:
                articulo_obj.talle_l = 'l'
            if articulo_obj.talle_xl > 0:
                articulo_obj.talle_xl = 'xl'

            context["articulo"] = articulo_obj

            context['articulo_picture_full'] = str(articulo_obj.picture)
            context['articulo_picture_1full'] = str(articulo_obj.picture_1)
            context['articulo_picture_2full'] = str(articulo_obj.picture_2)
            context['articulo_picture_3full'] = str(articulo_obj.picture_3)

            context['articulo_nombre'] = str(articulo_obj.nombre).replace('<br>', '\n')

            context['articulo_color'] = str(articulo_obj.color_id)

            context['articulo_talle_xs'] = str(articulo_obj.talle_xs)
            context['articulo_talle_s'] = str(articulo_obj.talle_s)
            context['articulo_talle_m'] = str(articulo_obj.talle_m)
            context['articulo_talle_l'] = str(articulo_obj.talle_l)
            context['articulo_talle_xl'] = str(articulo_obj.talle_xl)

            username = self.request.user
            if username is not None:
                user_obj = User.objects.filter(username = username)
                if user_obj.first() is not None:
                    wish_obj = WishList.objects.filter(user_id=user_obj[0].id, art_id = articulo_obj)

                    if wish_obj.first() is not None:
                        context["favorite"] = wish_obj.first().favorite
                        context["cart"] = wish_obj.first().cart
                        context["wished_qty"] = wish_obj.first().wished_qty
                    else:
                        context["favorite"] = False
                        context["cart"] = False
                        context["wished_qty"] = 0

        except:
            return context



        return context



def check_button(request):
    '''
    Esta función tiene como objetivo el cambio de estado de los botones de favoritos y carrito.
    '''
    if request.method == 'POST':
        print(request.path)
        # NOTE: Obtenemos los datos necesarios:
        username = request.POST.get('username')
        art_id = request.POST.get('art_id')
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        color_id = request.POST.get('color_id')
        talle_xs = request.POST.get('talle_xs')
        talle_s = request.POST.get('talle_s')
        talle_m = request.POST.get('talle_m')
        talle_l = request.POST.get('talle_l')
        talle_xl = request.POST.get('talle_xl')
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
        talle_xs = talle_xs if talle_xs != '' else None
        talle_s = talle_s if talle_s != '' else None
        talle_m = talle_m if talle_m != '' else None
        talle_l = talle_l if talle_l != '' else None
        talle_xl = talle_xl if talle_xl != '' else None
        user_authenticated = True if user_authenticated == 'True' else False
        type_button = type_button if type_button != '' else None
        actual_value = True if actual_value == 'True' else False
        path = path if path != None else 'index'

        print(f'Username:{username}')
        print(f'art_id:{art_id}')
        print(f'Nombre:{nombre}')
        print(f'Color:{color_id}')
        print(f'Precio:{precio}')
        print(f'Talle xs:{talle_xs}')
        print(f'Talle s:{talle_s}')
        print(f'Talle m:{talle_m}')
        print(f'Talle l:{talle_l}')
        print(f'Talle xl:{talle_xl}')

        if user_authenticated and username != None:
            # Si el usuario está autenticado, traemos su "wishlist"
            user_obj = User.objects.get(username=username)
            art_obj = Articulo.objects.get(art_id=art_id)
            wish_obj = WishList.objects.filter(
                user_id=user_obj, art_id=art_obj).first()
            if not wish_obj:
                # Si no tiene "wishlist" creamos una
                wish_obj = WishList.objects.create(
                    user_id=user_obj, art_id=art_obj)

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
        return redirect('index')


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
        username = self.request.user
        user_obj = User.objects.get(username=username)
        wish_obj = WishList.objects.filter(user_id=user_obj, cart=True)
        cart_items = [obj.art_id for obj in wish_obj]
        context['cart_items'] = cart_items
        context['precio_total'] = round((sum([float(articulo.precio) for articulo in cart_items])),2)


        print(context['cart_items'])
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
        username = self.request.user
        user_obj = User.objects.get(username=username)
        wish_obj = WishList.objects.filter(user_id=user_obj, favorite=True)
        cart_items = [obj.art_id for obj in wish_obj]
        context['fav_items'] = cart_items
        print(context['fav_items'])
        return context


class ThanksView(TemplateView):
    '''
    Página de agradecimiento. Esta es la página de respuesta una vez realizado el pedido.
    El Template tiene que tener un botón de redireccionamiento al index.
    '''

    template_name = 'e_shop/gracias.html'


class UpdateUserView(TemplateView):

    # Esta vista tiene como objetivo, proporcionar un formulario de actualización de los campos de usuario.

    template_name = 'e_shop/update-user.html'


    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)



        # TODO: Realizar la lógica de actualización de los datos de usuario.

class UserView(TemplateView):
    '''
    Vista con el detalle de los datos personales del usuario
    '''

    template_name = 'e_shop/user.html'

    # Preparamos en nuestro contexto la lista de articulos del usuario registrado.
    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)



def gracias_compra(request):
    '''
    Incluye la lógica de guardar lo pedido en la base de datos
    y devuelve el detalle de lo adquirido
    '''

    if request.method == 'POST':

    # Obtenemos los datos del request:
        username = request.POST.get('username')
        art_id = request.POST.get('art_id')
        nombre = request.POST.get('nombre')
        precio = request.POST.get('precio')
        color_id = request.POST.get('color_id')
        talle_xs = request.POST.get('talle_xs')
        talle_s = request.POST.get('talle_s')
        talle_m = request.POST.get('talle_m')
        talle_l = request.POST.get('talle_l')
        talle_xl = request.POST.get('talle_xl')
        user_authenticated = request.POST.get('user_authenticated')
        type_button = request.POST.get('type_button')
        actual_value = request.POST.get('actual_value')
        path = request.POST.get('path')

        # Obtener valores:
        print(f'Username:{username}')
        print(f'art_id:{art_id}')
        print(f'Nombre:{nombre}')
        print(f'Precio:{precio}')
        print(f'Color:{color_id}')
        print(f'Talle xs:{talle_xs}')
        print(f'Talle s:{talle_s}')
        print(f'Talle l:{talle_l}')
        print(f'Talle xl:{talle_xl}')


        # Validamos los datos y les damos formato:
        username = username if username != '' else None
        art_id = art_id if art_id != '' else None
        nombre = nombre if nombre != '' else None
        color_id = color_id if color_id != '' else None
        talle_xs = talle_xs if talle_xs != '' else None
        talle_s = talle_s if talle_s != '' else None
        talle_m = talle_m if talle_m != '' else None
        talle_l = talle_l if talle_l != '' else None
        talle_xl = talle_xl if talle_xl != '' else None
        user_authenticated = True if user_authenticated == 'True' else False
        type_button = type_button if type_button != '' else None
        actual_value = True if actual_value == 'True' else False
        path = path if path != None else 'index'

        user_obj = User.objects.get(username=username)
        art_obj = Articulo.objects.get(art_id=art_id)
        wish_obj = WishList.objects.filter(user_id=user_obj, art_id=art_obj).first()

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

        return redirect(path)
    else:
        return redirect('index')


# ------------------------------- NOTE: Categorias --------------------------

class CamisasView(ListView):

    queryset = Articulo.objects.filter(categoria_id=7)

    # Esta Api nos devuelve una lista de articulos por categorias

    template_name = 'e_shop/camisas.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class PantalonesView(ListView):

    queryset = Articulo.objects.filter(categoria_id=12)

    # Esta Api nos devuelve una lista de articulos por categorias

    template_name = 'e_shop/pantalones.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
class RemerasView(ListView):

    queryset = Articulo.objects.filter(categoria_id=8)

    # Esta Api nos devuelve una lista de articulos por categorias

    template_name = 'e_shop/remeras.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context
class VestidosView(ListView):

    queryset = Articulo.objects.filter(categoria_id=10)

    # Esta Api nos devuelve una lista de articulos por categorias

    template_name = 'e_shop/vestidos.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class CamperasView(ListView):

    queryset = Articulo.objects.filter(categoria_id=9)

    # Esta Api nos devuelve una lista de articulos por categorias

    template_name = 'e_shop/camperas.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

class JeansView(ListView):

    queryset = Articulo.objects.filter(categoria_id=11)

    # Esta Api nos devuelve una lista de articulos por categorias

    template_name = 'e_shop/jeans.html'
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context

# NOTE: Vistas con Bootstrap:

class BootstrapLoginUserView(TemplateView):

   # Vista para Template de login con estilo de bootstrap.

    template_name = 'e_shop/bootstrap-login.html'

class BootstrapSignupView(TemplateView):

    # Vista para Template de registro de usuario con estilo de bootstrap.

    template_name = 'e_shop/bootstrap-signup.html'
