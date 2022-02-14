#from django.shortcuts import render - No vamos a mostrar nada renderizado
#Traemos las librerias que se utilizar para mostrar las APIS
from rest_framework.views import APIView
from rest_framework.response import Response
#Esta libreria tiene varias opciones para http, y filters es para filtrar los datos
from rest_framework import status, filters
#Importamos para uso de viewsets que e usan para apis simples y manejo sencillo de base de datos
from rest_framework import viewsets
#Importa TokenAuthentication para autenticacion de usuario que es el que se utilizará en el API
from rest_framework.authentication import TokenAuthentication

#Obtención de los tokens de autenticación
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

#Importamos serializador de nuestra aplicacion que creamos en profiles_api\serializers.py y tambien los modelos de models.py y los permisos con permissions.py
from profiles_api import serializers, models, permissions

from rest_framework.permissions import IsAuthenticatedOrReadOnly



# Create your views here.
class HelloAPIView(APIView):
    #API View de prueba
    #permite tener el serializer_class que tenemos en serializers.py llamado HelloSerializer
    serializer_class = serializers.HelloSerializer

    def get(self, request, format=None):
    #Retornar lista de caracteristicas del API View
        an_apiview = [
            'Usa metodos HTTP como funciones (get, post, patch, put, delete)',
            'Es similar a una vista tradicional Django',
            'Nos da el mayor control sobre la logica de la aplicacion',
            'Es una buena practica para mantener la aplicacion limpia y ordenada',
            'Esta mapeado manualmente a los URL'
        ]
        #Para convertir algo a formato json tiene que ser una lista o un diccionario
        #Siempre retornar una respuesta response en caso de ser (get, post, patch, put, delete)
        return Response({'message': 'Hello APIView!', 'an_apiview': an_apiview})

    #Crea un mensaje con nuestro nombre y lo retorna
    def post(self, request):
        #Obtiene los datos con un serializador
        serializer = self.serializer_class(data=request.data)
        #Verifica si los datos son validos
        if serializer.is_valid():
            #Obtiene el nombre del serializador
            name = serializer.validated_data.get('name')
            #Crea el mensaje
            message = f'Hello {name}'
            #Retorna el mensaje con reponse
            return Response({'message': message})
        else:
            #En caso de que la información no sea valida retorna una respuesta con el error
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def put(self, request, pk=None):
        #Maneja actualizar un ojeto, se usa pk = none para que no nos pida un id
        return Response({'method': 'PUT'})
    
    def patch(self, request, pk=None):
        #Maneja actualización parcial de un ojeto, se usa pk = none para que no nos pida un id
        return Response({'method': 'PATCH'})
    
    def delete(self, request, pk=None):
        #Maneja eliminación de un ojeto, se usa pk = none para que no nos pida un id
        return Response({'method': 'DELETE'})

class HelloViewSet(viewsets.ViewSet):
    #Es clase se dio de alta también en urls.py usando routers
    #Test API de view set
    #permite tener el serializer_class que tenemos en serializers.py llamado HelloSerializer
    serializer_class = serializers.HelloSerializer

    def list(self, request):
        #Retorna lista de caracteristicas del API ViewSet
        a_viewset = [
            'Usa actions (list, create, retrieve, update, partial_update)',
            'Automaticamente mapea los URL a las routres',
            'Provee una mayor funcionalidad con menos codigo',
        ]
        return Response({'message': 'Hello ViewSet!', 'a_viewset': a_viewset})

    def create(self, request):
        #Creación de nuevo mensaje de hola mundo
        #Obtiene los datos con un serializador
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            #Obtiene el nombre del serializador
            name = serializer.validated_data.get('name')
            #Crea el mensaje
            message = f'Hello {name}!'
            #Retorna el mensaje con reponse
            return Response({'message': message})
        else:
            #En caso de que la información no sea valida retorna una respuesta con el error
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self, request, pk=None):
        #Obtiene un objeto y su respectivo ID
        return Response({'http_method': 'GET'})
    
    def update(self, request, pk=None):
        #actualiza un objeto
        return Response({'http_method': 'PUT'})
    
    def partial_update(self, request, pk=None):
        #actualiza un objeto parcialmente
        return Response({'http_method': 'PATCH'})
    
    def destroy(self, request, pk=None):
        #elimina un objeto
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    #Clase para manejar el modelo de UserProfile usando ModelViewSet que es casi igual a ViewSet pero para modelos creados en models.py
    #Obtiene los datos con un serializador
    serializer_class = serializers.UserProfileSerializer
    #Manda todos los usuarios registrados
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    #Utilizamos los permisos creadon en permissions.py
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)#Se agregan comas al final porque son tuplas
    search_fields = ('name', 'email',)

class UserLoginApiView(ObtainAuthToken):
    #Creación de tokens de autentificación del usuario
    #Se tiene que agrear a los URL de urls.py
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    #Clase para manejar crear, leer, actualizar y eliminar los profile feeds del usuario
    #Mandamos llamar la autentificación.
    authentication_classes = (TokenAuthentication,)
    #Obtiene los datos con un serializador creado para ProfileFeedItem
    serializer_class = serializers.ProfileFeedItemSerializer
    #Obtiene los datos con un queryset desde el modelo ProfileFeedItem
    queryset = models.ProfileFeedItem.objects.all()
    permissions_classes = (permissions.UpdateOwnStatus, IsAuthenticatedOrReadOnly)

    def perform_create(self, serializer):
        #Setear el perfil de ususario para el ususario que esta logueado
        serializer.save(user_profile=self.request.user)
