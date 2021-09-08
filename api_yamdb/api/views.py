from api_yamdb.reviews.models import CustomerUser
from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins
from rest_framework.pagination import PageNumberPagination
from reviews.models import Genre, Category, Title
from .serializers import GenreSerializer, TitleSerializer, CategorySerializer

User = get_user_model()

class CustomViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin
                    mixins.ListModelMixin, viewsets.GenericViewSet):
    pass


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializers_class = GenreSerializer
    pagination_class = PageNumberPagination

class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializers_class = CategorySerializer
    pagination_class = PageNumberPagination

class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializers_class = TitleSerializer
    pagination_class = PageNumberPagination 
