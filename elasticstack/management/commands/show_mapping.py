import json

from django.conf import settings
from django.core.management.base import BaseCommand

from haystack import connections


class Command(BaseCommand):

    help = "Prints the search mapping for specififed connections." \
        "\nDefaults to all connections in settings."

    def handle(self, *args, **options):
        backends = args if args else settings.HAYSTACK_CONNECTIONS.keys()
        for backend in backends:
            engine = connections[backend].get_backend()
            engine.setup()
            self.stdout.write("{0}\n{1}\n".format(backend, "-" * len(backend)))
            self.stdout.write(json.dumps(engine.existing_mapping, indent=4))
