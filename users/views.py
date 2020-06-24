from rest_framework import generics, mixins
from rest_framework.permissions import (
    AllowAny,
)

from .serializers import (
    UserCreateSerializer,
    UserSerializer,
)
from .models import (
    User,
)
from .permissions import (
    IsOwner,
)


class CreateAPIView(generics.GenericAPIView, mixins.CreateModelMixin):
    permission_classes = (AllowAny, )
    serializer_class = UserCreateSerializer

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class DetailViewAPI(generics.GenericAPIView, mixins.RetrieveModelMixin):
    permission_classes = (IsOwner,)

    serializer_class = UserSerializer

    def get_queryset(self):
        return User.get_user(self.kwargs['pk'])

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
