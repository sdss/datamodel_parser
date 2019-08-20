from bs4 import Tag, NavigableString
from datamodel_parser.application import Util
from datamodel_parser.application import Intro
from datamodel_parser.application.Type import Hdu_type
import string
from json import dumps


class Hdu:
    '''
        
    '''

    def __init__(self,logger=None,options=None,body=None):
        self.initialize(logger=logger,options=options)
        self.set_body(body=body)
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

    def set_body(self, body=None):
        '''Set the body class attribute.'''
        self.body = None
        if self.ready:
            self.body = body if body else None
            if not self.body:
                self.ready = False
                self.logger.error('Unable to set_body.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.ready   and
                          self.util    and
                          self.logger  and
                          self.body
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options  else None
            self.heading_tags        = self.util.heading_tag_names
            self.paragraph_tags      = self.util.paragraph_tags
            self.bold_tags           = self.util.bold_tags
            self.unordered_list_tags = self.util.unordered_list_tags
            self.file_hdu_info   = list()
            self.file_hdu_tables = list()
            self.hdu_type = None

    def parse_file(self,nodes=None):
        '''Parse file hdu content from given BeautifulSoup nodes.'''
        if self.ready:
            if nodes:
                type = Hdu_type(logger=self.logger,options=self.options)
                if type:
                    for node in nodes:
                        if self.ready:
                            self.hdu_type = type.get_hdu_type(node=node)
#                            print('node: %r'% node)
#                            print('self.hdu_type: %r'% self.hdu_type)
#                            input('pause')
                            if self.hdu_type:
                                if self.hdu_type == 1:
                                    self.parse_file_hdu_intro_1(node=node)
                                    self.parse_file_hdu_tables_1(node=node)
                                elif self.hdu_type == 2:
                                    self.parse_file_hdu_intro_2(node=node)
                                    self.parse_file_hdu_tables_1(node=node)
                                elif self.hdu_type == 3:
                                    self.parse_file_hdu_intro_3(node=node)
                                    self.parse_file_hdu_tables_2(node=node)
                                elif self.hdu_type == 4:
                                    self.parse_file_hdu_intro_3(node=node)
                                    self.parse_file_hdu_tables_3(node=node)
                                elif self.hdu_type == 5:
                                    self.parse_file_hdu_intro_3(node=node)
                                    self.parse_file_hdu_tables_4(node=node) # No table
                                elif self.hdu_type == 6:
                                    self.parse_file_hdu_intro_4(node=node)
                                    self.parse_file_hdu_tables_3(node=node)
                                elif self.hdu_type == 7:
                                    self.parse_file_hdu_intro_7(node=node)
                                    self.parse_file_hdu_tables_7(node=node)
                                elif self.hdu_type == 8:
                                    self.parse_file_hdu_intro_6(node=node)
                                    self.parse_file_hdu_tables_1(node=node)
                                elif self.hdu_type == 9:
                                    self.parse_file_hdu_intro_2(node=node)
                                    self.parse_file_hdu_tables_1(node=node)
                                elif self.hdu_type == 10:
                                    self.parse_file_hdu_intro_3(node=node)
                                    self.parse_file_hdu_tables_2(node=node)
                                elif self.hdu_type == 11:
                                    self.parse_file_hdu_intro_7(node=node)
                                    self.parse_file_hdu_tables_6(node=node)
                                elif self.hdu_type == 12:
                                    self.parse_file_hdu_intro_3(node=node)
                                    self.parse_file_hdu_tables_5(node=node)
                                else:
                                    self.ready = False
                                    self.logger.error('Unexpected self.hdu_type encountered ' +
                                                      'in Hdu.parse_file().')
                            else:
                                self.ready = False
                                self.logger.error('Unable to parse_file. ' +
                                                  'self.hdu_type: {}, '.format(self.hdu_type) )
                    self.set_hdu_count()
                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file. ' +
                                      'type: {}.'.format(type))
            else: # some files don't have hdus
                self.hdu_count = 0
                self.logger.warning('Unable to parse_file. ' +
                                  'nodes: {}.'.format(nodes))

    def set_hdu_count(self):
        '''Set the class attribute hdu_count.'''
        if self.ready:
            if self.file_hdu_info is not None and self.file_hdu_tables is not None:
                if len(self.file_hdu_info) == len(self.file_hdu_tables):
                    self.hdu_count = len(self.file_hdu_info)
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to parse_file. ' +
                        'len(self.file_hdu_info) != len(self.file_hdu_tables). ' +
                        'len(self.file_hdu_info): {}, '.format(len(self.file_hdu_info)) +
                        'len(self.file_hdu_tables): {}.'.format(len(self.file_hdu_tables)))
            else: self.hdu_count = 0

    def parse_file_hdu_intro_1(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # hdu_number and header_title (from only heading tag, if present)
                if self.util.get_heading_tag_child_names(node=node):
                    (hdu_number,hdu_title) = (
                        self.util.get_hdu_number_and_hdu_title_from_heading_tag(node=node))
                else:
                    (hdu_number,hdu_title) = (0,' ')
                if hdu_number is None:
                    self.logger.error('Unable to parse_file_hdu_intro_1. ' +
                                      'hdu_number cannot be None. ' +
                                      'hdu_number: {}, '.format(hdu_number))

                # hdu_description
                ps = node.find_all('p')
                hdu_descriptions = ([self.util.get_string(node=p) for p in ps
                                     if str(p) and not str(p).isspace()]
                                    if ps else list())
                hdu_description = ' '.join(hdu_descriptions)

                # datatype and hdu_size
                dl = node.find('dl')
                (datatype,hdu_size) = (self.util.get_datatype_and_hdu_size(node=dl)
                                       if dl else (None,None))
                                       
                # is_image
                is_image = (self.util.check_match(regex='(?i)IMAGE',string=datatype)
                            if datatype else None)
                
                # check if an error has occurred
                self.ready = self.util.ready
                
                # put it all together
                hdu_info = dict()
                if self.ready:
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = hdu_size
                    hdu_info['hdu_description'] = hdu_description
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_1. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_intro_2(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # hdu_number and header_title (from only heading tag, if present)
                if self.util.get_heading_tag_child_names(node=node):
                    (hdu_number,hdu_title) = (
                        self.util.get_hdu_number_and_hdu_title_from_heading_tag(node=node))
                else:
                    (hdu_number,hdu_title) = (0,' ')
                if hdu_number is None:
                    self.logger.error('Unable to parse_file_hdu_intro_2. ' +
                                      'hdu_number cannot be None. ' +
                                      'hdu_number: {}, '.format(hdu_number))

                # hdu.description
                ps = list()
                for p in node.find_all('p'): ps.append(p)
                ps.pop() # remove last p tag containing datatype and hdu_size
                hdu_description = ('\n\n'.join([self.util.get_string(node=p) for p in ps])
                                   if ps else None)
                
                # datatype and hdu_size
                for p in node.find_all('p'): pass # get last p tag
                (datatype,hdu_size) = self.util.get_datatype_and_hdu_size(node=p)

                # is_image
                is_image = (self.util.check_match(regex='(?i)IMAGE',string=datatype)
                            if datatype else None)

                # check if an error has occurred
                self.ready = self.util.ready

                # put it all together
                hdu_info = dict()
                if self.ready:
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = hdu_size
                    hdu_info['hdu_description'] = hdu_description
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_2. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_intro_3(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # hdu_number and header_title (from only heading tag, if present)
                if self.util.get_heading_tag_child_names(node=node):
                    (hdu_number,hdu_title) = (
                        self.util.get_hdu_number_and_hdu_title_from_heading_tag(node=node))
                else:
                    (hdu_number,hdu_title) = (0,' ')
                if hdu_number is None:
                    self.logger.error('Unable to parse_file_hdu_intro_3. ' +
                                      'hdu_number cannot be None. ' +
                                      'hdu_number: {}, '.format(hdu_number))
                
                # hdu_description
                ps = node.find_all('p')
                hdu_descriptions = ([self.util.get_string(p) for p in ps
                                     if str(p) and not str(p).isspace()]
                                    if ps else list())
                hdu_description = '\n'.join(hdu_descriptions) if hdu_descriptions else str()

                # datatype and hdu_size
                (datatype,hdu_size) = (None,None)

                # is_image
                is_image = None
                
                # check if an error has occurred
                self.ready = self.util.ready
                
                # put it all together
                hdu_info = dict()
                if self.ready:
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = hdu_size
                    hdu_info['hdu_description'] = hdu_description
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_3. ' +
                                  'node: {}, '.format(node) )

    def parse_file_hdu_intro_4(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # hdu_number and header_title (from only heading tag, if present)
                if self.util.get_heading_tag_child_names(node=node):
                    (hdu_number,hdu_title) = (
                        self.util.get_hdu_number_and_hdu_title_from_heading_tag(node=node))
                else:
                    (hdu_number,hdu_title) = (0,' ')
                if hdu_number is None:
                    self.logger.error('Unable to parse_file_hdu_intro_4. ' +
                                      'hdu_number cannot be None. ' +
                                      'hdu_number: {}, '.format(hdu_number))

                # hdu_description
                hdu_description = str()
                child_names = set(self.util.get_child_names(node=node))
                if 'p' in child_names:
                    ps = node.find_all('p')
                    hdu_description = '\n\n'.join([self.util.get_string(node=p) for p in ps])
                if 'ul' in child_names:
                    uls = node.find_all('ul')
                    hdu_description += '\n\n'.join([self.util.get_string(node=ul) for ul in uls])

                # datatype and hdu_size
                (datatype,hdu_size) = (None,None)

                # is_image
                is_image = None
                
                # check if an error has occurred
                self.ready = self.util.ready
                
                # put it all together
                hdu_info = dict()
                if self.ready:
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = hdu_size
                    hdu_info['hdu_description'] = hdu_description
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_4. ' +
                                  'node: {}, '.format(node) )

    def parse_file_hdu_intro_5(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # hdu_number and header_title (from first heading tag)
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title_from_p_tags_1(node=node))

                # hdu_description
                hdu_description = str()

                # datatype and hdu_size
                (datatype,hdu_size) = (None,None)

                # is_image
                is_image = None
                
                # check if an error has occurred
                self.ready = self.util.ready
                
                # put it all together
                hdu_info = dict()
                if self.ready:
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = hdu_size
                    hdu_info['hdu_description'] = hdu_description
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_5. ' +
                                  'node: {}, '.format(node) )

    def parse_file_hdu_intro_6(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # hdu_number and header_title (from only heading tag, if present)
                if self.util.get_heading_tag_child_names(node=node):
                    (hdu_number,hdu_title) = (
                        self.util.get_hdu_number_and_hdu_title_from_heading_tag(node=node))
                else:
                    (hdu_number,hdu_title) = (0,' ')
                if hdu_number is None:
                    self.logger.error('Unable to parse_file_hdu_intro_6. ' +
                                      'hdu_number cannot be None. ' +
                                      'hdu_number: {}, '.format(hdu_number))

                # hdu.description
                hdu_description = self.util.get_string_from_middle_children_1(node=node)

                # datatype and hdu_size
                for p in node.find_all('p'): pass # get last p tag
                (datatype,hdu_size) = self.util.get_datatype_and_hdu_size(node=p)

                # is_image
                is_image = (self.util.check_match(regex='(?i)IMAGE',string=datatype)
                            if datatype else None)
                
                # check if an error has occurred
                self.ready = self.ready and self.util.ready

                # put it all together
                hdu_info = dict()
                if self.ready:
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = hdu_size
                    hdu_info['hdu_description'] = hdu_description
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_6. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_intro_7(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # hdu_number and header_title (from only heading tag, if present)
                if self.util.get_heading_tag_child_names(node=node):
                    (hdu_number,hdu_title) = (
                        self.util.get_hdu_number_and_hdu_title_from_heading_tag(node=node))
                else:
                    (hdu_number,hdu_title) = (0,' ')
                if hdu_number is None:
                    self.logger.error('Unable to parse_file_hdu_intro_7. ' +
                                      'hdu_number cannot be None. ' +
                                      'hdu_number: {}, '.format(hdu_number))

                # hdu_description
                ps = node.find_all('p')
                regex = self.util.get_table_title_regex_1()
                hdu_descriptions = ([self.util.get_string(node=p) for p in ps
                                     if str(p) and not str(p).isspace()
                                     and not self.util.check_match(regex=regex,string=str(p))]
                                    if ps else list())
                hdu_description = '\n\n'.join(hdu_descriptions) if hdu_descriptions else str()
                # datatype and hdu_size
                (datatype,hdu_size) = (None,None)

                # is_image
                is_image = None
                
                # check if an error has occurred
                self.ready = self.util.ready
                
                # put it all together
                hdu_info = dict()
                if self.ready:
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = hdu_size
                    hdu_info['hdu_description'] = hdu_description
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_7. ' +
                                  'node: {}, '.format(node) )



    def parse_file_hdu_tables_1(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                tables = node.find_all('table')
                for (table_number,table) in enumerate(tables):
                    if self.ready:
                        # table caption
                        captions = self.util.get_children(node=table,names=['caption'])
                        table_caption = (self.util.get_string(node=captions[0])
                                         if captions and len(captions) == 1
                                         else None)

                        # column_names
                        column_names = list(table.find('thead').find('tr').strings)
                        
                        # is_header
                        is_header = self.get_is_header_1(table=table,
                                                         column_names=column_names,
                                                         table_number=table_number)
                        # table keyword/values
                        trs = table.find('tbody').find_all('tr')
                        table_rows = dict()
                        for (position,tr) in enumerate(trs):
                            table_row = list()
                            for td in tr.find_all('td'):
                                if self.util.ready:
                                    string = self.util.get_string(node=td)
                                    table_row.append(string)
                            table_rows[position]  = table_row
                    
                        # check if errors have occurred
                        self.ready = self.ready and self.util.ready

                        # put it all together
                        if self.ready:
                            hdu_table = dict()
                            hdu_table['is_header']          = is_header
                            hdu_table['table_caption']      = table_caption
                            hdu_table['table_column_names'] = column_names
                            hdu_table['table_rows']         = table_rows
                            hdu_tables.append(hdu_table)
                self.file_hdu_tables.append(hdu_tables)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_1. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_tables_2(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                tables = self.util.get_tables_1(node=node,table_tag='pre')
                if tables:
#                    print('tables: %r' % tables)
#                    input('pause')
                    for (table_number,table) in enumerate(tables):
                        if self.ready:
#                            print('\n\ntable: %r' % table)
#                            print('pre: %r' % table.find('pre'))
#                            input('pause')

                            # table caption
                            table_caption = None
                            
                            # is_header
                            is_header = self.get_is_header_2(table=table,
                                                             table_number=table_number)

                            # column_names
                            column_names = (['Key','Value','Type','Comment']
                                            if is_header == True else
                                            ['Name','Type','Unit','Description']
                                            if is_header == False
                                            else None
                                            )

                            # table_rows
                            table_rows = (self.get_table_rows_pre(table=table)
                                          if table and table.find('pre') else None)

                            # check if errors have occurred
                            self.ready = self.ready and self.util.ready

                            # put it all together
                            if self.ready:
                                hdu_table = dict()
                                hdu_table['is_header']          = is_header
                                hdu_table['table_caption']      = table_caption
                                hdu_table['table_column_names'] = column_names
                                hdu_table['table_rows']         = table_rows
                                hdu_tables.append(hdu_table)
                    self.file_hdu_tables.append(hdu_tables)
#                    print('\n\nhdu_tables: \n' + dumps(hdu_tables,indent=1))
#                    print('\n\nhdu_tables: %r' % hdu_tables)
#                    input('pause')
                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file_hdu_tables_2. ' +
                                      'tables: {}, '.format(tables)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_2. ' +
                                  'node: {}, '.format(node)
                                  )

    def parse_file_hdu_tables_3(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                tables = node.find_all('table')
                for (table_number,table) in enumerate(tables):
                    if self.ready:
                        # table_caption
                        captions = self.util.get_children(node=table,names=['caption'])
                        table_caption = (self.util.get_string(node=captions[0])
                                         if captions and len(captions) == 1
                                         else None)
                        
                        # table rows
                        trs = [tr for tr in table.find_all('tr')
                               if not self.util.get_string(node=tr).isspace()]
                        
                        # column_names
                        # get column names from trs with all th tag children
                        column_names = self.util.get_column_names(trs=trs)
                        # remove trs with all th tag children
                        trs = [tr for tr in trs
                               if not self.util.children_all_one_tag_type(node=tr,
                                                                          tag_name='th')]
                        # is_header
                        is_header = self.get_is_header_1(table=table,
                                                         column_names=column_names,
                                                         table_number=table_number)
                        # check if errors have occurred
                        self.ready = self.ready and self.util.ready
                        
                        # table keyword/values
                        table_rows = dict()
                        for (position,tr) in enumerate(trs):
                            if self.ready:
                                if column_names:
                                    table_row = self.get_table_row_tr_1(
                                                    column_names=column_names,
                                                    is_header=is_header,
                                                    node=tr)
                                else:
                                    column_names = (['key','value','type','comment']
                                                    if is_header else
                                                    ['name','type','unit','description'])
                                    table_row = list()
                                    for td in tr.find_all('td'):
                                        string = self.util.get_string(node=td)
                                        table_row.append(string)
                                table_rows[position]  = table_row

                        # put it all together
                        if self.ready:
                            hdu_table = dict()
                            hdu_table['is_header']          = is_header
                            hdu_table['table_caption']      = table_caption
                            hdu_table['table_column_names'] = column_names
                            hdu_table['table_rows']         = table_rows
                            hdu_tables.append(hdu_table)
                self.file_hdu_tables.append(hdu_tables)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_3. ' +
                                  'node: {}, '.format(node))

    def get_table_row_tr_1(self,
                           column_names=None,
                           is_header=None,
                           node=None):
        '''Get table row from the <td> children of the given BeautifulSoup node.'''
        table_row = [None,None,None,None]
        if self.ready:
            if column_names and is_header is not None and node:
                if is_header:
                    column_dict = {'key'         : 0,
                                   'name'        : 0,
                                   'value'       : 1,
                                   'example'     : 1,
                                   'type'        : 2,
                                   'comment'     : 3,
                                   'description' : 3,
                                   }
                else:
                    column_dict = {'name'         : 0,
                                   'channel'      : 0,
                                   'type'         : 1,
                                   'unit'         : 2,
                                   'units'        : 2,
                                   'comment'      : 3,
                                   'description'  : 3,
                                   'details of its content' : 3,
                                   }
                column_names = [n.strip().lower() for n in column_names]
                strings = list()
                # get strings from the <td> tags
                for td in node.find_all('td'):
                    strings.append(self.util.get_string(node=td))
                strings = [s.strip() for s in strings if not s.isspace()]
                
                # put the strings in the appropriate table rows
                for (column_name,string) in list(zip(column_names,strings)):
                    if self.ready:
                        if column_name in column_dict:
                            table_row[column_dict[column_name]] = string
                        else:
                            self.ready=False
                            self.logger.error('Unable to get_table_row_tr_1. '
                                              'Unanticipated column_name:{}'
                                                .format(column_name))
                # Warn when there is less columns than column_names
                if len(column_names) != len(strings):
                    self.logger.warning('Unable to get_table_row_tr_1. ' +
                                      'len(column_names) != len(strings). ' +
                                      'Truncating to the smaller length. ' +
                                      'len(column_names): {}, '.format(len(column_names)) +
                                      'len(strings): {}, '.format(len(strings)) +
                                      '\ncolumn_names: {}, '.format(column_names) +
                                      '\nstrings: {}.'.format(strings)
                                      )
                # Warn when len(column_names) > 4
                if len(column_names) > 4:
                    self.logger.warning('Table does not adhere to database schema. ' +
                                      'len(column_names) > 4. ' +
                                      '\ncolumn_names: {}, '.format(column_names)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_table_row_tr_1. ' +
                                  'table_column_names: {}, '.format(table_column_names) +
                                  'node: {}.'.format(node) )
        if table_row == [None,None,None,None]:
            self.ready = False
            self.logger.error('Unable to get_table_row_tr_1. ' +
                              'column_names: {}, '.format(column_names) +
                              'is_header: {}, '.format(is_header) +
                              'node: {}, '.format(node)
                              )
        return table_row

    def parse_file_hdu_tables_4(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                # No header or data table for this one
                hdu_table = dict()
                hdu_tables.append(hdu_table)
                self.file_hdu_tables.append(hdu_tables)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_4. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_tables_5(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                tables = self.util.get_tables_1(node=node,table_tag='ul')
                if tables:
#                    print('tables: %r' % tables)
#                    input('pause')
                    for (table_number,table) in enumerate(tables):
                        if self.ready:
#                            print('\n\ntable: %r' % table)
#                            print('pre: %r' % table.find('pre'))
#                            input('pause')

                            # table caption
                            table_caption = None
                            
                            # is_header
                            is_header = self.get_is_header_2(table=table,
                                                             table_number=table_number)

                            # column_names
                            column_names = (['Key','Value','Type','Comment']
                                            if is_header == True else
                                            ['Name','Type','Unit','Description']
                                            if is_header == False
                                            else None
                                            )

                            # table_rows
                            table_rows = (self.get_table_rows_ul(table=table)
                                          if table and table.find('ul') else None)

                            # check if errors have occurred
                            self.ready = self.ready and self.util.ready

                            # put it all together
                            if self.ready:
                                hdu_table = dict()
                                hdu_table['is_header']          = is_header
                                hdu_table['table_caption']      = table_caption
                                hdu_table['table_column_names'] = column_names
                                hdu_table['table_rows']         = table_rows
                                hdu_tables.append(hdu_table)
                    self.file_hdu_tables.append(hdu_tables)
#                    print('\n\nhdu_tables: \n' + dumps(hdu_tables,indent=1))
#                    print('\n\nhdu_tables: %r' % hdu_tables)
#                    input('pause')
                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file_hdu_tables_5. ' +
                                      'tables: {}, '.format(tables)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_5. ' +
                                  'node: {}, '.format(node)
                                  )

    def parse_file_hdu_tables_6(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                regex = self.util.get_table_title_regex_1()
                tables = self.util.get_tables_3(node=node,regex=regex)
                if tables:
                    for (table_number,table) in enumerate(tables):
                        if self.ready:
                            # table caption
                            ps = self.util.get_children(node=table,names=['p'])
                            p = ps[0] if ps else None
                            ps = ps[1:] if ps and len(ps) > 1 else None
                            (title,description) = (
                                self.util.get_title_and_description_from_p(p=p)
                                    if p else (None,None))
                            p_strings = ([self.util.get_string(node=p) for p in ps if p]
                                         if ps else list())
                            table_caption = (title.strip() + '. '
                                             if title.strip() else str())
                            table_caption += (description.strip() + '. '
                                              if description.strip() else str())
                            table_caption += ('\n'.join(p_strings)
                                              if p_strings else str())
                                              
                            # is_header
                            is_header = (True if title and
                                            self.util.check_match(
                                                regex = self.util.get_table_title_regex_2(),
                                                string=title)
                                        else False if title and
                                            self.util.check_match(
                                                regex = self.util.get_table_title_regex_3(),
                                                string=title)
                                        else None
                                        )

                            # column_names
                            column_names = (['Key','Value','Type','Comment']
                                            if is_header == True else
                                            ['Name','Type','Unit','Description']
                                            if is_header == False
                                            else None
                                            )
                            # table_rows
                            table_rows = (self.get_table_rows_pre(table=table)
                                          if table and table.find('pre') else dict())

                            # check if errors have occurred
                            self.ready = self.ready and self.util.ready

                            # put it all together
                            if self.ready:
                                hdu_table = dict()
                                previous_hdu_table = dict()
                                # concatenate split tables
                                if hdu_tables and hdu_tables[-1]['is_header'] == is_header:
                                    previous_hdu_table = hdu_tables.pop()
                                    previous_table_caption = previous_hdu_table['table_caption']
                                    previous_table_rows = previous_hdu_table['table_rows']
                                    hdu_table['is_header']          = is_header
                                    hdu_table['table_caption']      = (previous_table_caption +
                                                                       table_caption)
                                    hdu_table['table_column_names'] = column_names
                                    k = 0
                                    hdu_table['table_rows'] = dict()
                                    
                                    for key, value in previous_table_rows.items():
                                        hdu_table['table_rows'][k] = value
                                        k += 1
                                    for key, value in table_rows.items():
                                        hdu_table['table_rows'][k] = value
                                        k += 1
                                else:
                                    hdu_table['is_header']          = is_header
                                    hdu_table['table_caption']      = table_caption
                                    hdu_table['table_column_names'] = column_names
                                    hdu_table['table_rows']         = table_rows
                                hdu_tables.append(hdu_table)
                    self.file_hdu_tables.append(hdu_tables)
                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file_hdu_tables_6. ' +
                                      'tables: {}, '.format(tables)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_6. ' +
                                  'node: {}, '.format(node)
                                  )

    def parse_file_hdu_tables_7(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                regex = self.util.get_table_title_regex_1()
                tables = self.util.get_tables_3(node=node,regex=regex)
                if tables:
                    for (table_number,table) in enumerate(tables):
                        if self.ready:
                            # table caption
                            ps = self.util.get_children(node=table,names=['p'])
                            p = ps[0] if ps else None
                            ps = ps[1:] if ps and len(ps) > 1 else None
                            (title,description) = (
                                self.util.get_title_and_description_from_p(p=p)
                                    if p else (None,None))
                            p_strings = ([self.util.get_string(node=p) for p in ps if p]
                                         if ps else list())
                            p_strings = ([p for p in p_strings if not str(p).startswith('<b>')]
                                         if p_strings else list())
                            table_caption = (title.strip() + '. '
                                             if title.strip() else str())
                            table_caption += (description.strip() + '. '
                                              if description.strip() else str())
                            table_caption += ('\n'.join(p_strings)
                                              if p_strings else str())
                                              
                            # is_header
                            is_header = (True if title and
                                            self.util.check_match(
                                                regex = self.util.get_table_title_regex_2(),
                                                string=title)
                                        else False if title and
                                            self.util.check_match(
                                                regex = self.util.get_table_title_regex_3(),
                                                string=title)
                                        else None
                                        )

                            # column_names
                            column_names = (['Key','Value','Type','Comment']
                                            if is_header == True else
                                            ['Name','Type','Unit','Description']
                                            if is_header == False
                                            else None
                                            )
                            # table_rows
                            table_rows = (self.get_table_rows_ul(table=table)
                                          if table and table.find('ul') else dict())

                            # check if errors have occurred
                            self.ready = self.ready and self.util.ready

                            # put it all together
                            if self.ready:
                                hdu_table = dict()
                                previous_hdu_table = dict()
                                # concatenate split tables
                                if hdu_tables and hdu_tables[-1]['is_header'] == is_header:
                                    previous_hdu_table = hdu_tables.pop()
                                    previous_table_caption = previous_hdu_table['table_caption']
                                    previous_table_rows = previous_hdu_table['table_rows']
                                    hdu_table['is_header']          = is_header
                                    hdu_table['table_caption']      = (previous_table_caption +
                                                                       table_caption)
                                    hdu_table['table_column_names'] = column_names
                                    k = 0
                                    hdu_table['table_rows'] = dict()
                                    
                                    for key, value in previous_table_rows.items():
                                        hdu_table['table_rows'][k] = value
                                        k += 1
                                    for key, value in table_rows.items():
                                        hdu_table['table_rows'][k] = value
                                        k += 1
                                else:
                                    hdu_table['is_header']          = is_header
                                    hdu_table['table_caption']      = table_caption
                                    hdu_table['table_column_names'] = column_names
                                    hdu_table['table_rows']         = table_rows
                                hdu_tables.append(hdu_table)
                    self.file_hdu_tables.append(hdu_tables)
                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file_hdu_tables_7. ' +
                                      'tables: {}, '.format(tables)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_7. ' +
                                  'node: {}, '.format(node)
                                  )

    def get_is_header_1(self,table=None,column_names=None,table_number=None):
        '''Get is_header from either table.attrs, column_names, or table_number.'''
        is_header = None
        if self.ready:
            if table and table_number is not None:
                table_class = (table.attrs['class']
                               if table.attrs and 'class' in table.attrs else None)
                table_class = (table_class[0]
                              if isinstance(table_class,list) and len(table_class) == 1 else None)
                if table_class:
                    header_regex = '(?i)head'
                    bin_table_regex = '(?i)column' + '|' + '(?i)bintable'
                    is_header = (
                        True
                        if self.util.check_match(regex=header_regex,string=table_class)
                        else False
                        if self.util.check_match(regex=bin_table_regex,string=table_class)
                        else None)
                    if is_header is None:
                        self.ready = False
                        self.logger.error('Unable to get_is_header_1. ' +
                                          'is_header: {}, '.format(is_header) +
                                          'table.attrs: {}.'.format(table.attrs))
                elif column_names:
                    column_names = [c.lower() for c in column_names]
                    is_header = (False
                                if ('unit' in column_names or
                                    'units' in column_names)
                                else True)
                else:
                    is_header = True if table_number == 0 else False
            else:
                self.ready = False
                self.logger.error('Unable to get_is_header_1. ' +
                                  'table: {}, '.format(table) +
                                  'table_number: {}, '.format(table_number)
                                  )
        if is_header is None:
            self.ready = False
            self.logger.error('Unable to get_is_header_1. ' +
                              'is_header: {}, '.format(is_header)
                              )
        return is_header

    def get_is_header_2(self,table=None,table_number=None):
        '''Get is_header from either heading.attrs, column_names, or heading_title.'''
        is_header = None
        if self.ready:
            if table and table_number is not None:
                heading_tag_names = (self.util.get_heading_tag_child_names(node=table)
                                    if table else None)
                heading_tag_name = heading_tag_names[0] if heading_tag_names else None
                heading_tag = (table.find(heading_tag_name)
                               if heading_tag_name else None)
                heading_id = (heading_tag.attrs['id'] if heading_tag and
                              heading_tag.attrs and 'id' in heading_tag.attrs else None)
                heading_string = (self.util.get_string(node=heading_tag)
                                  if heading_tag else None)
                regex = ('(?i)header' + '|' +
                         '(?i)binary' + '|' + '(?i)field' + '|' + '(?i)column')
                is_table_heading = (self.util.check_match(regex=regex,string=heading_string)
                                    if heading_string else None)
                
#                print('heading_tag_names: %r'% heading_tag_names)
#                print('heading_tag_name: %r'% heading_tag_name)
#                print('heading_tag: %r'% heading_tag)
#                print('heading_id: %r'% heading_id)
#                print('heading_string: %r'% heading_string)
#                print('is_table_heading: %r'% is_table_heading)
#                input('pause')
                if heading_id:
                    header_regex = '(?i)head'
                    bin_table_regex = '(?i)field'
                    is_header = (
                        True
                        if self.util.check_match(regex=header_regex,string=heading_id)
                        else False
                        if self.util.check_match(regex=bin_table_regex,string=heading_id)
                        else None)
                    if is_header is None:
                        self.ready = False
                        self.logger.error('Unable to get_is_header_2. ' +
                                          'is_header: {}, '.format(is_header) +
                                          'heading.attrs: {}.'.format(heading.attrs))
                elif heading_tag and is_table_heading:
                    header_regex = '(?i)header'
                    bin_table_regex = '(?i)binary' + '|' + '(?i)field' + '|' + '(?i)column'
                    is_header = (
                        True
                        if self.util.check_match(regex=header_regex,string=heading_string)
                        else False
                        if self.util.check_match(regex=bin_table_regex,string=heading_string)
                        else None)
                else:
                    is_header = True if table_number == 0 else False
                if is_header is None: is_header = True if table_number == 0 else False
            else:
                self.ready = False
                self.logger.error('Unable to get_is_header_2. ' +
                                  'bool(table): {}, '.format(bool(table)) +
                                  'table_number: {}, '.format(table_number)
                                  )
            if is_header is None:
                self.ready = False
                self.logger.error('Unable to get_is_header_2. ' +
                                  'is_header: {}, '.format(is_header)
                                  )
        return is_header

    def set_hdu_tags(self):
        '''Set hdus from given body tag.'''
        self.hdu_tags = None
        if self.ready:
            if self.body and self.body.children:
                previous_child = None
                found_hdu_tags = False
                for child in self.util.get_children(node=self.body):
                    if child.name in self.heading_tags:
                        string = self.util.get_string(node=child)
                        if string and 'HDU' in string:
                            found_hdu_tags = True
                            self.hdu_tags = (previous_child.next_siblings
                                             if previous_child else None)
                            break
                    if not found_hdu_tags:
                        previous_child = child if child else None
            else:
                self.ready = False
                self.logger.error('Unable to set_hdu_tags. ' +
                                  'self.body: {}'.format(self.body) +
                                  'self.body.children: {}'
                                    .format(self.body.children))

    def set_hdu_headings_and_pres(self):
        '''Set hdu_headings and hdu_pres from the hdu_tags'''
        if self.ready:
            if self.hdu_tags:
                first_hdu = True
                self.hdu_headings = list()
                self.hdu_pres = list()
                pres = list()
                for tag in [tag for tag in self.hdu_tags if tag.name]:
                    string = self.util.get_string(node=tag)
                    if tag.name in self.heading_tags and 'HDU' in string:
                        self.hdu_headings.append(tag)
                        if first_hdu:
                            first_hdu = False
                        else:
                            self.hdu_pres.append(pres)
                            pres = list()
                    elif tag.name == 'pre':
                        pres.append(tag)
                    else: # Do nothing; only processing heading and pre tags
                        pass
                self.hdu_pres.append(pres)
            else:
                self.ready = False
                self.logger.error('Unable to set_hdu_headings_and_pres. ' +
                                  'self.hdu_tags: {}'
                                  .format(self.hdu_tags))

    def set_row_data(self,row=None):
        '''Set the header keyword-value pairs for the given row.'''
        self.row_data = list()
        if self.ready:
            if row:
                keyword = None
                value = None
                type = None
                comment = None
                value_comment = None
                if 'HISTORY' in row:
                    keyword = 'HISTORY'
                    value_comment = row.replace('HISTORY',str())
                elif '=' in row:
                    split = row.split('=')
                    keyword       = split[0].strip() if split else None
                    value_comment = split[1].strip() if split else None
                elif 'END' in row:
                    keyword = 'END'
                    value_comment = row.replace('END',str())
                else:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_row_data. ' +
                            "The strings 'HISTORY', 'END' and '=' " +
                            'not found in row. ' +
                            'row: {}'.format(row))
                if value_comment and '/' in value_comment:
                    split = value_comment.split('/')
                    value   = split[0].strip() if split else None
                    comment = split[1].strip() if split else None
                else:
                    value = value_comment.strip()
                    comment = None
                self.row_data = [keyword,value,type,comment]
            else:
                self.ready = False
                self.logger.error('Unable to set_row_data. ' +
                                  'row: {}'.format(row))

    def set_heading_tag_names(self,child_names=None):
        '''Set a list of child for the given BeautifulSoup child_names.'''
        self.heading_tag_names = list()
        if self.ready:
            if child_names:
                for name in child_names:
                    if name and name in self.heading_tags:
                        self.heading_tag_names.append(str(name))
            else:
                self.ready = False
                self.logger.error('Unable to set_heading_tag_names. ' +
                                  'child_names: {}'.format(child_names))

    def get_table_rows_pre(self,table=None):
        '''Get table rows from the <table> tag.'''
        table_rows = dict()
        if self.ready:
            pre = table.find('pre') if table else None
            if pre:
                pre_string = self.util.get_string(node=pre) if pre else None
                rows = pre_string.split('\n') if pre_string else None
                rows = [r for r in rows if r] if rows else None
                if rows:
                    for (position,row) in enumerate(rows):
                        if self.ready:
                            if row: # skip empty rows
                                table_row = self.get_table_row_1(row=row)
                                if table_row:
                                    table_rows[position] = table_row
                                else:
                                    print('row: %r'% row)
#                                    input('pause')
                                    self.ready = False
                                    self.logger.error('Unable to get_table_rows_pre. ' +
                                                      'row: {}, '.format(row) +
                                                      'table_row: {}, '.format(table_row)
                                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_table_rows_pre. ' +
                                  'table: {}'.format(table))
            if not table_rows:
                self.ready = False
                self.logger.error('Unable to get_table_rows_pre. ' +
                                  'table: {}'.format(table))
        return table_rows

    def get_table_rows_ul(self,table=None):
        '''Get table rows from the <table> tag.'''
        table_rows = dict()
        if self.ready:
            ul = table.find('ul') if table else None
            if ul:
                rows = [self.util.get_string(node=li) for li in table.find_all('li')]
                if rows:
                    for (position,row) in enumerate(rows):
                        if self.ready:
                            table_row = self.get_table_row_1(row=row)
                            if table_row:
                                table_rows[position] = table_row
                            else:
                                self.ready = False
                                self.logger.error('Unable to get_table_rows_ul. ' +
                                                  'row: {}, '.format(row) +
                                                  'table_row: {}, '.format(table_row)
                                                  )
            else:
                self.ready = False
                self.logger.error('Unable to get_table_rows_ul. ' +
                                  'table: {}'.format(table))
            if not table_rows:
                self.ready = False
                self.logger.error('Unable to get_table_rows_ul. ' +
                                  'table: {}'.format(table))
        return table_rows


    def get_table_row_1(self,row=None):
        '''Set the header keyword-value pairs for the given row.'''
        table_row = list()
        if self.ready:
            if row:
                regex0 = '^\s{5,}'  # starts with 5 or more spaces
                # starts with '*', '#', '}', or a digit
                regex1 = ('^\s*\*' + '|' + '^\s*\#' + '|' + '^\s*\}' + '|' +
                          '^\s*\{' + '|' + '^\s*\d+' + '|' + '^\s*\&+' + '|' +
                          '^\s*\/+' + '|' + '^\s*\<br' + '|' + '^\s*\.+' + '|' +
                          '^\s*\-\d+')
                regex2 = '^([A-Z\d*]{1,}\_){0,20}([A-Z\d*]{1,})\s*\=\s*'
                regex3 = '^([A-Z\d*]{1,}\-){0,20}([A-Z\d*]{1,})\s*\=\s*'
                regex4 = '^([A-Z\d*]{1,}\_){0,20}([A-Z\d*]{1,})\s*'
                regex5 = '^\s*<b>(.*?)</b>' # starts with bold tag
                regex6 = '^([A-Za-z\d*]{1,}\_){0,20}([A-Za-z\d*]{1,})\s*'
                regex7 = '^\s*\w' # starts with word character MUST BE LAST regex !!!!
                match0 = self.util.check_match(regex=regex0,string=row)
                match1 = self.util.check_match(regex=regex1,string=row.lstrip())
                match2 = self.util.check_match(regex=regex2,string=row.lstrip())
                match3 = self.util.check_match(regex=regex3,string=row.lstrip())
                match4 = self.util.check_match(regex=regex4,string=row.lstrip())
                match5 = self.util.check_match(regex=regex5,string=row.lstrip())
                match6 = self.util.check_match(regex=regex6,string=row.lstrip())
                match7 = self.util.check_match(regex=regex7,string=row.lstrip())
#                print('row: %r' %row)
#                print('match0: %r' % match0)
#                print('match1: %r' % match1)
#                print('match2: %r' % match2)
#                print('match3: %r' % match3)
#                print('match4: %r' % match4)
#                print('match5: %r' % match5)
#                print('match6: %r' % match6)
#                print('match7: %r' % match7)
#                input('pause')

                # header_table_columns = ['Key','Value','Type','Comment']
                # binary_table_columns = ['Name','Type','Unit','Description']
                if match0 or match1:
                    table_row = [None,None,None,row.strip()]
                elif match2 or match3:
                    row = row.strip()
                    matches2 = self.util.get_matches(regex=regex2,string=row)
                    match2 = matches2[0] if matches2 else None
                    matches3 = self.util.get_matches(regex=regex3,string=row)
                    match3 = matches3[0] if matches3 else None
                    match = match2 if match2 else match3
                    col0 = match if row.startswith(match) else None
                    if col0:
                        col13 = row.split(col0)[1].strip() # = ['',row.replace(col0,'')]
                        col0 = col0.replace('=',str()).strip()
                        if   ' / '  in col13: split_char = ' / '
                        elif ' /'   in col13: split_char = ' /'
                        elif '/ '   in col13: split_char = '/ '
                        elif '/'    in col13: split_char = '/'
                        else:                 split_char = None
                        split = col13.split(split_char) if col13 and split_char else None
                        col1  = split[0].strip() if split else col13
                        col3  = split[1].strip() if split else None
                        col1 = col1 if not col1 in set(string.punctuation) else None
                        table_row = [col0,col1,None,col3]
                elif match4:
                    row = row.strip()
                    matches = self.util.get_matches(regex=regex4,string=row)
                    match = matches[0] if matches else None
                    col0 = match if row.startswith(match) else None
                    if col0:
                        col13 = row.split(col0)[1].strip() # = ['',row.replace(col0,'')]
                        if col13 and col13.startswith('(') and ':' in col13:
                            key = ':'
                            split = [s.strip() for s in col13.split(key) if s]
                            split[0] = split[0].replace('(',str()).replace(')',str()).strip()
                        else:
                            key = ' '*3
                            split = [s.strip() for s in col13.split(key) if s]
                        l_split = len(split) if col13 else 0
                        if   l_split == 0: table_row = [col0,None,None,None]
                        elif l_split == 1: table_row = [col0,None,None,split[0]]
                        elif l_split == 2: table_row = [col0,split[0],None,split[1]]
                        elif l_split == 3: table_row = [col0,split[0],split[1],split[2]]
                        else:
                            self.ready = False
                            self.logger.error('Unable to get_table_row_1. ' +
                                              'l_split: {}'.format(l_split))
                    else:
                        self.ready = False
                        self.logger.error('Unable to get_table_row_1. ' +
                                          'col0: {}'.format(col0))
                elif match5:
                    row = row.strip()
                    matches = self.util.get_matches(regex=regex5,string=row)
                    match = matches[0] if matches else None
                    col0 = match if row.startswith(match) else None
                    if col0:
                        col23 = row.split(col0)[1].strip() # = [str(),row.replace(col0,str())]
                        col0 = col0.replace('<b>',str()).replace('</b>',str()).strip()
                        matches = self.util.get_matches(regex='\((.*?)\)',string=col23)
                        col2 = matches[0] if matches else None
                        col3 = col23.split(col2)[1].strip() if col2 else col23
                        col2 = col2.replace('(',str()).replace(')',str()).strip() if col2 else None
                        col3 = col3[1:].strip() if col3 and col3.startswith(':') else col3
                        col3 = None if col3 and col3.strip() == '.' else col3
                        table_row = [col0,col2,None,col3]

#                        print('/\n\nrow: %r' % row)
#                        print('col0: %r' % col0)
#                        print('col23: %r' % col23)
#                        print('matches: %r' % matches)
#                        print('col2: %r' % col2)
#                        print('col3: %r' % col3)
#                        print('table_row: %r' % table_row)
#                        input('pause')
                elif match6:
                    row = row.strip()
                    matches = self.util.get_matches(regex=regex6,string=row)
                    match = matches[0] if matches else None
                    col0 = match if row.startswith(match) else None
                    if col0:
                        col13 = row.split(col0)[1].strip() # = ['',row.replace(col0,'')]
                        col0 = col0.replace('=',str()).strip()
                        if   ' # '  in col13: split_char = ' # '
                        elif ' #'   in col13: split_char = ' #'
                        elif '# '   in col13: split_char = '# '
                        elif '#'    in col13: split_char = '#'
                        else:                 split_char = None
                        split = col13.split(split_char) if col13 and split_char else None
                        col1  = split[0].strip() if split else col13
                        col3  = split[1].strip() if split else None
                        table_row = [col0,col1,None,col3]
                elif match7:
                    row = row.strip()
                    table_row = [None,None,None,row]
                else:
                    self.ready = False
                    self.logger.error('Unable to get_table_row_1. ' +
                                      'no regex match. ' +
                                      'row: {}'.format(row))
            else:
                self.logger.debug('Unable to get_table_row_1. ' +
                                    'row: {}'.format(row)
                                  )
#        print('row: %r' % row)
#        print('table_row: %r' % table_row)
#        input('pause')

        return table_row

    def get_table_row_2(self,row=None):
        '''Set the header keyword-value pairs for the given row.'''
        table_row = list()
        if self.ready:
            if row:
                regex1 = '^\s*<b>(.*?)</b>'
                match1 = self.util.check_match(regex=regex1,string=row)
#                print('match1: %r' % match1)
#                input('pause')
                # header_table_columns = ['Key','Value','Type','Comment']
                # binary_table_columns = ['Name','Type','Unit','Description']
                if match0 or match1:
                    table_row = [None,None,None,row.strip()]
                elif match2:
                    row = row.strip()
                    matches = self.util.get_matches(regex=regex2,string=row)
                    match = matches[0] if matches else None
                    col0 = match if row.startswith(match) else None
                    if col0:
                        col13 = row.split(col0)[1].strip() # = ['',row.replace(col0,'')]

            else:
                self.logger.debug('Unable to get_table_row_2. ' +
                                    'row: {}'.format(row)
                                  )
#        print('row: %r' % row)
#        print('table_row: %r' % table_row)
#        input('pause')

        return table_row


