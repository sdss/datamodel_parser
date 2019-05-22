from datamodel_parser.application import File
from datamodel_parser.application import Database
from os import environ, walk
from os.path import join, exists, basename
from flask import render_template
from datamodel_parser import app
import logging
from json import dumps

class Store:

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
            self.datamodel_dir    = None
            self.path             = None
            self.tree_edition     = None
            self.env_variable     = None
            self.file_name        = None
            self.location_path    = None
            self.directory_names  = None
            self.directory_depths = None

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
        self.env_variable     = None
        self.file_name        = None
        self.location_path    = None
        self.directory_names  = None
        self.directory_depths = None
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

    def get_file_paths(self):
        '''Set a list of all files for the current tree edition.'''
        file_paths = list()
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
                                        file_paths.append(file_path)
                                else:
                                    self.ready = False
                                    self.logger.error('File does not exist: '
                                                      'file: {}'.format(file))
                    else: pass # it's okay to have empty filenames
            else:
                self.ready = False
                self.logger.error(
                    'Unable to get_file_paths. ' +
                    'self.datamodel_dir: {}'.format(self.datamodel_dir))
        return file_paths

    def set_file_path_skip_list(self):
        '''Set a list of file paths that don't conform to the database schema.'''
        self.file_path_skip_list = [
            'datamodel/files/MANGA_SPECTRO_REDUX/DRPVER/PLATE4/MJD5/mgFrame.html',
            'datamodel/files/MANGA_PIPE3D/MANGADRP_VER/PIPE3D_VER/PLATE/manga.Pipe3D.cube.html',
            ]


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
                    'self.database: {}.'.format(self.database) +
                    'self.tree_edition: {}.'.format(self.tree_edition))

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
                file =  join(self.datamodel_dir,self.path)
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
                self.logger.error('Unable to render_template.' +
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
