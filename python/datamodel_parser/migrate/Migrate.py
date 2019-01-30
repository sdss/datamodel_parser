from datamodel_parser.migrate import File
from datamodel_parser.migrate import Database
from os import environ
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
            self.set_datamodel_dir()
            self.set_edition()

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

    def set_edition(self):
        '''Set the datamodel edition.'''
        if self.ready:
            if self.datamodel_dir:
                self.edition = (self.datamodel_dir[-4:]
                                if self.datamodel_dir else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_edition. ' +
                                  'self.datamodel_dir: {0}'
                                  .format(self.datamodel_dir))

    def populate_database(self):
        '''Populate the database with file information.'''
        if self.ready:
            self.set_database()
            self.set_file()
            if self.ready:
                self.populate_tree_table()
                self.file.parse_path()
                self.populate_env_table()
                self.populate_location_table()
                self.populate_directory_table()

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

    def set_file(self):
        ''' Set instance of File class.'''
        self.file = None
        if self.ready:
            self.file = (File(logger=self.logger,options=self.options)
                         if self.logger and self.options else None)
            self.ready = bool(self.file and self.file.ready)
            if not self.ready:
                self.logger.error(
                    'Unable to set_file. ' +
                    'self.file: {0}'.format(self.file) +
                    'self.file.ready: {0}'.format(self.file.ready))

    def populate_tree_table(self):
        '''Populate the tree table.'''
        if self.ready:
            if self.edition:
                self.database.set_tree_columns(edition=self.edition)
                self.database.populate_tree_table()
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_tree_table. ' +
                    'self.edition: {0}'.format(self.edition))

    def populate_env_table(self):
        '''Populate the env table.'''
        if self.ready:
            if self.edition and self.file and self.file.env_variable:
                self.database.set_env_columns(variable=self.file.env_variable,
                                              edition=self.edition)
                self.database.populate_env_table()
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_env_table. ' +
                    'self.file: {0}'.format(self.file) +
                    'self.edition: {0}'.format(self.edition))

    def populate_location_table(self):
        '''Populate the location table.'''
        if self.ready:
            if (self.file and
                self.file.location_path and
                self.file.env_variable):
                self.database.set_location_columns(
                                        path=self.file.location_path,
                                        variable=self.file.env_variable)
                self.database.populate_location_table()
            else:
                self.ready = False
                self.logger.error('Unable to populate_location_table. ' +
                                  'self.file: {0}'.format(self.file))

    def populate_directory_table(self):
        '''Populate the directory table.'''
        if self.ready:
            if (self.file and
                self.file.location_path and
                self.file.directory_names and
                self.file.directory_depths):
                path = self.file.location_path
                names = self.file.directory_names
                depths = self.file.directory_depths
                for (name,depth) in list(zip(names,depths)):
                    self.database.set_directory_columns(path=path,
                                                        name=name,
                                                        depth=depth)
                    self.database.populate_directory_table()
            else:
                self.ready = False
                self.logger.error('Unable to populate_directory_table. ' +
                                  'self.file: {0}'.format(self.file))

    def exit(self):
        '''Report the presense/lack of errors.'''
        if self.ready:
            if self.verbose: self.logger.info('Finished!')
            exit(0)
        else:
            if self.verbose: self.logger.info('Fail!')
            exit(1)

