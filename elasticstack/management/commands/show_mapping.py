import json

from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from haystack import connections


class Command(BaseCommand):

    help = "Prints the search mapping for specififed connections." \
        "\nDefaults to all connections in settings."

    option_list = BaseCommand.option_list + (
            make_option('--detail', action='store_true', dest='detail', default=False,
            help='Display mapping details, including analyzers and boost levels.'),)

    def handle(self, *args, **options):
        backends = args if args else settings.HAYSTACK_CONNECTIONS.keys()
        for backend in backends:
            engine = connections[backend].get_backend()
            unified_index = connections[backend].get_unified_index()
            content_field_name, field_mapping = engine.build_schema(unified_index.all_searchfields())
            engine.setup()

            if options.get('detail'):
                mapping = field_mapping
            else:
                mapping = engine.existing_mapping

            self.stdout.write("{0}\n{1}\n".format(backend, "-" * len(backend)))
            self.stdout.write(json.dumps(mapping, indent=4))
