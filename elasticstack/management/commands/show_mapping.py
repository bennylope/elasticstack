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
