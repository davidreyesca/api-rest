from rest_framework import permissions

class UpdateOwnProfile(permissions.BasePermission):
    #Permite que el usuario pueda editar su propio perfil

    def has_object_permission(self, request, view, obj):
        # Si el ususario intenta editar su propio perfil, se verifica que el usuario tenga permiso para hacerlo

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.id == request.user.id

class UpdateOwnStatus(permissions.BasePermission):
    #Permite que el usuario pueda actualizar su propio status feed

    def has_object_permission(self, request, view, obj):
        # Si el ususario intenta editar su propio perfil, se verifica que el usuario tenga permiso para hacerlo

        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user_profile.id == request.user.id