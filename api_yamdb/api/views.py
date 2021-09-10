from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from reviews.models import Genre, Category, Title
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser, AllowAny

from .filter import TitleFilter
from .serializers import GetUsersSerializer, CreateUserSerializer
from .serializers import GetPatchDeteleUserSerializer
from .serializers import GenreSerializer, TitleSerializer, CategorySerializer
from .pagination import CustomPagination
from reviews.models import CustomUser, Genre, Category, Title
from reviews.models import Review, Comment
from .permissions import AuthorOrReadOnly, ModeratorOrReadOnly
from .permissions import AdminOrReadOnly, SuperUserOrReadOnly

user = get_user_model()
moderator = get_user_model()
admin = get_user_model()


class GetUsersViewSet(ListModelMixin, GenericViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GetUsersSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = CustomPagination


class CreateUserViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class GetCreateViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    pass


class GetPatchDeteleViewSet(RetrieveModelMixin, UpdateModelMixin,
                            DestroyModelMixin, GenericViewSet):
    pass


class GetPatchDeteleUserView(GetPatchDeteleViewSet):
    serializer_class = GetPatchDeteleUserSerializer
    permission_classes = (IsAdminUser,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]


class CustomViewSet(CreateModelMixin, DestroyModelMixin,
                    ListModelMixin, GenericViewSet):
    pass


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializers_class = GenreSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class GetCreateTitleViewSet(GetCreateViewSet):
    queryset = Title.objects.all()
    serializers_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class GetPatchDeleteTitleViewSet(GetPatchDeteleViewSet):
    queryset = Title.objects.all()
    serializers_class = TitleSerializer
    permission_classes = (AdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter


class GetCreateReviewViewSet(GetCreateViewSet):
    queryset = Review.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GetPatchDeleteReviewViewSet(GetPatchDeteleViewSet):
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.user.is_superuser is True:
            return (SuperUserOrReadOnly(),)
        elif self.user.is_staff is False:
            return (AuthorOrReadOnly(), ModeratorOrReadOnly())
        else:
            return (IsAdminUser)


class GetCreateCommentViewSet(GetCreateViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class GetPatchDeleteCommentViewSet(GetPatchDeteleViewSet):
    queryset = Comment.objects.all()

    def get_permissions(self, request):
        if self.user.is_superuser is True:
            return (SuperUserOrReadOnly(),)
        elif request.user.role is admin:
            return (AdminOrReadOnly(),)
        elif request.user.role is moderator:
            return (ModeratorOrReadOnly(),)
        elif request.user.role is user:
            return (AuthorOrReadOnly(),)
        else:
            return (IsAuthenticatedOrReadOnly,)
