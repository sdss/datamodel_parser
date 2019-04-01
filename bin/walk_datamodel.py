#!/usr/bin/env python3
import os
from os.path import join, getsize

from datamodel_parser.application import Argument
from datamodel_parser.migrate import Migrate

print('Walking DATAMODEL_DIR')
arg = Argument('walk_datamodel')
options = arg.options if arg else None
migrate = Migrate(options=options) if options else None
logger = migrate.logger if migrate else None
ready = options and migrate and logger
ready = ready and migrate.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
    exit(1)
else:
    migrate.set_datamodel_dir()
    

#    migrate.populate_database()
#    migrate.exit()

