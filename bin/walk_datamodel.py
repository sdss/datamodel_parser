#!/usr/bin/env python3
from os import walk
from os.path import join, exists

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
    migrate.set_database()
    migrate.set_datamodel_dir()
    migrate.set_tree_edition()
    for path in migrate.get_file_paths():
#        print('path: %r' % path)
        migrate.set_path(path=path)
        migrate.parse_path()
        migrate.populate_history_table(status='pending')
    migrate.exit()

