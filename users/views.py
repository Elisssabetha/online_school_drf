from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer, UserCreateSerializer
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class UserViewSet(ModelViewSet):
    """Viewset for User model. To create need to enter 'email' and 'password' """
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.create(serializer.validated_data)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
