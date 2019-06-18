#!/usr/bin/env python3
from os import walk
from os.path import join, exists
from datamodel_parser.application import Argument
from datamodel_parser.application import Store

from json import dumps

print('Finding SVN Products')
arg = Argument('find_svn_products')
options = arg.options if arg else None
store = Store(options=options) if options else None
logger = store.logger if store else None
ready = options and store and logger
ready = ready and store.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
    exit(1)
else:
    store.svn_products = list()
    root_dir = 'https://svn.sdss.org/repo/'
    store.set_svn_products(root_dir=root_dir)
    print('store.svn_products: \n' + dumps(store.svn_products,indent=1))
    store.exit()

