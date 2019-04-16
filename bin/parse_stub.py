#!/usr/bin/env python3
from datamodel_parser.application import Argument
from datamodel_parser.application import Store
from datamodel_parser.application import Stub

from os.path import join
from json import dumps

print('Parsing fits file stub .')
arg = Argument('parse_stub')
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

    basename = '/data'
    file = join(basename,options.path)
    files = [file]
    stub = Stub(files=files)
    stub.getModelName()
    stub.readFile()
    stub.buildDict()

    store.populate_fits_tables(fits_dict=stub.tempDict)




'''
Examples:
parse_stub.py -l error -v --path datamodel/files/BOSS_SPECTRO_REDUX/RUN2D/PLATE4/RUN1D/spZbest-3606-55182.fits
'''



