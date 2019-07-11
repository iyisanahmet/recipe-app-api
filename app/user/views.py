from rest_framework import generics

from user.serializers import UserSerializer

class CreateUserView(generics.CreateAPIView):
    """Creates a new suser in the system"""
    serializer_class = UserSerializer


