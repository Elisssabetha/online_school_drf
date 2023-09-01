from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(ModelViewSet):
    """Viewset for User model. To create need to enter 'email' and 'password' """
    serializer_class = UserSerializer
    queryset = User.objects.all()
