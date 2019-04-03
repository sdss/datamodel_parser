#!/usr/bin/env python3
from os import walk
from os.path import join, exists
from datamodel_parser.application import Argument
from datamodel_parser.migrate import Migrate

from json import dumps

print('Populating File Path Tables')
arg = Argument('parse_paths')
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
    migrate.set_tree_edition()
    migrate.set_database()
    file_paths = migrate.get_file_paths() # DEBUG
    flagships = list()
    for path in migrate.get_file_paths():
        if migrate.ready:
            if ('BOSS_SPECTRO_REDUX'     in path or
                'MANGA_SPECTRO_REDUX'    in path or
                'MANGA_SPECTRO_ANALYSIS' in path or
                'MANGA_TARGET'           in path or
                'APOGEE_REDUX'           in path
                ):
                flagships.append(path)
            migrate.set_path(path=path)
            migrate.split_path()
            migrate.populate_file_path_tables()
    print('flagships: \n' + dumps(flagships,indent=1))
    migrate.exit()

