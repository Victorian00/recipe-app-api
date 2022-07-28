"""
Tests para confirmar la salud y que funciona todo bien de la API
"""

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient


class HealthCheckTests(TestCase):
    'Test para comprobar el buen funcionamiento de la API'

    def test_health_check(self):
        'Lo mismo que arriba, que me da pereza'
        client = APIClient()
        url = reverse('health-check')
        res = client.get(url)

        self.assertEqual(res.status_code, status.HTTP_200_OK)