from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import GetUsersViewSet, GetPatchDeteleUserView
from .views import GenreViewSet, CategoryViewSet
from .views import TitleViewSet
from .views import GetCreateReviewViewSet, GetPatchDeleteReviewViewSet
from .views import GetCreateCommentViewSet, GetPatchDeleteCommentViewSet


router_v1 = DefaultRouter()
router_v1.register('users', GetUsersViewSet, basename='users')
router_v1.register(
    r'^users/(?P<username>[\w.@+-]+)/$',
    GetPatchDeteleUserView, basename='user')
router_v1.register('genres', GenreViewSet, basename='genres')
router_v1.register('categories', CategoryViewSet, basename='categories')
router_v1.register('titles', TitleViewSet, basename='titles')
router_v1.register(
    r'titles/(?P<title_id>\d+)/review', GetCreateReviewViewSet,
    basename='review')
router_v1.register(
    r'titles/(?P<title_id>\d+)/review/(?P<review_id>\d+)/',
    GetPatchDeleteReviewViewSet, basename='review_detail')
router_v1.register(
    r'titles/(?P<title_id>\d+)/review/(?P<review_id>\d+)/com',
    GetCreateCommentViewSet, basename='comment')
router_v1.register(
    r'titles/(?P<title_id>\d+)/review/(?P<review_id>\d+)/com/(?P<com_id>\d+)/',
    GetPatchDeleteCommentViewSet, basename='comment_detail')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include('api.inner', namespace='api')),
]
