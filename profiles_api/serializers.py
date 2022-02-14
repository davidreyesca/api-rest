#Se crea un seriaizador por cada modelo
#Archivo con todos los serializadores de nuestra aplicacion
#Un serializable es una clase que se puede convertir en un diccionario o lista en json o viceversa
#Los campos Relaciones de serialización se utilizan para representar relaciones modelo. Se pueden aplicar a relaciones ForeignKey , ManyToManyField y OneToOneField , 
    #así como a relaciones inversas y relaciones personalizadas como GenericForeignKey .
from rest_framework import serializers
#Importamos el modelo de nuestra aplicación
from profiles_api import models

class HelloSerializer(serializers.Serializer):
    #Serializa un campo para probar nuestro API View
    name = serializers.CharField(max_length=10)

#Se serializa el modelo por eso se hereda ModelSerializer en la clase
class UserProfileSerializer(serializers.ModelSerializer):
    #Serializa el un perfil de usuario desde nuestro modelo ususario
    class Meta:
        model = models.UserProfile
        #Que campos se serializan, usualmente son todos los campos del modelo
        fields = ('id', 'email', 'name', 'password')
        #Que campos se ocultan
        extra_kwargs = {
            #Oculta el campo password solo se muestra cuando se crea un nuevo usuario
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }

    #Se sobreescribe el metodo create para que no se pueda crear un usuario sin contraseña
    def create(self, validated_data):
        #Crea un usuario con contraseña
        user = models.UserProfile.objects.create_user(
            #validación de datos
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user
    
    def update(self, instance, validated_data):
        #Actualiza un usuario
        if 'password' in validated_data:
            #Si el campo password esta en el diccionario de datos
            password = validated_data.pop('password')
            #Se remueve el campo password del diccionario de datos
            instance.set_password(password)
        #Actualiza los datos del usuario
        return super().update(instance, validated_data)

class ProfileFeedItemSerializer(serializers.ModelSerializer):
    #Serializador de profile feed item
    class Meta:
        #Configuramos el serializador para que trabaje con el modelo ProfileFeedItem
        model = models.ProfileFeedItem
        #Que campos se serializan, usualmente son todos los campos del modelo
        fields = ('id', 'user_profile', 'status_text', 'created_on')
        #Que campos se ocultan
        extra_kwargs = {
            #Oculta el campo password solo se muestra cuando se crea un nuevo usuario
            'user_profile': {
                'read_only': True,
            }
        }