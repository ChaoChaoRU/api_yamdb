from django.contrib.auth import get_user_model
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from reviews.models import Genre, Category, Title

from .filter import TitleFilter
from .serializers import GenreSerializer, TitleSerializer, CategorySerializer
<<<<<<< HEAD
=======
from .pagination import CustomPagination
from reviews.models import CustomUser, Genre, Category, Title
from reviews.models import Review, Comment
from .permissions import AuthorOrReadOnly, ModeratorOrReadOnly
from .permissions import SuperUserOrReadOnly
>>>>>>> 06a932da9ce882b8a33693fe57636f25d3127861

User = get_user_model()


class CustomViewSet(mixins.CreateModelMixin, mixins.DestroyModelMixin,
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


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.user.is_superuser is True:
            return (SuperUserOrReadOnly(),)
        elif self.user.is_staff is False:
            return (AuthorOrReadOnly(), ModeratorOrReadOnly())
        else:
            return (IsAdminUser)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminUser,)
