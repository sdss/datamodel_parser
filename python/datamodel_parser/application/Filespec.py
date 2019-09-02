from datamodel_parser.application import Util
from string import punctuation as string_punctuation
from sdssdb.sqlalchemy.archive.sas import *
from os.path import basename, dirname, exists, isdir, join, splitext
from os import environ, walk
from configparser import RawConfigParser
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
            self.datamodel_filepath             = None
            self.datamodel_env_variable          = None
            self.datamodel_filename             = None
            self.datamodel_filename_start       = None
            self.datamodel_directory_names       = None
            self.directory_substitution_dict     = None
            self.substitution_location                = None
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
                self.datamodel_filepath         = path_info['filepath']
                self.datamodel_env_variable     = path_info['env_variable']
                self.datamodel_filename         = path_info['file_name']
                self.datamodel_location_path    = path_info['location_path']
                self.datamodel_directory_names  = path_info['directory_names']
                self.datamodel_directory_depths = path_info['directory_depths']

    def set_species_values(self):
        '''Determine and populate self.species values'''
        if self.ready:
            self.set_substitution_filename()
            self.set_substitution_location()
            self.set_substitution_tree_paths()
            self.set_potential_path_example_file_rows() # this also sets self.tree_id
            self.set_example_filepaths()
            print('self.datamodel_filepath: %r' % self.datamodel_filepath)
            print('self.datamodel_filename: %r' % self.datamodel_filename)
            print('self.datamodel_filename_start: %r' % self.datamodel_filename_start)
            print('self.substitution_filename: %r' % self.substitution_filename)
            print('self.substitution_filename_start: %r' % self.substitution_filename_start)
            print('self.filename_start: %r' % self.filename_start)
            print('self.substitution_location: %r' % self.substitution_location)
            print('self.example_filepaths: %r' % self.example_filepaths)
            input('pause')
            self.set_location_example_datamodel_dict()
            self.set_species_name()
#            self.validate_species_path()
            if self.ready:
                self.species['tree_edition']  = 'dr' + str(self.tree_id)
                self.species['location']      = self.substitution_location
                self.species['name']          = self.species_name
                self.species['ext']           = self.species_ext
                self.species['path_example']  = self.path_example_file_row.path
                self.species['note']          = self.species_note
            print('self.species: \n' + dumps(self.species,indent=1))
            input('pause')

    def set_substitution_filename(self,filename='filename_substitutions.yaml'):
        '''Set the filename text substitution dictionary.'''
        self.substitution_filename = None
        if self.ready:
            self.set_yaml_dir()
            self.ready = bool(self.yaml_dir and filename and self.datamodel_filepath)
            if self.ready:
                self.set_yaml_data(dir=self.yaml_dir,filename=filename)
                name = (self.yaml_data[self.datamodel_filepath]
                        if self.datamodel_filepath else None)
                self.substitution_filename = (name[0] if isinstance(name,list)
                                         else name    if isinstance(name,str)
                                         else None)
#                print('name: %r' % name)
#                print('self.substitution_filename: %r' % self.substitution_filename)
#                input('pause')

            if not self.substitution_filename:
                self.ready = False
                self.logger.error('Unable to set_substitution_filename. ' +
                                  'self.substitution_filename: {}, '
                                    .format(self.substitution_filename) +
                                  'filename: {}, '.format(filename) +
                                  'self.datamodel_filepath: {}, '
                                    .format(self.datamodel_filepath)
                                  )

    def set_substitution_location(self):
        '''Set substitution_location from self.datamodel_directory_names and text
            substitution conventions'''
        self.substitution_location = str()
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
                self.substitution_location = join(*names)
            ### self.substitution_location can be empty ###
            else: pass
            if not self.substitution_location: pass

    def set_potential_path_example_file_rows(self):
        '''Set the list self.potential_path_example_file_rows from self.datamodel_filename'''
        self.tree_id = None
        self.potential_path_example_file_rows = list()
        if self.ready:
            self.logger.info('Setting path_examples for {} from the archive database'
                                .format(self.datamodel_filepath))
            self.set_session()
            self.set_tree_id_range()
            self.set_filename_start()
            self.ready = bool(self.ready and self.datamodel_env_variable and
                              self.session and self.tree_id_range and self.filename_start)
            if self.ready:
                for self.tree_id in self.tree_id_range:
                    self.set_env(tree_id      = self.tree_id,
                                 env_variable = self.datamodel_env_variable)
                    env_id = self.env.id if self.env else None

                    if env_id:
                        if self.options and self.options.location:
                            self.set_directories(env_id=env_id,
                                                 location=self.options.location)
                        else:
                            self.set_directories(env_id=env_id)
                    directories = self.directories if self.directories else None

                    if directories:
                        for directory in directories:
                            self.set_files(directory_id   = directory.id,
                                           filename_start = self.filename_start)
                            if self.files:
                                self.logger.debug(
                                    'Files found with file.path like %{0}%: {1}'
                                        .format(self.filename_start,self.files))
                                self.potential_path_example_file_rows.extend(self.files)
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

    def set_filename_start(self):
        self.filename_start = None
        if self.ready:
            self.set_substitution_filename_start()
            self.set_datamodel_filename_start()
            sub_start = self.substitution_filename_start
            data_start = self.datamodel_filename_start
            self.filename_start = (sub_start if sub_start and sub_start != 'None'
                              else data_start if data_start
                              else None)
        if not self.filename_start:
            self.ready = False
            self.logger.error('Unable to set_filename_start. ' +
                              'self.filename_start: {}'.format(self.filename_start))

    def set_substitution_filename_start(self):
        '''Set the first part of the filename, up to the first punctuation character.'''
        self.substitution_filename_start = None
        if self.ready:
            if self.substitution_filename:
                split_char = ('{' if '{' in self.substitution_filename
                         else '.' if '.' in self.substitution_filename
                         else None)
                split = (self.substitution_filename.split(split_char)
                         if split_char else [self.substitution_filename])
                filename_start = split[0] if split else None
                self.substitution_filename_start = (
                    filename_start if filename_start and filename_start != 'None'
                    else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_substitution_filename_start. ' +
                                  'self.substitution_filename: {}'.format(self.substitution_filename))
            # self.substitution_filename_start can be None
            if not self.substitution_filename_start: pass

    def set_datamodel_filename_start(self):
        '''Set the first part of the filename, up to the first punctuation character.'''
        self.datamodel_filename_start = None
        if self.ready:
            if self.datamodel_filename:
                punctuation = str(string_punctuation).replace('_',str())
#                regex = "[\w']+|[.,!?;]"
                regex = "[\w']+|[" + punctuation + "]"
                string = self.datamodel_filename.strip()
                matches = self.util.get_matches(regex=regex,string=string)
                match = matches[0] if matches else None
                self.datamodel_filename_start = match
            else:
                self.ready = False
                self.logger.error('Unable to set_datamodel_filename_start. ' +
                                  'self.datamodel_filename: {}'.format(self.datamodel_filename))
            if not self.datamodel_filename_start:
                self.ready = False
                self.logger.error('Unable to set_datamodel_filename_start. ' +
                                  'self.datamodel_filename_start: {}'
                                    .format(self.datamodel_filename_start))

    def set_env(self,tree_id=None,env_variable=None):
        '''Set env table row from tree_id and env_variable.'''
        self.env = None
        if self.ready:
            if self.session and tree_id and env_variable:
                try:
                    self.env = (self.session.query(Env)
                                            .filter(Env.tree_id == tree_id)
                                            .filter(Env.label == env_variable)
                                            .one())
                except:
                    self.env = None
            else:
                self.ready = False
                self.logger.error('Unable to set_env. ' +
                                  'self.session: {}, '.format(self.session) +
                                  'tree_id: {}, '.format(tree_id) +
                                  'env_variable: {}, '.format(env_variable)
                                  )
            ### self.env can be None ###
            if not self.env: pass

    def set_directories(self,env_id=None,location=None):
        '''Set directories table row from env_id and location.'''
        self.directories = None
        if self.ready:
            if self.session and env_id: ### location can be None
                if location:
                    try:
                        self.directories = (self.session
                                                .query(Directory)
                                                .filter(Directory.env_id == env_id)
                                                .filter(Directory.location == location)
                                                .all())
                    except:
                        self.directories = None
                else:
                    try:
                        self.directories = (self.session
                                                .query(Directory)
                                                .filter(Directory.env_id == env_id)
                                                .all())
                    except:
                        self.directories = None
            else:
                self.ready = False
                self.logger.error('Unable to set_directories. ' +
                                  'self.session: {}, '.format(self.session) +
                                  'env_id: {}, '.format(env_id)
                                  )
            ### self.directories can be None ###
            if not self.directories: pass

    def set_files(self,directory_id=None,filename_start=None):
        '''Set files table row from directory_id and filename_start.'''
        self.files = None
        if self.ready:
            if self.session and directory_id and filename_start:
                try:
                    self.files = (self.session
                                      .query(File)
                                      .filter(File.directory_id == directory_id)
                                      .filter(File.location.like('%' + filename_start + '%'))
                                      .all())
                except:
                    self.files = None
            else:
                self.ready = False
                self.logger.error('Unable to set_files. ' +
                                  'self.session: {}, '.format(self.session) +
                                  'directory_id: {}, '.format(directory_id) +
                                  'filename_start: {}, '.format(filename_start)
                                  )
            ### self.files can be None ###
            if not self.files: pass

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
            ### self.example_location_path and self.datamodel_directory_names can be empty ###
            else: pass

    def set_directory_substitution_dict(self,
                                        filename='directory_substitutions_init.yaml'):
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

    def set_example_filepaths(self):
        '''Split the path of the found path_example_file_row'''
        self.example_filepaths = list()
        if self.ready:
            if self.potential_path_example_file_rows:
                N = 10 # number of file table rows to examine
                if len(self.potential_path_example_file_rows) > N:
                    self.logger.info('Truncating the number of rows found to {}'.format(N))
                    self.potential_path_example_file_rows = self.potential_path_example_file_rows[:N]
                for file_row in self.potential_path_example_file_rows:
                    filepath = file_row.path if file_row else None

                    # get location_name
                    self.set_env(tree_id      = self.tree_id,
                                 env_variable = self.datamodel_env_variable)
                    env_location = self.env.location if self.env else None
                    split = (filepath.split(env_location)
                             if filepath and env_location else None)
                    location_name = split[1] if split else None

                    # separate name, location, and extension
                    split = location_name.split('/') if location_name else None
                    example_name = split[-1] if split else None
                    example_location_path = '/'.join(split[:-1]) if split else str()
                    if example_name: # example_location_path can be empty
                        self.set_example_ext(filename=example_name)
                        if example_location_path.startswith('/'):
                            example_location_path = example_location_path[1:]
                        if example_location_path.endswith('/'):
                            example_location_path = example_location_path[:-1]
                        example_filepath = {'name'    : example_name,
                                            'location': example_location_path,
                                            'ext'     : self.example_ext,
                                            }
                        self.example_filepaths.append(example_filepath)
        
#                    print('filepath: %r' % filepath)
#                    print('env_location: %r' % env_location)
#                    print('self.tree_id: %r' % self.tree_id)
#                    print('location_name: %r' % location_name)
#                    print('split: %r' % split)
#                    print('example_name: %r' % example_name)
#                    print('example_location_path: %r' % example_location_path)
#                    input('pause')

            else:
                self.ready = False
                self.logger.error('Unable to set_example_filepaths. ' +
                                  'self.potential_path_example_file_rows: {}'
                                    .format(self.potential_path_example_file_rows))
            if not self.example_filepaths: # self.example_location_path can be None
                self.ready = False
                self.logger.error('Unable to set_example_filepaths. ' +
                                  'self.example_filepaths: {}'.format(self.example_filepaths))

    def set_example_ext(self,filename=None):
        '''Set the file extension for the given filename'''
        self.example_ext = None
        if self.ready:
            self.set_file_extensions()
            if filename and self.file_extensions:
                found_ext = False
                for ext in self.file_extensions:
                    if ext in filename:
                        found_ext = True
                        break
                self.example_ext = ext if found_ext else None
            if not self.example_ext:
                self.ready = False
                self.logger.error('Unable to set_example_ext. '
                                  'Please manually add extension to Filespec.file_extensions. ' +
                                  'filename: {}, '.format(filename) +
                                  'self.file_extensions: {}, '.format(self.file_extensions))

    def set_file_extensions(self):
        '''Set list of file extensions of interest for path_examples'''
        self.file_extensions = ['dat.gz','fits.gz','fits.bz2','fit.gz','tar.gz',
                                'log.gz','log.html','rdzw.gz',
                                'dat','fits','fit','tar','log'
                                ,'rdzw','png','ply','apz','par','hdr','o',
                                'sha1sum','ps','txt','html','model',
                                ]

    def set_substitution_tree_paths(self):
        '''Set a list of substitution_tree_paths from the CFG files in
            $DATAMODEL_PARSER_TREE_DATA_DIR'''
        self.substitution_tree_paths = dict()
        if self.ready:
#            if self.datamodel_filename_start:
            self.set_env_variable_dir(env_variable='DATAMODEL_PARSER_TREE_DATA_DIR')
            self.set_filenames(directory=self.env_variable_dir)
            if self.ready:
                self.filenames.sort()
                for filename in self.filenames:
                    config = RawConfigParser()
                    config.optionxform = str # disable setting section keys to lower()
                    config.read(join(self.env_variable_dir,filename))
                    basename = splitext(filename)[0] if filename else None
                    self.substitution_tree_paths[basename] = dict()
                    if config.has_section('PATHS'):
                        for path in config['PATHS']:
                            self.substitution_tree_paths[basename][path] = config['PATHS'][path]
            if not self.substitution_tree_paths:
                self.ready = False
                self.logger.error('Unable to set_substitution_tree_paths. ' +
                                  'self.substitution_tree_paths: {}'.format(self.substitution_tree_paths))


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
            ### self.location_example_datamodel_dict can be empty ###
#            else:
#                self.ready = False
#                self.logger.error('Unable to set_species_name. ' +
#                                  'self.example_name: {}'
#                                    .format(self.example_name))
#            if not self.species_name:
#                self.ready = False
#                self.logger.error('Unable to set_species_name. ' +
#                                  'self.species_name: {}'.format(self.species_name))


