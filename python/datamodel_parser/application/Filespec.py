from datamodel_parser.application import Util
from string import punctuation as string_punctuation
from sdssdb.sqlalchemy.archive.sas import *
from os.path import basename, dirname, exists, isdir, join
from os import environ, walk
from configparser import ConfigParser
from json import dumps



class Filespec:
    '''Populate the species dictionary'''

    def __init__(self,logger=None,options=None):
        self.initialize(logger=logger,options=options)
        self.set_ready()
        self.set_attributes()

    def initialize(self,logger=None,options=None):
        '''Initialize utility class, logger, and command line options.'''
        self.util = Util(logger=logger,options=options)
        if self.util and self.util.ready:
            self.logger  = self.util.logger  if self.util.logger  else None
            self.options = self.util.options if self.util.options else None
            self.ready   = bool(self.logger)
        else:
            self.ready = False
            print('ERROR: Unable to initialize. self.util: {}'.format(self.util))

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.ready   and
                          self.util    and
                          self.logger
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.datamodel_file_path             = None
            self.datamodel_env_variable          = None
            self.datamodel_file_name             = None
            self.datamodel_filename_start       = None
            self.datamodel_directory_names       = None
            self.directory_substitution_dict     = None
            self.species_location                = None
            self.tree_id                         = None
            self.species_path_example            = None
            self.species_name                    = None
            self.path_example_file_row           = None
            self.session                         = None
            self.env                             = None
            self.path_example_file_row           = None
            self.species_note                    = str()
            self.location_example_datamodel_dict = None

    def set_env_variable_dir(self,env_variable=None):
        '''Set the directory path associated with the datamodel environmental variable.'''
        self.env_variable_dir = None
        if self.ready:
            if env_variable:
                try: self.env_variable_dir = environ[env_variable]
                except Exception as e:
                    self.ready = False
                    self.logger.error('Unable to set_env_variable_dir. ' +
                                      'exception: {}'.format(e))
            else:
                self.ready = False
                self.logger.error('Unable to set_env_variable. ' +
                                  'env_variable: {}'.format(env_variable))
            if not self.env_variable_dir:
                self.ready = False
                self.logger.error('Unable to set_env_variable_dir. '
                                  'self.env_variable_dir: {} '
                                    .format(self.env_variable_dir))

    def set_species(self,species=None):
        '''Set the species class attribute.'''
        self.species = None
        if self.ready:
            self.species = species if species else None
            if not self.species:
                self.ready = False
                self.logger.error('Unable to set_species.'
                                  'species: {} '.format(species))

    def set_path_info(self,path_info=None):
        '''Set the path_info class attribute.'''
        self.path_info = None
        if self.ready:
            self.path_info = path_info if path_info else None
            if not self.path_info:
                self.ready = False
                self.logger.error('Unable to set_path_info.')
            else:
                self.datamodel_file_path        = path_info['filepath']
                self.datamodel_env_variable     = path_info['env_variable']
                self.datamodel_file_name        = path_info['file_name']
                self.datamodel_location_path    = path_info['location_path']
                self.datamodel_directory_names  = path_info['directory_names']
                self.datamodel_directory_depths = path_info['directory_depths']

    def set_species_values(self):
        '''Determine and populate self.species values'''
        if self.ready:
            self.set_potential_path_example_file_rows() # this also sets self.tree_id
            self.set_path_example_file_row()
            self.split_path()
            self.set_species_paths()
            self.set_species_location()
            self.set_location_example_datamodel_dict()
            self.set_species_ext()
            self.set_species_name()
            if self.ready:
                self.species['tree_edition']  = 'dr' + str(self.tree_id)
                self.species['location']      = self.species_location
                self.species['name']          = self.species_name
                self.species['ext']           = self.species_ext
                self.species['path_example']  = self.path_example_file_row.path
                self.species['note']          = self.species_note
            print('self.species: \n' + dumps(self.species,indent=1))
            input('pause')

    def set_potential_path_example_file_rows(self):
        '''Set the list self.potential_path_example_file_rows from self.datamodel_file_name'''
        self.tree_id = None
        self.potential_path_example_file_rows = list()
        if self.ready:
            self.logger.info('Setting path_examples for {} from the archive database'
                                .format(self.datamodel_file_path))
            self.set_session()
            self.set_tree_id_range()
            self.set_datamodel_filename_start()
            self.ready = bool(self.ready and self.datamodel_env_variable and self.session and
                              self.tree_id_range and self.datamodel_filename_start)
            if self.ready:
                for self.tree_id in self.tree_id_range:
                    self.set_env(tree_id      = self.tree_id,
                                 env_variable = self.datamodel_env_variable)
                    if self.ready:
                        env = self.env if self.env else None
                        if self.options and self.options.test:
                            directories = (self.session
                                               .query(Directory)
                                               .filter(Directory.env_id == env.id)
                                               .filter(Directory.location == self.options.location)
                                               .all())
                        else:
                            directories = (self.session.query(Directory)
                                                       .filter(Directory.env_id == env.id)
                                                       .all())
                        for directory in directories:
                            files = (self.session.query(File)
                                                 .filter(File.directory_id == directory.id)
                                                 .filter(File.location.like('%' + self.datamodel_filename_start + '%'))
                                                 .all())
                            if files:
                                self.logger.debug('Files found with file.path like %{0}%: {1}'
                                    .format(self.datamodel_filename_start,files))
                                self.potential_path_example_file_rows.extend(files)
                    if self.potential_path_example_file_rows: break
            if not self.potential_path_example_file_rows and self.tree_id:
                self.ready = False
                self.logger.error('Unable to populate_filespec_table_archive. ' +
                                  'self.potential_path_example_file_rows: {}'
                                    .format(self.potential_path_example_file_rows) +
                                  'self.tree_id: {}'.format(self.tree_id)
                                  )

    def set_session(self):
        '''Set sdssdb.sqlalchemy.archive.sas database session.'''
        if not self.session:
            self.session = database.Session()
        if not self.session:
            self.ready = False
            self.logger.error('Unable to set_session. ' +
                              'self.session: {}'.format(self.session))

    def set_tree_id_range(self):
        '''Set tree_ids to search for path_example.'''
        self.tree_id_range = list(range(15,6,-1))
        if not self.tree_id_range:
            self.ready = False
            self.logger.error('Unable to set_tree_id_range. ' +
                              'self.tree_id_range: {}'.format(self.tree_id_range))

    def set_datamodel_filename_start(self):
        '''Set the first part of the filename, up to the first punctuation character.'''
        self.datamodel_filename_start = None
        if self.ready:
            if self.datamodel_file_name:
                punctuation = str(string_punctuation).replace('_',str())
#                regex = "[\w']+|[.,!?;]"
                regex = "[\w']+|[" + punctuation + "]"
                string = self.datamodel_file_name.strip()
                matches = self.util.get_matches(regex=regex,string=string)
                match = matches[0] if matches else None
                self.datamodel_filename_start = match
            else:
                self.ready = False
                self.logger.error('Unable to set_datamodel_filename_start. ' +
                                  'self.datamodel_file_name: {}'.format(self.datamodel_file_name))
            if not self.datamodel_filename_start:
                self.ready = False
                self.logger.error('Unable to set_datamodel_filename_start. ' +
                                  'self.datamodel_filename_start: {}'
                                    .format(self.datamodel_filename_start))

    def set_env(self,tree_id=None,env_variable=None):
        '''Set env table row from tree_id and env_variable.'''
        self.env = None
        if self.ready:
            if tree_id and env_variable:
                self.set_session()
                if self.ready:
                    self.env = (self.session.query(Env)
                                            .filter(Env.tree_id == tree_id)
                                            .filter(Env.label == env_variable)
                                            .one())
            else:
                self.ready = False
                self.logger.error('Unable to set_env. ' +
                                  'tree_id: {}, '.format(tree_id) +
                                  'env_variable: {}, '.format(env_variable)
                                  )
            if not self.env:
                self.ready = False
                self.logger.error('Unable to set_env. ' +
                                  'self.env: {}'.format(self.env))


    def set_species_location(self):
        '''Set species_location from self.datamodel_directory_names and text
            substitution conventions'''
        self.species_location = str()
        if self.ready:
            if self.datamodel_directory_names:
                if not self.directory_substitution_dict: self.set_directory_substitution_dict()
                names = list()
                for directory_name in self.datamodel_directory_names:
                    if self.ready:
                        if directory_name in self.directory_substitution_dict:
                            name = self.directory_substitution_dict[directory_name]
                        else:
                            self.ready = False
                            self.logger.error('Unable to set_filespec_tree_id. ' +
                                              'self.filespec_dict: {}, '.format(self.filespec_dict)
                                              )
                        names.append(name)
                self.species_location = join(*names)
            # self.species_location can be empty
#            else:
#                self.ready = False
#                self.logger.error('Unable to set_species_location. ' +
#                                  'self.datamodel_directory_names: {}'
#                                    .format(self.datamodel_directory_names))
#            if not self.species_location:
#                self.ready = False
#                self.logger.error('Unable to set_species_location. ' +
#                                  'self.species_location: {}'.format(self.species_location))

    def set_location_example_datamodel_dict(self):
        '''Validate that the example_location_path and the datamodel_location_path
            follow the same naming convention. If so, create the dictionary
            location_example_datamodel_dict which provides a mapping from the
            example_location_path to datamodel_location_path. If not, add a
            comment to the note attribute.'''
        self.location_example_datamodel_dict = dict()
        if self.ready:
            if self.example_location_path and self.datamodel_directory_names:
                split_example = self.example_location_path.split('/')
                if len(split_example) == len(self.datamodel_directory_names):
                    self.location_example_datamodel_dict = (
                        dict(zip(split_example,self.datamodel_directory_names)))
                else:
                    note = ("ERROR: The example and datamodel location paths don't " +
                            "have the same number of directories. " +
                            "self.example_location_path: {}".format(self.example_location_path) +
                            "self.datamodel_directory_names: {}".format(self.datamodel_directory_names)
                            )
                    self.species_note += note + '\n'
                    self.logger.warning(note)
            # self.example_location_path and self.datamodel_directory_names can be empty
#            else:
#                self.ready = False
#                self.logger.error('Unable to set_location_example_datamodel_dict. ' +
#                                  'self.example_location_path: {}'
#                                    .format(self.example_location_path) +
#                                  'self.datamodel_directory_names: {}'
#                                    .format(self.datamodel_directory_names)
#                                    )

    def set_directory_substitution_dict(self,filename='directory_substitutions.yaml'):
        '''Set directory_substitution_dict from directory_substitutions.yaml.'''
        self.directory_substitution_dict = None
        if self.ready:
            self.set_yaml_dir()
            self.ready = bool(self.yaml_dir and filename)
            if self.ready:
                self.set_yaml_data(dir=self.yaml_dir,filename=filename)
                self.directory_substitution_dict = self.yaml_data if self.yaml_data else None
            else:
                self.ready = False
                self.logger.error('Unable to set_directory_substitution_dict. ' +
                                  'filename: {}'.format(filename))
            if not self.directory_substitution_dict:
                self.ready = False
                self.logger.error('Unable to set_directory_substitution_dict. ' +
                                  'self.directory_substitution_dict: {}'
                                    .format(self.directory_substitution_dict))

    def set_yaml_dir(self,yaml_dir=None):
        '''Set DATAMODEL_PARSER_YAML_DIR'''
        self.yaml_dir = None
        if self.ready:
            self.util.set_yaml_dir(yaml_dir=yaml_dir)
            self.yaml_dir = self.util.yaml_dir
            self.ready = self.util.ready
        else: pass # Let Util.set_yaml_dir do the error logging

    def set_yaml_data(self,dir=None,filename=None):
        '''Create a data structure from the given yaml file'''
        self.yaml_data = None
        if self.ready:
            if dir and filename:
                self.util.set_yaml_data(dir=dir,filename=filename)
                self.yaml_data = self.util.yaml_data
                self.ready = self.util.ready
        else: pass # Let Util.set_yaml_data do the error logging

    def set_path_example_file_row(self):
        '''Set path_example_file_row from self.potential_path_example_file_rows'''
        ##### Under construction #####
        self.path_example_file_row = list()
        self.removed_potential_path_example_file_rows = list()
        if self.ready:
            if self.potential_path_example_file_rows:
                # restrict to expected file extensions
                self.set_file_extensions()
                path_example_file_rows = list()
                for file_row in self.potential_path_example_file_rows:
                    filepath = file_row.path if file_row else None
                    split = filepath.split('.') if filepath else None
                    ext = split[-1] if split else None
                    if ext in self.file_extensions:
                        path_example_file_rows.append(file_row)
                    else:
                        self.removed_potential_path_example_file_rows.append(filepath)
                        self.logger.debug('Removing potential_path_example: {}'.format(filepath))
                if len(path_example_file_rows) == 1:
                    self.path_example_file_row = path_example_file_rows[0]
                else:
                    # restrict to filenames that start with filename_start_hyphen
                    rows = list()
                    filename_start_hyphen = self.datamodel_filename_start + '-'
                    for file_row in path_example_file_rows:
                        filepath = file_row.path if file_row else None
                        if filename_start_hyphen in filepath:
                            rows.append(file_row)
                        else:
                            self.removed_potential_path_example_file_rows.append(filepath)
                            self.logger.debug('Removing potential_path_example: {}'.format(filepath))
                    if len(rows) == 1:
                        self.path_example_file_row = rows[0]
                    else:
                        self.ready = False
                        self.logger.error('Unable to set_path_example_file_row. ' +
                                          'Multiple path_examples found. Need to restrict.' +
                                          'self.path_example_file_row: {}'
                                            .format(self.path_example_file_row))
            else:
                self.ready = False
                self.logger.error('Unable to set_path_example_file_row. ' +
                                  'self.potential_path_example_file_rows: {}'
                                    .format(self.potential_path_example_file_rows))
            if not self.path_example_file_row:
                self.ready = False
                self.logger.error('Unable to set_path_example_file_row. ' +
                                  'self.path_example_file_row: {}'
                                    .format(self.path_example_file_row))

    def set_file_extensions(self):
        '''Set list of file extensions of interest for path_examples'''
        self.file_extensions = ['dat.gz','fits','tar.gz','dat','log.html','log',
                                'log.gz','png','ply','apz','par','hdr','o',
                                'fit.gz','fits.gz','sha1sum','ps','fits.bz2',
                                'txt','html','model','rdzw.gz',
                                ]

    def split_path(self):
        '''Split the path of the found path_example_file_row'''
        self.example_name = None
        self.example_location_path = None
        if self.ready:
            if self.path_example_file_row:
                # find location_name
                filepath = (self.path_example_file_row.path
                             if self.path_example_file_row else None)
                self.set_env(tree_id      = self.tree_id,
                             env_variable = self.datamodel_env_variable)
                env_location = self.env.location if self.env else None
                split = (filepath.split(env_location)
                         if filepath and env_location else None)
                location_name = split[1] if split else None
                # separate location and name
                split = location_name.split('/') if location_name else None
                self.example_name = split[-1] if split else None
                self.example_location_path = '/'.join(split[:-1]) if split else None
                if self.example_location_path.startswith('/'):
                    self.example_location_path = self.example_location_path[1:]
                if self.example_location_path.endswith('/'):
                    self.example_location_path = self.example_location_path[:-1]
            else:
                self.ready = False
                self.logger.error('Unable to split_path. ' +
                                  'self.path_example_file_row: {}'
                                    .format(self.path_example_file_row))
            if not self.example_name: # self.example_location_path can be None
                self.ready = False
                self.logger.error('Unable to split_path. ' +
                                  'self.example_name: {}'.format(self.example_name))

    def set_species_paths(self):
        '''Set a list of species_paths from the CFG files in
            $DATAMODEL_PARSER_TREE_DATA_DIR'''
        self.species_paths = dict()
        if self.ready:
            if self.datamodel_filename_start:
                self.set_env_variable_dir(env_variable='DATAMODEL_PARSER_TREE_DATA_DIR')
                self.set_filenames(directory=self.env_variable_dir)
                self.filenames.sort()
                if self.ready:
                    config = ConfigParser()
                    for filename in self.filenames:
                        config.read(join(self.env_variable_dir,filename))
                        if self.datamodel_filename_start in config['PATHS']:
                            self.species_paths[filename] = config['PATHS'][self.datamodel_filename_start]
            else:
                self.ready = False
                self.logger.error('Unable to set_species_paths. ' +
                                  'self.path_example_file_row: {}'
                                    .format(self.path_example_file_row))
            if not self.example_name: # self.example_location_path can be None
                self.ready = False
                self.logger.error('Unable to set_species_paths. ' +
                                  'self.example_name: {}'.format(self.example_name))


    def set_filenames(self,directory=None):
        '''Set a list of filenames in the directory given.'''
        self.filenames = list()
        if self.ready:
            if directory:
                for (dirpath, dirnames, filenames) in walk(directory):
                    if filenames:
                        for filename in filenames:
                            self.filenames.append(filename)
            else:
                self.ready = False
                self.logger.error('Unable to set_filenames. ' +
                                  'directory: {}'.format(directory))
            if not self.filenames:
                self.ready = False
                self.logger.error('Unable to set_filenames. ' +
                                  'self.filenames: {}'.format(self.filenames))

    def set_species_ext(self):
        '''Set the file extension for self.example_name'''
        self.species_ext = None
        if self.ready:
            if self.example_name:
                split = self.example_name.split('.')
                self.species_ext = split[-1] if split else None
            else:
                self.ready = False
                self.logger.error('Unable to set_species_ext. ' +
                                  'self.example_name: {}'.format(self.example_name))
            if not self.species_ext:
                self.ready = False
                self.logger.error('Unable to set_species_ext. ' +
                                  'self.species_ext: {}'.format(self.species_ext))

    def set_species_name(self):
        '''Set the {text substitution} name for self.species_path_example'''
        self.species_name = None
        if self.ready:
            if self.example_name and self.location_example_datamodel_dict:
                self.species_name = self.example_name
                dictionary = self.location_example_datamodel_dict
                for key in dictionary.keys():
                    value = self.directory_substitution_dict[dictionary[key]]
                    self.species_name = self.species_name.replace(key,value)
            else: self.species_name = self.example_name
            # self.location_example_datamodel_dict can be empty
#            else:
#                self.ready = False
#                self.logger.error('Unable to set_species_name. ' +
#                                  'self.example_name: {}'
#                                    .format(self.example_name))
#            if not self.species_name:
#                self.ready = False
#                self.logger.error('Unable to set_species_name. ' +
#                                  'self.species_name: {}'.format(self.species_name))


