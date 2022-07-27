"""
Testeo para los usuarios de la API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


def create_user(**params):
    'Crear y devolver nuevo usuario'
    return get_user_model().objects.create_user(**params)



class PublicUserApiTest(TestCase):
    'Testear las características públicas de los usuarios de la API'

    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        'Test para comprobar que el usuario se ha creado satisfactoriamente'
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_with_email_exists_error(self):
        'Testeo para que te devuelva un error si ya hay un email igual'
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_password_too_short_error(self):
        'Testeo de error si metes una contraseña más pequeña que tu pito (5 caracteres)'
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_users(self):
        'Testeo de generar tokens para validar las credenciales del usuario'
        user_details = {
            'name': 'Test Name',
            'email': 'test@example.com',
            'password': 'test-user-password123',
        }
        create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        'Testeo de devolver error si le introduces credenciales incorrectas'
        create_user(email='test@example.com', password='goodpass')

        payload = {'email': 'test@example.com', 'password': 'badpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_email_not_found(self):
        """Test error returned if user not found for given email."""
        payload = {'email': 'test@example.com', 'password': 'pass123'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_blank_password(self):
        'Testeo para cuando dejas la contraseña en blanco te da error'
        payload = {'email': 'test@example.com', 'password': ''}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_retirve_user_unauthorized(self):
        'Testeo de que la autenticación es requerida para los usuarios'
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    'Testeo de la solicitud de la API de pedir autenticación'

    def setUp(self):
        self.user = create_user(
            email = 'test@example.com',
            password = 'testpass123',
            name = 'Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retirve_profile_success(self):
        'Testeo de la recuperación de perfiles tras la conexión de los usuarios'
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        'Testeo de postear que el usuario no está permitido'
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        'Testeo de actualizar el perfil del usuario para la autenticación del usuario'
        payload = {'name': 'Updated name', 'password': 'newpass123'}

        res = self.client.patch(ME_URL, payload)

        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)

