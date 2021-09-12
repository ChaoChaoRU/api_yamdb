from django.contrib.auth import get_user_model
from django.db.models import AVG
from rest_framework import viewsets, mixins, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from reviews.models import Genre, Category, Title

from .filter import TitleFilter
from .serializers import GenreSerializer, TitleReadSerializer,
from .serializers import CategorySerializer, TitleWriteSerializer
from .pagination import CustomPagination
from reviews.models import CustomUser, Genre, Category, Title
from reviews.models import Review, Comment
from .permissions import AuthorOrReadOnly, ModeratorOrReadOnly
from .permissions import SuperUserOrReadOnly

User = get_user_model()


class GetUsersViewSet(ListModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = GetUsersSerializer
    permission_classes = (IsAdminUser,)
    pagination_class = CustomPagination


class CreateUserViewSet(CreateModelMixin):
    serializer_class = CreateUserSerializer
    permission_classes = (IsAdminUser,)


class GetPatchDeteleUserViewSet(RetrieveModelMixin, UpdateModelMixin,
                                DestroyModelMixin, GenericViewSet):
    pass


class GetPatchDeteleUserView(LoginRequiredMixin, GetPatchDeteleUserViewSet):
    serializer_class = GetPatchDeteleUserSerializer
    permission_classes = (IsAdminUser,)
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
    queryset = Title.objects.annotate(
        rating=AVG('reviews__score')).order_by('-id'))
    pagination_class = PageNumberPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer


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
