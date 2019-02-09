from datamodel_parser.models.datamodel import Tree
from datamodel_parser.models.datamodel import Env
from datamodel_parser.models.datamodel import Location
from datamodel_parser.models.datamodel import Directory
from datamodel_parser.models.datamodel import File
from datamodel_parser.models.datamodel import Intro
from datamodel_parser.models.datamodel import Section
from datamodel_parser.models.datamodel import Extension
from datamodel_parser.models.datamodel import Data
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
                                      'self.tree_id: {0}'.format(self.tree_id))
            else:
                self.logger = False
                self.logger.error('Unable to get_tree_id. ' +
                                  'tree_edition: {0}'.format(tree_edition))

    def set_env_id(self,tree_edition=None,env_variable=None):
        '''Get env_id.'''
        if self.ready:
            if tree_edition and env_variable:
                self.set_tree_id(tree_edition=tree_edition)
                self.set_env(tree_id=self.tree_id,variable=env_variable)
                self.env_id = self.env.id if self.env else None
                if not self.env_id:
                    self.ready = False
                    self.logger.error('Unable to set_env_id. self.env_id: {0}'
                                      .format(self.env_id))
            else:
                self.logger = False
                self.logger.error('Unable to set_env_id. '
                                  'tree_edition: {0}'.format(tree_edition) +
                                  'env_variable: {0}'.format(env_variable)
                                  )

    def set_location_id(self,
                        tree_edition=None,
                        env_variable=None,
                        location_path=None
                        ):
        '''Get location_id.'''
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
                            'self.location_id: {0}'.format(self.location_id))
            else:
                self.logger = False
                self.logger.error('Unable to set_location_id. '
                                  'tree_edition: {0}'.format(tree_edition) +
                                  'env_variable: {0}'.format(env_variable) +
                                  'location_path: {0}'.format(location_path)
                                  )

    def set_file_id(self,
                    tree_edition  = None,
                    env_variable  = None,
                    location_path = None,
                    file_name     = None
                    ):
        '''Get file_id.'''
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
                            'self.file_id: {0}'.format(self.file_id))
            else:
                self.logger = False
                self.logger.error('Unable to set_file_id. '
                                  'tree_edition: {0}'.format(tree_edition) +
                                  'env_variable: {0}'.format(env_variable) +
                                  'location_path: {0}'.format(location_path) +
                                  'file_name: {0}'.format(file_name)
                                  )

    def set_extension_id(self,
                    tree_edition  = None,
                    env_variable  = None,
                    location_path = None,
                    file_name     = None,
                    hdu_number    = None
                    ):
        '''Get extension_id.'''
        if self.ready:
            if (tree_edition and
                env_variable and
                location_path and
                file_name and
                hdu_number!=None):
                self.set_file_id(tree_edition  = tree_edition,
                                 env_variable  = env_variable,
                                 location_path = location_path,
                                 file_name     = file_name)
                self.set_extension(file_id=self.file_id,hdu_number=hdu_number)
                extension_id = self.extension.id if self.extension else None
                if not self.extension_id:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_extension_id. ' +
                            'self.extension_id: {0}'.format(self.extension_id))
            else:
                self.logger = False
                self.logger.error('Unable to set_extension_id. '
                                  'tree_edition: {0}'.format(tree_edition) +
                                  'env_variable: {0}'.format(env_variable) +
                                  'location_path: {0}'.format(location_path) +
                                  'file_name: {0}'.format(file_name)         +
                                  'hdu_number: {0}'.format(hdu_number)
                                  )

    def set_tree_columns(self,edition=None):
        '''Set columns of the tree table.'''
        if self.ready:
            if edition:
                self.tree_columns = {'edition': edition if edition else None}
            else:
                self.ready = False
                self.logger.error('Unable to set_tree_columns. '
                                  'edition: {0}'.format(edition))

    def populate_tree_table(self):
        '''Update/Create tree table row.'''
        if self.ready:
            self.set_tree()
            if self.tree: self.update_tree_row()
            else:         self.create_tree_row()

    def set_tree(self,edition=None):
        '''Load row from tree table.'''
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
                                  'edition: {0}'.format(edition))

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
                self.logger.error('Unable to update_tree_row. columns: {0}'
                                  .format(columns))

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
                                      'tree = \n{0}'.format(tree))
            else:
                self.ready = False
                self.logger.error('Unable to create_tree_row. ' +
                                  'columns: {0}'.format(columns))

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
                                  'tree_id: {0}.'.format(tree_id) +
                                  'variable: {0}.'.format(variable))

    def populate_env_table(self):
        '''Update/Create env table row.'''
        if self.ready:
            self.set_env()
            if self.env: self.update_env_row()
            else:        self.create_env_row()

    def set_env(self,tree_id=None,variable=None):
        '''Load row from env table.'''
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
                                  'tree_id: {0}, '.format(tree_id) +
                                  'variable: {0}.'.format(variable))

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
                self.logger.error('Unable to update_env_row. columns: {0}'
                                    .format(columns))

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
                                      'env = \n{0}'.format(env))
            else:
                self.ready = False
                self.logger.error('Unable to create_env_row. ' +
                                  'columns: {0}'.format(columns))

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
                                  'env_id: {0}, '.format(env_id) +
                                  'path: {1}.'.format(path))

    def populate_location_table(self):
        '''Update/Create location table row.'''
        if self.ready:
            self.set_location()
            if self.location: self.update_location_row()
            else:             self.create_location_row()

    def set_location(self,env_id=None,path=None):
        '''Load row from location table.'''
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
                                  'env_id: {0}'.format(env_id) +
                                  'path: {0}'.format(path))

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
                self.logger.error('Unable to update_location_row. columns: {0}'
                                    .format(columns))

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
                                      'location = \n{0}'.format(location))
            else:
                self.ready = False
                self.logger.error('Unable to create_location_row. ' +
                                  'columns: {0}'.format(columns))

    def set_directory_columns(self,name=None,depth=None):
        '''Set columns of the directory table.'''
        self.directory_columns = dict()
        if self.ready:
            location_id = self.location_id if self.location_id else None
            if location_id and name and depth!=None:
                self.directory_columns = {
                    'location_id' : location_id  if location_id  else None,
                    'name'        : name         if name         else None,
                    'depth'       : depth        if depth!=None  else None,
                    }
            else:
                self.ready = False
                self.logger.error('Unable to set_directory_columns.'       +
                                  'location_id: {0}, '.format(location_id) +
                                  'name: {0}, '       .format(name)        +
                                  'depth: {0}.'       .format(depth))

    def populate_directory_table(self):
        '''Update/Create directory table row.'''
        if self.ready:
            self.set_directory()
            if self.directory: self.update_directory_row()
            else:              self.create_directory_row()

    def set_directory(self):
        '''Load row from directory table.'''
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
                                  'columns: {0}'.format(columns))

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
                        'Updated Directory[id={0}], '.format(self.directory.id) +
                        'location_id = {0}, '.format(self.directory.location_id) +
                        'name = {0}, '.format(self.directory.name) +
                        'depth = {0}.'.format(self.directory.depth))
            else:
                self.logger.error('Unable to update_directory_row. columns: {0}'
                                    .format(columns))

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
                        'Added Directory[id={0}], '.format(directory.id) +
                        'location_id = {0}, '.format(directory.location_id) +
                        'name = {0}, '.format(directory.name) +
                        'depth = {0}.'.format(directory.depth))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_directory_row. ' +
                                      'directory = \n{0}'.format(directory))
            else:
                self.logger.error('Unable to create_directory_row. ' +
                                  'columns: {0}'.format(columns))

    def set_file_columns(self,name=None,extension_count=None):
        '''Set columns of the file table.'''
        self.file_columns = dict()
        if self.ready:
            location_id = self.location_id if self.location_id else None
            if location_id and name and extension_count:
                self.file_columns = {
                    'location_id'     :
                        location_id     if location_id     else None,
                    'name'            :
                        name            if name            else None,
                    'extension_count' :
                        extension_count if extension_count else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                                'Unable to set_file_columns.' +
                                'location_id: {0}, '.format(location_id) +
                                'name: {0}, '.format(name) +
                                'extension_count: {0}.'.format(extension_count))

    def populate_file_table(self):
        '''Update/Create file table row.'''
        if self.ready:
            self.set_file()
            if self.file: self.update_file_row()
            else:         self.create_file_row()

    def set_file(self,location_id=None,name=None):
        '''Load row from file table.'''
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
                                  'location_id: {0}, '.format(location_id) +
                                  'name: {0}.'.format(name))

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
                self.logger.error('Unable to update_file_row. columns: {0}'
                                    .format(columns))

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
                    extension_count = columns['extension_count']
                        if columns and 'extension_count' in columns else None,
                                  )
                if file:
                    file.add()
                    file.commit()
                    self.logger.info('Added File[id={0}], name = {1}.'
                        .format(file.id, file.name))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_file_row. ' +
                                      'file = \n{0}'.format(file))
            else:
                self.ready = False
                self.logger.error('Unable to create_file_row. ' +
                                  'columns: {0}'.format(columns))

    def set_intro_columns(self,
                          heading_order = None,
                          heading_level = None,
                          heading_title = None,
                          description   = None,
                          ):
        '''Set columns of the intro table.'''
        self.intro_columns = dict()
        if self.ready:
            file_id = self.file_id if self.file_id else None
            if (file_id               and
                heading_order != None and
                heading_level         and
                heading_title         and
                description != None
                ):
                self.intro_columns = {
                    'file_id'       : file_id
                                      if file_id       else None,
                    'heading_order' : heading_order
                                      if heading_order != None else None,
                    'heading_level' : heading_level
                                      if heading_level else None,
                    'heading_title' : heading_title
                                      if heading_title else None,
                    'description'   : description
                                      if description   else '',
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_intro_columns. ' +
                    'file_id: {0}, '.format(file_id) +
                    'heading_order: {0}, '.format(heading_order) +
                    'heading_level: {0}, '.format(heading_level) +
                    'heading_title: {0}, '.format(heading_title) +
                    'description: {0}.'   .format(description))

    def populate_intro_table(self):
        '''Update/Create intro table row.'''
        if self.ready:
            self.set_intro()
            if self.intro: self.update_intro_row()
            else:          self.create_intro_row()

    def set_intro(self,file_id=None,heading_title=None):
        '''Load row from intro table.'''
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
                                  'file_id: {0}, '.format(file_id) +
                                  'heading_title: {0}'.format(heading_title))

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
                self.logger.error('Unable to update_intro_row. columns: {0}'
                                    .format(columns))

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
                    heading_order = columns['heading_order']
                        if columns and 'heading_order' in columns else None,
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
                                      'intro = \n{0}'.format(intro))
            else:
                self.ready = False
                self.logger.error('Unable to create_intro_row. ' +
                                  'columns: {0}'.format(columns))

    def set_section_columns(self,hdu_number=None,hdu_name=None):
        '''Set columns of the section table.'''
        self.section_columns = dict()
        if self.ready:
            file_id = self.file_id if self.file_id else None
            if file_id and hdu_number!=None and hdu_name:
                self.section_columns = {
                    'file_id'    : file_id    if file_id          else None,
                    'hdu_number' : hdu_number if hdu_number!=None else None,
                    'hdu_name'   : hdu_name   if hdu_name         else None,
                    }
            else:
                self.ready = False
                self.logger.error('Unable to set_section_columns. ' +
                                  'file_id: {0}, '.format(file_id) +
                                  'hdu_number: {0}, '.format(hdu_number) +
                                  'hdu_name: {0}, '  .format(hdu_name))

    def populate_section_table(self):
        '''Update/Create section table row.'''
        if self.ready:
            self.set_section()
            if self.section: self.update_section_row()
            else:            self.create_section_row()

    def set_section(self,file_id=None,hdu_number=None,hdu_name=None):
        '''Load row from section table.'''
        if self.ready:
            file_id = (file_id if file_id
                else self.section_columns['file_id']
                if self.section_columns and 'file_id' in self.section_columns
                else None)
            hdu_number = (hdu_number if hdu_number!=None
                else self.section_columns['hdu_number']
                if self.section_columns and 'hdu_number' in self.section_columns
                else None)
            hdu_name = (hdu_name if hdu_name
                else self.section_columns['hdu_name']
                if self.section_columns and 'hdu_name' in self.section_columns
                else None)
            if file_id and hdu_number!=None and hdu_name:
                self.section = (Section.load(file_id=file_id,
                                           hdu_number=hdu_number,
                                           hdu_name=hdu_name)
                                if file_id and hdu_number!=None and hdu_name
                                else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_section. ' +
                                  'file_id: {0}, '.format(file_id) +
                                  'hdu_number: {0}'.format(hdu_number) +
                                  'hdu_name: {0}'.format(hdu_name))

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
                        'Updated Section[id={0}], hdu_number: {1}, hdu_name: {2}'
                        .format(self.section.id,
                                self.section.hdu_number,
                                self.section.hdu_name))
            else:
                self.ready = False
                self.logger.error('Unable to update_section_row. columns: {0}'
                                    .format(columns))

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
                    hdu_name = columns['hdu_name']
                        if columns and 'hdu_name' in columns else None,
                                  )
                if section:
                    section.add()
                    section.commit()
                    self.logger.info(
                        'Added Section[id={0}], hdu_number: {1}, hdu_name: {2}'
                        .format(section.id,section.hdu_number,section.hdu_name))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_section_row. ' +
                                      'section = \n{0}'.format(section))
            else:
                self.ready = False
                self.logger.error('Unable to create_section_row. ' +
                                  'columns: {0}'.format(columns))

    def set_extension_columns(self,hdu_number=None):
        '''Set columns of the extension table.'''
        self.extension_columns = dict()
        if self.ready:
            file_id = self.file_id if self.file_id else None
            if file_id and hdu_number!=None:
                self.extension_columns = {
                    'file_id'    : file_id    if file_id          else None,
                    'hdu_number' : hdu_number if hdu_number!=None else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_extension_columns. ' +
                    'file_id: {0}, '.format(file_id) +
                    'hdu_number: {0}, '.format(hdu_number))

    def populate_extension_table(self):
        '''Update/Create extension table row.'''
        if self.ready:
            self.set_extension()
            if self.extension: self.update_extension_row()
            else:              self.create_extension_row()

    def set_extension(self,file_id=None,hdu_number=None):
        '''Load row from extension table.'''
        if self.ready:
            file_id = (file_id if file_id
                else self.extension_columns['file_id']
                if self.extension_columns
                and 'file_id' in self.extension_columns
                else None)
            hdu_number = (hdu_number if hdu_number!=None
                else self.extension_columns['hdu_number']
                if self.extension_columns
                and 'hdu_number' in self.extension_columns
                else None)
            if file_id and hdu_number!=None:
                self.extension = (Extension.load(file_id=file_id,
                                                 hdu_number=hdu_number)
                                if file_id and hdu_number!=None else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_extension. ' +
                                  'file_id: {0}, '.format(file_id) +
                                  'hdu_number: {0}'.format(hdu_number))

    def update_extension_row(self):
        '''Update row in extension table.'''
        if self.ready:
            columns = self.extension_columns if self.extension_columns else None
            if columns:
                self.logger.debug('Updating row in extension table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                skip_keys = []
                self.extension.update_if_needed(columns=columns,
                                                skip_keys=skip_keys)
                if self.extension.updated:
                    self.logger.info(
                        'Updated Extension[id={0}], file_id: {1}, hdu_number: {2}'
                        .format(self.extension.id,
                                self.extension.file_id,
                                self.extension.hdu_number))
            else:
                self.ready = False
                self.logger.error('Unable to update_extension_row. columns: {0}'
                                    .format(columns))

    def create_extension_row(self):
        '''Create row in extension table.'''
        if self.ready:
            columns = self.extension_columns if self.extension_columns else None
            if columns:
                self.logger.debug('Adding new row to extension table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                extension = Extension(
                    file_id = columns['file_id']
                        if columns and 'file_id' in columns else None,
                    hdu_number = columns['hdu_number']
                        if columns and 'hdu_number' in columns else None,
                                  )
                if extension:
                    extension.add()
                    extension.commit()
                    self.logger.info(
                        'Added Extension[id={0}], file_id: {1}, hdu_number: {2}'
                        .format(extension.id,
                                extension.file_id,
                                extension.hdu_number))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_extension_row. ' +
                                      'extension = \n{0}'.format(extension))
            else:
                self.ready = False
                self.logger.error('Unable to create_extension_row. ' +
                                  'columns: {0}'.format(columns))

    def set_data_columns(self,is_image=None):
        '''Set columns of the data table.'''
        self.data_columns = dict()
        if self.ready:
            extension_id = self.extension_id if self.extension_id else None
            if extension_id and is_image!=None:
                self.data_columns = {
                    'extension_id' : extension_id if extension_id   else None,
                    'is_image'     : is_image     if is_image!=None else None,
                    }
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_data_columns. ' +
                    'extension_id: {0}, '.format(extension_id) +
                    'is_image: {0}, '.format(is_image))

    def populate_data_table(self):
        '''Update/Create data table row.'''
        if self.ready:
            self.set_data()
            if self.data: self.update_data_row()
            else:         self.create_data_row()

    def set_data(self,extension_id=None,is_image=None):
        '''Load row from data table.'''
        if self.ready:
            extension_id = (extension_id if extension_id
                else self.data_columns['extension_id']
                if self.data_columns and 'extension_id' in self.data_columns
                else None)
            is_image = (is_image if is_image
                else self.data_columns['is_image']
                if self.data_columns and 'is_image' in self.data_columns
                else None)
            if extension_id and is_image!=None:
                self.data = (Data.load(extension_id=extension_id)
                             if extension_id else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_data. ' +
                                  'extension_id: {0}, '.format(extension_id) +
                                  'is_image: {0}'.format(is_image))

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
                        'Updated Data[id={0}], '.format(self.data.id) +
                        'extension_id: {0}, '.format(self.data.extension_id) +
                        'is_image: {0}.'.format(self.data.is_image))
            else:
                self.ready = False
                self.logger.error('Unable to update_data_row. columns: {0}'
                                    .format(columns))

    def create_data_row(self):
        '''Create row in data table.'''
        if self.ready:
            columns = self.data_columns if self.data_columns else None
            if columns:
                self.logger.debug('Adding new row to data table.')
                if self.verbose: self.logger.debug('columns:\n' +
                                                   dumps(columns,indent=1))
                data = Data(
                    extension_id = columns['extension_id']
                        if columns and 'extension_id' in columns else None,
                    is_image = columns['is_image']
                        if columns and 'is_image' in columns else None,
                                  )
                if data:
                    data.add()
                    data.commit()
                    self.logger.info(
                        'Added Data[id={0}], '.format(data.id) +
                        'extension_id: {0}, '.format(data.extension_id) +
                        'is_image: {0}.'.format(data.is_image))
                else:
                    self.ready = False
                    self.logger.error('Unable to create_data_row. ' +
                                      'data = \n{0}'.format(data))
            else:
                self.ready = False
                self.logger.error('Unable to create_data_row. ' +
                                  'columns: {0}'.format(columns))

