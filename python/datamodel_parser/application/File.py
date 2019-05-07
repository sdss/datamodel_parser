from datamodel_parser.application import Util
from datamodel_parser.application import Intro
from datamodel_parser.application import Hdu
from datamodel_parser.application import Database
from datamodel_parser.application import Stub
from datamodel_parser.application.Type import File_type
from bs4 import BeautifulSoup
from flask import render_template
from datamodel_parser import app
from os import environ
from os.path import join
from json import dumps


class File:

    def __init__(self,logger=None,options=None):
        self.initialize(logger=logger,options=options)
        self.set_database()
        self.set_ready()
        self.set_attributes()

    def initialize(self,logger=None,options=None,tree_edition=None):
        self.util = Util(logger=logger,options=options)
        self.logger  = self.util.logger  if self.util.logger  else None
        self.options = self.util.options if self.util.options else None
        self.ready   = self.util.ready   if self.util.ready   else None
    
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
        self.ready = bool(self.ready        and
                          self.util         and
                          self.logger       and
                          self.options      and
                          self.database
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.intro_type = None
            self.hdu_type = None
            

    def set_file_path_info(self,file_path_info=None):
        '''Set the html file file_path_info.'''
        self.tree_edition  = None
        self.env_variable  = None
        self.file_name     = None
        self.location_path = None
        if self.ready:
            file_path_info = file_path_info if file_path_info else None
            self.tree_edition  = (file_path_info['tree_edition']
                                  if file_path_info and
                                  'tree_edition' in file_path_info
                                  else None)
            self.env_variable  = (file_path_info['env_variable']
                                  if file_path_info and
                                  'env_variable' in file_path_info
                                  else None)
            self.file_name     = (file_path_info['file_name']
                                  if file_path_info and
                                  'file_name' in file_path_info
                                  else None)
            self.location_path = (file_path_info['location_path']
                                  if file_path_info and
                                  'location_path' in file_path_info
                                  else None)
            if not (self.tree_edition and
                    self.env_variable and
                    self.file_name):
                    # self.location_path can be None
                self.ready = False
                self.logger.error(
                            'Unable to set_file_path_info. '
                            'self.tree_edition: {}, '.format(self.tree_edition) +
                            'self.env_variable: {}, '.format(self.env_variable) +
                            'self.file_name: {}.'.format(self.file_name) +
                            'self.location_path: {}.'.format(self.location_path)
                                  )

    def set_html_text(self,html_text=None):
        '''Set the html file html_text.'''
        self.html_text = None
        if self.ready:
            self.html_text = html_text if html_text else None
            if not self.html_text:
                self.ready = False
                self.logger.error('Unable to set_html_text.')

    def set_body(self):
        '''Set a class BeautifulSoup instance
           from the HTML text of the given URL.
        '''
        self.body = None
        if self.ready:
            soup = (BeautifulSoup(self.html_text, 'html.parser')
                    if self.html_text else None)
            self.body = soup.body if soup else None
            if not self.body:
                self.ready = False
                self.logger.error('Unable to set_body. ' +
                                  'self.html_text: {}'.format(self.html_text))

    def populate_file_hdu_info_tables(self):
        '''Populate tables comprised of file HTML text information.'''
        if self.ready:
            self.populate_intro_table()
            self.populate_hdu_table()
            self.populate_header_and_data_tables()
            self.populate_keyword_and_column_tables()

    def parse_file(self):
        '''Parse the given file using the determined File instance.'''
        if self.ready:
            self.set_intro_and_hdu()
            if self.ready:
                self.logger.info('Parsing file HTML')
                node = self.body
                type = File_type(logger=self.logger,options=self.options)
                self.file_type = type.get_file_type(node=node)
                (intro,hdus) = self.util.get_intro_and_hdus(node=node,
                                                            file_type=self.file_type)
                self.intro.parse_file(node=intro)
                self.ready = self.ready and type.ready and self.intro.ready
                if self.ready:
                    self.hdu.parse_file(nodes=hdus)
                    self.ready = self.ready and self.hdu.ready
                    self.intro_type = self.intro.intro_type
                    self.hdu_type   = self.hdu.hdu_type
                    if self.ready:
                        self.intro_positions      = self.intro.intro_positions
                        self.intro_heading_levels = self.intro.intro_heading_levels
                        self.intro_heading_titles = self.intro.intro_heading_titles
                        self.intro_descriptions   = self.intro.intro_descriptions
                        self.hdu_count            = self.hdu.hdu_count
                        self.file_hdu_info        = self.hdu.file_hdu_info
                        self.file_hdu_tables      = self.hdu.file_hdu_tables

#                        print('HI File.parse_file()')
#                        print('self.intro_positions: {}'.format(self.intro_positions))
#                        print('self.intro_heading_levels: %r' % self.intro_heading_levels)
#                        print('self.intro_heading_titles: {}'.format(self.intro_heading_titles))
#                        print('self.intro_descriptions: {}'.format(self.intro_descriptions))
#                        print('self.hdu_count: {}'.format(self.hdu_count))
#                        print('self.file_hdu_info: \n' + dumps(self.file_hdu_info,indent=1))
#                        print('self.file_hdu_tables: {}'.format(self.file_hdu_tables))
#                        input('pause')

    def set_intro_and_hdu(self):
        '''Set file intro tags and hdu tags.'''
        self.intro = None
        self.hdu = None
        if self.ready:
            self.intro = Intro(logger  = self.logger,
                               options = self.options,
                               body    = self.body)
            self.hdu = Hdu(logger  = self.logger,
                           options = self.options,
                           body    = self.body)
            if not (self.intro and self.body):
                self.ready = False
                self.logger.error('Unable to set_intro_and_hdu. ' +
                                  'self.intro: {}, '.format(self.intro) +
                                  'self.hdu: {}, '.format(self.hdu))

    def parse_fits(self,fits_dict=None):
        '''From the given dictionary, creat data structures needed for the method
            populate_file_hdu_info_tables().
        '''
        if self.ready:
            if fits_dict:
                stub = Stub()
                self.hdu_count = len(fits_dict['hdus'])
                # intro database table
                self.intro_heading_titles = ['Data Model: ' + fits_dict['name'],
                                             'General Description',
                                             'Naming Convention',
                                             'Approximate Size',
                                             'File Type',
                                             'Generated by Product',
                                             ]
                self.intro_descriptions = [str(),
                                           str(),
                                           str(),
                                           fits_dict['filesize'],
                                           fits_dict['filetype'],
                                           str(),
                                           ]
                number_headings = len(self.intro_heading_titles)
                self.intro_positions = list(range(number_headings))
                self.intro_heading_levels = [1]
                self.intro_heading_levels.extend([4] * (number_headings - 1))
#                filename = fits_dict['filename']

                # file hdu's
                self.file_hdu_info = list()
                self.file_hdu_tables = list()
                for (hdu_number,hdu) in enumerate(fits_dict['hdus']):

                    # hdu database table
                    hdu_info = dict()
                    hdu_info['is_image']        = hdu.is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu.name if hdu.name else ' '
                    hdu_info['hdu_size']        = stub.formatBytes(hdu.size)
                    hdu_info['hdu_description'] = str()
                    self.file_hdu_info.append(hdu_info)
                    
                    # header and binary-data HDU tables
                    hdu_tables = list()
                    
                    # header and keyword database tables
                    hdu_table  = dict()
                    table_rows = dict()
                    table_row  = list()
                    position = 0
                    type = str() # not implemented
                    hdr = hdu.header
                    for (key,value) in hdr.items():
                        if stub.isKeyAColumn(key):
                            table_row = [key,value,type,hdr.comments[key]]
                            table_rows[position]  = table_row
                            position += 1
                    # put it all together
                    hdu_table['is_header']          = True
                    hdu_table['table_caption']      = ('Header Table Caption for HDU'
                                                        + str(hdu_number))
                    hdu_table['table_column_names'] = ['Key','Value','Type','Comment']
                    hdu_table['table_rows']         = table_rows
                    hdu_tables.append(hdu_table)

                    # data and column database tables
                    unit = str() # not implemented
                    description = str()
                    if not hdu.is_image:
                        hdu_table  = dict()
                        table_rows = dict()
                        table_row  = list()
                        hdr = hdu.header
                        position = 0
                        for row in hdu.columns:
                            if stub.isKeyAColumn(key):
                                table_row = [row.name.upper(),
                                             stub.getType(row.format),
                                             unit,
                                             description
                                             ]
                                table_rows[position]  = table_row
                                position += 1
                        # put it all together
                        hdu_table['is_header'] = False
                        hdu_table['table_caption'] = (
                            'Binary Table Caption for HDU' + str(hdu_number))
                        hdu_table['table_column_names'] = (
                                        ['Name','Type','Unit','Description'])
                        hdu_table['table_rows'] = table_rows
                        hdu_tables.append(hdu_table)
                    self.file_hdu_tables.append(hdu_tables)

    def populate_intro_table(self):
        '''Populate the intro table.'''
        if self.ready:
            if (self.tree_edition              and
                self.env_variable              and
#               self.location_path # can be None
                self.file_name                 and
                self.intro_positions and
                self.intro_heading_levels and
                self.intro_heading_titles and
                self.intro_descriptions
                ):
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                positions = self.intro_positions
                heading_levels = self.intro_heading_levels
                heading_titles = self.intro_heading_titles
                descriptions   = self.intro_descriptions

                for (position,
                     heading_level,
                     heading_title,
                     description) in list(zip(
                     positions,
                     heading_levels,
                     heading_titles,
                     descriptions)):
                    if self.ready:
                        self.database.set_intro_columns(
                                                position = position,
                                                heading_level = heading_level,
                                                heading_title = heading_title,
                                                description   = description)
                        self.database.populate_intro_table()
                        self.ready = self.database.ready
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_intro_table. '                     +
                    'self.tree_edition: {}, ' .format(self.tree_edition)  +
                    'self.env_variable: {}, ' .format(self.env_variable)  +
                    'self.file_name: {}, '    .format(self.file_name)     +
                    'self.intro_positions: {}, '
                    .format(self.intro_positions)                +
                    'self.intro_heading_levels: {}, '
                    .format(self.intro_heading_levels)                +
                    'self.intro_heading_titles: {}, '
                    .format(self.intro_heading_titles)                +
                    'self.intro_descriptions: {}.'
                    .format(self.intro_descriptions)
                    )

    def populate_hdu_table(self):
        '''Populate the hdu table.'''
        if self.ready:
            if (self.tree_edition               and
                self.env_variable               and
#               self.location_path # can be None
                self.file_name
#                self.file_hdu_info # can be None
                ):
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                if self.file_hdu_info is not None:
                    for hdu_info in self.file_hdu_info:
                        if self.ready:
                            is_image     = (hdu_info['is_image']
                                            if hdu_info and 'is_image' in hdu_info
                                            else None)
                            hdu_number   = (hdu_info['hdu_number']
                                            if hdu_info and 'hdu_number' in hdu_info
                                            else None)
                            hdu_title    = (hdu_info['hdu_title']
                                            if hdu_info and 'hdu_title' in hdu_info
                                            else None)
                            size         = (hdu_info['hdu_size']
                                            if hdu_info and 'hdu_size' in hdu_info
                                            else None)
                            description  = (hdu_info['hdu_description']
                                            if hdu_info and 'hdu_description' in hdu_info
                                            else None)
                            hdu_type     = (hdu_info['hdu_type']
                                            if hdu_info and 'hdu_type' in hdu_info
                                            else None)
                            self.database.set_hdu_columns(
                                                        is_image     = is_image,
                                                        number       = hdu_number,
                                                        title        = hdu_title,
                                                        size         = size,
                                                        description  = description,
                                                        hdu_type     = hdu_type,
                                                          )
                            self.database.populate_hdu_table()
                            self.ready = self.database.ready
                else: pass # Don't add a row to hdu table

            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_hdu_table. '                 +
                    'self.tree_edition: {}, ' .format(self.tree_edition)  +
                    'self.env_variable: {}, ' .format(self.env_variable)  +
                    'self.file_name: {}, '    .format(self.file_name)     +
                    'self.file_hdu_info: {}'
                    .format(self.file_hdu_info)
                    )

    def populate_header_and_data_tables(self):
        '''Populate the header table.'''
        if self.ready:
            if (self.tree_edition           and
                self.env_variable           and
#               self.location_path          # can be None
                self.file_name
#                self.file_hdu_info         # can be None
#                self.file_hdu_tables       # can be None
                ):
                hdu_info = self.file_hdu_info
                hdu_tables = self.file_hdu_tables
                if hdu_info is not None:
                    if len(hdu_info) == len(hdu_tables):
                        for (hdu_info,hdu_tables) in list(zip(self.file_hdu_info,self.file_hdu_tables)):
                            if self.ready:
                                for hdu_table in hdu_tables:
                                    hdu_number = (hdu_info['hdu_number']
                                                  if hdu_info and 'hdu_number' in hdu_info
                                                  else None)
                                    hdu_title  = (hdu_info['hdu_title']
                                                  if hdu_info and 'hdu_title' in hdu_info
                                                  else None)
                                    table_caption = (hdu_table['table_caption']
                                                     if hdu_table and 'table_caption' in hdu_table
                                                     else None)
                                    is_header = (hdu_table['is_header']
                                                 if hdu_table and 'is_header' in hdu_table
                                                 else None)
                                    self.database.set_hdu_id(
                                                    tree_edition  = self.tree_edition,
                                                    env_variable  = self.env_variable,
                                                    location_path = self.location_path,
                                                    file_name     = self.file_name,
                                                    hdu_number    = hdu_number)
                                    if is_header == True:
                                        self.database.set_header_columns(
                                                            hdu_number    = hdu_number,
                                                            table_caption = table_caption)
                                        self.database.populate_header_table()
                                    elif is_header == False:
                                        self.database.set_data_columns(
                                                            hdu_number    = hdu_number,
                                                            table_caption = table_caption)
                                        self.database.populate_data_table()
                                    else: pass # can have empty table
                                    self.ready = self.database.ready
                    else:
                        self.ready = False
                        self.logger.error(
                                'Unable to populate_header_and_data_tables. ' +
                                'Data and header lists have unequal length. ' +
                                'len(hdu_info): {}, '.format(len(hdu_info)) +
                                'len(hdu_tables): {}, '.format(len(hdu_tables)))
                
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_header_and_data_tables. '                 +
                    'self.tree_edition: {}, ' .format(self.tree_edition)  +
                    'self.env_variable: {}, ' .format(self.env_variable)  +
                    'self.file_name: {}, '    .format(self.file_name)
                    )

    def populate_keyword_and_column_tables(self):
        '''Populate the keyword table.'''
        if self.ready:
            if (self.tree_edition           and
                self.env_variable           and
#               self.location_path          # can be None
                self.file_name
#                self.file_hdu_info         # can be None
#                self.file_hdu_tables       # can be None
                ):
                hdu_info = self.file_hdu_info
                hdu_tables = self.file_hdu_tables
                if hdu_info is not None:
                    if len(hdu_info) == len(hdu_tables):
                        for (hdu_info,hdu_tables) in list(zip(hdu_info,hdu_tables)):
                            if self.ready:
                                hdu_number = hdu_info['hdu_number']
                                for hdu_table in hdu_tables:
                                    is_header = (hdu_table['is_header']
                                                 if hdu_table and 'is_header' in hdu_table
                                                 else None)
                                    table_rows = (hdu_table['table_rows']
                                                 if hdu_table and 'table_rows' in hdu_table
                                                 else None)
                                    # Populate keyword table
                                    if is_header == True:
                                        self.database.set_header_id(
                                                tree_edition  = self.tree_edition,
                                                env_variable  = self.env_variable,
                                                location_path = self.location_path,
                                                file_name     = self.file_name,
                                                hdu_number    = hdu_number)
                                        for position in table_rows.keys():
                                            if self.ready:
                                                self.database.set_keyword_columns(
                                                    position  = position,
                                                    table_row = table_rows[position])
                                                self.database.populate_keyword_table()
                                                self.ready = self.database.ready
                                
                                    # Populate column table
                                    elif is_header == False:
                                        self.database.set_data_id(
                                                tree_edition  = self.tree_edition,
                                                env_variable  = self.env_variable,
                                                location_path = self.location_path,
                                                file_name     = self.file_name,
                                                hdu_number    = hdu_number)
                                        for position in table_rows.keys():
                                            if self.ready:
                                                self.database.set_column_columns(
                                                    position  = position,
                                                    table_row = table_rows[position])
                                                self.database.populate_column_table()
                                                self.ready = self.database.ready
                                    else: pass # can have empty table
                    else:
                        self.ready = False
                        self.logger.error(
                            'Unable to populate_keyword_and_column_tables. ' +
                            'hdu_info and hdu_tables lists have unequal length. ' +
                            'len(hdu_info): {}, '.format(len(hdu_info)) +
                            'len(hdu_tables): {}, '.format(len(hdu_tables)))
                
            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_keyword_and_column_tables. '                 +
                    'self.tree_edition: {}, ' .format(self.tree_edition)  +
                    'self.env_variable: {}, ' .format(self.env_variable)  +
                    'self.file_name: {}, '    .format(self.file_name)
                    )
