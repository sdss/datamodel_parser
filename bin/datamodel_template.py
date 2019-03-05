#!/usr/bin/env python3
from flask import render_template
from datamodel_parser import app, logger
from datamodel_parser.application import Argument
from datamodel_parser.migrate import Migrate
from datamodel_parser.migrate import Database
# Model classes
from datamodel_parser.models.datamodel import Tree
from datamodel_parser.models.datamodel import Env
from datamodel_parser.models.datamodel import Location
from datamodel_parser.models.datamodel import Directory
from datamodel_parser.models.datamodel import File
from datamodel_parser.models.datamodel import Intro
from datamodel_parser.models.datamodel import Section
from datamodel_parser.models.datamodel import Extension
from datamodel_parser.models.datamodel import Data
from datamodel_parser.models.datamodel import Column
from datamodel_parser.models.datamodel import Header
from datamodel_parser.models.datamodel import Keyword
from json import dumps

print('Templating Database.')
arg = Argument('parse_html')
options = arg.options if arg else None
migrate = Migrate(options=options) if options else None
logger = migrate.logger if migrate else None
database = Database(logger=logger,options=options) if logger and options else None
ready = options and migrate and logger and database
ready = ready and migrate.ready and database.ready
if not ready:
    print('Fail! ready: {}'.format(ready))
else:

    migrate.parse_path() # get env_variable, location_path, and file_name
    migrate.set_tree_edition()
    database.set_file_id(tree_edition  = migrate.tree_edition,
                         env_variable  = migrate.env_variable,
                         location_path = migrate.location_path,
                         file_name     = migrate.file_name)
    if not (migrate.ready and database.ready):
        print('Fail! \nTry running parse_html for the file: %r' % options.path)
    
    else:
        intros = Intro.load_all(file_id=database.file_id)
        sections = Section.load_all(file_id=database.file_id)
        extensions = Extension.load_all(file_id=database.file_id)
        headers = Header.load_all(extensions=extensions) if extensions else None
        datas = Data.load_all(extensions=extensions) if extensions else None

        # set sections = None if sections has empty hdu information
        if (len(sections) == 1             and
            sections[0].hdu_number is None and
            sections[0].hdu_name   is None
            ):
            sections = None
#        print('sections: %r' % sections)
#        input('pause')

        if intros and headers:
            hdus = dict()
            for (data,header) in list(zip(datas,headers)):
                hdu = dict()
                hdu['extension'] = dict()
                column = (Column.load(data_id=data.id)
                            if data and data.id else None)
                hdu['column'] = (column if column
                                and not
                                (column.datatype is None and
                                 column.datatype is None and
                                 column.datatype is None)
                                 else None)
                hdu['extension']['header'] = header
                hdu['extension']['keywords'] = (Keyword.load_all(header_id=header.id)
                    if header and header.id else None)
                hdus[header.hdu_number] = hdu


#            for hdu_number in hdus.keys():
#                print("hdus[hdu_number]['column']: %r" % hdus[hdu_number]['column'])
#                print("hdus[hdu_number]['extension']['header']: %r" % hdus[hdu_number]['extension']['header'])
#                print("hdus[hdu_number]['extension']['keywords']: %r" % hdus[hdu_number]['extension']['keywords'])
#                input('pause')


            template = "datamodel/datamodel.txt"
            with app.app_context():
                result = render_template(template,
                                         intros   = intros,
                                         sections = sections,
                                         hdus     = hdus,
                                         )
#            print('result: %r' % result)
#            input('pause')
            file = '/Users/ben/Desktop/Work/Scratch_Stuff/template_result.txt'
            with open(file, 'w') as text_file:
                text_file.write(result)

'''
Examples:
File Type 1)
    datamodel/dr15
        datamodel_template.py --path datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/PLATE4/stack/manga-RSS.html -l debug -v
        
File Type 2)
    datamodel/dr15:
        datamodel_template.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/exposures/INSTRUMENT/MJD5/ap2D.html -l debug -v
    datamodel/dr14:
        datamodel_template.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/red/MJD5/ap2Dmodel.html -l debug -v
        datamodel_template.py --path datamodel/files/APOGEE_REDUX/APRED_VERS/red/MJD5/ap2D.html -l debug -v
        
File Type 3)
    datamodel/dr14 and datamodel/dr15
    Fail!
    parse_html.py --path datamodel/files/BOSS_SPECTRO_DATA/MJD/sdR.html -l debug -v
'''
