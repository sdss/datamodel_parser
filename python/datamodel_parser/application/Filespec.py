from sdssdb.sqlalchemy.archive.sas import *
from sdss_install.utils.module import Module
from string import punctuation as string_punctuation
from datamodel_parser.application import Util
from os.path import basename, dirname, exists, isdir, join
from os import environ
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
        self.logger  = self.util.logger  if self.util.logger  else None
        self.options = self.util.options if self.util.options else None
        self.ready   = self.util and self.util.ready if self.util else None

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.ready   and
                          self.util    and
                          self.logger  and
                          self.options )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.datamodel_file_path       = None
            self.datamodel_env_variable    = None
            self.datamodel_file_name       = None
            self.datamodel_file_name_start = None
            self.datamodel_directory_names = None
            self.dir_substitution          = None
            self.species_location          = None
            self.tree_id                   = None
            self.species_path_example      = None
            self.species_name              = None
            self.path_example_file_row     = None

    def set_datamodel_env_variable_dir(self):
        '''Set the directory path associated with the datamodel environmental variable.'''
        self.datamodel_env_variable_dir = None
        print('self.datamodel_env_variable: %r' % self.datamodel_env_variable)
        input('pause')
        try: self.datamodel_env_variable_dir = environ[self.datamodel_env_variable]
        except Exception as e:
            self.ready = False
            self.logger.error('Unable to set_datamodel_env_variable_dir. exception: {}'.format(e))
        if not self.datamodel_env_variable_dir:
            self.ready = False
            self.logger.error('Unable to set_datamodel_env_variable_dir. '
                              'self.datamodel_env_variable_dir: {} '
                                .format(self.datamodel_env_variable_dir))

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
                self.datamodel_file_path        = path_info['file_path']
                self.datamodel_env_variable     = path_info['env_variable']
                self.datamodel_file_name        = path_info['file_name']
                self.datamodel_location_path    = path_info['location_path']
                self.datamodel_directory_names  = path_info['directory_names']
                self.datamodel_directory_depths = path_info['directory_depths']

    def set_module(self):
        '''Set the module class attribute.'''
        self.module = None
        if self.ready:
            self.module = Module(logger=self.logger,options=self.options)
            if not self.module:
                self.ready = False
                self.logger.error('Unable to set_module.')

    def set_species_values(self):
        '''Determine and populate self.species values'''
        if self.ready:
            self.set_potential_path_example_file_rows() # this also sets self.tree_id
            self.set_path_example_file_row()
            self.split_path()
            self.set_species_location()
            self.set_species_ext()
            self.set_species_name()
            self.set_species_note()
            if self.ready:
                self.species['tree_edition']  = 'dr' + str(self.tree_id)
                self.species['location']      = self.species_location
                self.species['name']          = self.species_name
                self.species['ext']           = self.species_ext
                self.species['path_example']  = self.path_example_file_row.path
                self.species['note']          = self.species_note

    def set_potential_path_example_file_rows(self):
        '''Set the list self.potential_path_example_file_rows from self.datamodel_file_name'''
        self.tree_id = None
        self.potential_path_example_file_rows = list()
        if self.ready:
            self.logger.info('Setting path_examples for {} from the archive database'
                                .format(self.datamodel_file_path))
            self.set_session()
            self.set_tree_id_range()
            self.set_file_name_start()
            self.ready = bool(self.ready and self.datamodel_env_variable and self.session and
                              self.tree_id_range and self.datamodel_file_name_start)
            if self.ready:
                for self.tree_id in self.tree_id_range:
                    env = (self.session.query(Env)
                                       .filter(Env.tree_id == self.tree_id)
                                       .filter(Env.label == self.datamodel_env_variable)
                                       .one())

                    self.loc = 'manga/spectro/analysis/v2_4_3/2.2.1' ## DEBUG ##

                    directories = (self.session.query(Directory)
                                               .filter(Directory.env_id == env.id)
                                               .filter(Directory.location == self.loc) ## DEBUG ##
                                               .all())
                    for directory in directories:
                        files = (self.session.query(File)
                                             .filter(File.directory_id == directory.id)
                                             .filter(File.location.like('%' + self.datamodel_file_name_start + '%'))
                                             .all())
                        if files:
                            self.logger.debug('Files found with file.path like %{0}%: {1}'
                                .format(self.datamodel_file_name_start,files))
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

    def set_file_name_start(self):
        '''Set the first part of the filename, up to the first punctuation character.'''
        self.datamodel_file_name_start = None
        if self.ready:
            if self.datamodel_file_name:
                punctuation = str(string_punctuation).replace('_',str())
#                regex = "[\w']+|[.,!?;]"
                regex = "[\w']+|[" + punctuation + "]"
                string = self.datamodel_file_name.strip()
                matches = self.util.get_matches(regex=regex,string=string)
                match = matches[0] if matches else None
                self.datamodel_file_name_start = match
            else:
                self.ready = False
                self.logger.error('Unable to set_file_name_start. ' +
                                  'self.datamodel_file_name: {}'.format(self.datamodel_file_name))
            if not self.datamodel_file_name_start:
                self.ready = False
                self.logger.error('Unable to set_file_name_start. ' +
                                  'self.datamodel_file_name_start: {}'
                                    .format(self.datamodel_file_name_start))

    def set_species_location(self):
        '''Set species_location from self.datamodel_directory_names and text
            substitution conventions'''
        # Need to check if this way of finding the location agrees with the location
        # found in the species_path_example
        self.species_location = None
        if self.ready:
            if self.datamodel_directory_names:
                if not self.dir_substitution: self.set_dir_substitution()
                names = list()
                for directory_name in self.datamodel_directory_names:
                    if directory_name in self.dir_substitution:
                        name = self.dir_substitution[directory_name]
                    else:
                        name = directory_name
                    names.append(name)
                self.species_location = join(*names)
                
                
                ### 1) Validate that self.species_location has
                ###     as many directories as self.example_location
                ### 2) Create dictionary of {'actual directory' : 'text substitution string'}
            else:
                self.ready = False
                self.logger.error('Unable to set_species_location. ' +
                                  'self.datamodel_directory_names: {}'
                                    .format(self.datamodel_directory_names))
            if not self.species_location:
                self.ready = False
                self.logger.error('Unable to set_species_location. ' +
                                  'self.species_location: {}'.format(self.species_location))

    def set_dir_substitution(self):
        self.dir_substitution = {
            # Done up to
            # - path: "BOSS_LSS_REDUX/dr11_qpm_mocks/mock_galaxy_DRX_SAMPLE_NS_QPM_IDNUMBER.html"
            # in filespec.yaml
                                    'dr11_patchy_mocks' : '{dr}_multidark_patchy_mocks',
                                    'DRPVER'            : '{drpver}',
                                    'DAPVER'            : '{dapver}',
                                    'ELG_COMPOSITE_VER' : '{ver}',
                                    'GALAXY_VERSION'    : '{version}',
                                    'MJD'               : '{mjd}',
                                    'MJD5'              : '{mjd}',
                                    'PLATE4'            : '{plate:0>4}',
                                    'PLATE4-MJD'        : '{plate:0>4}-{mjd}',
                                    'RUN1D'             : '{run1d}',
                                    'RUN2D'             : '{run2d}',
                                    'TARGET_RUN'        : '{target_run}',
                                    
                                }

    def set_path_example_file_row(self):
        '''Set path_example_file_row from self.potential_path_example_file_rows'''
        ##### Under construction #####
        self.path_example_file_row = list()
        self.removed_potential_path_example_file_rows = list()
        if self.ready:
            if self.potential_path_example_file_rows:
                self.set_file_extensions()
                for file_row in self.potential_path_example_file_rows:
                    file_path = file_row.path if file_row else None
                    split = file_path.split('.') if file_path else None
                    ext = split[-1] if split else None
                    if ext in self.file_extensions:
                        self.path_example_file_row.append(file_row)
                    else:
                        self.removed_potential_path_example_file_rows.append(file_path)
                        self.logger.debug('Removing potential_path_example: {}'.format(file_path))
                if len(self.path_example_file_row) == 1:
                    self.path_example_file_row = self.path_example_file_row[0]
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
        self.example_location = None
        if self.ready:
            if self.path_example_file_row:
                file_path = self.path_example_file_row.path
                # split file_path
                self.set_module()
                if self.ready:
                    arguments = join('tree','dr' + str(self.tree_id))
                    self.module.set_command(command='load',arguments=arguments)
                    self.module.execute_command()
#                    print('arguments: %r'% arguments)
#                    print('self.module.stdout: %r'% self.module.stdout)
#                    print('self.module.stderr: %r'% self.module.stdout)
#                    print('self.module.returncode: %r'% self.module.returncode)
#                    input('pause')
                    self.ready = bool(self.ready and self.module.ready and
                                  self.module.returncode == 0 and self.module.stdout)
                if self.ready:
#                    self.set_datamodel_env_variable_dir() # DOESN'T WORK
                    ########  Fragile ########
                    regex = "environ\[\'" + self.datamodel_env_variable + "(.*?)\\n"
                    matches = self.util.get_matches(regex=regex,string=self.module.stdout)
                    environ_def = matches[0] if matches else None
                    regex = "(?<=\/)(.*?)(?=\')"
                    matches = (self.util.get_matches(regex=regex,string=environ_def)
                               if environ_def else None)
                    environ_path = matches[0] if matches else None
                    ########  Fragile ########
                    split = environ_path.split('/') if environ_path else None
                    last_dir = split[-1] + '/' if split else None
                    split = file_path.split(last_dir) if last_dir else None
                    location_name = split[-1] if split else None
                    split = location_name.split('/') if location_name else None
                    self.example_location = '/'.join(split[:-1]) if split else None
                    self.example_name = split[-1] if split else None

#                    print('environ_def: %r' %  environ_def)
#                    print('environ_path: %r' %  environ_path)
#                    print('last_dir: %r' %  last_dir)
#                    print('location_name: %r' %  location_name)
#                    print('self.example_location: %r' %  self.example_location)
#                    print('self.example_name: %r' %  self.example_name)
#                    print('file_path: %r' %  file_path)
#                    input('pause')
            else:
                self.ready = False
                self.logger.error('Unable to split_path. ' +
                                  'self.path_example_file_row: {}'
                                    .format(self.path_example_file_row))
            if not self.example_name: # self.example_location can be None
                self.ready = False
                self.logger.error('Unable to split_path. ' +
                                  'self.path_example_file_row: {}'
                                    .format(self.path_example_file_row))

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
            if self.example_name:
                self.species_name = self.example_name
                ### Process
                ### 1) use dictionary of {'actual directory' : 'text substitution string'}
                ###     in set_species_location to insert the text substitution strings
                ### 2) Validate that all the text substitution strings were accounted for.
            else:
                self.ready = False
                self.logger.error('Unable to set_species_name. ' +
                                  'self.example_name: {}'
                                    .format(self.example_name))
            if not self.species_name:
                self.ready = False
                self.logger.error('Unable to set_species_name. ' +
                                  'self.species_name: {}'.format(self.species_name))

    def set_species_note(self):
        '''Set a note of any warnings or errors that occurred while running
            set_species_values'''
        #### UNDER CONSTRUCTION ####
        self.species_note = 'undetermined'




