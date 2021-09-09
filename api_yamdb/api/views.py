from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from reviews.models import Genre, Category, Title
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.mixins import RetrieveModelMixin, UpdateModelMixin
from rest_framework.mixins import DestroyModelMixin
from rest_framework.viewsets import GenericViewSet
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAdminUser

from .filter import TitleFilter
from .serializers import GetUsersSerializer, CreateUserSerializer
from .serializers import GetPatchDeteleUserSerializer
from .serializers import GenreSerializer, TitleSerializer, CategorySerializer
from .pagination import CustomPagination
from reviews.models import CustomUser, Genre, Category, Title

User = get_user_model()


class GetUsersViewSet(LoginRequiredMixin, ListModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = GetUsersSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = CustomPagination
    login_url = 'api/v1/auth/token/'
    redirect_field_name = 'redirect_to'


class CreateUserViewSet(LoginRequiredMixin, CreateModelMixin):
    serializer_class = CreateUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser,)
    login_url = 'api/v1/auth/token/'
    redirect_field_name = 'redirect_to'


class GetPatchDeteleUserViewSet(RetrieveModelMixin, UpdateModelMixin,
                                DestroyModelMixin, GenericViewSet):
    pass


class GetPatchDeteleUserView(LoginRequiredMixin, GetPatchDeteleUserViewSet):
    serializer_class = GetPatchDeteleUserSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
    login_url = 'api/v1/auth/token/'
    redirect_field_name = 'redirect_to'


class CustomViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializers_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializers_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser,)
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
