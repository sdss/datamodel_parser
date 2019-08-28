#!/usr/bin/env python3
from datamodel_parser.application import Argument
from datamodel_parser.application import Store

from json import dumps

print('Populating filespec table.')
arg = Argument('filespec_db')
options = arg.options if arg else None
store = Store(options=options) if options else None
store.set_database()
logger = store.logger if store else None
ready = options and store and logger
ready = ready and store.ready and store.database and store.database.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
    exit(1)
else:
    store.set_tree_edition()
    store.set_filepaths()
    store.set_yaml_dir()
    store.set_yaml_data(dir=store.yaml_dir,filename='filespec.yaml')
    store.filespec_dict_yaml = store.yaml_data
    store.populate_filespec_table_yaml()
    store.exit()

