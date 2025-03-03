from time import sleep
from django.db import connections
from django.db.utils import OperationalError
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Django command to pause execution until db is available ...
    """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for database ...')

        db_connection = False
        while not db_connection:
            try:
                db_connection = connections['default']
            except OperationalError:
                self.stdout.write('Database unavailable, Retrying ...')
                sleep(1)
        self.stdout.write(self.style.SUCCESS('Database available'))
