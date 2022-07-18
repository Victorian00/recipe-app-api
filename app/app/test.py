"""
Test de ejemplo
"""
from django.test import SimpleTestCase

from app import calculos

class CalcTest(SimpleTestCase):
    "Probamos lo de calcular a ver si es verdad."

    
    def test_add_numbers(self):
        "Se suman dos números."
        suma = calculos.add(4,5)

        self.assertEqual(suma, 9)
    

    def test_subtract_numbers(self):
        "Se restan dos números."
        resta = calculos.subtract (8,3)

        self.assertEqual(resta, 5)