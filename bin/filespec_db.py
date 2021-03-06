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
    store.util.set_yaml_attr(attr_obj=store,
                            attr_name='filespec_dict_yaml',
                            filename='filespec.yaml')
    store.populate_filespec_table_yaml()
    store.exit()

