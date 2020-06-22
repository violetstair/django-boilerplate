from django.urls import path

from .views import (
    CreateAPIView,
    DetailViewAPI,
)

urlpatterns = [
    path('', CreateAPIView.as_view(), name='가입'),
    path('detail/<str:pk>/', DetailViewAPI.as_view(), name='계정 정보'),
]
