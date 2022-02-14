#Se agrega a admin por cada modelo que se se quiere administrar desde el panel administrador
from django.contrib import admin
#Importamos nuestros modelos que queremos administrar
from profiles_api import models

# Register your models here.
#Se le da acceso al administrador para que pueda editar estos modelos desde la página de administración
admin.site.register(models.UserProfile)
admin.site.register(models.ProfileFeedItem)