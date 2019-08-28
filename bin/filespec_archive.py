#!/usr/bin/env python3
from datamodel_parser.application import Argument
from datamodel_parser.application import Store
from sdssdb.sqlalchemy.archive.sas import *

from json import dumps

import time

print('Populating filespec table.')
arg = Argument('filespec_archive')
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
    store.populate_filespec_table_archive()
    store.exit()

'''
Examples:

filespec_archive.py -l debug -v -t -p MANGA_SPECTRO_ANALYSIS/DRPVER/DAPVER/dapall.html -o manga/spectro/analysis/v2_4_3/2.2.1
'''
