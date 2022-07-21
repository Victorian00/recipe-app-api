"""
Vistas para las recetas de las APIs
"""

from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Recipe
from recipe import serializers


class RecipeViewSet(viewsets.ModelViewSet):
    'Vista para la gestion de las recetas de las APIs'
    serializer_class = serializers.RecipeSerializer
    queryset = Recipe.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        'Recupera las recetas para el usuario autenticado'
        return self.queryset.filter(user=self.request.user).order_by('-id')

    def get_serializer_class(self):
        'Devuelve la clase del resializador para la petición'
        if self.action == 'retrieve':
            return serializers.RecipeDetailSerializer

        return self.serializer_class

    def perform_create(self, serializer):
        'Crear una nueva receta'
        serializer.save(user=self.request.user)
