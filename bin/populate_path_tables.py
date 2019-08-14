#!/usr/bin/env python3
from os import walk
from os.path import join, exists
from datamodel_parser.application import Argument
from datamodel_parser.application import Store

from json import dumps

print('Populating File Path Tables')
arg = Argument('populate_path_tables')
options = arg.options if arg else None
store = Store(options=options) if options else None
logger = store.logger if store else None
ready = options and store and logger
ready = ready and store.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
    exit(1)
else:
    store.set_datamodel_dir()
    store.set_tree_edition()
    store.set_database()
    store.set_file_paths() 
    file_list = list()
    for path in store.file_paths:
        if store.ready:
#            if ('BOSS_SPECTRO_REDUX'     in path or
#                'MANGA_SPECTRO_REDUX'    in path or
#                'MANGA_SPECTRO_ANALYSIS' in path or
#                'MANGA_TARGET'           in path or
#                'APOGEE_REDUX'           in path
#                ):
#                file_list.append(path)
            file_list.append(path)
            store.set_path(path=path)
            store.split_path()
            store.populate_file_path_tables()
    print('file_list: \n' + dumps(file_list,indent=1))
    store.exit()

