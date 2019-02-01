from datamodel_parser.migrate import File
from datamodel_parser.migrate import Database
from bs4 import BeautifulSoup
from os import environ
from os.path import join, exists
import logging
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
            self.set_datamodel_dir()
            self.set_tree_edition()
            self.set_html_text()

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

    def set_tree_edition(self):
        '''Set the datamodel edition.'''
        if self.ready:
            if self.datamodel_dir:
                self.tree_edition = (self.datamodel_dir[-4:]
                                if self.datamodel_dir else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_tree_edition. ' +
                                  'self.datamodel_dir: {0}'
                                  .format(self.datamodel_dir))

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

    def populate_database(self):
        '''Populate the database with file information.'''
        if self.ready:
            self.set_database()
            self.populate_file_path_tables()
            self.populate_html_text_tables()

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
            self.file.parse_file()
            if self.ready and self.file.ready:
                self.populate_file_table()
#                self.populate_description_table()
#                self.populate_extension_table()
#                self.populate_header_table()
#                self.populate_keyword_table()
#                self.populate_data_table()
#                self.populate_column_table()

    def parse_path(self):
        self.env_variable = None
        self.location_path = None
        if self.ready:
            if self.path:
                path = self.path.replace('/datamodel/files/','')
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
        ''' Set instance of File class.'''
        self.file = None
        if self.ready:
            if self.soup:
                body = self.soup.body if self.soup else None
                self.set_all_divs(body=body)
                if self.ready and self.all_divs: self.set_file_div(body=body)
                else:
                    self.ready = False
                    self.logger.error('Not working on this File class yet.')
            else:
                self.ready = False
                self.logger.error('Unable to set_file. ' +
                                  'self.soup: {0}'.format(self.soup))

    def set_all_divs(self,body=None):
        '''Check if the HTML body is comprised of only division tags.'''
        self.all_divs = True
        if self.ready:
            if body:
                all_div = True
                for child in body.children:
                    if child.name and child.name != 'div': self.all_div = False
            else:
                self.ready = False
                self.logger.error('Unable to set_all_divs. ' +
                                  'body: '.format(body))

    def set_file_div(self,body=None):
        '''Set instance of File derived class comprised of HTML div's.'''
        if self.ready:
            if body:
                divs = body.find_all('div')
                self.file = (
                    File(logger=self.logger,options=self.options,divs=divs)
                    if self.logger and self.options and self.soup else None)
                self.ready = bool(self.file and self.file.ready)
                if not self.ready:
                    self.logger.error(
                        'Unable to set_file. ' +
                        'self.file: {0}'.format(self.file) +
                        'self.file.ready: {0}'.format(self.file.ready))
            else:
                self.ready = False
                self.logger.error('Unable to set_file_div. ' +
                                  'divs: {0}'.format(divs))

    def populate_tree_table(self):
        '''Populate the tree table.'''
        if self.ready:
            if self.tree_edition:
                self.database.set_tree_columns(edition=self.tree_edition)
                self.database.populate_tree_table()
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_tree_table. ' +
                    'self.tree_edition: {0}'.format(self.tree_edition))

    def populate_env_table(self):
        '''Populate the env table.'''
        if self.ready:
            if self.tree_edition and self.env_variable:
                self.database.set_env_columns(variable=self.env_variable,
                                              edition=self.tree_edition)
                self.database.populate_env_table()
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_env_table. ' +
                    'self.tree_edition: {0}'.format(self.tree_edition))

    def populate_location_table(self):
        '''Populate the location table.'''
        if self.ready:
            if (self.location_path and
                self.env_variable):
                self.database.set_location_columns(
                                        path=self.location_path,
                                        variable=self.env_variable)
                self.database.populate_location_table()
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_location_table. ' +
                    'self.location_path: {0}'.format(self.location_path) +
                    'self.env_variable: {0}'.format(self.env_variable))

    def populate_directory_table(self):
        '''Populate the directory table.'''
        if self.ready:
            if (self.location_path   and
                self.directory_names and
                self.directory_depths):
                path   = self.location_path
                names  = self.directory_names
                depths = self.directory_depths
                for (name,depth) in list(zip(names,depths)):
                    self.database.set_directory_columns(path=path,
                                                        name=name,
                                                        depth=depth)
                    self.database.populate_directory_table()
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_directory_table. ' +
                    'self.location_path: {0}'.format(self.location_path) +
                    'self.directory_names: {0}'.format(self.directory_names))

    def exit(self):
        '''Report the presense/lack of errors.'''
        if self.ready:
            if self.verbose: self.logger.info('Finished!')
            exit(0)
        else:
            if self.verbose: self.logger.info('Fail!')
            exit(1)

    def populate_file_table(self):
        '''Populate the file table.'''
        if self.ready:
            if (self.location_path        and
                self.file_name            and
                self.file                 and
                self.file.extension_count
                ):
                self.database.set_file_columns(
                                path = self.location_path,
                                name=self.file_name,
                                extension_count=self.file.extension_count)
                self.database.populate_file_table()
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_file_table. ' +
                    'self.file_file_path: {0}'.format(self.file_file_path) +
                    'self.env_variable: {0}'.format(self.env_variable))


