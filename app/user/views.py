"""
Vista de los usuarios de la API
"""

from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer
)

class CreateUserView(generics.CreateAPIView):
    'Crear nuevo usuario en el sistema'
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    'Crear una nueva autentificación del token del usuario'
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    'Administrar la autenticación de los usuarios'
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        'Recupera y devuelve la autenticación del usuario'
        return self.request.user


