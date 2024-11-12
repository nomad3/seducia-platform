# main_app/permissions.py

from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Permiso personalizado para permitir que solo los propietarios de un objeto lo editen.
    """
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user

class IsCoach(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un coach.
    """
    def has_permission(self, request, view):
        return request.user.userprofile.is_coach

class IsProvider(permissions.BasePermission):
    """
    Permiso personalizado para verificar si el usuario es un proveedor (coach o escort).
    """
    def has_permission(self, request, view):
        return request.user.userprofile.role in [UserRole.COACH, UserRole.ESCORT]