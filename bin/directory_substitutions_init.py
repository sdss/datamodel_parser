#!/usr/bin/env python3
from datamodel_parser.application import Argument
from datamodel_parser.application import Store

from json import dumps

print('Creating yaml file with directory substitutions')
arg = Argument('filespec_init')
options = arg.options if arg else None
store = Store(options=options) if options else None
logger = store.logger if store else None
ready = options and store and logger
ready = ready and store.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
    exit(1)
else:
    store.init_directory_substitutions_yaml()
    store.exit()



