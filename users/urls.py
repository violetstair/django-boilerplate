from django.urls import path

from rest_framework_simplejwt import views as jwt_views

from .views import (
    CreateAPIView,
    DetailViewAPI,
)

urlpatterns = [
    path(r'', CreateAPIView.as_view(), name='가입'),
    path(r'signin/', jwt_views.TokenObtainPairView.as_view(), name='signin'),
    path(r'refresh/', jwt_views.TokenRefreshView.as_view(), name='refresh'),
    path(r'<str:pk>/', DetailViewAPI.as_view(), name='계정 정보'),
]
