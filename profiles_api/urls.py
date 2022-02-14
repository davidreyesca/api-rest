#Este archivo se creo manualmente para también tener un archivo de URL de la aplicación
from django.db import router
from django.urls import path, include
#Importamos los views (controladores) de la aplicacion profiles_api
from profiles_api import views
#Para el uso de ViewSet es necesario usar routers, es por eso que importamos la libreria
from rest_framework.routers import DefaultRouter

#Crea un router para el viewset
router = DefaultRouter()
#Agrega el viewset de profiles_api al reouter creado
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet)#No es necesario el basename porque estamos mandando llamar con all a todos los objetos
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [    
    path('hello-view/', views.HelloAPIView.as_view()),#views.HelloAPIView no se puede ver una clase así que se agrega as_view() al final para cargarlo como función
    path('login/', views.UserLoginApiView.as_view()),#views.UserProfileViewSet no se puede ver una clase así que se agrega as_view() al final para cargarlo como función
    path('', include(router.urls)),
]