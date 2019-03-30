from datamodel_parser.models.datamodel import Tree
from datamodel_parser.models.datamodel import Env
from datamodel_parser.models.datamodel import Location
from datamodel_parser.models.datamodel import Directory
from datamodel_parser.models.datamodel import File
from datamodel_parser.models.datamodel import Intro
from datamodel_parser.models.datamodel import Section
from datamodel_parser.models.datamodel import Hdu
from datamodel_parser.models.datamodel import Data
from datamodel_parser.models.datamodel import Column
from datamodel_parser.models.datamodel import Header
from datamodel_parser.models.datamodel import Keyword
from json import dumps

class Database:

    def __init__(self, logger=None, options=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_ready()
        self.set_attributes()

    def set_logger(self, logger=None):
        '''Set class logger.'''
        self.logger = logger if logger else None
        self.ready = bool(self.logger)
        if not self.ready: print('ERROR: Unable to set_logger.')

    def set_options(self, options=None):
        '''Set the options class attribute.'''
        self.options = None
        if self.ready:
            self.options = options if options else None
            if not self.options:
                self.ready = False
                self.logger.error('Unable to set_options')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger and
                          self.options)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.tree_columns = None

    def get_intros_sections_hdus(self):
        '''
            Get the rows from the intro and section table, as well as a data
            structure with columns from the data, header, and keyword tables.
        '''
        (intros,hdu_info_dict)=(None,None)
        if self.ready:
            if self.file_id:
                intros        = Intro.load_all(file_id=self.file_id)
                hdus          = Hdu.load_all(file_id=self.file_id)
                hdu_info_dict = self.get_hdu_info_dict(hdus=hdus)
                if not (intros and hdu_info_dict):
                    self.ready = False
                    self.logger.error('Unable to get_intros_sections_hdus.' +
                                      'intros: {}, '.format(intros) +
                                      'hdu_info_dict: {}.'.format(hdu_info_dict))
            else:
                self.ready = False
                self.logger.error('Unable to get_intros_sections_hdus.' +
                                  'self.file_id: {}.'.format(self.file_id))
        return (intros,hdu_info_dict)

    def get_hdu_info_dict(self,hdus=None):
        '''
            Get a data structure with columns from the data, header,
            and keyword hdus.
        '''
        hdu_info_dict = None
        if self.ready:
            headers = Header.load_all(hdus=hdus) if hdus else None
            datas   = Data.load_all(hdus=hdus)   if hdus else None
            if hdus and headers:
                hdu_info_dict = dict()
                for hdu in hdus: # datas can be empth
                    hdu_info_dict[hdu.number] = dict()
                    # hdu table information
                    hdu_info_dict[hdu.number]['hdu_number'] = (
                                               hdu.number if hdu else None)
                    hdu_info_dict[hdu.number]['hdu_title'] = (
                                               hdu.title if hdu else None)
                    hdu_info_dict[hdu.number]['hdu_description'] = (
                                               hdu.description if hdu else None)
                    hdu_info_dict[hdu.number]['hdu_datatype'] = (
                                'IMAGE' if hdu.is_image else
                                'BINARY TABLE' if hdu.is_image is not None
                                else None)
                    hdu_info_dict[hdu.number]['hdu_size'] = (
                                               hdu.size if hdu else None)
                    # header and data tables
                    hdu_info_dict[hdu.number]['header_table'] = dict()
                    hdu_info_dict[hdu.number]['data_table']    = dict()
                    header = headers[hdu.number] if hdu.number in headers else None
                    data   = datas[hdu.number]   if hdu.number in datas   else None
                    keywords = (Keyword.load_all(header_id=header.id)
                                if header else None)
                    columns =  (Column.load_all(data_id=data.id)
                                if data else None)
                    hdu_info_dict[hdu.number]['header_table']['caption'] = (
                                    header.table_caption if header else None)
                    hdu_info_dict[hdu.number]['header_table']['keywords'] = (
                                    keywords if keywords else None)
                    hdu_info_dict[hdu.number]['data_table']['caption'] = (
                                    data.table_caption if data else None)
                    hdu_info_dict[hdu.number]['data_table']['columns'] = (
                                    columns if columns else None)
            else:
                self.ready = False
                self.logger.error('Unable to get_hdu_info_dict. ' +
                                  '\nhdus: {}, '.format(hdus) +
                                  '\nheaders: {}, '.format(headers) +
                                  '\ndatas: {}.'.format(datas))
        return hdu_info_dict

    def set_tree_id(self,tree_edition=None):
        '''Get tree_id.'''
        self.tree_id = None
        if self.ready:
            if tree_edition:
                self.set_tree(edition=tree_edition)
                self.tree_id = self.tree.id if self.tree else None
                if not self.tree_id:
                    self.ready = False
                    self.logger.error('Unable to set_tree_id. ' +
                                      'self.tree_id: {}.'.format(self.tree_id))
            else:
                self.ready = False
                self.logger.error('Unable to get_tree_id. ' +
                                  'tree_edition: {}.'.format(tree_edition))

    def set_env_id(self,tree_edition=None,env_variable=None):
        '''Get env_id.'''
        self.env_id = None
        if self.ready:
            if tree_edition and env_variable:
                self.set_tree_id(tree_edition=tree_edition)
                self.set_env(tree_id=self.tree_id,variable=env_variable)
                self.env_id = self.env.id if self.env else None
                if not self.env_id:
                    self.ready = False
                    self.logger.error('Unable to set_env_id. '+
                                      'self.env_id: {}.'.format(self.env_id))
            else:
                self.ready = False
                self.logger.error('Unable to set_env_id. '
                                  'tree_edition: {}, '.format(tree_edition) +
                                  'env_variable: {}.'.format(env_variable)
                                  )

    def set_location_id(self,
                        tree_edition=None,
                        env_variable=None,
                        location_path=None
                        ):
        '''Get location_id.'''
        self.location_id = None
        if self.ready:
            if tree_edition and env_variable and location_path:
                self.set_env_id(tree_edition=tree_edition,
                                env_variable=env_variable)
                self.set_location(env_id=self.env_id,path=location_path)
                self.location_id = self.location.id if self.location else None
                if not self.location_id:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_location_id. ' +
                            'self.location_id: {}.'.format(self.location_id))
            else:
                self.ready = False
                self.logger.error('Unable to set_location_id. '
                                  'tree_edition: {}, '.format(tree_edition) +
                                  'env_variable: {}, '.format(env_variable) +
                                  'location_path: {}.'.format(location_path)
                                  )

    def set_file_id(self,
                    tree_edition  = None,
                    env_variable  = None,
                    location_path = None,
                    file_name     = None
                    ):
        '''Get file_id.'''
        self.file_id = None
        if self.ready:
            if tree_edition and env_variable and location_path and file_name:
                self.set_location_id(tree_edition  = tree_edition,
                                     env_variable  = env_variable,
                                     location_path = location_path)
                self.set_file(location_id=self.location_id,name=file_name)
                self.file_id = self.file.id if self.file else None
                if not self.file_id:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_file_id. ' +
                            'self.file_id: {}.'.format(self.file_id))
            else:
                self.ready = False
                self.logger.error('Unable to set_file_id. '
                                  'tree_edition: {}, '.format(tree_edition) +
                                  'env_variable: {}, '.format(env_variable) +
                                  'location_path: {}, '.format(location_path) +
                                  'file_name: {}.'.format(file_name)
                                  )

    def set_hdu_id(self,
                         tree_edition  = None,
                         env_variable  = None,
                         location_path = None,
                         file_name     = None,
                         hdu_number    = None
                         ):
        '''Get hdu_id.'''
        self.hdu_id = None
        if self.ready:
            if (tree_edition  and
                env_variable  and
                location_path and
                file_name     and
                hdu_number is not None
                ):
                self.set_file_id(tree_edition  = tree_edition,
                                 env_variable  = env_variable,
                                 location_path = location_path,
                                 file_name     = file_name)
                self.set_hdu(file_id=self.file_id,number=hdu_number)
                self.hdu_id = (self.hdu.id
                                     if self.hdu else None)
                if not self.hdu_id:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_hdu_id. ' +
                            'self.hdu_id: {}.'.format(self.hdu_id))
            else:
                self.ready = False
                self.logger.error('Unable to set_hdu_id. '
                                  'tree_edition: {}, '.format(tree_edition) +
                                  'env_variable: {}, '.format(env_variable) +
                                  'location_path: {}, '.format(location_path) +
                                  'file_name: {}, '.format(file_name)         +
                                  'hdu_number: {}.'.format(hdu_number)
                                  )

    def set_header_id(self,
                         tree_edition  = None,
                         env_variable  = None,
                         location_path = None,
                         file_name     = None,
                         hdu_number    = None,
                         ):
        '''Get header_id.'''
        self.header_id = None
        if self.ready:
            if (tree_edition           and
                env_variable           and
                location_path          and
                file_name              and
                hdu_number is not None
                ):
                self.set_hdu_id(tree_edition  = tree_edition,
                                      env_variable  = env_variable,
                                      location_path = location_path,
                                      file_name     = file_name,
                                      hdu_number    = hdu_number)
                self.set_header(hdu_id = self.hdu_id)
                self.header_id = self.header.id if self.header else None
                if not self.header_id:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_header_id. ' +
                            'self.header_id: {}.'.format(self.header_id))
            else:
                self.ready = False
                self.logger.error('Unable to set_header_id. ' +
                                  'tree_edition: {}, '.format(tree_edition) +
                                  'env_variable: {}, '.format(env_variable) +
                                  'location_path: {}, '.format(location_path) +
                                  'file_name: {}, '.format(file_name) +
                                  'hdu_number: {}.'.format(hdu_number)
                                  )

    def set_data_id(self,
                    tree_edition  = None,
                    env_variable  = None,
                    location_path = None,
                    file_name     = None,
                    hdu_number    = None
                    ):
        self.data_id = None
        '''Get data_id.'''
        if self.ready:
            if (tree_edition  and
                env_variable  and
                location_path and
                file_name     and
                hdu_number is not None
                ):
                self.set_hdu_id(tree_edition  = tree_edition,
                                      env_variable  = env_variable,
                                      location_path = location_path,
                                      file_name     = file_name,
                                      hdu_number    = hdu_number)
                self.set_data(hdu_id=self.hdu_id)
                self.data_id = self.data.id if self.data else None
                if not self.data_id:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_data_id. ' +
                            'self.data_id: {}.'.format(self.data_id))
            else:
                self.ready = False
                self.logger.error('Unable to set_data_id. '
                                  'tree_edition: {}, '.format(tree_edition) +
                                  'env_variable: {}, '.format(env_variable) +
                                  'location_path: {}, '.format(location_path) +
                                  'file_name: {}, '.format(file_name) +
                                  'hdu_number: {}.'.format(hdu_number)
                                  )

    def set_tree_columns(self,edition=None):
        '''Set columns of the tree table.'''
        self.tree_columns = None
        if self.ready:
            if edition:
                self.tree_columns = {'edition': edition if edition else None}
            else:
                self.ready = False
                self.logger.error('Unable to set_tree_columns. '
                                  'edition: {}.'.format(edition))

    def populate_tree_table(self):
        '''Update/Create tree table row.'''
        if self.ready:
            self.set_tree()
            if self.tree: self.update_tree_row()
            else:         self.create_tree_row()

    def set_tree(self,edition=None):
        '''Load row from tree table.'''
        self.tree = None
        if self.ready:
            edition = (edition if edition
                       else self.tree_columns['edition']
                       if self.tree_columns and 'edition' in self.tree_columns
                       else None)
            if edition:
                self.tree = Tree.load(edition=edition) if edition else None
            else:
                self.ready = False
                self.logger.error('Unable to set_tree. ' +
                                  'edition: {}.'.format(edition))

    def update_tree_row(self):
        '''Update row in tree table.'''
        if self.ready:
            columns = self.tree_columns if self.tree_columns else None
            if columns:
                self.logger.debug('Updating row in tree table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.tree.update_if_needed(columns=columns,skip_keys=skip_keys)
                if self.tree.updated:
                    self.logger.info('Updated Tree[id={0}], edition: {1}.'
                        .format(self.tree.id, self.tree.edition))
            else:
                self.ready = False
                self.logger.error('Unable to update_tree_row. '
                                  'columns: {}.'.format(columns))

    def create_tree_row(self):
        '''Create row in tree table.'''
        if self.ready:
            columns = self.tree_columns if self.tree_columns else None
            if columns:
                self.logger.debug('Adding new row to tree table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))

                tree = Tree(edition = columns['edition']
                            if columns and 'edition' in columns else None)
                if tree:
                    tree.add()
                    tree.commit()
                    self.logger.info('Added Tree[id={0}], edition = {1}.'
                        .format(tree.id, tree.edition))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_tree_row. ' +
                                      'tree = \n{}.'.format(tree))
            else:
                self.ready = False
                self.logger.error('Unable to create_tree_row. ' +
                                  'columns: {}.'.format(columns))

    def set_env_columns(self,variable=None):
        '''Set columns of the env table.'''
        self.env_columns = dict()
        if self.ready:
            tree_id = self.tree_id if self.tree_id else None
            if tree_id and variable:
                self.env_columns = {
                    'tree_id' : tree_id  if tree_id  else None,
                    'variable': variable if variable else None,
                    }
            else:
                self.ready = False
                self.logger.error('Unable to set_env_columns.' +
                                  'tree_id: {}.'.format(tree_id) +
                                  'variable: {}.'.format(variable))

    def populate_env_table(self):
        '''Update/Create env table row.'''
        if self.ready:
            self.set_env()
            if self.env: self.update_env_row()
            else:        self.create_env_row()

    def set_env(self,tree_id=None,variable=None):
        '''Load row from env table.'''
        self.env = None
        if self.ready:
            tree_id = (tree_id if tree_id
                       else self.env_columns['tree_id']
                       if self.env_columns and 'tree_id' in self.env_columns
                       else None)
            variable = (variable if variable
                       else self.env_columns['variable']
                       if self.env_columns and 'variable' in self.env_columns
                       else None)
            if tree_id and variable:
                self.env = (Env.load(tree_id=tree_id,variable=variable)
                            if tree_id and variable else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_env. ' +
                                  'tree_id: {}, '.format(tree_id) +
                                  'variable: {}.'.format(variable))

    def update_env_row(self):
        '''Update row in env table.'''
        if self.ready:
            columns = self.env_columns if self.env_columns else None
            if columns:
                self.logger.debug('Updating row in env table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.env.update_if_needed(columns=columns,skip_keys=skip_keys)
                if self.env.updated:
                    self.logger.info('Updated Env[id={0}], variable: {1}.'
                        .format(self.env.id, self.env.variable))
            else:
                self.ready = None
                self.logger.error('Unable to update_env_row. ' +
                                  'columns: {}.'.format(columns))

    def create_env_row(self):
        '''Create row in env table.'''
        if self.ready:
            columns = self.env_columns if self.env_columns else None
            if columns:
                self.logger.debug('Adding new row to env table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                env = Env(
                    tree_id = columns['tree_id']
                                if columns and 'tree_id' in columns else None,
                    variable = columns['variable']
                                if columns and 'variable' in columns else None,
                                  )
                if env:
                    env.add()
                    env.commit()
                    self.logger.info('Added Env[id={0}], variable = {1}.'
                        .format(env.id, env.variable))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_env_row. ' +
                                      'env = \n{}.'.format(env))
            else:
                self.ready = False
                self.logger.error('Unable to create_env_row. ' +
                                  'columns: {}.'.format(columns))

    def set_location_columns(self,path=None):
        '''Set columns of the location table.'''
        self.location_columns = dict()
        if self.ready:
            env_id = self.env_id if self.env_id else None
            if env_id and path:
                self.location_columns = {
                    'env_id' : env_id  if env_id  else None,
                    'path'   : path    if path    else None,
                    }
            else:
                self.ready = False
                self.logger.error('Unable to set_location_columns.' +
                                  'env_id: {}, '.format(env_id) +
                                  'path: {}.'.format(path))

    def populate_location_table(self):
        '''Update/Create location table row.'''
        if self.ready:
            self.set_location()
            if self.location: self.update_location_row()
            else:             self.create_location_row()

    def set_location(self,env_id=None,path=None):
        '''Load row from location table.'''
        self.location = None
        if self.ready:
            env_id = (env_id if env_id
                    else self.location_columns['env_id']
                    if self.location_columns and 'env_id' in self.location_columns
                    else None)
            path = (path if path
                    else self.location_columns['path']
                    if self.location_columns and 'path' in self.location_columns
                    else None)
            if env_id and path:
                self.location = (Location.load(env_id=env_id,path=path)
                                 if env_id and path else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_location. ' +
                                  'env_id: {}, '.format(env_id) +
                                  'path: {}.'.format(path))

    def update_location_row(self):
        '''Update row in location table.'''
        if self.ready:
            columns = self.location_columns if self.location_columns else None
            if columns:
                self.logger.debug('Updating row in location table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.location.update_if_needed(columns=columns,skip_keys=skip_keys)
                if self.location.updated:
                    self.logger.info('Updated Location[id={0}], path: {1}.'
                        .format(self.location.id, self.location.path))
            else:
                self.ready = False
                self.logger.error('Unable to update_location_row. ' +
                                  'columns: {}.'.format(columns))

    def create_location_row(self):
        '''Create row in location table.'''
        if self.ready:
            columns = self.location_columns if self.location_columns else None
            if columns:
                self.logger.debug('Adding new row to location table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                location = Location(
                            env_id = columns['env_id']
                                if columns and 'env_id' in columns else None,
                            path = columns['path']
                                if columns and 'path' in columns else None,
                                  )
                if location:
                    location.add()
                    location.commit()
                    self.logger.info('Added Location[id={0}], path = {1}.'
                        .format(location.id, location.path))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_location_row. ' +
                                      'location = \n{}.'.format(location))
            else:
                self.ready = False
                self.logger.error('Unable to create_location_row. ' +
                                  'columns: {}.'.format(columns))

    def set_directory_columns(self,name=None,depth=None):
        '''Set columns of the directory table.'''
        self.directory_columns = dict()
        if self.ready:
            location_id = self.location_id if self.location_id else None
            if location_id and name and depth is not None:
                self.directory_columns = {
                    'location_id' : location_id  if location_id        else None,
                    'name'        : name         if name               else None,
                    'depth'       : depth        if depth is not None  else None,
                    }
            else:
                self.ready = False
                self.logger.error('Unable to set_directory_columns.'       +
                                  'location_id: {}, '.format(location_id) +
                                  'name: {}, '.format(name)        +
                                  'depth: {}.'.format(depth))

    def populate_directory_table(self):
        '''Update/Create directory table row.'''
        if self.ready:
            self.set_directory()
            if self.directory: self.update_directory_row()
            else:              self.create_directory_row()

    def set_directory(self):
        '''Load row from directory table.'''
        self.directory = None
        if self.ready:
            columns = self.directory_columns if self.directory_columns else None
            self.ready = bool(columns and 'location_id' in columns
                                      and 'name' in columns
                                      and 'depth' in columns)
            if self.ready:
                self.directory = Directory.load(
                    location_id = columns['location_id'],
                    name = columns['name'],
                    depth = columns['depth'],
                    )
            else:
                self.logger.error('Unable to set_directory. ' +
                                  'columns: {}.'.format(columns))

    def update_directory_row(self):
        '''Update row in directory table.'''
        if self.ready:
            columns = self.directory_columns if self.directory_columns else None
            self.ready = bool(columns and 'location_id' in columns
                                      and 'name' in columns
                                      and 'depth' in columns)
            if self.ready:
                self.logger.debug('Updating row in directory table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.directory.update_if_needed(columns=columns,
                                                skip_keys=skip_keys)
                if self.directory.updated:
                    self.logger.info(
                        'Updated Directory[id={}], '.format(self.directory.id) +
                        'location_id = {}, '.format(self.directory.location_id) +
                        'name = {}, '.format(self.directory.name) +
                        'depth = {}.'.format(self.directory.depth))
            else:
                self.logger.error('Unable to update_directory_row. ' +
                                  'columns: {}.'.format(columns))

    def create_directory_row(self):
        '''Create row in directory table.'''
        if self.ready:
            columns = self.directory_columns if self.directory_columns else None
            self.ready = bool(columns and 'location_id' in columns
                                      and 'name' in columns
                                      and 'depth' in columns)
            if self.ready:
                self.logger.debug('Adding new row to directory table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                directory = Directory(
                            location_id = columns['location_id'],
                            name        = columns['name'],
                            depth       = columns['depth'],
                                  )
                if directory:
                    directory.add()
                    directory.commit()
                    self.logger.info(
                        'Added Directory[id={}], '.format(directory.id) +
                        'location_id = {}, '.format(directory.location_id) +
                        'name = {}, '.format(directory.name) +
                        'depth = {}.'.format(directory.depth))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_directory_row. ' +
                                      'directory = \n{}.'.format(directory))
            else:
                self.logger.error('Unable to create_directory_row. ' +
                                  'columns: {}.'.format(columns))

    def set_file_columns(self,name=None,hdu_count=None):
        '''Set columns of the file table.'''
        self.file_columns = dict()
        if self.ready:
            location_id = self.location_id if self.location_id else None
            if location_id and name and hdu_count:
                self.file_columns = {
                    'location_id'     :
                        location_id     if location_id     else None,
                    'name'            :
                        name            if name            else None,
                    'hdu_count' :
                        hdu_count if hdu_count else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                                'Unable to set_file_columns.' +
                                'location_id: {}, '.format(location_id) +
                                'name: {}, '.format(name) +
                                'hdu_count: {}.'.format(hdu_count))

    def populate_file_table(self):
        '''Update/Create file table row.'''
        if self.ready:
            self.set_file()
            if self.file: self.update_file_row()
            else:         self.create_file_row()

    def set_file(self,location_id=None,name=None):
        '''Load row from file table.'''
        self.file = None
        if self.ready:
            location_id = (location_id if location_id
                    else self.file_columns['location_id']
                    if self.file_columns and 'location_id' in self.file_columns
                    else None)
            name = (name if name
                    else self.file_columns['name']
                    if self.file_columns and 'name' in self.file_columns
                    else None)
            if location_id and name:
                self.file = (File.load(location_id=location_id,name=name)
                             if location_id and name else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_file. ' +
                                  'location_id: {}, '.format(location_id) +
                                  'name: {}.'.format(name))

    def update_file_row(self):
        '''Update row in file table.'''
        if self.ready:
            columns = self.file_columns if self.file_columns else None
            if columns:
                self.logger.debug('Updating row in file table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.file.update_if_needed(columns=columns,skip_keys=skip_keys)
                if self.file.updated:
                    self.logger.info('Updated File[id={0}], name: {1}.'
                        .format(self.file.id, self.file.name))
            else:
                self.ready = False
                self.logger.error('Unable to update_file_row. ' +
                                  'columns: {}.'.format(columns))

    def create_file_row(self):
        '''Create row in file table.'''
        if self.ready:
            columns = self.file_columns if self.file_columns else None
            if columns:
                self.logger.debug('Adding new row to file table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                file = File(
                    location_id = columns['location_id']
                        if columns and 'location_id' in columns else None,
                    name = columns['name']
                        if columns and 'name' in columns else None,
                    hdu_count = columns['hdu_count']
                        if columns and 'hdu_count' in columns else None,
                                  )
                if file:
                    file.add()
                    file.commit()
                    self.logger.info('Added File[id={0}], name = {1}.'
                        .format(file.id, file.name))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_file_row. ' +
                                      'file = \n{}.'.format(file))
            else:
                self.ready = False
                self.logger.error('Unable to create_file_row. ' +
                                  'columns: {}.'.format(columns))

    def set_intro_columns(self,
                          position = None,
                          heading_level = None,
                          heading_title = None,
                          description   = None,
                          ):
        '''Set columns of the intro table.'''
        self.intro_columns = dict()
        if self.ready:
            file_id = self.file_id if self.file_id else None
            if (file_id                   and
                position is not None and
#                heading_level is not None and
                heading_title         and
                description is not None
                ):
                self.intro_columns = {
                    'file_id'       : file_id
                                      if file_id                   else None,
                    'position' : position
                                      if position is not None else None,
                    'heading_level' : heading_level
                                      if heading_level is not None else None,
                    'heading_title' : heading_title
                                      if heading_title             else None,
                    'description'   : description
                                      if description               else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_intro_columns. ' +
                    'file_id: {}, '.format(file_id) +
                    'position: {}, '.format(position) +
                    'heading_level: {}, '.format(heading_level) +
                    'heading_title: {}, '.format(heading_title) +
                    'description: {}.'.format(description))

    def populate_intro_table(self):
        '''Update/Create intro table row.'''
        if self.ready:
            self.set_intro()
            if self.intro: self.update_intro_row()
            else:          self.create_intro_row()

    def set_intro(self,file_id=None,heading_title=None):
        '''Load row from intro table.'''
        self.intro = None
        if self.ready:
            file_id = (file_id if file_id
                    else self.intro_columns['file_id']
                    if self.intro_columns and 'file_id' in self.intro_columns
                    else None)
            heading_title = (heading_title if heading_title
                    else self.intro_columns['heading_title']
                    if self.intro_columns and 'heading_title' in self.intro_columns
                    else None)
            if file_id and heading_title:
                self.intro = (Intro.load(file_id=file_id,
                                        heading_title=heading_title)
                              if file_id and heading_title else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_intro. ' +
                                  'file_id: {}, '.format(file_id) +
                                  'heading_title: {}.'.format(heading_title))

    def update_intro_row(self):
        '''Update row in intro table.'''
        if self.ready:
            columns = self.intro_columns if self.intro_columns else None
            if columns:
                self.logger.debug('Updating row in intro table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.intro.update_if_needed(columns=columns,skip_keys=skip_keys)
                if self.intro.updated:
                    self.logger.info('Updated Intro[id={0}], heading_title: {1}.'
                                     .format(self.intro.id,
                                             self.intro.heading_title))
            else:
                self.ready = False
                self.logger.error('Unable to update_intro_row. ' +
                                  'columns: {}.'.format(columns))

    def create_intro_row(self):
        '''Create row in intro table.'''
        if self.ready:
            columns = self.intro_columns if self.intro_columns else None
            if columns:
                self.logger.debug('Adding new row to intro table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                intro = Intro(
                    file_id = columns['file_id']
                        if columns and 'file_id' in columns else None,
                    position = columns['position']
                        if columns and 'position' in columns else None,
                    heading_level = columns['heading_level']
                        if columns and 'heading_level' in columns else None,
                    heading_title = columns['heading_title']
                        if columns and 'heading_title' in columns else None,
                    description = columns['description']
                        if columns and 'description' in columns else None,
                                  )
                if intro:
                    intro.add()
                    intro.commit()
                    self.logger.info('Added Intro[id={0}], heading_title: {1}.'
                                     .format(intro.id,intro.heading_title))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_intro_row. ' +
                                      'intro = \n{}.'.format(intro))
            else:
                self.ready = False
                self.logger.error('Unable to create_intro_row. ' +
                                  'columns: {}.'.format(columns))

    def set_section_columns(self,hdu_number=None,hdu_title=None):
        '''Set columns of the section table.'''
        self.section_columns = dict()
        if self.ready:
            file_id = self.file_id if self.file_id else None
            # When there's no file section hdu_number and hdu_title are None
            if file_id:
                self.section_columns = {
                    'file_id'    : file_id    if file_id                else None,
                    'hdu_number' : hdu_number if hdu_number is not None else None,
                    'hdu_title'   : hdu_title   if hdu_title               else None,
                    }
            else:
                self.ready = False
                self.logger.error('Unable to set_section_columns. ' +
                                  'file_id: {}, '.format(file_id) +
                                  'hdu_number: {}, '.format(hdu_number) +
                                  'hdu_title: {}.'.format(hdu_title))

    def populate_section_table(self):
        '''Update/Create section table row.'''
        if self.ready:
            self.set_section()
            if self.section: self.update_section_row()
            else:            self.create_section_row()

    def set_section(self,file_id=None,hdu_number=None,hdu_title=None):
        '''Load row from section table.'''
        self.section = None
        if self.ready:
            file_id = (file_id if file_id
                else self.section_columns['file_id']
                if self.section_columns and 'file_id' in self.section_columns
                else None)
            hdu_number = (hdu_number if hdu_number is not None
                else self.section_columns['hdu_number']
                if self.section_columns and 'hdu_number' in self.section_columns
                else None)
            hdu_title = (hdu_title if hdu_title
                else self.section_columns['hdu_title']
                if self.section_columns and 'hdu_title' in self.section_columns
                else None)
            if file_id: # if there's no file section hdu_number=hdu_title=None
                self.section = Section.load(file_id  = file_id,
                                           hdu_number = hdu_number,
                                           hdu_title   = hdu_title)
            else:
                self.ready = False
                self.logger.error('Unable to set_section. ' +
                                  'file_id: {}, '.format(file_id))

    def update_section_row(self):
        '''Update row in section table.'''
        if self.ready:
            columns = self.section_columns if self.section_columns else None
            if columns:
                self.logger.debug('Updating row in section table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.section.update_if_needed(columns=columns,skip_keys=skip_keys)
                if self.section.updated:
                    self.logger.info(
                        'Updated Section[id={0}], hdu_number: {1}, hdu_title: {2}'
                        .format(self.section.id,
                                self.section.hdu_number,
                                self.section.hdu_title))
            else:
                self.ready = False
                self.logger.error('Unable to update_section_row. ' +
                                  'columns: {}.'.format(columns))

    def create_section_row(self):
        '''Create row in section table.'''
        if self.ready:
            columns = self.section_columns if self.section_columns else None
            if columns:
                self.logger.debug('Adding new row to section table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                section = Section(
                    file_id = columns['file_id']
                        if columns and 'file_id' in columns else None,
                    hdu_number = columns['hdu_number']
                        if columns and 'hdu_number' in columns else None,
                    hdu_title = columns['hdu_title']
                        if columns and 'hdu_title' in columns else None,
                                  )
                if section:
                    section.add()
                    section.commit()
                    self.logger.info(
                        'Added Section[id={0}], hdu_number: {1}, hdu_title: {2}'
                        .format(section.id,section.hdu_number,section.hdu_title))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_section_row. ' +
                                      'section = \n{}.'.format(section))
            else:
                self.ready = False
                self.logger.error('Unable to create_section_row. ' +
                                  'columns: {}.'.format(columns))

    def set_hdu_columns(self,
                        is_image=None,
                        number=None,
                        title=None,
                        size=None,
                        description=None,
                        ):
        '''Set columns of the hdu table.'''
        self.hdu_columns = dict()
        if self.ready:
            file_id = self.file_id if self.file_id else None
            if file_id and number is not None and title:
                # size and description can be null
                self.hdu_columns = {
                    'file_id'      : file_id
                                        if file_id              else None,
                    'is_image'     : is_image
                                        if is_image             else None,
                    'number'       : number
                                        if number   is not None else None,
                    'title'        : title
                                        if title                else None,
                    'size'         : size
                                        if size                 else None,
                    'description'  : description
                                        if description          else None,

                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_hdu_columns. ' +
                    'file_id: {}, '.format(file_id) +
                    'is_image: {}, '.format(is_image) +
                    'number: {}, '.format(number) +
                    'title: {}.'.format(title))

    def populate_hdu_table(self):
        '''Update/Create hdu table row.'''
        if self.ready:
            self.set_hdu()
            if self.hdu: self.update_hdu_row()
            else:        self.create_hdu_row()

    def set_hdu(self,file_id=None,number=None):
        '''Load row from hdu table.'''
        self.hdu = None
        if self.ready:
            file_id = (file_id if file_id
                else self.hdu_columns['file_id']
                if self.hdu_columns
                and 'file_id' in self.hdu_columns
                else None)
            number = (number if number is not None
                else self.hdu_columns['number']
                if self.hdu_columns
                and 'number' in self.hdu_columns
                else None)
            if file_id and number is not None:
                self.hdu = (Hdu.load(file_id=file_id,number=number)
                            if file_id and number is not None
                            else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_hdu. ' +
                                  'file_id: {}, '.format(file_id)+
                                  'number: {}.'.format(number))

    def update_hdu_row(self):
        '''Update row in hdu table.'''
        if self.ready:
            columns = self.hdu_columns if self.hdu_columns else None
            if columns:
                self.logger.debug('Updating row in hdu table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.hdu.update_if_needed(columns=columns,
                                                skip_keys=skip_keys)
                if self.hdu.updated:
                    self.logger.info(
                        'Updated Hdu[id={0}], file_id: {1}, number: {2}'
                        .format(self.hdu.id,
                                self.hdu.file_id,
                                self.hdu.number))
            else:
                self.ready = False
                self.logger.error('Unable to update_hdu_row. ' +
                                  'columns: {}.'.format(columns))

    def create_hdu_row(self):
        '''Create row in hdu table.'''
        if self.ready:
            columns = self.hdu_columns if self.hdu_columns else None
            if columns:
                self.logger.debug('Adding new row to hdu table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                hdu = Hdu(
                    file_id = columns['file_id']
                        if columns and 'file_id' in columns else None,
                    is_image = columns['is_image']
                        if columns and 'is_image' in columns else None,
                    number = columns['number']
                        if columns and 'number' in columns else None,
                    title = columns['title']
                        if columns and 'title' in columns else None,
                    size = columns['size']
                        if columns and 'size' in columns else None,
                    description = columns['description']
                        if columns and 'description' in columns else None,
                                  )
                if hdu:
                    hdu.add()
                    hdu.commit()
                    self.logger.info(
                        'Added Hdu[id={0}], file_id: {1}, number: {2}'
                        .format(hdu.id, hdu.file_id,  hdu.number))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_hdu_row. ' +
                                      'hdu = \n{}.'.format(hdu))
            else:
                self.ready = False
                self.logger.error('Unable to create_hdu_row. ' +
                                  'columns: {}.'.format(columns))

    def set_data_columns(self,hdu_number=None,table_caption=None):
        '''Set columns of the data table.'''
        self.data_columns = dict()
        if self.ready:
            hdu_id = self.hdu_id if self.hdu_id else None
            if hdu_id and hdu_number is not None:
                self.data_columns = {
                    'hdu_id'  : hdu_id  if hdu_id
                                                    else None,
                    'hdu_number'    : hdu_number    if hdu_number is not None
                                                    else None,
                    'table_caption' : table_caption if table_caption is not None
                                                    else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_data_columns. ' +
                    'hdu_id: {}, '.format(hdu_id) +
                    'hdu_number: {}, '.format(hdu_number) +
                    'table_caption: {}, '.format(table_caption))

    def populate_data_table(self):
        '''Update/Create data table row.'''
        if self.ready:
            self.set_data()
            if self.data: self.update_data_row()
            else:           self.create_data_row()

    def set_data(self,hdu_id=None,hdu_number=None):
        '''Load row from data table.'''
        self.data = None
        if self.ready:
            hdu_id = (hdu_id if hdu_id
                else self.data_columns['hdu_id']
                if self.data_columns and 'hdu_id' in self.data_columns
                else None)
            hdu_number = (hdu_number if hdu_number is not None
                else self.data_columns['hdu_number']
                if self.data_columns and 'hdu_number' in self.data_columns
                else None)
            if hdu_id and hdu_number is not None:
                self.data = (Data.load(hdu_id=hdu_id)
                               if hdu_id else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_data. ' +
                                  'hdu_id: {}, '.format(hdu_id))

    def update_data_row(self):
        '''Update row in data table.'''
        if self.ready:
            columns = self.data_columns if self.data_columns else None
            if columns:
                self.logger.debug('Updating row in data table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.data.update_if_needed(columns=columns,
                                             skip_keys=skip_keys)
                if self.data.updated:
                    self.logger.info(
                        'Updated Data[id={}], '.format(self.data.id) +
                        'hdu_id: {}, '.format(self.data.hdu_id) +
                        'hdu_number: {}.'.format(self.data.hdu_number) +
                        'table_caption: {}.'.format(self.data.table_caption))
            else:
                self.ready = False
                self.logger.error('Unable to update_data_row. ' +
                                  'columns: {}.'.format(columns))

    def create_data_row(self):
        '''Create row in data table.'''
        if self.ready:
            columns = self.data_columns if self.data_columns else None
            if columns:
                self.logger.debug('Adding new row to data table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                data = Data(
                    hdu_id = columns['hdu_id']
                        if columns and 'hdu_id' in columns else None,
                    hdu_number = columns['hdu_number']
                        if columns and 'hdu_number' in columns else None,
                    table_caption = columns['table_caption']
                        if columns and 'table_caption' in columns else None,
                                  )
                if data:
                    data.add()
                    data.commit()
                    self.logger.info(
                        'Added Data[id={}], '.format(data.id) +
                        'hdu_id: {}, '.format(data.hdu_id) +
                        'hdu_number: {}.'.format(data.hdu_number))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_data_row. ' +
                                      'data = \n{}.'.format(data))
            else:
                self.ready = False
                self.logger.error('Unable to create_data_row. ' +
                                  'columns: {}.'.format(columns))

    def set_column_columns(self,position=None,table_row=None):
        '''Set columns of the column table.'''
        self.column_columns = dict()
        if self.ready:
            data_id = self.data_id if self.data_id else None
            if data_id and position is not None and table_row:
                name        = table_row[0] if table_row else None
                datatype    = table_row[1] if table_row else None
                units       = table_row[2] if table_row else None
                description = table_row[3] if table_row else None
                self.column_columns = {
                    'data_id'     : data_id     if data_id              else None,
                    'position'    : position    if position is not None else None,
                    'name'        : name        if name                 else None,
                    'datatype'    : datatype    if datatype is not None else None,
                    'units'       : units       if units                else None,
                    'description' : description if description          else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_column_columns. ' +
                    'data_id: {}, '.format(data_id) +
                    'position: {}, '.format(position) +
                    'table_row: {}, '.format(table_row))

    def populate_column_table(self):
        '''Update/Create column table row.'''
        if self.ready:
            self.set_column()
            if self.column: self.update_column_row()
            else:           self.create_column_row()

    def set_column(self,data_id=None,position=None,name=None):
        '''Load row from column table.'''
        self.column = None
        if self.ready:
            data_id = (data_id if data_id
                else self.column_columns['data_id']
                if self.column_columns and 'data_id' in self.column_columns
                else None)
            position = (position if position is not None
                else self.column_columns['position']
                if self.column_columns and 'position' in self.column_columns
                else None)
            name = (name if name
                else self.column_columns['name']
                if self.column_columns and 'name' in self.column_columns
                else None)
            if data_id and position is not None and name:
                self.column = (Column.load(data_id = data_id,
                                           position  = position,
                                           name      = name)
                                if data_id
                                and position is not None
                                and name
                                else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_column. ' +
                                  'data_id: {}, '.format(data_id))

    def update_column_row(self):
        '''Update row in column table.'''
        if self.ready:
            columns = self.column_columns if self.column_columns else None
            if columns:
                self.logger.debug('Updating row in column table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.column.update_if_needed(columns=columns,
                                             skip_keys=skip_keys)
                if self.column.updated:
                    self.logger.info(
                        'Updated Column[id={}], '.format(self.column.id) +
                        'data_id: {}, '.format(self.column.data_id) +
                        'name: {}.'.format(self.column.name))
            else:
                self.ready = False
                self.logger.error('Unable to update_column_row. ' +
                                  'columns: {}.'.format(columns))

    def create_column_row(self):
        '''Create row in column table.'''
        if self.ready:
            columns = self.column_columns if self.column_columns else None
            if columns:
                self.logger.debug('Adding new row to column table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                column = Column(
                    data_id = columns['data_id']
                        if columns and 'data_id' in columns else None,
                    position = columns['position']
                        if columns and 'position' in columns else None,
                    name = columns['name']
                        if columns and 'name' in columns else None,
                    datatype = columns['datatype']
                        if columns and 'datatype' in columns else None,
                    units = columns['units']
                        if columns and 'units' in columns else None,
                    description = columns['description']
                        if columns and 'description' in columns else None,
                                  )
                if column:
                    column.add()
                    column.commit()
                    self.logger.info(
                        'Added Column[id={}], '.format(column.id) +
                        'data_id: {}, '.format(column.data_id) +
                        'name: {}.'.format(column.name))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_column_row. ' +
                                      'name = \n{}.'.format(name))
            else:
                self.ready = False
                self.logger.error('Unable to create_column_row. ' +
                                  'columns: {}.'.format(columns))

    def set_header_columns(self,hdu_number=None,table_caption=None):
        '''Set columns of the header table.'''
        self.header_columns = dict()
        if self.ready:
            hdu_id = self.hdu_id if self.hdu_id else None
            if hdu_id and hdu_number is not None:
                self.header_columns = {
                    'hdu_id'  : hdu_id  if hdu_id
                                                    else None,
                    'hdu_number'    : hdu_number    if hdu_number is not None
                                                    else None,
                    'table_caption' : table_caption if table_caption is not None
                                                    else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_header_columns. ' +
                    'hdu_id: {}, '.format(hdu_id) +
                    'hdu_number: {}, '.format(hdu_number) +
                    'table_caption: {}, '.format(table_caption))

    def populate_header_table(self):
        '''Update/Create header table row.'''
        if self.ready:
            self.set_header()
            if self.header: self.update_header_row()
            else:           self.create_header_row()

    def set_header(self,hdu_id=None,hdu_number=None):
        '''Load row from header table.'''
        self.header = None
        if self.ready:
            hdu_id = (hdu_id if hdu_id
                else self.header_columns['hdu_id']
                if self.header_columns and 'hdu_id' in self.header_columns
                else None)
            hdu_number = (hdu_number if hdu_number is not None
                else self.header_columns['hdu_number']
                if self.header_columns and 'hdu_number' in self.header_columns
                else None)
            if hdu_id and hdu_number is not None:
                self.header = (Header.load(hdu_id=hdu_id)
                               if hdu_id else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_header. ' +
                                  'hdu_id: {}, '.format(hdu_id))

    def update_header_row(self):
        '''Update row in header table.'''
        if self.ready:
            columns = self.header_columns if self.header_columns else None
            if columns:
                self.logger.debug('Updating row in header table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.header.update_if_needed(columns=columns,
                                             skip_keys=skip_keys)
                if self.header.updated:
                    self.logger.info(
                        'Updated Header[id={}], '.format(self.header.id) +
                        'hdu_id: {}, '.format(self.header.hdu_id) +
                        'hdu_number: {}.'.format(self.header.hdu_number) +
                        'table_caption: {}.'.format(self.header.table_caption))
            else:
                self.ready = False
                self.logger.error('Unable to update_header_row. ' +
                                  'columns: {}.'.format(columns))

    def create_header_row(self):
        '''Create row in header table.'''
        if self.ready:
            columns = self.header_columns if self.header_columns else None
            if columns:
                self.logger.debug('Adding new row to header table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                header = Header(
                    hdu_id = columns['hdu_id']
                        if columns and 'hdu_id' in columns else None,
                    hdu_number = columns['hdu_number']
                        if columns and 'hdu_number' in columns else None,
                    table_caption = columns['table_caption']
                        if columns and 'table_caption' in columns else None,
                                  )
                if header:
                    header.add()
                    header.commit()
                    self.logger.info(
                        'Added Header[id={}], '.format(header.id) +
                        'hdu_id: {}, '.format(header.hdu_id) +
                        'hdu_number: {}.'.format(header.hdu_number))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_header_row. ' +
                                      'header = \n{}.'.format(header))
            else:
                self.ready = False
                self.logger.error('Unable to create_header_row. ' +
                                  'columns: {}.'.format(columns))

    def set_keyword_columns(self,position=None,table_row=None):
        '''Set columns of the keyword table.'''
        self.keyword_columns = dict()
        if self.ready:
            header_id = self.header_id if self.header_id else None
            if header_id and position is not None and table_row:
                keyword  = table_row[0] if table_row else None
                value    = table_row[1] if table_row else None
                datatype = table_row[2] if table_row else None
                comment  = table_row[3] if table_row else None
                self.keyword_columns = {
                    'header_id'     : header_id     if header_id
                                                    else None,
                    'position'      : position      if position is not None
                                                    else None,
                    'keyword'       : keyword       if keyword
                                                    else None,
                    'value'         : value         if value is not None
                                                    else None,
                    'datatype'      : datatype      if datatype
                                                    else None,
                    'comment'       : comment       if comment
                                                    else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_keyword_columns. ' +
                    'header_id: {}, '.format(header_id) +
                    'position: {}, '.format(position) +
                    'table_row: {}, '.format(table_row))

    def populate_keyword_table(self):
        '''Update/Create keyword table row.'''
        if self.ready:
            self.set_keyword()
            if self.keyword: self.update_keyword_row()
            else:            self.create_keyword_row()

    def set_keyword(self,header_id=None,position=None,keyword=None):
        '''Load row from keyword table.'''
        self.keyword = None
        if self.ready:
            header_id = (header_id if header_id
                else self.keyword_columns['header_id']
                if self.keyword_columns and 'header_id' in self.keyword_columns
                else None)
            position = (position if position is not None
                else self.keyword_columns['position']
                if self.keyword_columns and 'position' in self.keyword_columns
                else None)
            keyword = (keyword if keyword
                else self.keyword_columns['keyword']
                if self.keyword_columns and 'keyword' in self.keyword_columns
                else None)
            if header_id and position is not None and keyword:
                self.keyword = (Keyword.load(header_id     = header_id,
                                             position = position,
                                             keyword   = keyword)
                                if header_id
                                and position is not None
                                and keyword
                                else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_keyword. ' +
                                  'header_id: {}, '.format(header_id))

    def update_keyword_row(self):
        '''Update row in keyword table.'''
        if self.ready:
            columns = self.keyword_columns if self.keyword_columns else None
            if columns:
                self.logger.debug('Updating row in keyword table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.keyword.update_if_needed(columns=columns,
                                             skip_keys=skip_keys)
                if self.keyword.updated:
                    self.logger.info(
                        'Updated Keyword[id={}], '.format(self.keyword.id) +
                        'header_id: {}, '.format(self.keyword.header_id) +
                        'keyword: {}.'.format(self.keyword.keyword))
            else:
                self.ready = False
                self.logger.error('Unable to update_keyword_row. ' +
                                  'columns: {}.'.format(columns))

    def create_keyword_row(self):
        '''Create row in keyword table.'''
        if self.ready:
            columns = self.keyword_columns if self.keyword_columns else None
            if columns:
                self.logger.debug('Adding new row to keyword table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                keyword = Keyword(
                    header_id = columns['header_id']
                        if columns and 'header_id' in columns else None,
                    position = columns['position']
                        if columns and 'position' in columns else None,
                    keyword = columns['keyword']
                        if columns and 'keyword' in columns else None,
                    value = columns['value']
                        if columns and 'value' in columns else None,
                    datatype = columns['datatype']
                        if columns and 'datatype' in columns else None,
                    comment = columns['comment']
                        if columns and 'comment' in columns else None,
                                  )
                if keyword:
                    keyword.add()
                    keyword.commit()
                    self.logger.info(
                        'Added Keyword[id={}], '.format(keyword.id) +
                        'header_id: {}, '.format(keyword.header_id) +
                        'keyword: {}.'.format(keyword.keyword))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_keyword_row. ' +
                                      'keyword = \n{}.'.format(keyword))
            else:
                self.ready = False
                self.logger.error('Unable to create_keyword_row. ' +
                                  'columns: {}.'.format(columns))

