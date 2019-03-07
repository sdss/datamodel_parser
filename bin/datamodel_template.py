#!/usr/bin/env python3
from datamodel_parser.application import Argument
from datamodel_parser.migrate import Migrate
from json import dumps

print('Templating Database.')
arg = Argument('parse_html')
options = arg.options if arg else None
migrate = Migrate(options=options) if options else None
logger = migrate.logger if migrate else None
ready = options and migrate and logger
ready = ready and migrate.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
else:
#    template = "datamodel/datamodel_txt.txt"
    template = "datamodel/datamodel_md.txt"
    migrate.render_template(template=template)
    migrate.exit()

'''
Examples:
File Type 1)
    datamodel/dr15
        datamodel_template.py --path datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/PLATE4/stack/manga-RSS.html -l debug -v
        
File Type 2)
    datamodel/dr15:
        Fail!
        datamodel_template.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/exposures/INSTRUMENT/MJD5/ap2D.html -l debug -v
    datamodel/dr14:
        datamodel_template.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/red/MJD5/ap2Dmodel.html -l debug -v
        datamodel_template.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/red/MJD5/ap2D.html -l debug -v
        
File Type 3)
    datamodel/dr14 and datamodel/dr15
    Fail!
    parse_html.py --path datamodel/files/BOSS_SPECTRO_DATA/MJD/sdR.html -l debug -v
'''
