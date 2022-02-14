from django.contrib import admin
#Se agrega el include abajo para que se pueda acceder a los modelos de la aplicacion con el archivo urls.py de la aplicación
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    #Cuando se entra a domino.com/api/ se va a profiles_api/urls.py por el include
    path('api/', include('profiles_api.urls')),
]
