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
    if database.file_id:
        intros = Intro.load_all(file_id=database.file_id)
        sections = Section.load_all(file_id=database.file_id)
        extensions = Extension.load_all(file_id=database.file_id)
        headers = Header.load_all(extensions=extensions) if extensions else None
        datas = Data.load_all(extensions=extensions) if extensions else None
        keywords = dict()
        columns = list()
        for (data,header) in list(zip(datas,headers)):
            if data and data.id:
                columns.append(Column.load(data_id=data.id))
            keywords[header.id] = (Keyword.load_all(header_id=header.id)
                                   if header and header.id else None)

#        print('\nintros: \n%r' % intros)
#        input('pause')
#        print('\nsections: \n%r' % sections)
#        input('pause')
#        print('\nheaders: \n%r' % headers)
#        input('pause')
#        print('\nkeywords: \n%r' % keywords)
#        input('pause')
#        print('\ncolumns: \n%r' % columns)
#        input('pause')

        template = "datamodel/datamodel.txt"
        with app.app_context():
            result1 = render_template(template,
                                      intros   = intros,
                                      sections = sections,
                                      headers  = headers,
                                      keywords = keywords,
                                      columns  = columns,
                                      )
            print('result1 %r' % result1)

'''
Examples:
File Type 1)
    datamodel/dr15
        datamodel_template.py --path datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/PLATE4/stack/manga-RSS.html -l debug -v
'''
