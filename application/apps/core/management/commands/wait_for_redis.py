from time import sleep
from redis import Redis
from redis.exceptions import ConnectionError, BusyLoadingError
from django.conf import settings
from django.core.management import BaseCommand


class Command(BaseCommand):
    """
    Django command to pause execution until redis is available ...
    """

    def handle(self, *args, **options):
        self.stdout.write('Waiting for redis ...')

        if not settings.DEBUG:
            redis_connection = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

            while True:
                try:
                    redis_connection.client_list()
                except (ConnectionError, BusyLoadingError):
                    self.stdout.write('Redis unavailable, Retrying ...')
                    sleep(1)
                else:
                    break

            self.stdout.write(self.style.SUCCESS('Redis available'))
        self.stdout.write(self.style.MIGRATE_HEADING('Redis availability passed because debug mode is True'))
