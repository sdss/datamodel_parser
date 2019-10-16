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
                          self.logger  and
                          self.options
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose
            self.datamodel_filepath                 = None
            self.datamodel_env_variable             = None
            self.datamodel_filename                 = None
            self.datamodel_directory_names          = None
            self.directory_substitution_dict        = None
            self.tree_id                            = None
            self.species_path_example               = None
            self.species_name                       = None
            self.path_example_file_row              = None
            self.session                            = None
            self.env                                = None
            self.path_example_file_row              = None
            self.species_note                       = str()
            self.location_example_datamodel_dict    = None
            self.failed_datamodel_filepaths         = list()
            self.file_extensions                    = None
            self.yaml_dir                           = None
            self.found_consistent_example_filepath  = None
            self.substitution_filenames             = None
            self.substitution_location              = None
            self.substitution_locations             = None
            self.filename_search_strings            = None
            self.consistent_example_filepath        = None
            self.filepaths                          = None
            self.valid_env_variable                 = None

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

    def initialize_species(self,species=None):
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

    def set_valid_env_variable(self):
        '''Determine if the environmental variable exists in the archive db.'''
        self.valid_env_variable = None
        if self.ready:
            self.logger.info('Checking in archive db for env_variable: {}'
                .format(self.datamodel_env_variable))
            if not self.session: self.set_session()
            self.set_env(env_variable = self.datamodel_env_variable)
            if self.env:
                self.valid_env_variable = True
                self.logger.info('Found env_variable: {}'
                    .format(self.datamodel_env_variable))
            else:
                self.failed_datamodel_filepaths.append(self.datamodel_filepath)
                self.logger.info('WARNING: env_variable {} '.format(self.datamodel_env_variable) +
                                 'not found in archive db. Skipping')
        
    def set_species(self):
        '''Determine and populate self.species values'''
        if self.ready:
            self.logger.info('Setting species values for: %r' % self.datamodel_filepath)
            self.set_filename_search_string()
            if self.filename_search_string:
                self.set_substitution_values()
                if self.ready:
                    self.find_species_values()
                    if self.found_consistent_example_filepath:
                        self.set_species_values()
            else:
                self.failed_datamodel_filepaths.append(self.datamodel_filepath)
                # let set_filename_search_string() do error logging

    def set_substitution_values(self):
        if self.ready:
            self.set_substitution_filename()
            self.set_substitution_location()
            self.set_substitution_filepath()

    def set_env_location(self):
        self.env_location = None
        if self.ready:
            if self.tree_id and self.datamodel_env_variable:
                self.set_env(tree_id      = self.tree_id,
                             env_variable = self.datamodel_env_variable)
                self.env_location = self.env.location if self.env else None
            else:
                self.ready = False
                self.logger.error('Unable to set_env_location. '+
                                  'self.tree_id: {}, '.format(self.tree_id) +
                                  'self.datamodel_env_variable: {}, '
                                    .format(self.datamodel_env_variable)
                                  )
            if not self.env_location:
                # self.env_location can be empty
                self.logger.debug('No env_location found for tree_id: {}.'
                    .format(self.tree_id))

    def set_env_id(self):
        self.env_id = None
        if self.ready:
            if self.tree_id and self.datamodel_env_variable:
                self.set_env(tree_id      = self.tree_id,
                             env_variable = self.datamodel_env_variable)
                self.env_id = self.env.id if self.env else None
            else:
                self.ready = False
                self.logger.error('Unable to set_env_id. '+
                                  'self.tree_id: {}, '.format(self.tree_id) +
                                  'self.datamodel_env_variable: {}, '
                                    .format(self.datamodel_env_variable)
                                  )
            if not self.env_id:
                # self.env_id can be empty for certain tree_id's
                self.logger.debug('No env_id found for tree_id: {}.'
                    .format(self.tree_id))

    def set_filename_search_string(self,datamodel_filepath=None):
        '''Set the filename text search_string dictionary.'''
        self.filename_search_string = None
        if self.ready:
            datamodel_filepath = (datamodel_filepath if datamodel_filepath
                                  else self.datamodel_filepath)
            if not self.filename_search_strings: self.set_filename_search_strings()
            self.ready = bool(self.filename_search_strings and datamodel_filepath)
            if self.ready:
                name = self.filename_search_strings[datamodel_filepath]
                self.filename_search_string = (name[0] if isinstance(name,list)
                                          else name    if isinstance(name,str)
                                          else None)
            if not self.filename_search_string:
                self.ready = False
                self.logger.error('Unable to set_filename_search_string. ' +
                                  'self.filename_search_string: {}, '
                                    .format(self.filename_search_string) +
                                  'datamodel_filepath: {}, '
                                    .format(datamodel_filepath)
                                  )
            else:
                if self.filename_search_string == 'None':
                    self.logger.warning('Need to assign self.filename_search_string ' +
                                        'in filename_search_strings.yaml. '
                                        'Skipping this file. ' +
                                        'self.filename_search_string: {0!r}'
                                            .format(self.filename_search_string))
                    self.filename_search_string = None

    def set_filename_search_strings(self,filename='filename_search_strings.yaml'):
        '''Set the filename text search_string dictionary.'''
        self.filename_search_strings = None
        if self.ready:
            if not self.yaml_dir: self.set_yaml_dir()
            self.ready = bool(self.yaml_dir and filename)
            if self.ready:
                self.set_yaml_data(dir=self.yaml_dir,filename=filename)
                self.filename_search_strings = self.yaml_data if self.yaml_data else None
            if not self.filename_search_strings:
                self.ready = False
                self.logger.error('Unable to set_filename_search_strings. ' +
                                  'self.filename_search_strings: {}, '
                                    .format(self.filename_search_strings)
                                  )

    def set_substitution_filename(self,datamodel_filepath=None):
        '''Set the filename text substitution dictionary.'''
        self.substitution_filename = None
        if self.ready:
            datamodel_filepath = (datamodel_filepath if datamodel_filepath
                                  else self.datamodel_filepath)
            if not self.substitution_filenames: self.set_substitution_filenames()
            self.ready = bool(self.substitution_filenames and datamodel_filepath)
            if self.ready:
                name = (self.substitution_filenames[datamodel_filepath]
                        if datamodel_filepath in self.substitution_filenames
                        else None)
                self.substitution_filename = (name[0] if isinstance(name,list)
                                         else name    if isinstance(name,str)
                                         else None)
            if not self.substitution_filename:
                self.ready = False
                self.logger.error('Unable to set_substitution_filename. ' +
                                  'self.substitution_filename: {}, '
                                    .format(self.substitution_filename) +
                                  'datamodel_filepath: {}, '
                                    .format(datamodel_filepath)
                                  )

    def set_substitution_filenames(self,filename='filename_substitutions.yaml'):
        '''Set the filename text substitution dictionary.'''
        self.substitution_filenames = None
        if self.ready:
            if not self.yaml_dir: self.set_yaml_dir()
            self.ready = bool(self.yaml_dir and filename)
            if self.ready:
                self.set_yaml_data(dir=self.yaml_dir,filename=filename)
                self.substitution_filenames = self.yaml_data if self.yaml_data else None
            if not self.substitution_filenames:
                self.ready = False
                self.logger.error('Unable to set_substitution_filenames. ' +
                                  'self.substitution_filenames: {}, '
                                    .format(self.substitution_filenames)
                                  )

    def set_substitution_location(self):
        '''Set the location text substitution dictionary.'''
        self.substitution_location = None
        if self.ready:
            if not self.substitution_locations: self.set_substitution_locations()
            self.ready = bool(self.substitution_locations and self.datamodel_filepath)
            if self.ready:
                loc = self.substitution_locations[self.datamodel_filepath]
                self.substitution_location = (loc[0] if isinstance(loc,list)
                                         else loc    if isinstance(loc,str)
                                         else None)
            # self.substitution_location can be empty
            if not self.substitution_location: pass

    def set_substitution_locations(self,filename='location_substitutions.yaml'):
        '''Set the location text substitution dictionary.'''
        self.substitution_locations = None
        if self.ready:
            if not self.yaml_dir: self.set_yaml_dir()
            self.ready = bool(self.yaml_dir and filename)
            if self.ready:
                self.set_yaml_data(dir=self.yaml_dir,filename=filename)
                self.substitution_locations = self.yaml_data if self.yaml_data else None
            if not self.substitution_locations:
                self.ready = False
                self.logger.error('Unable to set_substitution_locations. ' +
                                  'self.substitution_locations: {}, '
                                    .format(self.substitution_locations)
                                  )

    def set_substitution_filepath(self):
        '''Set a dictionary with text substitution filename, location, and extension.'''
        self.substitution_filepath = dict()
        if self.ready:
            if self.substitution_filename: # self.substitution_location can be empty
                self.substitution_filepath = {'name'    : self.substitution_filename,
                                              'location': self.substitution_location,
                                              'ext'     : str()}
                if self.substitution_filename != 'None':
                    self.set_extension(filename=self.substitution_filename)
                    self.substitution_filepath['ext'] = self.extension

    def set_extension(self,filename=None):
        '''Set the file extension for the given filename'''
        self.extension = None
        if self.ready:
            if not self.file_extensions: self.set_file_extensions()
#            print('filename: %r' % filename)
#            input('pause')
            if filename and self.file_extensions:
                found_ext = False
                for ext in self.file_extensions:
                    if '.' in filename:
                        if '.' + ext in filename:
                            found_ext = True
                            break
                    else:
                        found_ext = True
                        ext = str()
                        break
                self.extension = ext if found_ext else str()
            if self.extension is None:
                #self.ready = False
                self.extension = str()
                self.logger.warning('Unable to set_extension. '
                                    'Please manually add extension to Filespec.file_extensions. ' +
                                    'filename: {}, '.format(filename) +
                                    'self.file_extensions: {}, '.format(self.file_extensions))

    def set_potential_path_example_file_rows(self):
        '''Set the list self.potential_path_example_file_rows
            from self.datamodel_filename'''
        self.potential_path_example_file_rows = list()
        if self.ready:
            self.logger.debug('Attempting to set path_examples from archive db ' +
                              'for {} '.format(self.datamodel_filepath))
            self.ready = bool(self.ready and self.datamodel_env_variable and
                              self.session and self.tree_id and
                              self.filename_search_string and self.env_id)
            if self.ready:
                self.set_directories(env_id=self.env_id,
                                     location=self.options.location,
                                     limit=self.options.limit)
                directories = self.directories if self.directories else None

                if directories:
                    for directory in directories:
                        self.set_files(directory_id   = directory.id,
                                       search_string = self.filename_search_string,
                                       limit=self.options.limit)
                        if self.files:
                            self.potential_path_example_file_rows.extend(self.files)
        
            if self.ready:
                if self.potential_path_example_file_rows:
                    self.logger.info('Found potential_path_example_file_rows for ' +
                                      'self.tree_id: {}'.format(self.tree_id))
                else:
                    # self.potential_path_example_file_rows can be empty
                    self.logger.debug('No potential_path_example_file_rows found for ' +
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
        self.tree_id_range = list()
        if self.ready:
            tree_id_range = list(range(15,6,-1))
            self.tree_id_range = (self.options.tree_ids
                                  if self.options and self.options.tree_ids
                                  else tree_id_range)
            if not self.tree_id_range:
                self.ready = False
                self.logger.error('Unable to set_tree_id_range. ' +
                                  'self.tree_id_range: {}'.format(self.tree_id_range))

    def find_species_values(self):
        '''Find values of the species database.'''
        if self.ready:
            self.logger.debug('self.tree_id: %r' % self.tree_id)
            self.potential_path_example_file_rows = list()
            self.set_env_location()
            self.set_env_id()
            if self.env_location and self.env_id:
                self.set_potential_path_example_file_rows()
            if self.potential_path_example_file_rows:
                self.split_example_filepaths()
                self.set_consistent_example_filepath()
            else:
                self.found_consistent_example_filepath = False
            #self.set_substitution_tree_paths()  ### Incorporate me ###


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
            if self.session and env_variable:
                if tree_id:
                    try:
                        self.env = (self.session.query(Env)
                                                .filter(Env.tree_id == tree_id)
                                                .filter(Env.label == env_variable)
                                                .one())
                    except:
                        self.env = None
                else:
                    try:
                        self.env = (self.session.query(Env)
                                                .filter(Env.label == env_variable)
                                                .all())
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

    def set_directories(self,env_id=None,location=None,limit=None):
        '''Set directories table row from env_id and location.'''
        self.directories = None
        if self.ready:
            if self.session and self.tree_id and env_id: ### location and limit can be None
                limit = int(limit) if limit else None
                directory_query = (self.session
                                       .query(Directory)
                                       .filter(Directory.tree_id == self.tree_id)
                                       .filter(Directory.env_id == env_id)
                                   )
                if location and limit:
                    try: self.directories = (directory_query
                                                .filter(Directory.location == location)
                                                .limit(limit)
                                                .all())
                    except: self.directories = None
                elif location and not limit:
                    try: self.directories = (directory_query
                                                .filter(Directory.location == location)
                                                .all())
                    except: self.directories = None
                elif not location and limit:
                    try: self.directories = (directory_query
                                                .limit(limit)
                                                .all())
                    except: self.directories = None

                else:
                    try:
                        self.directories = (directory_query
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

    def set_files(self,directory_id=None,search_string=None,limit=None):
        '''Set files table row from directory_id and search_string.'''
        self.files = None
        if self.ready:
            if (self.session and directory_id and search_string and
                self.env_location and self.env_id
                ):
#                search_string = search_string.replace('_','\_')
                search_string = '/' + search_string
                search_string = '%' + search_string + '%'
                if limit:
                    try:
                        self.files = (self.session
                                          .query(File)
                                          .filter(File.env_id == self.env_id)
                                          .filter(File.directory_id == directory_id)
                                          .filter(File.location.like(search_string))
                                          .limit(limit)
                                          .all())
                    except:
                        self.files = None
                else:
                    try:
                        self.files = (self.session
                                          .query(File)
                                          .filter(File.env_id == self.env_id)
                                          .filter(File.directory_id == directory_id)
                                          .filter(File.location.like(search_string))
                                          .all())
                    except:
                        self.files = None

            else:
                self.ready = False
                self.logger.error('Unable to set_files. ' +
                                  'self.session: {}, '.format(self.session) +
                                  'directory_id: {}, '.format(directory_id) +
                                  'env_id: {}, '.format(env_id) +
                                  'search_string: {}, '.format(search_string)
                                  )
            ### self.files can be None ###
            if not self.files: pass

    def set_consistent_example_filepath(self):
        '''Find an example_filepath that is consistent with substitution_filepath.
            If found, set'''
        self.consistent_example_filepath = dict()
        if self.ready:
            if self.example_filepaths and self.substitution_filepath:
                s_name     = self.substitution_filepath['name']
                s_loc = self.substitution_filepath['location']
                s_ext = self.substitution_filepath['ext']
                note = str()
#                print('self.example_filepaths: %r' % self.example_filepaths)
#                input('pause')
                for example_filepath in self.example_filepaths:
                    e_name = example_filepath['name']
                    e_loc = example_filepath['location']
                    e_ext = example_filepath['ext']

                    # compare filenames
                    # filenames use -, _, and . so only the first few letters can be tested
                    # this is redundant since this is being tested by the SQL query
                    # using filename_search_string.yaml
                    zip_names = {i for i, (x,y) in enumerate(zip(e_name,s_name))
                                 if x != y}
                    consistent_name = ((zip_names == set()) or (min(zip_names) > 0)
                                        or s_name.startswith('{'))
                    if self.options and self.options.test and self.options.verbose:
                        self.logger.debug('e_name: {}\n'.format(e_name) +
                                          's_name: {}\n'.format(s_name) +
                                          'consistent_name: {}\n'.format(consistent_name)
                                          )

                    # compare location paths
                    e_loc_split = e_loc.split('/')
                    s_loc_split = s_loc.split('/')
                    if len(e_loc_split)==len(s_loc_split):
                        if len(e_loc_split) > 1:
                            consistent_loc = True
                        else:
                            # True if both empty or both non-empty else False
                            a = bool(e_loc_split[0])
                            b = bool(s_loc_split[0])
                            consistent_loc = not(a!=b)
                    else: consistent_loc = False
                    if self.options and self.options.test and self.options.verbose:
                        self.logger.debug('e_loc_split: {}\n'.format(e_loc_split) +
                                          's_loc_split: {}\n'.format(s_loc_split) +
                                          'consistent_loc: {}\n'.format(consistent_loc)
                                          )

                    # compare filename extensions
                    if '.' in e_ext and '.' in s_ext:
                        consistent_ext = (e_ext == s_ext)
                    elif '.' in e_ext or '.' in s_ext:
                        e_ext_split = e_ext.split('.')
                        s_ext_split = s_ext.split('.')
                        e_ext_0 = e_ext_split[0] if e_ext_split else e_ext
                        s_ext_0 = s_ext_split[0] if s_ext_split else s_ext
                        consistent_ext = (e_ext_0 == s_ext_0)
                    else:
                        consistent_ext = (e_ext == s_ext)
                    if self.options and self.options.test and self.options.verbose:
                        self.logger.debug('e_ext: {}\n'.format(e_ext) +
                                          's_ext: {}\n'.format(s_ext) +
                                          'consistent_ext: {}\n'.format(consistent_ext)
                                          )

                    # add note to consistent_example_filepath
                    if consistent_name and consistent_loc:
                        self.found_consistent_example_filepath = True
                        self.consistent_example_filepath = example_filepath
                        if not consistent_ext:
                            note += ('Inconsistent extensions. ' +
                                     'substitution_ext: {}, '.format(s_ext) +
                                     'example_ext: {0!r}'.format(e_ext) )
                        self.consistent_example_filepath['note'] = note
                        break
                if not self.found_consistent_example_filepath:
                    inconsistent_example_filepath = example_filepath
                    self.logger.debug('Unable to set_consistent_example_filepath. ' +
                                      'self.found_consistent_example_filepath: {}, '
                                        .format(self.found_consistent_example_filepath) +
                                      'self.substitution_filepath: {}, '
                                        .format(self.substitution_filepath))
                    self.logger.debug('inconsistent_example_filepath: \n' +
                                      dumps(inconsistent_example_filepath,indent=1))
            else:
                # self.example_filepaths can be empty
                self.logger.debug('Unable to set_consistent_example_filepath. ' +
                                  'self.substitution_filepath: {}, '
                                    .format(self.substitution_filepath) +
                                  'self.example_filepaths: {}, '
                                    .format(self.example_filepaths)
                                  )

    def set_species_values(self):
        '''Set values of the dictionary self.species.'''
        if self.ready:
            self.logger.info('Successfully found_consistent_example_filepath.')
            path_example = join('$' + self.datamodel_env_variable,
                                self.consistent_example_filepath['location'],
                                self.consistent_example_filepath['name']
                               )
            #path_example = self.consistent_example_filepath['filepath']
            self.species['tree_edition']  = 'dr' + str(self.tree_id)
            self.species['location']      = self.substitution_filepath['location']
            self.species['name']          = self.substitution_filepath['name']
            self.species['ext']           = self.consistent_example_filepath['ext']
            self.species['path_example']  = path_example
            self.species['note']          = self.consistent_example_filepath['note']


    def set_directory_substitution_dict(self,
                                        filename='directory_substitutions.yaml'):
        '''Set directory_substitution_dict from directory_substitutions.yaml.'''
        self.directory_substitution_dict = None
        if self.ready:
            if not self.yaml_dir: self.set_yaml_dir()
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
            if not self.yaml_dir: pass # Let Util.set_yaml_dir do the error logging

    def set_yaml_data(self,dir=None,filename=None):
        '''Create a data structure from the given yaml file'''
        self.yaml_data = None
        if self.ready:
            if dir and filename:
                self.util.set_yaml_data(dir=dir,filename=filename)
                self.yaml_data = self.util.yaml_data
                self.ready = self.util.ready
            else: pass # Let Util.set_yaml_data do the error logging

    def split_example_filepaths(self):
        '''Split the path of the found path_example_file_row'''
        self.example_filepaths = list()
        if self.ready:
            if self.potential_path_example_file_rows and self.env_location:
                self.logger.debug('Splitting filepaths')
                for file_row in self.potential_path_example_file_rows:
                    filepath = file_row.path if file_row else None

                    # get location_name
                    split = (filepath.split(self.env_location)
                             if filepath and self.env_location else None)
                    location_name = split[1] if split else None

                    # separate name, location, and extension
                    split = location_name.split('/') if location_name else None
                    example_name = split[-1] if split else None
                    example_location_path = '/'.join(split[:-1]) if split else str()
                    if example_name: # example_location_path can be empty
                        self.set_extension(filename=example_name)
                        if example_location_path.startswith('/'):
                            example_location_path = example_location_path[1:]
                        if example_location_path.endswith('/'):
                            example_location_path = example_location_path[:-1]
                        example_filepath = {'filepath': filepath,
                                            'name'    : example_name,
                                            'location': example_location_path,
                                            'ext'     : self.extension,
                                            }
                        self.example_filepaths.append(example_filepath)
        
#                    print('filepath: %r' % filepath)
#                    print('self.env_location: %r' % self.env_location)
#                    print('self.tree_id: %r' % self.tree_id)
#                    print('location_name: %r' % location_name)
#                    print('split: %r' % split)
#                    print('example_name: %r' % example_name)
#                    print('example_location_path: %r' % example_location_path)
#                    print('example_filepath: %r' % example_filepath)
#                    input('pause')

            else:
                # self.potential_path_example_file_rows can be empty
                self.logger.warning('Unable to split_example_filepaths. ' +
                                    'self.potential_path_example_file_rows: {}, '
                                        .format(self.potential_path_example_file_rows) +
                                    'self.env_location: {}, '.format(self.env_location))
            if not self.example_filepaths: # self.example_location_path can be None
                self.logger.warning('Unable to split_example_filepaths. ' +
                                    'self.example_filepaths: {}'.format(self.example_filepaths))

    def set_file_extensions(self):
        '''Set list of file extensions of interest for path_examples'''
        self.file_extensions = ['dat.gz','fits.gz','fits.bz2','fit.gz','tar.gz',
                                'log.gz','log.html','rdzw.gz',
                                'dat','fits','fit','tar','log','rdzw',
                                'whrl','png','ply','apz','par','hdr','o','e',
                                'sha1sum','ps','txt','html','model','csv','mp4',
                                'pdf','list','batch','batch.wrap.sh','condor','gif',
                                'md5sum',
                                ]

    def set_substitution_tree_paths(self):
        '''Set a list of substitution_tree_paths from the CFG files in
            $DATAMODEL_PARSER_TREE_DATA_DIR'''
        self.substitution_tree_paths = dict()
        if self.ready:
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

    def restrict_filepaths(self):
        '''Restrict the filepaths used.'''
        if self.ready:
            self.restrict_filepaths_options()
            self.restrict_filepaths_skip_list()

    def restrict_filepaths_options(self):
        '''Restrict filepaths using command line options, if necessary.'''
        if self.ready:
            if self.filepaths and self.options:
                if self.options.path:
                    self.filepaths = [self.options.path]
                elif self.options.start:
                    i = self.filepaths.index(self.options.start)
                    self.filepaths = self.filepaths[i:]
                elif self.options.failed:
                    self.set_yaml_dir()
                    self.set_yaml_data(dir=self.yaml_dir,
                                       filename='all_failed_datamodels.yaml')
                    self.filepaths = (self.yaml_data
                                      if self.yaml_data else None)
                else: pass # use all filepaths
            else:
                self.ready = False
                self.logger.error('Unable to restrict_filepaths_options. ' +
                                  'self.filepaths: {},\n'.format(self.filepaths) +
                                  'self.options: {} '.format(self.options)
                                  )

    def restrict_filepaths_skip_list(self):
        '''Remove filepaths in filepath_skip_list.'''
        if self.ready:
            self.set_filepath_skip_list()
            if self.filepath_skip_list:
                self.logger.info('Removing filepaths in filepath_skip_list')
                self.filepaths = [f for f in self.filepaths
                                  if f not in self.filepath_skip_list]
            else:
                self.ready = False
                self.logger.error('Unable to restrict_filepaths_skip_list. ' +
                                  'self.filepath_skip_list: {}'
                                    .format(self.filepath_skip_list))

    def set_filepath_skip_list(self):
        if self.ready:
            self.filepath_skip_list = [
                # Joel said to skip when populating filespec.yaml
                'BOSS_LYA/mocks/rawlite_VERS.html',
                'BOSS_LYA/mocks/VERS/rawlite/PLATE4/mock_lya.html',
                'BOSS_LYA/mocks/VERS/rawlite/PLATE4/mockrawShort_lya.html',
                'BOSS_LYA/cat/speclya.html',
                'APOGEE_OBSOLETE/APOGEE_ASPCAP/VERS_v_IDLn_FERREn.n.n_LIBn/plates/results/aspcapPlate-plateid-mjd.html',
                'APOGEE_OBSOLETE/APOGEE_ASPCAP/VERS4.2/spec/aspcapFluxError.html',
                'APOGEE_OBSOLETE/APOGEE_ASPCAP/VERS4.2/spec/aspcapFlux.html',
                'APOGEE_OBSOLETE/APOGEE_ASPCAP/VERS4.2/param/aspcapParam.html',
                'APOGEE_OBSOLETE/APOGEE_ASPCAP/VERS4.2/param/aspcapCova.html',
                'APOGEE_OBSOLETE/APOGEE_ASPCAP/VERS4.2/lib/aspcapSynth.html',
                'MARVELS_REDUX/RERUN_V001/ASCII/RXXXDXXX/RXXXDXXX.html',
                'RAWDATA_DIR/MJD/MJD.md5sum.html',

               #### BOSSTILELIST_DIR does not exist on archive_20190507####
               #### need `module load bosstilelist` on sas ####
               'BOSSTILELIST_DIR/bosschunks.html',                                  # This is an SVN product X
               'BOSSTILELIST_DIR/bosstiles.html',                                   # This is an SVN product X
               'BOSSTILELIST_DIR/geometry/boss_sector2tile.html',                   # This is an SVN product X
               'BOSSTILELIST_DIR/geometry/boss_locations.html',                     # This is an SVN product X
               'BOSSTILELIST_DIR/geometry/boss_sectors.html',                       # This is an SVN product X
               'BOSSTILELIST_DIR/geometry/boss_geometry.html',                      # This is an SVN product X
               'BOSSTILELIST_DIR/outputs/bossN/final-bossN.html',                   # This is an SVN product X
               'BOSSTILELIST_DIR/outputs/bossN/platePlans-bossN.html',              # This is an SVN product X
               'BOSSTILELIST_DIR/outputs/bossN/sector-bossN.html',                  # This is an SVN product X
               'BOSSTILELIST_DIR/outputs/bossN/tiles-bossN.html',                   # This is an SVN product X
               'BOSSTILELIST_DIR/outputs/bossN/stpair-bossN.html',                  # This is an SVN product X
               'BOSSTILELIST_DIR/outputs/bossN/geometry-bossN.html',                # This is an SVN product X
               'BOSSTILELIST_DIR/outputs/bossN/plugtest-bossN.html',                # This is an SVN product X
               'BOSSTILELIST_DIR/inputs/bossN/plan-bossN.html',                     # This is an SVN product X
               'BOSSTILELIST_DIR/inputs/bossN/targets-bossN.html',                  # This is an SVN product X
               'BOSSTILELIST_DIR/inputs/ancillary/bossN/ancillary-targets.html',    # This is an SVN product X
               'BOSSTILELIST_DIR/inputs/ancillary/bossN/ancillary-bossN.html',      # This is an SVN product X
               
                # found on the sas. not found on archive_20190507
               'BOSS_LSS_REDUX/data_DR14_LRG_NS.html',
               'BOSS_LSS_REDUX/random_DR14_QSO_NS.html',
               'BOSS_LSS_REDUX/random_DR14_LRG_NS.html',
               'BOSS_LSS_REDUX/data_DR14_QSO_NS.html',
               'APOGEE_RC/cat/apogee-rc-DR12.html',
               'APOGEE_RC/cat/apogee-rc-DR11.html',
               'MANGA_SPECTRO_DATA/MJD5/sdR.html',
               'PHOTO_REDUX/runList.html',
               'PHOTO_REDUX/RERUN/RUN/objcs/CAMCOL/fpC.html', # deprecated in SDSS-IV
               'SPIDERS_ANALYSIS/spiders_quasar_bhmass.html',

               # not found on the sas. not found on archive_20190507
               'BOSS_LSS_REDUX/trimmed-collate-SAMPLE-DRX.html',
               'BOSS_LSS_REDUX/bosstile-final-collated-boss2-bossN-photoObj.html',
               'BOSS_LSS_REDUX/bosstile-final-collated-boss2-bossN-specObj.html',
               'BOSS_LSS_REDUX/bosstile-final-collated-boss2-bossN-photoObj-specObj.html',
               'SPECTRO_REDUX/RUN2D/PLATE4/spDiag.html',
               'SSPP_REDUX/duplicates/dup.html',
               'REDMONSTER_SPECTRO_REDUX/RUN2D/REDMONSTER_VER/PLATE4/redmonster.html',
               'MARVELS_DATA/MJD/done.html',


               # env var doesn't exist on archive_20190507
               'MANGAPREIM_DIR/data/DESIGNID6XX/DESIGNID/preimage.html',                # This is an SVN product X
               'APOGEE_OCCAM/occam_member.html',
               'APOGEE_OCCAM/occam_cluster.html',
               'MANGACORE_DIR/hdrfix/MJD/sdHdrFix.html',                                # This is an SVN product X
               'MANGACORE_DIR/drill/PLATEID6XX/plateCMM.html',                          # This is an SVN product X
               'MANGACORE_DIR/metrology/maXXX/ma.html',                                 # This is an SVN product X
               'MANGACORE_DIR/metrology/hexferrules/hexferrules.html',                  # This is an SVN product X
               'MANGACORE_DIR/mapper/PLATEID6XX/PLATE/plPlugMapM.html',                 # This is an SVN product X
               'MANGACORE_DIR/slitmaps/PLATEID6XX/PLATE/slitmap.html',                  # This is an SVN product X
               'MANGACORE_DIR/cartmaps/cartmap.html',                                   # This is an SVN product X
               'MANGACORE_DIR/ifuflat/cartXX/MJD/ifuflat.html',                         # This is an SVN product X
               'MANGACORE_DIR/platedesign/foregroundstars/foregroundstars.html',        # This is an SVN product X
               'MANGACORE_DIR/platedesign/platetargets/platetargets.html',              # This is an SVN product X
               'MANGACORE_DIR/platedesign/plateholes/PLATEID6XX/plateHolesSorted.html', # This is an SVN product X
               'MANGACORE_DIR/platedesign/platemags/DESIGNID6XX/platemags.html',        # This is an SVN product X
               'MANGACORE_DIR/platedesign/targetfix/PLATEID6XX/targetfix.html',         # This is an SVN product X
               'MANGACORE_DIR/apocomplete/bogey.html',                                  # This is an SVN product X
               'MANGACORE_DIR/apocomplete/PLATEID6XX/apocomp.html',                     # This is an SVN product X
               'PLATELIST_DIR/platePlans.html',                                         # This is an SVN product X
               'PLATELIST_DIR/designs/DESIGNID6XX/DESIGNID6/plateStandard.html',        # This is an SVN product X
               'PLATELIST_DIR/designs/DESIGNID6XX/DESIGNID6/plateGuide.html',           # This is an SVN product X
               'PLATELIST_DIR/designs/DESIGNID6XX/DESIGNID6/plateTrap.html',            # This is an SVN product X
               'PLATELIST_DIR/designs/DESIGNID6XX/DESIGNID6/plateDesign.html',          # This is an SVN product X
               'PLATELIST_DIR/designs/DESIGNID6XX/DESIGNID6/plateInput-output.html',    # This is an SVN product ?
               'PLATELIST_DIR/plates/PLATEID6XX/PLATEID6/plateLines.html',              # This is an SVN product X
               'PLATELIST_DIR/plates/PLATEID6XX/PLATEID6/plateGuideAdjust.html',        # This is an SVN product X
               'PLATELIST_DIR/plates/PLATEID6XX/PLATEID6/plateGuideOffsets.html',       # This is an SVN product X
               'PLATELIST_DIR/plates/PLATEID6XX/PLATEID6/plateHoles.html',              # This is an SVN product X
               'PLATELIST_DIR/plates/PLATEID6XX/PLATEID6/plPlugMapP.html',              # This is an SVN product X
               'PLATELIST_DIR/plates/PLATEID6XX/PLATEID6/plateHolesSorted.html',        # This is an SVN product X
               'PLATELIST_DIR/definitions/DESIGNID6XX/plateDefinition.html',            # This is an SVN product X
               'PLATELIST_DIR/runs/PLATERUN/plParam.html',                              # This is an SVN product X
               'PLATELIST_DIR/runs/PLATERUN/plMeas.html',                               # This is an SVN product X
               'PLATELIST_DIR/runs/PLATERUN/plOverlay.html',                            # This is an SVN product X
               'PLATELIST_DIR/runs/PLATERUN/plPlan.html',                               # This is an SVN product X
               'PLATELIST_DIR/runs/PLATERUN/plFanuc.html',                              # This is an SVN product ?
               'PLATELIST_DIR/runs/PLATERUN/plPlugMap.html',                            # This is an SVN product X
               'PLATELIST_DIR/runs/PLATERUN/plDrillPos.html',                           # This is an SVN product X
               'PLATELIST_DIR/runs/PLATERUN/plObs.html',                                # This is an SVN product X
               'PLATELIST_DIR/inputs/plateInput.html',                                  # This is an SVN product ?
               'CAS_LOAD/phCSV/SKYVERSION/RUN/csv_ready.html',
               'CAS_LOAD/phCSV/SKYVERSION/RUN/sqlField.html',
               'CAS_LOAD/phCSV/SKYVERSION/RUN/sqlPhotoProfile.html',
               'CAS_LOAD/phCSV/SKYVERSION/RUN/sqlFieldProfile.html',
               'CAS_LOAD/phCSV/SKYVERSION/RUN/sqlRun.html',
               'CAS_LOAD/phCSV/SKYVERSION/RUN/sqlPhotoObjAll.html',
               'SPECLOG_DIR/MJD/plPlugMapM.html',
               'SPECLOG_DIR/MJD/sdhdrfix.html',
               'SPECLOG_DIR/MJD/guidermon.html',
               'BOSSTARGET_DIR/data/geometry/boss_survey.html',
               'SPINSPECT_DIR/data/NAME/spInspect.html',
               'PLATEDESIGN_DIR/defaults/plateDefault.html',
               'CALIBPLATE_DIR/calibPlateP.html',                                       # This is an SVN product
                
                # Joel needs to fix these on archive_20190507
               'EBOSS_FIREFLY/FIREFLY_VER/sdss_eboss_firefly.html',
               'EBOSS_FIREFLY/FIREFLY_VER/RUN2D/sdss_firefly.html',
               'EBOSS_FIREFLY/FIREFLY_VER/RUN2D/eboss_firefly.html',
               'EBOSS_FIREFLY/FIREFLY_VER/RUN2D/SPMODELS_VER/PLATE/spFly.html',
               'EBOSS_FIREFLY/FIREFLY_VER/RUN2D/SPMODELS_VER/PLATE/spFlyPlate.html',
               
               # Needs to be renamed and redone
               'ECAM_DATA/MJD/all_files.html',

                # Make trac tickets for these
               'STAGING_DATA/oplogs/MJD/idCCDLog.html',                                 # not released to public
               'STAGING_DATA/oplogs/MJD/sdReport.html',                                 # not released to public
               'STAGING_DATA/oplogs/MJD/idReport.html',                                 # not released to public
               'STAGING_DATA/oplogs/MJD/mdReport.html',                                 # not released to public
               'STAGING_DATA/gangs/MJD/gangs.list.html',                                # not released to public


]
