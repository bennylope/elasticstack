import json

from optparse import make_option

from django.core.management.base import BaseCommand
from django.db.models import get_model

from ...utils import prepare_object


class Command(BaseCommand):

    help = "Prints the indexing document generated for a model object." \
            "\nUse dotted path name for model and the primary key."

    option_list = BaseCommand.option_list + (
        make_option('--using',
            action='store',
            dest='using',
            default='default',
            help='The Haystack backend to use'),
        )

    def handle(self, *args, **options):
        try:
            label, pk = args
        except IndexError:
            self.stderr.write("Provide the model name and primary key")
        app_label, model_name = label.split('.')
        model = get_model(app_label, model_name)
        obj = model.objects.get(pk=pk)
        doc_json = prepare_object(obj, options.get('using'))
        self.stdout.write(json.dumps(doc_json, indent=4))
