"""
Modelo del database
"""

import uuid
import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,   # POR EL AMOR DE DIOS, NI SE TE OCURRA PONERLE UNA R AL FINAL, PODRÍAS DESINTEGRAR EL UNIVERSO CONOCIDO Y ACABAR CON TODA LA VIDA EXISTENTE EN ÉL, DANDO COMO RESULTADO UN LUGAR QUE SERÍA CONOCIDO COMO "LA NADA" Y QUE NI LOS MEJORES CIENTÍFICOS SON CAPACES DE IMAGINAR, UN LUGAR FUERA DE NUESTRO PROPIO ENTENDIMIENTO.
)                       # Es broma, solo no lo pongas porque no funciona, pero me tengo que inventar algo para darle vidilla a esto


def recipe_image_file_path(instance, filename):
    'Generar path del archivo para una nueva imagen de la receta'
    ext = os.path.splitext(filename)[1]
    filename = f'{uuid.uuid4()}{ext}'

    return os.path.join('uploads', 'recipe', filename)


class UserManager(BaseUserManager):
    'Gestor de usuarios'

    def create_user(self, email, password=None, **extra_fields):
        'Crear, guardar y devolver un nuevo usuario'
        if not email:
            raise ValueError('User must have an email address.')
        user=self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        'Crear y devolver un superuser'
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user



class User(AbstractBaseUser, PermissionsMixin):
    'Usuario en el sistema'

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Recipe(models.Model):
    'Objeto receta'
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )
    title = models.CharField(max_length = 255)
    description = models.TextField(blank = True)
    time_minutes = models.IntegerField()
    price = models.DecimalField(max_digits = 5, decimal_places = 2)
    link = models.CharField(max_length = 255, blank = True)
    tags = models.ManyToManyField('Tag')
    ingredients = models.ManyToManyField('Ingredient')
    image = models.ImageField(null=True, upload_to = recipe_image_file_path)


    def __str__(self):
        return self.title


class Tag(models.Model):
    'Tag para filtrar las recetas'
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete = models.CASCADE,
    )

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    'Ingredientes para las recetas'
    name = models.CharField(max_length=255)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name
