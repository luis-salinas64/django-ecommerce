
from django.test import TestCase
from e_shop import models
from django.test import Client
from django.contrib.auth.models import User


class MiClaseDePrueba(TestCase):
    '''
    Clase de prueba para hacer Unit Test sobre las entidades de la base de datos.
    '''
    nombre = 'Nombre de prueba'
    categoria_id = 1
    color_id = 1
    talle_xs = 1
    talle_s = 1
    talle_m = 1
    talle_l = 1
    talle_xl = 1
    precio = 2500
    
    def setUp(self):
        '''
        Aquí configuramos las condiciones de la prueba, por lo general insertamos a la DB
        NOTE: Aquí debemos crear los objetos para la base de datos de prueba, 
        de lo contrario, se insertarán en la base de datos del sistema.
        '''

        articulo = models.Articulo.objects.create(
            art_id=1,
            nombre=self.nombre,
            categoria_id=self.categoria_id,
            color_id=self.color_id,
            talle_xs = self.talle_xs,
            talle_s = self.talle_s,
            talle_m = self.talle_m,
            talle_l = self.talle_l,
            talle_xl = self.talle_xl,
            precio = self.precio,
            
        )

    def test_pruebas_de_integridad_de_datos(self):
        '''
        Este método realiza la prueba de integridad de los dato insertados en la base de datos, 
        aprovechando "self.atributo" para verificarlos. 
        '''
        # Llamamos al objeto seteado:

        articulo = models.Articulo.objects.get(art_id=1)
        
        # Extraemos sus atributos:
        nombre = articulo.nombre
        categoria_id = articulo.categoria_id
        color_id = articulo.color_id
        talle_xs = articulo.talle_xs
        talle_s = articulo.talle_s
        talle_m = articulo.talle_m
        talle_l = articulo.talle_l
        talle_xl = articulo.talle_xl
        precio = articulo.precio
        
        # Generamos dos listas para compararlas, una con los datos extraidos del modelo
        # y otra con los datos que fueron insertados en el modelo
        object_values = [nombre,categoria_id,color_id,talle_xs, talle_s, talle_m, talle_l, talle_xl, precio]
        test_values = [self.nombre, self.categoria_id,self.color_id,self.talle_xs,self.talle_s,self.talle_m,
                       self.talle_l, self.talle_xl,self.precio]
        # Comparamos uno a uno los datos:
        for index in range(len(test_values)):
            if object_values[index] != test_values[index]:
                # Si los datos son distintos, hacemos que la prueba de fallida:
                self.assertEqual(object_values[index], test_values[index])
        # Si los datos son iguales, verificamos que las pruebas son exitosas:
        self.assertTrue(True)


class PruebaDeAPIs(TestCase):
    '''
    Test para las APIs del sistema, utilizaremos una DB y un server de prueba.
    '''
    # NOTE: Configuramos los atributos de la clase para utilizarlos en todos los métodos:
    username = 'root'
    password = '12345'
    email = 'algo@algo.com'
    user = None
    comic = None

    # Client() es un objeto que gestiona la conexión con los endpoints, como lo haría un request
    client = Client()

    def setUp(self):
        '''
        Aquí configuramos las condiciones de la prueba, 
        creamos un comic y generamos la conexión al server de prueba
        NOTE: Aquí debemos crear los objetos para la base de datos de prueba, 
        de lo contrario, se insertarán en la base de datos del sistema.
        '''

        # NOTE: Creamos un superusuario para las pruebas:
        self.user = User.objects.create_superuser(self.username, self.email, self.password)
        # Ahora lo autenticamos en el servidor de pruebas:
        self.client.login(username=self.username, password=self.password)

        # Insertamos un comic en la DB de prueba:
        self.comic = models.Comic.objects.create(
            art_id=2,
            nombre='Título de prueba 2',
            categoria_id = 1
            color_id = 1
            talle_xs = 1
            talle_s = 1
            talle_m = 1
            talle_l = 1
            talle_xl = 1
            precio = 2500
        )

    def ssstest_api_comics(self):
        '''
        Test de endpoint: comics/get-post
        Pruebas sobre todos los métodos.
        '''
        # Preparamos los datos:
        endpoint = '/e-commerce/comics/get-post'
        data = {
            'marvel_id': 3,
            'title': 'Título de prueba 3',
            'description': 'Descripción de prueba 3',
            'price': 10.99,
            'stock_qty': 100,
            'picture': 'https://www.inove.com.ar'
        }

        # GET test:
        resp = self.client.get(endpoint)
        self.assertEqual(resp.status_code, 200) 

        # POST test:
        resp = self.client.post(
            endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 201)

        # PUT test:
        resp = self.client.put(endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 405)

        # PATCH test:
        resp = self.client.patch(
            endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 405)

        # DELETE test:
        resp = self.client.delete(
            endpoint, data, content_type="application/json")
        self.assertEqual(resp.status_code, 405)
