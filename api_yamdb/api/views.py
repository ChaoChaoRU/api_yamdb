from api_yamdb.reviews.models import CustomerUser
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from reviews.models import Genre, Category, Title

from .filter import TitleFilter
from .serializers import GenreSerializer, TitleSerializer, CategorySerializer

User = get_user_model()

class CustomViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializers_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', ]
    lookup_field = 'slug'

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializers_class = TitleSerializer
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter
