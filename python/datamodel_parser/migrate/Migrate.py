from datamodel_parser.migrate import File
from datamodel_parser.migrate import Database
from bs4 import BeautifulSoup
from os import environ
from os.path import join, exists
import logging
from flask import render_template
from datamodel_parser import app, logger

from json import dumps

class Migrate:

    def __init__(self, options=None):
        self.set_logger(options=options)
        self.set_options(options=options)
        self.set_ready()
        self.set_attributes()

    def set_logger(self, options=None):
        '''Set class logger.'''
        self.ready = True
        self.logger = None
        if options and logging:
            self.logger = logging.getLogger('datamodel_parser')
            if self.logger:
                if   options.level == 'debug':
                    self.logger.setLevel(logging.DEBUG)
                elif options.level == 'info':
                    self.logger.setLevel(logging.INFO)
                elif options.level == 'warning':
                    self.logger.setLevel(logging.WARNING)
                elif options.level == 'error':
                    self.logger.setLevel(logging.ERROR)
                elif options.level == 'critical':
                    self.logger.setLevel(logging.CRITICAL)
                else: self.logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler()
                if options.level == 'debug':
                    formatter = logging.Formatter("%(name)s - " +
                                                  "%(levelname)s - " +
                                                  "%(filename)s - " +
                                                  "line %(lineno)d - " +
                                                  "%(message)s\n")
                else:
                    formatter = logging.Formatter("%(name)s - " +
                                                  "%(levelname)s - " +
                                                  "%(message)s")
                    formatter = logging.Formatter("%(name)s - " +
                                                  "%(levelname)s - " +
                                                  "%(filename)s - " +
                                                  "%(message)s")
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                if options.nolog: self.logger.disabled = True
            else:
                self.ready = False
                print('Unable to set_logger')
        else:
            self.ready = False
            print('Unable to set_logger. options={0}, logging={1}'
                .format(options,logging))

    def set_options(self, options=None):
        self.options = None
        if self.ready:
            self.options = options if options else None
            if not self.options: self.logger.error('Unable to set_options.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger and
                          self.options)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.path    = self.options.path    if self.options else None
            self.set_tree_edition()
            self.set_html_text()
            self.set_database()

    def set_tree_edition(self):
        '''Set the datamodel edition.'''
        if self.ready:
            self.set_datamodel_dir()
            if self.datamodel_dir:
                self.tree_edition = (self.datamodel_dir[-4:]
                                if self.datamodel_dir else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_tree_edition. ' +
                                  'self.datamodel_dir: {0}'
                                  .format(self.datamodel_dir))

    def set_datamodel_dir(self):
        '''Set the DATAMODEL_DIR file path on cypher.'''
        self.datamodel_dir = None
        if self.ready:
            try: self.datamodel_dir = environ['DATAMODEL_DIR']
            except:
                self.ready = False
                self.logger.error(
                    'Unable to populate_tree_table from the ' +
                    'environmental variable DATAMODEL_DIR. ' +
                    'Try loading a datamodel module file.')

    def set_html_text(self):
        '''Set the HTML text for the given URL.'''
        self.html_text = None
        if self.ready:
            if self.datamodel_dir and self.path:
                self.validate_path(path=self.path)
                if self.ready:
                    file =  join(self.datamodel_dir,self.path)
                    if exists(file):
                        with open(file, 'r') as html_text:
                            self.html_text = html_text.read()
                    else:
                        self.ready = False
                        self.logger.error('Unable to set_html_text. ' +
                                          'This file does not exist: {0}'
                                          .format(file))
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_html_text. ' +
                    'self.datamodel_dir: {0}'.format(self.datamodel_dir) +
                    'self.path: {0}'.format(self.path))

    def validate_path(self,path=None):
        '''Check that path is a non-absolute path.'''
        if self.ready:
            if path:
                if path[0] == '/':
                    self.ready = False
                    self.logger.error('Invalid self.path: {0}'.format(path))
            else:
                self.ready = False
                self.logger.error('Unable to validate_path.' +
                                  'path: {0}'.format(path))

    def set_database(self):
        '''Set class Database instance.'''
        self.database = None
        if self.ready:
            self.database = (Database(logger=self.logger,options=self.options)
                             if self.logger and self.options else None)
            self.ready = bool(self.database and self.database.ready)
            if not self.ready:
                self.logger.error(
                    'Unable to set_database. ' +
                    'self.database: {0}'.format(self.database) +
                    'self.database.ready: {0}'.format(self.database.ready))

    def render_template(self,template=None):
        '''Use database information to render the given template.'''
        if self.ready:
            if template:
                self.parse_path() # set env_variable, location_path, and file_name
                self.set_tree_edition()
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                (intros,sections,hdus) = (self.database.get_intros_sections_hdus()
                                          if self.ready and self.database.ready
                                          else None)
                self.ready = self.ready and self.database.ready
                if self.ready:
                    result = None
                    with app.app_context():
                        result = render_template(template,
                                                 intros   = intros,
                                                 sections = sections,
                                                 hdus     = hdus,
                                                 )
                    self.process_rendered_template(result   = result,
                                                   template = template)
                else:
                    print('Fail! \nTry running parse_html for the file: %r'
                            % self.options.path)
            else:
                self.ready = False
                self.logger.error('Unable to render_template.' +
                                  'template: {0}'.format(template))

    def process_rendered_template(self,result=None,template=None):
        '''Process the result of the rendered Jinja2 template.'''
        if self.ready:
            if result and template:
                self.set_datamodel_parser_rendered_dir()
                file_extension = template.split('.')[0].split('_')[1]
                dir_name = (self.datamodel_parser_rendered_dir
                            if self.datamodel_parser_rendered_dir else None)
                file_name = self.file_name.split('.')[0] + '.' + file_extension
                file = join(dir_name,file_name)
                self.logger.info('writing rendered template to file: %r' % file)
                with open(file, 'w+') as text_file:
                    text_file.write(result)
            else:
                self.ready = False
                self.logger.error('Unable to process_rendered_template. ' +
                                  'result: {0}, '.format(result) +
                                  'template: {0}, '.format(template))

    def set_datamodel_parser_rendered_dir(self):
        '''Set the DATAMODEL_DIR file path on cypher.'''
        self.datamodel_parser_rendered_dir = None
        if self.ready:
            try: self.datamodel_parser_rendered_dir = (
                    environ['DATAMODEL_PARSER_RENDERED_TEMPLATES_DIR'])
            except:
                self.ready = False
                self.logger.error(
                    'Unable to set_datamodel_parser_rendered_dir from the ' +
                    'environmental variable DATAMODEL_PARSER_RENDERED_TEMPLATES_DIR. ' +
                    'Try loading a datamodel_parser module file.')

    def populate_database(self):
        '''Populate the database with file information.'''
        if self.ready:
            self.populate_file_path_tables()
            self.populate_html_text_tables()

    def populate_file_path_tables(self):
        '''Populate tables comprised of file path information.'''
        if self.ready:
            self.parse_path()
            self.populate_tree_table()
            self.populate_env_table()
            self.populate_location_table()
            self.populate_directory_table()

    def populate_html_text_tables(self):
        '''Populate tables comprised of file HTML text information.'''
        if self.ready:
            self.set_soup()
            self.set_file()
            if self.file and self.file.ready:
                self.file.parse_file()
                if self.ready and self.file.ready:
                    self.populate_file_table()
                    self.populate_intro_table()
                    self.populate_section_table()
                    self.populate_extension_table()
                    self.populate_data_table()
                    self.populate_column_table()
                    self.populate_header_table()
                    self.populate_keyword_table()
            else:
                self.ready = False
                self.logger.error('Unable to populate_html_text_tables. ' +
                                  'self.file: {0}, '.format(self.file) +
                                  'self.file.ready: {0}.'.format(self.file.ready))

    def parse_path(self):
        '''Extract information from the given file path.'''
        self.env_variable     = None
        self.file_name        = None
        self.location_path    = None
        self.directory_names  = None
        self.directory_depths = None
        if self.ready:
            if self.path:
                path = self.path.replace('datamodel/files/','')
                split = path.split('/')
                self.env_variable  = split[0]              if split else None
                self.file_name     = split[-1]             if split else None
                self.location_path = '/'.join(split[1:-1]) if split else None
                self.directory_names  = list()
                self.directory_depths = list()
                for name in split[1:-1]:
                    self.directory_names.append(name)
                    self.directory_depths.append(
                        self.directory_names.index(name))
            else:
                self.ready = False
                self.logger.error('Unable to parse_path. ' +
                                  'self.path: {0}'.format(self.path))

    def set_soup(self):
        '''Set a class BeautifulSoup instance
           from the HTML text of the given URL.
        '''
        self.soup = None
        if self.ready:
            self.soup = (BeautifulSoup(self.html_text, 'html.parser')
                         if self.html_text else None)
            if not self.soup:
                self.ready = None
                self.logger.error('Unable to set_soup. self.html_text: {0}'
                                    .format(self.html_text))

    def set_file(self):
        ''' Set class File instance.'''
        self.file = None
        if self.ready:
            if self.soup:
                body = self.soup.body if self.soup else None
                self.file = (File(logger=self.logger,
                                  options=self.options,
                                  body=body)
                             if self.logger and self.options and body else None)
                self.ready = self.file.ready

    def populate_tree_table(self):
        '''Populate the tree table.'''
        if self.ready:
            if self.database and self.tree_edition:
                self.database.set_tree_columns(edition=self.tree_edition)
                self.database.populate_tree_table()
                self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_tree_table. ' +
                    'self.database: {0}.'.format(self.database) +
                    'self.tree_edition: {0}.'.format(self.tree_edition))

    def populate_env_table(self):
        '''Populate the env table.'''
        if self.ready:
            if self.database and self.tree_edition and self.env_variable:
                self.database.set_tree_id(tree_edition=self.tree_edition)
                self.database.set_env_columns(variable=self.env_variable)
                self.database.populate_env_table()
                self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_env_table. ' +
                    'self.database: {0}, '.format(self.database) +
                    'self.env_variable: {0}.' .format(self.env_variable))

    def populate_location_table(self):
        '''Populate the location table.'''
        if self.ready:
            if (self.database     and
                self.tree_edition and
                self.env_variable and
                self.location_path
                ):
                self.database.set_env_id(tree_edition = self.tree_edition,
                                         env_variable = self.env_variable)
                self.database.set_location_columns(path = self.location_path)
                self.database.populate_location_table()
                self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_location_table. '                +
                    'self.tree_edition: {0}, '.format(self.tree_edition) +
                    'self.env_variable: {0}, '.format(self.env_variable) +
                    'self.location_path: {0}.'.format(self.location_path)
                    )

    def populate_directory_table(self):
        '''Populate the directory table.'''
        if self.ready:
            if (self.tree_edition     and
                self.env_variable     and
                self.location_path    and
                self.directory_names  and
                self.directory_depths
                ):
                self.database.set_location_id(
                                            tree_edition = self.tree_edition,
                                            env_variable = self.env_variable,
                                            location_path = self.location_path)
                names         = self.directory_names
                depths        = self.directory_depths
                for (name,depth) in list(zip(names,depths)):
                    if self.ready:
                        self.database.set_directory_columns(name=name,
                                                            depth=depth)
                        self.database.populate_directory_table()
                        self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_directory_table. '                     +
                    'self.tree_edition: {0}, '   .format(self.tree_edition)    +
                    'self.env_variable: {0}, '   .format(self.env_variable)    +
                    'self.location_path: {0}, '  .format(self.location_path)   +
                    'self.directory_names: {0}, '.format(self.directory_names) +
                    'self.directory_depths: {0}.'.format(self.directory_depths))

    def populate_file_table(self):
        '''Populate the file table.'''
        if self.ready:
            if (self.tree_edition         and
                self.env_variable         and
                self.location_path        and
                self.file_name            and
                self.file                 and
                self.file.extension_count
                ):
                self.database.set_location_id(
                                            tree_edition = self.tree_edition,
                                            env_variable = self.env_variable,
                                            location_path = self.location_path)
                name=self.file_name
                extension_count=self.file.extension_count
                self.database.set_file_columns(
                                            name            = name,
                                            extension_count = extension_count)
                self.database.populate_file_table()
                self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_file_table. '                      +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file: {0}, '         .format(self.file)          +
                    'self.file.extension_count: {0}.'
                    .format(self.file.extension_count))

    def populate_intro_table(self):
        '''Populate the intro table.'''
        if self.ready:
            if (self.tree_edition              and
                self.env_variable              and
                self.location_path             and
                self.file_name                 and
                self.file                      and
                self.file.intro_heading_orders and
                self.file.intro_heading_levels and
                self.file.intro_heading_titles and
                self.file.intro_descriptions
                ):
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                heading_orders = self.file.intro_heading_orders
                heading_levels = self.file.intro_heading_levels
                heading_titles = self.file.intro_heading_titles
                descriptions   = self.file.intro_descriptions

                for (heading_order,
                     heading_level,
                     heading_title,
                     description) in list(zip(
                     heading_orders,
                     heading_levels,
                     heading_titles,
                     descriptions)):
                    if self.ready:
                        self.database.set_intro_columns(
                                                heading_order = heading_order,
                                                heading_level = heading_level,
                                                heading_title = heading_title,
                                                description   = description)
                        self.database.populate_intro_table()
                        self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_intro_table. '                     +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file.intro_heading_orders: {0}, '
                    .format(self.file.intro_heading_orders)                +
                    'self.file.intro_heading_levels: {0}, '
                    .format(self.file.intro_heading_levels)                +
                    'self.file.intro_heading_titles: {0}, '
                    .format(self.file.intro_heading_titles)                +
                    'self.file.intro_descriptions: {0}.'
                    .format(self.file.intro_descriptions)
                    )

    def populate_section_table(self):
        '''Populate the section table.'''
        if self.ready:
            if (self.tree_edition                 and
                self.env_variable                 and
                self.location_path                and
                self.file_name                    and
                self.file                         and
                self.file.section_hdu_names is not None
                ):
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                section_hdu_names = self.file.section_hdu_names
                if section_hdu_names:
                    for (hdu_number,hdu_name) in section_hdu_names.items():
                        if self.ready:
                            self.database.set_section_columns(
                                                hdu_number = int(hdu_number),
                                                hdu_name   = hdu_name)
                            self.database.populate_section_table()
                            self.ready = self.database.ready
                else: # the file does not have a section list
                    self.database.set_section_columns(hdu_number = None,
                                                      hdu_name   = None)
                    self.database.populate_section_table()
                    self.ready = self.database.ready

            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_section_table. '                   +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file: {0},'          .format(self.file)          +
                    'self.file.section_hdu_names: {0}.'
                    .format(self.file.section_hdu_names))

    def populate_extension_table(self):
        '''Populate the extension table.'''
        if self.ready:
            if (self.tree_edition               and
                self.env_variable               and
                self.location_path              and
                self.file_name                  and
                self.file                       and
                self.file.file_extension_data
                ):
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                for hdu_data in self.file.file_extension_data:
                    hdu_number = hdu_data['hdu_number']
                    self.database.set_extension_columns(hdu_number=hdu_number)
                    self.database.populate_extension_table()
                    self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_extension_table. '                 +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file: {0}'           .format(self.file)          +
                    'self.file.file_extension_data: {0}'
                    .format(self.file.file_extension_data)
                    )

    def populate_data_table(self):
        '''Populate the data table.'''
        if self.ready:
            if (self.tree_edition               and
                self.env_variable               and
                self.location_path              and
                self.file_name                  and
                self.file                       and
                self.file.file_extension_data
                ):
                for hdu_data in self.file.file_extension_data:
                    if self.ready:
                        hdu_number = hdu_data['hdu_number']
                        is_image   = hdu_data['data_is_image']
                        self.database.set_extension_id(
                                            tree_edition  = self.tree_edition,
                                            env_variable  = self.env_variable,
                                            location_path = self.location_path,
                                            file_name     = self.file_name,
                                            hdu_number    = hdu_number)
                        self.database.set_data_columns(is_image=is_image)
                        self.database.populate_data_table()
                        self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_data_table. '                 +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file: {0}'           .format(self.file)          +
                    'self.file.file_extension_data: {0}'
                    .format(self.file.file_extension_data)
                    )

    def populate_column_table(self):
        '''Populate the column table.'''
        if self.ready:
            if (self.tree_edition               and
                self.env_variable               and
                self.location_path              and
                self.file_name                  and
                self.file                       and
                self.file.file_extension_data
                ):
                for hdu_data in self.file.file_extension_data:
                    if self.ready:
                        hdu_number   = hdu_data['hdu_number']
                        header_title = hdu_data['header_title']
                        datatype     = hdu_data['column_datatype']
                        size         = hdu_data['column_size']
                        description  = hdu_data['column_description']
                        self.database.set_data_id(
                                            tree_edition  = self.tree_edition,
                                            env_variable  = self.env_variable,
                                            location_path = self.location_path,
                                            file_name     = self.file_name,
                                            hdu_number    = hdu_number)
                        self.database.set_column_columns(
                                                    header_title = header_title,
                                                    datatype     = datatype,
                                                    size         = size,
                                                    description  = description)
                        self.database.populate_column_table()
                        self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_column_table. '                 +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file: {0}'           .format(self.file)          +
                    'self.file.file_extension_data: {0}'
                    .format(self.file.file_extension_data)
                    )

    def populate_header_table(self):
        '''Populate the header table.'''
        if self.ready:
            if (self.tree_edition                   and
                self.env_variable                   and
                self.location_path                  and
                self.file_name                      and
                self.file                           and
                self.file.file_extension_data       and
                self.file.file_extension_headers
                ):
                data    = self.file.file_extension_data
                headers = self.file.file_extension_headers

                if len(data) == len(headers):
                    for (hdu_data,hdu_header) in list(zip(data,headers)):
                        if self.ready:
                            hdu_number    = hdu_data['hdu_number']
                            header_title  = hdu_data['header_title']
                            table_caption = hdu_header['table_caption']
                            self.database.set_extension_id(
                                            tree_edition  = self.tree_edition,
                                            env_variable  = self.env_variable,
                                            location_path = self.location_path,
                                            file_name     = self.file_name,
                                            hdu_number    = hdu_number)
                            self.database.set_header_columns(
                                                hdu_number    = hdu_number,
                                                title         = header_title,
                                                table_caption = table_caption)
                            self.database.populate_header_table()
                            self.ready = self.database.ready
                else:
                    self.ready = None
                    self.logger.error(
                            'Unable to populate_header_table. ' +
                            'Data and header lists have unequal length. ' +
                            'len(data): {0}, '.format(len(data)) +
                            'len(headers): {0}, '.format(len(headers)))
                            
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_header_table. '                 +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file: {0}'           .format(self.file)          +
                    'self.file.file_extension_data: {0}'
                    .format(self.file.file_extension_data)                 +
                    'self.file.file_extension_headers: {0}'
                    .format(self.file.file_extension_headers)
                    )

    def populate_keyword_table(self):
        '''Populate the keyword table.'''
        if self.ready:
            if (self.tree_edition                   and
                self.env_variable                   and
                self.location_path                  and
                self.file_name                      and
                self.file                           and
                self.file.file_extension_data       and
                self.file.file_extension_headers
                ):
                data    = self.file.file_extension_data
                headers = self.file.file_extension_headers
                if len(data) == len(headers):
                    for (hdu_data,hdu_header) in list(zip(data,headers)):
                        if self.ready:
                            hdu_number     = hdu_data['hdu_number']
                            self.database.set_header_id(
                                            tree_edition  = self.tree_edition,
                                            env_variable  = self.env_variable,
                                            location_path = self.location_path,
                                            file_name     = self.file_name,
                                            hdu_number    = hdu_number)
                            table_keywords = hdu_header['table_keywords']
                            table_rows   = hdu_header['table_rows']
                            for keyword_order in table_rows.keys():
                                if self.ready:
                                    self.database.set_keyword_columns(
                                        keyword_order = keyword_order,
                                        table_row     = table_rows[keyword_order])
                                    self.database.populate_keyword_table()
                                    self.ready = self.database.ready
                else:
                    self.ready = None
                    self.logger.error(
                            'Unable to populate_keyword_table. ' +
                            'Data and header lists have unequal length. ' +
                            'len(data): {0}, '.format(len(data)) +
                            'len(headers): {0}, '.format(len(headers)))
                
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_keyword_table. '                 +
                    'self.tree_edition: {0}, ' .format(self.tree_edition)  +
                    'self.env_variable: {0}, ' .format(self.env_variable)  +
                    'self.location_path: {0}, '.format(self.location_path) +
                    'self.file_name: {0}, '    .format(self.file_name)     +
                    'self.file: {0}'           .format(self.file)          +
                    'self.file.file_extension_data: {0}'
                    .format(self.file.file_extension_data)                 +
                    'self.file.file_extension_headers: {0}'
                    .format(self.file.file_extension_headers)
                    )

    def exit(self):
        '''Report the presense/lack of errors.'''
        if self.ready:
            if self.verbose: print('Finished!\n')
            exit(0)
        else:
            if self.verbose: print('Fail!\n')
            exit(1)

