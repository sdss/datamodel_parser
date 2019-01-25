#!/usr/bin/env python3
from datamodel_parser.application import Argument
from datamodel_parser.migrate import Migrate

print('Parsing HTML.')
arg = Argument('parse_html')
options = arg.options if arg else None
migrate = Migrate(options=options) if options else None
logger = migrate.logger if migrate else None
ready = options and migrate and logger
ready = ready and migrate.ready
if not ready: print('Fail!')
else:
    migrate.parse_file()
    migrate.exit()

