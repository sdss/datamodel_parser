#!/usr/bin/env python3
from flask import render_template
from datamodel_parser import app, logger
from datamodel_parser.application import Argument
from datamodel_parser.migrate import Migrate
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

    migrate.parse_path()
    migrate.set_datamodel_dir()
    migrate.set_tree_edition()
    tree_id = (Tree.load(edition=migrate.tree_edition).id
                              if migrate.tree_edition
                              else None)
    env_id = (Env.load(tree_id  = tree_id,
                       variable = migrate.env_variable).id
                              if  tree_id
                              and migrate.env_variable
                              else None)
    location_id = (Location.load(env_id = env_id,
                                 path   = migrate.location_path).id
                                      if  env_id
                                      and migrate.location_path
                                      else None)
    directories = (Directory.load_all(location_id=location_id)
                                               if location_id
                                               else None)
    file_id = (File.load(location_id = location_id,
                         name        = migrate.file_name).id
                                   if  location_id
                                   and migrate.file_name
                                   else None)
    intros = Intro.load_all(file_id=file_id) if file_id else None

    print('migrate.env_variable: %r' % migrate.env_variable)
    print('migrate.file_name: %r' % migrate.file_name)
    print('migrate.location_path: %r' % migrate.location_path)
    print('migrate.directory_names: %r' % migrate.directory_names)
    print('migrate.directory_depths: %r' % migrate.directory_depths)
    print('migrate.datamodel_dir: %r' % migrate.datamodel_dir)
    print('migrate.tree_edition: %r' % migrate.tree_edition)
    print('tree_id: %r' % tree_id)
    print('env_id: %r' % env_id)
    print('location_id: %r' % location_id)
    print('directories: \n%r' % directories)
    print('file_id: %r' % file_id)
    print('intros: \n%r' % intros)
    
    
    input('pause')

    trees = Tree.query.all()
    envs = Env.query.all()
    locations = Location.query.all()
    directories = Directory.query.all()
    files = File.query.all()
    intros = Intro.query.all()
    sections = Section.query.all()
    extensions = Extension.query.all()
    data = Data.query.all()
    columns = Column.query.all()
    headers = Header.query.all()
    keywords = Keyword.query.all()

    template1 = "datamodel/datamodel.txt"
    with app.app_context():
        result1 = render_template(template1,
                                  trees = trees,
                                  envs = envs,
                                  locations = locations,
                                  directories = directories,
                                  files = files,
                                  intros = intros,
                                  sections = sections,
                                  extensions = extensions,
                                  data = data,
                                  columns = columns,
                                  keywords = keywords,
                                  )
        print('result1 %r' % result1)

'''
Examples:
File Type 1)
    datamodel/dr15
        datamodel_template.py --path datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/PLATE4/stack/manga-RSS.html -l debug -v
'''
