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
    migrate.populate_database()
    migrate.exit()

'''
Examples:
Template 1) https://data.sdss.org/datamodel/template.html

datamodel/dr15
Finished
parse_html.py --path datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/PLATE4/stack/manga-RSS.html -l debug -v

Template 2) https://data.sdss.org/datamodel/template.html

datamodel/dr15:
Finished
parse_html.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/exposures/INSTRUMENT/MJD5/ap2D.html -l debug -v

datamodel/dr14:
Fail
parse_html.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/red/MJD5/ap2Dmodel.html -l debug -v

Finished
parse_html.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/red/MJD5/ap2D.html -l debug -v
'''
