from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView

app_name = 'api'

urlpatterns = [
    path('/', include('djoser.urls')),
    path('/', include('djoser.urls.jwt')),
    path('token/', TokenObtainPairView.as_view(), name='token')
]
