from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    user = 'user'

    def has_permission(self, request, view):
        user = 'user'
        return (request.method in permissions.SAFE_METHODS
                or request.user.role is user)

    def has_object_permission(self, request, view, obj):
        return (obj.author == request.user)


class ModeratorOrReadOnly(permissions.BasePermission):
    # obj.author != request.user  ВОТ ОН И ЕСТЬ МОДЕРАТОР ЭТО ТОТ КТО НЕ АВТОР.
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.user.is_moderator is True)


class AdminOrReadOnly(permissions.BasePermission):
    # Custom Admin.
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        ADMIN = 'admin'
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_admin is ADMIN)


class SuperUserOrReadOnly(permissions.BasePermission):
    # юзер является суерюзером.

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_superuser)


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or (request.user.is_authenticated and (
                    request.user.is_admin or request.user.is_superuser)))