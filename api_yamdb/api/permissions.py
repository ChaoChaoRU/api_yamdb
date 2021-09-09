from rest_framework import permissions


class AuthorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)


class ModeratorOrReadOnly(permissions.BasePermission):
    # здесь для модератора надо прописать какие методы он может.
    # непонятно что за SAFE_METHODS.
    # obj.author != request.user  ВОТ ОН И ЕСТЬ МОДЕРАТОР ЭТО ТОТ КТО НЕ АВТОР.
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author != request.user)


class SuperUserOrReadOnly(permissions.BasePermission):
    # здесь для супер юзера надо заново всё прописать.

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or obj.author == request.user)
