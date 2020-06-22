from rest_framework import generics, mixins

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from .models import User


class CreateAPIView(mixins.CreateModelMixin, generics.GenericAPIView):

    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DetailViewAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.get_user(self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
