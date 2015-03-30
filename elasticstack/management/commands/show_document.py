# Copyright (c) 2014-2015, Ben Lopatin
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.  Redistributions in binary
# form must reproduce the above copyright notice, this list of conditions and the
# following disclaimer in the documentation and/or other materials provided with
# the distribution

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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
            help='The Haystack backend to use'),)

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
