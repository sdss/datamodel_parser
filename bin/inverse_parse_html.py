#!/usr/bin/env python3
from datamodel_parser.application import Argument
from datamodel_parser.application import Store

print('\nInverse Parsing HTML.')
arg = Argument('inverse_parse_html')
options = arg.options if arg else None
store = Store(options=options) if options else None
logger = store.logger if store else None
ready = options and store and logger
ready = ready and store.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
    exit(1)
else:
    print('path: {}'.format(options.path))
    store.set_tree_edition()
    store.set_path(path=options.path)
    store.split_path()
    #store.get_db_column_tags()
    store.get_db_keyword_tags()
    store.exit()


'''
inverse_parse_html -l error -v --path MANGA_SPECTRO_REDUX/DRPVER/PLATE4/stack/manga-CUBE.html --string VERSPLDS
'''
