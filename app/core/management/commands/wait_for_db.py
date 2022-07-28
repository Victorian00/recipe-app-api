"""
Comando para que Django espere al database, que va lentico el pobre, para que funcione bien
"""

import time

from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    'Comando de Django para la espera'

    def handle(self, *args, **options):
        'Entrada de los comandos'
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2OpError, OperationalError):
                self.stdout.write('Database unavailable, waiting...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available!'))