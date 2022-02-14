#Se crea un modelo por cada tabla en la base de datos
from unicodedata import name
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import BaseUserManager
#Importamos los settings para pque tenemos para el proyecto
from django.conf import settings

#Manager para perfiles de usuario
class UserProfileManager(BaseUserManager):
    #Crea un nuevo perfil usuario
    def create_user(self, email, name, password=None):
        if not email:
            raise ValueError('El email debe ser obligatorio')
        #Obtiene el email y lo normaliza
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    #Crea un nuevo perfil de super usuario
    def create_superuser(self, email, name, password):
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user

# Create your models here.
#ESTE MODELO SE PUSO DENTRO DE SETTINGS.PY PARA SU USO
#ESTO MODELO SE PUSO DENTRO DE ADMIN.PY PARA PODERLO ADMINISTRAR DESDE SUPERADMIN
#Modelo base de datos para usuarios del sistema
class UserProfile(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    #Se utiliza un modelo de django personalizado
    objects = UserProfileManager()
    #Lo principal para iniciar seria email
    USERNAME_FIELD = 'email'
    #Campos requeridos
    REQUIRED_FIELDS = ['name']

    #Para llamar el nombre como string
    def get_full_name(self):
        return self.name

    #Para llamar el nombre corto del usuario como string
    def get_short_name(self):
        return self.name
    
    def __str__(self):
        #Retornar cadena representando el usuario
        return self.email

#Creación de la clase para el modelo del perfil de ususario
class ProfileFeedItem(models.Model):
    #Relacion con el usuario usando llave foranea, se utiliza el modelo de UserProfile usado en settings.py
    user_profile = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    #Contenido del post
    status_text = models.CharField(max_length=255)
    #Fecha de creación
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        #Retornar cadena representando el post
        return self.status_text