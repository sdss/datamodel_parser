from datamodel_parser.application import Util
from datamodel_parser.application import Intro
from datamodel_parser.application import Hdu
from datamodel_parser.application import Database
from bs4 import BeautifulSoup
from flask import render_template
from datamodel_parser import app
from os import environ
from os.path import join
from json import dumps


class File:

    def __init__(self,logger=None,options=None,file_path_info=None,html_text=None):
        self.initialize(logger=logger,options=options)
        self.set_file_path_info(file_path_info=file_path_info)
        self.set_html_text(html_text=html_text)
        self.set_body()
        self.set_database()
        self.set_ready()
        self.set_attributes()
        self.set_intro_and_hdu()

    def initialize(self,logger=None,options=None,tree_edition=None):
        self.util = Util(logger=logger,options=options)
        self.logger  = self.util.logger  if self.util.logger  else None
        self.options = self.util.options if self.util.options else None
        self.ready   = self.util.ready   if self.util.ready   else None

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
                    self.file_name and
                    self.location_path):
                self.ready = False
                self.logger.error(
                            'Unable to set_html_text. '
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
                self.ready = None
                self.logger.error('Unable to set_body. ' +
                                  'self.html_text: {}'.format(self.html_text))

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
                          self.html_text    and
                          self.tree_edition and
                          self.env_variable and
                          self.file_name    and
                          self.body         and
                          self.database
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None

    def populate_file_html_tables(self):
        '''Populate tables comprised of file HTML text information.'''
        if self.ready:
            self.parse_file()
            if self.ready:
                self.logger.info('Populating HTML Text Tables')
                self.populate_intro_table()
                self.populate_section_table()
                self.populate_hdu_table()
                self.populate_header_and_data_tables()
                self.populate_keyword_and_column_tables()

    def parse_file(self):
        '''Parse the given file using the determined File instance.'''
        if self.ready:
            self.set_intro_and_hdu()
            if self.ready:
                self.logger.info('Parsing file HTML')
                self.intro.parse_file()
                self.hdu.parse_file()
                self.ready = self.ready and self.intro.ready and self.hdu.ready
                if self.ready:
                    self.intro_positions      = self.intro.intro_positions
                    self.intro_heading_levels = self.intro.intro_heading_levels
                    self.intro_heading_titles = self.intro.intro_heading_titles
                    self.intro_descriptions   = self.intro.intro_descriptions
                    self.section_hdu_titles   = self.intro.section_hdu_titles
                    self.hdu_count            = self.hdu.hdu_count
                    self.file_hdu_info        = self.hdu.file_hdu_info
                    self.file_hdu_tables      = self.hdu.file_hdu_tables

#                    print('HI File.parse_file()')
#                    print('self.intro_positions: {}'.format(self.intro_positions))
#                    print('self.intro_heading_levels: %r' % self.intro_heading_levels)
#                    print('self.intro_heading_titles: {}'.format(self.intro_heading_titles))
#                    print('self.intro_descriptions: {}'.format(self.intro_descriptions))
#                    print('self.section_hdu_titles: {}'.format(self.section_hdu_titles))
#                    print('self.hdu_count: {}'.format(self.hdu_count))
#                    print('self.file_hdu_info: \n' + dumps(self.file_hdu_info,indent=1))
#                    print('self.file_hdu_tables: {}'.format(self.file_hdu_tables))
#                    input('pause')

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

    def populate_section_table(self):
        '''Populate the section table.'''
        if self.ready:
            if (self.tree_edition                 and
                self.env_variable                 and
#               self.location_path # can be None
                self.file_name                    and
                self.section_hdu_titles is not None
                ):
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                section_hdu_titles = self.section_hdu_titles
                if section_hdu_titles:
                    for (hdu_number,hdu_title) in section_hdu_titles.items():
                        if self.ready:
                            self.database.set_section_columns(
                                                hdu_number = int(hdu_number),
                                                hdu_title   = hdu_title)
                            self.database.populate_section_table()
                            self.ready = self.database.ready
                else: # the file does not have a section list
                    self.database.set_section_columns(hdu_number = None,
                                                      hdu_title   = None)
                    self.database.populate_section_table()
                    self.ready = self.database.ready

            else:
                self.ready = False
                self.logger.error(
                    'Unable to populate_section_table. '                   +
                    'self.tree_edition: {}, ' .format(self.tree_edition)  +
                    'self.env_variable: {}, ' .format(self.env_variable)  +
                    'self.file_name: {}, '    .format(self.file_name)     +
                    'self.section_hdu_titles: {}.'
                    .format(self.section_hdu_titles))

    def populate_hdu_table(self):
        '''Populate the hdu table.'''
        if self.ready:
            if (self.tree_edition               and
                self.env_variable               and
#               self.location_path # can be None
                self.file_name                  and
                self.file_hdu_info
                ):
                self.database.set_file_id(tree_edition  = self.tree_edition,
                                          env_variable  = self.env_variable,
                                          location_path = self.location_path,
                                          file_name     = self.file_name)
                for hdu_info in self.file_hdu_info:
                    if self.ready:
                        is_image     = hdu_info['is_image']
                        hdu_number   = hdu_info['hdu_number']
                        hdu_title    = hdu_info['hdu_title']
                        size         = hdu_info['hdu_size']
                        description  = hdu_info['hdu_description']
                        self.database.set_hdu_columns(
                                                    is_image     = is_image,
                                                    number       = hdu_number,
                                                    title        = hdu_title,
                                                    size         = size,
                                                    description  = description,
                                                      )
                        self.database.populate_hdu_table()
                        self.ready = self.database.ready
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
#               self.location_path # can be None
                self.file_name              and
                self.file_hdu_info     and
                self.file_hdu_tables
                ):
                hdu_info = self.file_hdu_info
                hdu_tables = self.file_hdu_tables
                if len(hdu_info) == len(hdu_tables):
                    for (hdu_info,hdu_tables) in list(zip(self.file_hdu_info,self.file_hdu_tables)):
                        if self.ready:
                            for hdu_table in hdu_tables:
                                hdu_number = hdu_info['hdu_number']
                                hdu_title  = hdu_info['hdu_title']
                                table_caption = hdu_table['table_caption']
                                self.database.set_hdu_id(
                                                tree_edition  = self.tree_edition,
                                                env_variable  = self.env_variable,
                                                location_path = self.location_path,
                                                file_name     = self.file_name,
                                                hdu_number    = hdu_number)
                                if hdu_table['is_header']:
                                    self.database.set_header_columns(
                                                        hdu_number    = hdu_number,
                                                        table_caption = table_caption)
                                    self.database.populate_header_table()
                                else:
                                    self.database.set_data_columns(
                                                        hdu_number    = hdu_number,
                                                        table_caption = table_caption)
                                    self.database.populate_data_table()

                                self.ready = self.database.ready
                else:
                    self.ready = None
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
                    'self.file_name: {}, '    .format(self.file_name)     +
                    'self.file_hdu_info: {}'
                    .format(self.file_hdu_info)                 +
                    'self.file_hdu_tables: {}'
                    .format(self.file_hdu_tables)
                    )

    def populate_keyword_and_column_tables(self):
        '''Populate the keyword table.'''
        if self.ready:
            if (self.tree_edition           and
                self.env_variable           and
#               self.location_path # can be None
                self.file_name              and
                self.file_hdu_info     and
                self.file_hdu_tables
                ):
                hdu_info = self.file_hdu_info
                hdu_tables = self.file_hdu_tables

                if len(hdu_info) == len(hdu_tables):
                    for (hdu_info,hdu_tables) in list(zip(hdu_info,hdu_tables)):
                        if self.ready:
                            hdu_number = hdu_info['hdu_number']
                            for hdu_table in hdu_tables:
                                is_header          = hdu_table['is_header']
                                table_rows         = hdu_table['table_rows']

                                # Populate keyword table
                                if is_header:
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
                                else:
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
                else:
                    self.ready = None
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
                    'self.file_name: {}, '    .format(self.file_name)     +
                    'self.file_hdu_info: {}'
                    .format(self.file_hdu_info)                 +
                    'self.file_hdu_tables: {}'
                    .format(self.file_hdu_tables)
                    )
