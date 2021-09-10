from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user)


class ModeratorOrReadOnly(permissions.BasePermission):
    # obj.author != request.user  ВОТ ОН И ЕСТЬ МОДЕРАТОР ЭТО ТОТ КТО НЕ АВТОР.
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author != request.user)


class AdminOrReadOnly(permissions.BasePermission):
    # Custom Admin.
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff)


class SuperUserOrReadOnly(permissions.BasePermission):
    # юзер является суерюзером.

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)
