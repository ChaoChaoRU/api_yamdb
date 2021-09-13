from django.contrib import admin
from django.contrib.auth import get_user_model
from rest_framework import filters, viewsets
from django_filters.rest_framework import DjangoFilterBackend
# from django.db.models import Avg
from rest_framework.pagination import PageNumberPagination
from reviews.models import Genre, Category, Title
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser, AllowAny

from .filter import TitleFilter
from .serializers import GenreSerializer, TitleReadSerializer
from .serializers import CategorySerializer, TitleWriteSerializer
from .serializers import GetUsersSerializer, CreateUserSerializer
from .serializers import GetPatchDeteleUserSerializer
from .pagination import CustomPagination
from reviews.models import CustomerUser, Genre, Category, Title
from reviews.models import Review, Comment
from .permissions import AuthorOrReadOnly, ModeratorOrReadOnly
from .permissions import AdminOrReadOnly, SuperUserOrReadOnly
from .permissions import IsAdminOrReadOnly

user = get_user_model()
moderator = get_user_model()
admin = get_user_model()


class GetUsersViewSet(ListModelMixin, GenericViewSet):
    queryset = CustomerUser.objects.all()
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
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly, )
    pagination_class = CustomPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = (AdminOrReadOnly,)
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


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
