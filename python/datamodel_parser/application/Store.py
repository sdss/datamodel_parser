from datamodel_parser.application import Filespec
from datamodel_parser.application import File
from datamodel_parser.application import Database
from datamodel_parser.application import Util
from os import environ, walk
from os.path import basename, dirname, exists, isdir, join
from flask import render_template
from datamodel_parser import app
import logging
from subprocess import Popen, PIPE
import yaml
from json import dumps

class Store():

    def __init__(self, options=None):
        self.set_logger(options=options)
        self.set_options(options=options)
        self.set_database()
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
                    'self.database: {}'.format(self.database) +
                    'self.database.ready: {}'.format(self.database.ready))

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger  and
                          self.options and
                          self.database
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.util = Util(logger=self.logger,options=self.options)
            self.datamodel_dir                      = None
            self.path                               = None
            self.tree_edition                       = None
            self.env_variable                       = None
            self.file_name                          = None
            self.location_path                      = None
            self.directory_names                    = None
            self.directory_depths                   = None
            self.svn_products                       = None
            self.path_info                          = None

    def populate_filespec_table_archive(self):
        '''Set self.filespec_dict for each datamodel path in self.file_paths.'''
        if self.ready:
            if self.file_paths:
                ### DEBUG ###
                self.file_paths = ['MANGA_SPECTRO_ANALYSIS/DRPVER/DAPVER/dapall.html'] ### DEBUG ###
                self.loc = 'manga/spectro/analysis/v2_4_3/2.2.1' ## DEBUG ##
                ### DEBUG ###
                filespec = Filespec(logger=self.logger,options=self.options)
                if filespec and filespec.ready:
                    for self.file_path in self.file_paths:
                        if self.ready:
                            self.set_path_info()
                            self.initialize_filespec_dict()
                            if self.ready:
                                filespec.set_path_info(path_info=self.path_info)
                                filespec.set_species(species=self.filespec_dict)
                                filespec.set_species_values()
                                self.filespec_dict = filespec.species
                                self.ready = self.ready and filespec.ready
                            if self.ready:
                                self.populate_file_path_tables()
                                self.populate_filespec_table()
            else:
                self.ready = False
                self.logger.error('Unable to populate_filespec_table_archive. ' +
                                  'self.file_paths: {}'.format(self.file_paths))

    def set_path_info(self):
        '''Set information obtained from the datamodel file path.'''
        self.path_info = None
        if self.ready:
            if self.file_path:
                # set datamodel path, self.env_variable, self.file_name, and self.directory_names
                path = self.file_path
                self.set_path(path=path)
                self.split_path()
                if self.ready:
                    self.path_info = {'file_path'        : self.file_path       ,
                                      'env_variable'     : self.env_variable    ,
                                      'file_name'        : self.file_name       ,
                                      'location_path'    : self.location_path   ,
                                      'directory_names'  : self.directory_names ,
                                      'directory_depths' : self.directory_depths,
                                      }
            else:
                self.ready = False
                self.logger.error('Unable to set_path_info. ' +
                                  'self.file_path: {}'.format(self.file_path)
                                  )
            if not self.path_info:
                self.ready = False
                self.logger.error('Unable to set_path_info. ' +
                                  'self.path_info: {}'.format(self.path_info))


    def initialize_filespec_dict(self):
        '''Set filespec_dict from self.file_path using the archive database.'''
        self.filespec_dict = dict()
        if self.ready:
            if self.file_path:
                self.filespec_dict['path']          = self.file_path
                self.filespec_dict['tree_edition']  = 'undetermined'
                self.filespec_dict['env_label']     = self.env_variable
                self.filespec_dict['location']      = 'undetermined'
                self.filespec_dict['name']          = 'undetermined'
                self.filespec_dict['ext']           = 'undetermined'
                self.filespec_dict['path_example']  = 'undetermined'
                self.filespec_dict['note']          = str()
            else:
                self.ready = False
                self.logger.error('Unable to initialize_filespec_dict. ' +
                                  'self.file_path: {}'.format(self.file_path))
            if not self.filespec_dict:
                self.ready = False
                self.logger.error('Unable to initialize_filespec_dict. ' +
                                  'self.filespec_dict: {}'.format(self.filespec_dict))

    def init_yaml(self,filename='filespec.yaml'):
        '''Write a yaml file containing datamodel file paths.'''
        if self.ready:
            if self.file_paths:
                # create yaml file contents
                yaml_str = 'datamodels:\n'
                for path in self.file_paths:
                    path = path.replace('datamodel/files/',str())
                    self.set_path(path=path)
                    self.split_path()

                    yaml_str += ' - path: "{}"\n'.format(path)
                    yaml_str += '   tree_edition: "temp"\n'
                    yaml_str += '   env_label: "{}"\n'.format(self.env_variable)
                    yaml_str += '   location: ""\n'
                    yaml_str += '   name: " "\n'
                    yaml_str += '   ext: " "\n'
                    yaml_str += '   path_example: "${}/"\n'.format(self.env_variable)
                    yaml_str += '   note: ""\n'
                    yaml_str += '\n'

                # write yaml file
                self.set_yaml_dir()
                yaml_file = join(self.yaml_dir,filename) if self.yaml_dir else None
                if not exists(yaml_file):
                    with open(yaml_file,'w') as filespec:
                        filespec.write(yaml_str)
                else:
                    self.ready = False
                    self.logger.error('Unable to init_yaml. ' +
                                      'The file already exists: {}. '.format(yaml_file) +
                                      'If you wish to replace this file please first delete it.')
            else:
                self.ready = False
                self.logger.error('Unable to write_yaml. ' +
                                  'self.file_paths: {}'.format(self.file_paths))

    def set_filespec_dict_yaml(self,filename='filespec.yaml'):
        '''Create a dictionary from the filespec.yaml file'''
        self.filespec_dict_yaml = None
        if self.ready:
            self.set_yaml_dir()
            yaml_file = join(self.yaml_dir,filename) if self.yaml_dir else None
            if yaml_file and exists(yaml_file):
                with open(yaml_file,'r') as filespec:
                    try: self.filespec_dict_yaml = yaml.safe_load(filespec)
                    except yaml.YAMLError as e:
                        self.ready = False
                        self.logger.error('Unable to set_filespec_dict_yaml. ' +
                                          'An error occurred diring yaml.safe_load(). ' +
                                          'Exception: {}'.format(e))
            else:
                self.ready = False
                self.logger.error('Unable to set_filespec_dict_yaml. ' +
                                  'yaml_file: {}'.format(yaml_file))

    def populate_filespec_table_yaml(self):
        '''Populate the filespec table row for each dict in filespec_dicts.'''
        if self.ready:
            filespec_dicts = (self.filespec_dict_yaml['datamodels']
                              if self.filespec_dict_yaml
                              and 'datamodels' in self.filespec_dict_yaml
                              else None)
            for self.filespec_dict in filespec_dicts:
                self.populate_filespec_table()
                
    def populate_filespec_table(self):
        '''Populate Database.filespec table from self.filespec_dict'''
        if self.ready:
            if self.filespec_dict:
                self.set_filespec_tree_id()
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                self.ready = self.ready and self.database.ready
                if self.ready:
                    self.database.set_filespec_columns(
                        tree_id      = self.filespec_tree_id,
                        env_label    = self.filespec_dict['env_label'],
                        location     = self.filespec_dict['location'],
                        name         = self.filespec_dict['name'],
                        ext          = self.filespec_dict['ext'],
                        path_example = self.filespec_dict['path_example'],
                        note         = self.filespec_dict['note'],
                                       )
                    self.database.populate_filespec_table()
                    self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error('Unable to populate_filespec_table_yaml. ' +
                                  'self.filespec_dict: {}, '.format(self.filespec_dict)
                                  )

    def set_filespec_tree_id(self):
        '''Set filespec_tree_id from '''
        self.filespec_tree_id = None
        if self.ready:
            if self.filespec_dict:
                # split_path and populate_file_path_tables if necessary
                path = (self.filespec_dict['path']
                        if self.filespec_dict and 'path' in self.filespec_dict
                        else None)
                self.set_path(path=path)
                self.split_path()
                self.populate_file_path_tables()
                
                if self.ready:
                    filespec_tree_edition = (self.filespec_dict['tree_edition']
                                             if self.filespec_dict
                                             and 'tree_edition' in self.filespec_dict
                                             else None)
                    self.populate_tree_table(tree_edition=filespec_tree_edition)
                    self.database.set_tree_id(tree_edition=filespec_tree_edition)
                    self.filespec_tree_id = (self.database.tree_id
                                             if self.database.ready else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_filespec_tree_id. ' +
                                  'self.filespec_dict: {}, '.format(self.filespec_dict)
                                  )
            if not self.filespec_tree_id:
                self.ready = False
                self.logger.error('Unable to set_filespec_tree_id. ' +
                                  'self.filespec_tree_id: {}, '
                                    .format(self.filespec_tree_id)
                                  )

    def set_yaml_dir(self):
        '''Set DATAMODEL_PARSER_YAML_DIR'''
        self.yaml_dir = None
        try: self.yaml_dir = environ['DATAMODEL_PARSER_YAML_DIR']
        except Exception as e:
            self.ready = False
            self.logger.error('Unable to set_yaml_dir. exception: {}'.format(e))

    def set_tree_edition(self):
        '''Set the datamodel edition.'''
        self.tree_edition = None
        if self.ready:
            if not self.datamodel_dir: self.set_datamodel_dir()
            if self.ready:
                self.tree_edition = (self.datamodel_dir.split('/')[-1]
                                     if self.datamodel_dir else None)
            if not self.tree_edition:
                self.ready = False
                self.logger.error('Unable to set_tree_edition. ' +
                                  'self.tree_edition: {}'
                                    .format(self.tree_edition))

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

    def set_path(self, path=None):
        self.path = None
        if self.ready:
            self.path = path if path else None
            if not self.path: self.logger.error('Unable to set_path.')

    def split_path(self,path=None):
        '''Extract information from the given file path.'''
        if self.ready:
            path = path if path else self.path
            if path:
                path = path.replace('datamodel/files/',str())
                split = path.split('/')
                self.env_variable  = split[0]              if split else None
                self.file_name     = split[-1]             if split else None
                self.location_path = '/'.join(split[1:-1]) if split else None
                self.directory_names  = list()
                self.directory_depths = list()
                for name in split[1:-1]:
                    self.directory_names.append(name)
                    self.directory_depths.append(self.directory_names.index(name))
            else:
                self.ready = False
                self.logger.error('Unable to split_path. ' +
                                  'path: {}'.format(path))
            if not (
                self.env_variable     and
                self.file_name
                #self.location_path    # can be None
                #self.directory_names  # can be None
                #self.directory_depths # can be None
                ):
                self.ready = False
                self.logger.error(
                    'Unable to split_path. '                              +
                    'self.env_variable: {}, ' .format(self.env_variable)  +
                    'self.file_name: {}, '    .format(self.file_name)
                    )

    def set_file_paths(self):
        '''Set a list of all files for the current tree edition.'''
        self.file_paths = list()
        if self.ready:
            self.set_file_path_skip_list()
            if not self.datamodel_dir:
                self.set_datamodel_dir()
            if self.ready:
                root_dir = join(self.datamodel_dir,'datamodel/files/')
                for (dirpath, dirnames, filenames) in walk(root_dir):
                    if filenames:
                        for filename in filenames:
                            if (filename.endswith('.html') and
                                'readme' not in filename.lower()
                                ):
                                file = join(dirpath,filename)
                                if exists(file):
                                    file_path = file.replace(
                                                    self.datamodel_dir + '/',str())
                                    if (file_path and
                                        file_path not in self.file_path_skip_list
                                        ):
                                        self.file_paths.append(file_path)
                                else:
                                    self.ready = False
                                    self.logger.error('File does not exist: '
                                                      'file: {}'.format(file))
                    else: pass # it's okay to have empty filenames
            else:
                self.ready = False
                self.logger.error('Unable to set_file_paths. ' +
                                  'self.datamodel_dir: {}'.format(self.datamodel_dir))
            if not self.file_paths:
                self.ready = False
                self.logger.error('Unable to set_file_paths. ' +
                                  'self.file_paths: {}'.format(self.file_paths))

    def set_file_path_skip_list(self):
        '''Set a list of file paths that don't conform to the database schema.'''
        self.file_path_skip_list = [
            'datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/PLATE4/MJD5/mgFrame.html',
            'datamodel/files/MANGA_PIPE3D/MANGADRP_VER/PIPE3D_VER/PLATE/manga.Pipe3D.cube.html',
            'datamodel/files/PHOTO_REDUX/RERUN/RUN/objcs/CAMCOL/fpC.html',
            'datamodel/files/PHOTO_REDUX/RERUN/RUN/astrom/asTrans.html',
            'BOSS_PHOTOOBJ/photoz-weight/pofz.html',
            ]

    def set_svn_products(self,root_dir=None):
        '''Set a list of directories containing the subdirectories:
            branches, tags, and trunk'''
        if self.ready:
            if root_dir and self.svn_products is not None:
                command = ['svn','list',root_dir]
                (stdout,stderr,proc_returncode) = self.util.execute_command(command)
                self.logger.info('Traversing directory: %r' % root_dir)
                if proc_returncode == 0:
                    basenames = ([d.replace('/',str())
                                  for d in str(stdout.decode("utf-8")).split('\n')
                                  if d and d.endswith('/')]
                                 if stdout else None)
                    if basenames:
#                        if {'branches','tags','trunk'}.issubset(set(basenames)):
                        if 'trunk' in basenames:
                            self.svn_products.append(root_dir)
                            root_dir = dirname(root_dir)
                        else:
                            for basename in basenames:
                                if self.ready:
                                    sub_dir = join(root_dir,basename)
                                    self.set_svn_products(root_dir=sub_dir)
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to get_svn_products. ' +
                        'An error has occured while executing the command, ' +
                        'command: {}, '.format(command) +
                        'proc_returncode: {}, '.format(proc_returncode)
                        )
            else:
                self.ready = False
                self.logger.error(
                    'Unable to get_svn_products. ' +
                    'root_dir: {}'.format(root_dir) +
                    'self.svn_product: {}'.format(self.svn_product)
                    )

    def get_column_tag(self):
        '''Populate tables comprised of file HTML text information.'''
        if self.ready:
            self.set_file_body()
            self.file.get_column_tag()

    def get_db_column_tags(self):
        '''Populate tables comprised of file HTML text information.'''
        if self.ready:
            self.set_file_body()
            self.file.get_db_column_tags()

    def get_db_keyword_tags(self):
        '''Populate tables comprised of file HTML text information.'''
        if self.ready:
            self.set_file_body()
            self.file.get_db_keyword_tags()

    def set_file_body(self):
        if self.ready:
            self.set_file_path_info()
            self.set_html_text()
            self.set_file()
            if self.file_path_info and self.html_text and self.file:
                self.file.set_file_path_info(file_path_info=self.file_path_info)
                self.file.set_html_text(html_text=self.html_text)
                self.file.set_body()
            else:
                self.ready = False
                self.logger.error(
                            'Unable to populate_file_html_tables. ' +
                            'self.file_path_info: {}, '.format(self.file_path_info) +
                            'self.html_text: {}, '.format(self.html_text) +
                            'self.file: {}.'.format(self.file) )

    def populate_database(self):
        '''Populate the database with file information.'''
        if self.ready:
            if self.ready: self.populate_file_path_tables()
            if self.ready: self.populate_file_html_tables()
            self.ready = self.ready and self.database.ready and self.file.ready
            if self.ready:
                intro_type = self.file.intro_type
                file_type = self.file.file_type
                self.database.update_file_table_status(ready=self.ready,
                                                       intro_type=intro_type,
                                                       file_type=file_type)

    def populate_file_path_tables(self):
        '''Populate tables comprised of file path information.'''
        if self.ready:
            self.populate_tree_table()
            self.populate_env_table()
            self.populate_location_table()
            self.populate_directory_table()
            self.populate_file_table()

    def populate_tree_table(self,tree_edition=None):
        '''Populate the tree table.'''
        if self.ready:
            tree_edition = tree_edition if tree_edition else self.tree_edition
            if self.database and tree_edition:
                self.database.set_tree_columns(edition=tree_edition)
                self.database.populate_tree_table()
                self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_tree_table. ' +
                    'self.database: {}.'.format(self.database) +
                    'tree_edition: {}.'.format(tree_edition))

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
                    'self.database: {}, '.format(self.database) +
                    'self.env_variable: {}.' .format(self.env_variable))

    def populate_location_table(self):
        '''Populate the location table.'''
        if self.ready:
            if (self.database     and
                self.tree_edition and
                self.env_variable
#               self.location_path # can be None
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
                    'self.tree_edition: {}, '.format(self.tree_edition) +
                    'self.env_variable: {}, '.format(self.env_variable)
                    )

    def populate_directory_table(self):
        '''Populate the directory table.'''
        if self.ready:
            if (self.tree_edition     and
                self.env_variable     
#               self.location_path    # can be None
#               self.directory_names  # can be None
#               self.directory_depths # can be None
                ):
                self.database.set_location_id(
                                            tree_edition = self.tree_edition,
                                            env_variable = self.env_variable,
                                            location_path = self.location_path)
                names  = (self.directory_names  if self.directory_names  else list())
                depths = (self.directory_depths if self.directory_depths else list())
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
                    'self.tree_edition: {}, '   .format(self.tree_edition)    +
                    'self.env_variable: {}, '   .format(self.env_variable)
                    )

    def populate_file_table(self):
        '''Populate the file table.'''
        if self.ready:
            if (self.tree_edition         and
                self.env_variable         and
#               self.location_path # can be None
                self.file_name
                ):
                self.database.set_location_id(
                                            tree_edition = self.tree_edition,
                                            env_variable = self.env_variable,
                                            location_path = self.location_path)
                self.database.set_file_columns(name=self.file_name)
                self.database.populate_file_table()
                self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_file_table. '                      +
                    'self.tree_edition: {}, ' .format(self.tree_edition)  +
                    'self.env_variable: {}, ' .format(self.env_variable)  +
                    'self.file_name: {}, '    .format(self.file_name)     +
                    'self.file: {}, '         .format(self.file)          +
                    'self.file.hdu_count: {}.'
                    .format(self.file.hdu_count))

    def populate_file_html_tables(self):
        '''Populate tables comprised of file HTML text information.'''
        if self.ready:
            self.set_file_path_info()
            self.set_html_text()
            self.set_file()
            if self.file_path_info and self.html_text and self.file:
                self.file.set_file_path_info(file_path_info=self.file_path_info)
                self.file.set_html_text(html_text=self.html_text)
                self.file.set_body()
                self.file.set_intro_and_hdu()
                self.file.parse_file()
                self.file.populate_file_hdu_info_tables()
            else:
                self.ready = False
                self.logger.error(
                            'Unable to populate_file_html_tables. ' +
                            'self.file_path_info: {}, '.format(self.file_path_info) +
                            'self.html_text: {}, '.format(self.html_text) +
                            'self.file: {}.'.format(self.file) )

    def populate_fits_tables(self,fits_dict=None):
        '''Populate tables comprised of fits file information.'''
        if self.ready:
            self.set_file_path_info()
            self.set_file()
            if fits_dict and self.file_path_info and self.file:
                self.file.set_file_path_info(file_path_info=self.file_path_info)
                self.file.parse_fits(fits_dict=fits_dict)
                self.file.populate_file_hdu_info_tables()
                self.file.populate_file_hdu_info_tables()
            else:
                self.ready = False
                self.logger.error(
                            'Unable to populate_file_html_tables. ' +
                            'fits_dict: {}, '.format(fits_dict) +
                            'self.file_path_info: {}, '.format(self.file_path_info) +
                            'self.file: {}.'.format(self.file) )


    def set_file_path_info(self):
        '''Set the html file file_path_info.'''
        self.file_path_info = None
        if self.ready:
            if (self.tree_edition  and
                self.env_variable  and
                self.file_name):
                # self.location_path can be null
                self.file_path_info = {'tree_edition'  : self.tree_edition,
                                       'env_variable'  : self.env_variable,
                                       'file_name'     : self.file_name,
                                       'location_path' : self.location_path,
                                        }
                                        
            else:
                self.ready = False
                self.logger.error('Unable to render_template. ' +
                                  'self.tree_edition: {}, '.format(self.tree_edition) +
                                  'self.env_variable: {}, '.format(self.env_variable) +
                                  'self.file_name: {}, '.format(self.file_name) +
                                  'self.location_path: {}.'.format(self.location_path)
                                  )

    def set_html_text(self):
        '''Set the HTML text for the given URL.'''
        self.html_text = None
        if self.ready:
            if not self.datamodel_dir:
                self.set_datamodel_dir()
            if self.path and not self.path.startswith('/'):
#                file =  join(self.datamodel_dir,self.path)
                file =  join(self.datamodel_dir,'datamodel/files',self.path)
                if exists(file):
                    with open(file, 'r') as html_text:
                        self.html_text = html_text.read()
                else:
                    self.ready = False
                    self.logger.error('Unable to set_html_text. ' +
                                      'File does not exist: {}'.format(file))
            else:
                self.ready = False
                self.logger.error('Invalid path: {}'.format(self.path))

    def set_file(self):
        ''' Set class File instance.'''
        self.file = None
        if self.ready:
                self.file = (File(logger=self.logger,options=self.options)
                             if self.logger and self.options else None)

    def render_template(self,template=None):
        '''Use database information to render the given template.'''
        if self.ready:
            self.set_database()
            if template and self.database:
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                (intros,hdu_info_dict) = (self.database.get_intros_sections_hdus()
                                          if self.ready and self.database.ready
                                          else None)
                self.ready = self.ready and self.database.ready
                if self.ready:
                    result = None
                    with app.app_context():
                        result = render_template(template,
                                                 intros        = intros,
                                                 hdu_info_dict = hdu_info_dict,
                                                 )
                    self.process_rendered_template(result   = result,
                                                   template = template)
                else:
                    print('Fail! \nTry running parse_html for the file: %r'
                            % self.options.path)
            else:
                self.ready = False
                self.logger.error('Unable to render_template. ' +
                                  'template: {}'.format(template) +
                                  'self.database: {}'.format(self.database)
                                  )

    def process_rendered_template(self,result=None,template=None):
        '''Process the result of the rendered Jinja2 template.'''
        if self.ready:
            if result and template:
                self.set_datamodel_parser_rendered_dir()
                file_hdu = template.split('.')[0].split('_')[1]
                dir_name = (self.datamodel_parser_rendered_dir
                            if self.datamodel_parser_rendered_dir else None)
                file_name = self.file_name.split('.')[0] + '.' + file_hdu
                file = join(dir_name,file_name)
                self.logger.info('writing rendered template to file: %r' % file)
                with open(file, 'w+') as text_file:
                    text_file.write(result)
            else:
                self.ready = False
                self.logger.error('Unable to process_rendered_template. ' +
                                  'result: {}, '.format(result) +
                                  'template: {}, '.format(template))

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

    def exit(self):
        '''Report the presense/lack of errors.'''
        if self.ready:
            if self.verbose: print('Completed!\n')
            exit(0)
        else:
            if self.verbose: print('Fail!\n')
            exit(1)
