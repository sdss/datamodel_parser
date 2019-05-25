from bs4 import Tag, NavigableString
from datamodel_parser.application import Util
from datamodel_parser.application import Intro
from datamodel_parser.application.Type import Hdu_type

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
        self.logger  = self.util.logger  if self.util.logger  else None
        self.options = self.util.options if self.util.options else None
        self.ready   = self.util and self.util.ready if self.util else None

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
                          self.options and
                          self.body)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
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
                                    self.parse_file_hdu_intro_4(node=node)
                                    self.parse_file_hdu_tables_3(node=node)
                                elif self.hdu_type == 5:
                                    self.parse_file_hdu_intro_5(node=node)
                                    self.parse_file_hdu_tables_4(node=node) # No table
                                elif self.hdu_type == 6:
                                    self.parse_file_hdu_intro_6(node=node)
                                    self.parse_file_hdu_tables_3(node=node)
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


#    def parse_file(self):
#        '''Parse the HTML of the given BeautifulSoup object.'''
#        self.hdu_count = None
#        if self.ready:
#            # process different hdu types
#            if self.body:
#                # self.body all div tags
#                if self.util.children_all_one_tag_type(node = self.body,
#                                                       tag_name = 'div'):
#                    print('***** All divs *****')
#                    hdu_divs = self.util.get_hdu_divs(node=self.body)
##                    print('divs: %r' %  divs)
##                    input('pause')
#                    if hdu_divs:
#                        for (self.hdu_number,hdu_div) in enumerate(hdu_divs):
#                            if self.ready: self.parse_file_hdu_div(node=hdu_div)
#                    else: pass # some files don't have div hdus
#                else:
#                    self.parse_file_hdus()
#                self.set_hdu_count()
#            else:
#                self.ready = False
#                self.logger.error('Unable to parse_file. ' +
#                                  'self.body: {}.'.format(self.body))
#
#    def parse_file_hdu_div(self,node=None):
#        '''Parse file hdu content from given BeautifulSoup division node.'''
#        if self.ready:
#            if node:
#                type = Hdu_type(logger=self.logger,options=self.options)
#                self.hdu_type = type.get_hdu_type(node=node)
#
##                print('self.hdu_type: %r' % self.hdu_type)
##                input('pause')
#
#                if self.hdu_type:
#                    if self.hdu_type == 1:
#                        self.parse_file_hdu_intro_1(node=node)
#                        self.parse_file_hdu_tables_1(node=node)
#                    elif self.hdu_type == 2:
#                        self.parse_file_hdu_intro_2(node=node)
#                        self.parse_file_hdu_tables_1(node=node)
#                    elif self.hdu_type == 3:
#                        self.parse_file_hdu_intro_3(node=node)
#                        self.parse_file_hdu_tables_2(node=node)
#                    elif self.hdu_type == 4:
#                        self.parse_file_hdu_intro_4(node=node)
#                        self.parse_file_hdu_tables_3(node=node)
#                    elif self.hdu_type == 5:
#                        self.parse_file_hdu_intro_5(node=node)
#                        self.parse_file_hdu_tables_4(node=node) # No table
#                    elif self.hdu_type == 6:
#                        self.parse_file_hdu_intro_6(node=node)
#                        self.parse_file_hdu_tables_3(node=node)
#                    else:
#                        self.ready = False
#                        self.logger.error('Unexpected self.hdu_type encountered ' +
#                                          'in Hdu.parse_file_hdu_div().')
#                else:
#                    self.ready = False
#                    self.logger.error('Unable to parse_file_hdu_div. ' +
#                                      'self.hdu_type: {}, '.format(self.hdu_type) )
#            else:
#                self.ready = False
#                self.logger.error('Unable to parse_file_hdu_div. ' +
#                                  'node: {}.'.format(node))
#
#    def parse_file_hdus(self):
#        '''Parse file hdu content from given BeautifulSoup node.'''
#        if self.ready:
#            node = self.body
#            if node:
#                child_names = set(self.util.get_child_names(node=node)) # REMOVE
#                type = Hdu_type(logger=self.logger,options=self.options)
#                self.hdu_type = type.get_hdu_type(node=node)
#
##                print('self.hdu_type: %r' % self.hdu_type)
##                input('pause')
#
#                if self.hdu_type == 7:
#                    self.parse_file_hdu_intro_type_5(node=node)
#                    self.parse_file_hdu_tables_type_5(node=node)
#
#
#                if child_names == {'h1','p','h3','ul','pre'}:
#                    self.parse_file_h1_p_h3_ul_pre()
#                else:
#                    self.ready = False
#                    self.logger.error('Unexpected HTML body type encountered ' +
#                                      'in Hdu.parse_file.')
#            else:
#                self.ready = False
#                self.logger.error('Unable to parse_file_hdus. ' +
#                                  'node: {}.'.format(node))

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
                # hdu_number and header_title (from first heading tag)
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # hdu_description
                ps = node.find_all('p')
                hdu_descriptions = ([self.util.get_string(p) for p in ps
                                     if str(p) and not str(p).isspace()]
                                    if ps else list())
                hdu_description = ' '.join(hdu_descriptions)

                # datatype and hdu_size
                dl = node.find('dl')
                (datatype,hdu_size) = (self.util.get_datatype_and_hdu_size(node=dl)
                                       if dl else (None,None))
                                       
                # is_image
                is_image = True if datatype.lower() == 'image' else False
                
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
                # hdu_number and header_title (from first heading tag)
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # hdu.description
                ps = list()
                for p in node.find_all('p'): ps.append(p)
                ps.pop() # remove last p tag containing datatype and hdu_size
                hdu_description = ('\n'.join([self.util.get_string(node=p) for p in ps])
                                   if ps else None)
                
                # datatype and hdu_size
                for p in node.find_all('p'): pass # get last p tag
                (datatype,hdu_size) = self.util.get_datatype_and_hdu_size(node=p)

                # is_image
                is_image = True if datatype.lower() == 'image' else False
                
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
                # hdu_number and header_title (from first heading tag)
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))
                    
                # hdu_description
                ps = node.find_all('p')
                hdu_descriptions = ([self.util.get_string(p) for p in ps
                                     if str(p) and not str(p).isspace()]
                                    if ps else list())
                hdu_description = ' '.join(hdu_descriptions)

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
                # hdu_number and header_title (from first heading tag)
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # hdu_description
                hdu_description = None
                child_names = set(self.util.get_child_names(node=node))
                if 'p' in child_names:
                    ps = node.find_all('p')
                    hdu_description = '\n'.join([self.util.get_string(node=p) for p in ps])

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
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # hdu_description
                ps = node.find_all('p')
                hdu_description = ('\n'.join([self.util.get_string(node=p) for p in ps])
                                    if ps else None)
                                    
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
                # hdu_number and header_title (from first heading tag)
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # hdu_description
                hdu_description = str()
                child_names = set(self.util.get_child_names(node=node))
                if 'p' in child_names:
                    ps = node.find_all('p')
                    hdu_description = '\n'.join([self.util.get_string(node=p) for p in ps])
                if 'ul' in child_names:
                    uls = node.find_all('ul')
                    hdu_description += '\n'.join([self.util.get_string(node=ul) for ul in uls])

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
                self.logger.error('Unable to parse_file_hdu_intro_6. ' +
                                  'node: {}, '.format(node) )


    def parse_file_hdu_tables_1(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                tables = node.find_all('table')
                for table in tables:
                    # table caption
                    captions = self.util.get_children(node=table,name='caption')
                    table_caption = (self.util.get_string(node=captions[0])
                                     if captions and len(captions) == 1
                                     else None)

                    # column_names
                    column_names = list(table.find('thead').find('tr').strings)
                    # is_header
                    s = set([x.lower() for x in column_names])
                    is_header = (s == {'key','value','type','comment'})
                    
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
                    for (table_number,table) in enumerate(tables):
                        if self.ready:
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
                                          if table else None)

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
                        captions = self.util.get_children(node=table,name='caption')
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
                              'table_row: {}, '.format(table_row)
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
                    header_regex = '(?i)header'
                    bin_table_regex = '(?i)column'
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
                elif heading_tag:
                    string = self.util.get_string(node=heading_tag)
                    header_regex = '(?i)header'
                    bin_table_regex = '(?i)binary' + '|' + '(?i)field' + '|' + '(?i)column'
                    is_header = (
                        True
                        if self.util.check_match(regex=header_regex,string=string)
                        else False
                        if self.util.check_match(regex=bin_table_regex,string=string)
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

    def parse_file_h1_p_h3_ul_pre(self):
        '''Parse the HTML of the given BeautifulSoup div tag object with
            children: h1, h4 and p.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h1_p_h3_ul_pre()
            if self.body and assumptions:
                self.set_hdu_tags()
                self.set_hdu_headings_and_pres()
                if (self.ready and
                    self.hdu_headings and self.hdu_pres and
                    len(self.hdu_headings) == len(self.hdu_pres)):
                    intro_position = -1
                    for (heading_tag,pre_tags) in list(zip(self.hdu_headings,
                                                          self.hdu_pres)):
                        hdu_title = (self.util.get_string(node=heading_tag)
                                            .replace(':',str()))
                        table_info = list()
                        for pre_tag in pre_tags:
                            string = self.util.get_string(node=pre_tag)
                            table_info.append(string)
                        table_info = '\n' + '\n'.join(table_info)
                        # put it all together
                        self.parse_file_hdu_info_h1_p_h3_ul_pre(
                                                        hdu_title  = hdu_title,
                                                        table_info = table_info)
                        self.parse_file_hdu_tables_h1_p_h3_ul_pre(table_info=table_info)
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to parse_file_h1_p_h3_ul_pre. ' +
                        'Possible unequal list lenghts. ' +
                        'self.hdu_headings: {}'
                            .format(self.hdu_headings) +
                        'self.hdu_pres: {}'
                            .format(self.hdu_pres) +
                        'len(self.hdu_headings): {}'
                            .format(len(self.hdu_headings)) +
                        'len(self.hdu_pres): {}'
                            .format(len(self.hdu_pres)))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_h1_p_h3_ul_pre. ' +
                                  'self.body: {}'.format(self.body) +
                                  'assumptions: {}'.format(assumptions))

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

    def parse_file_hdu_info_h1_p_h3_ul_pre(self,hdu_title=None,table_info=None):
        '''Parse file description content from given hdu_titleision tag.'''
        if self.ready:
            if hdu_title and table_info:
                if self.ready:
                    # hdu.hdu_number and table_info.title
                    hdu_number = (
                        [int(s) for s in list(hdu_title) if s.isdigit()][0])
                    # data.is_image
                    rows = table_info.split('\n') if table_info else list()
                    rows = [row for row in rows
                            if row and 'XTENSION' in row and 'IMAGE' in row]
                    is_image = bool(rows)
                    is_image = None if not is_image and hdu_number == 0 else is_image
                    hdu_info = dict()
                    hdu_info['is_image']        = is_image
                    hdu_info['hdu_number']      = hdu_number
                    hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                    hdu_info['hdu_size']        = None
                    hdu_info['hdu_description'] = None
                    hdu_info['hdu_type']        = self.hdu_type if self.hdu_type else None
                    self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_info_h1_p_h3_ul_pre. ' +
                                  'hdu_title: {}'.format(hdu_title) +
                                  'table_info: {}'.format(table_info))

    def parse_file_hdu_tables_h1_p_h3_ul_pre(self,table_info=None):
        '''Parse file description content from given table_infoision tag.'''
        hdu_table = dict()
        hdu_tables = list()
        if self.ready:
            if table_info:
                # table caption
                table_caption = None
                # table column table_infos
                column_names = ['key','value','type','comment']
                # table values
                table_rows = dict()
                rows = table_info.split('\n') if table_info else list()
                rows = [row for row in rows if row]
                if rows:
                    for (position,row) in enumerate(rows):
                        self.set_row_data(row=row)
                        table_rows[position] = (self.row_data
                                                 if self.row_data else None)
                    
                    hdu_table['is_header']          = True #DEBUG
                    hdu_table['table_caption']      = table_caption
                    hdu_table['table_column_names'] = column_names
                    hdu_table['table_rows']         = table_rows
                    hdu_tables.append(hdu_table)
                    self.file_hdu_tables.append(hdu_tables)
                else:
                    self.ready = False
                    self.logger.error(
                                'Unable to parse_file_hdu_tables_h1_p_h3_ul_pre. ' +
                                'rows: {}'.format(rows))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_h1_p_h3_ul_pre. ' +
                                  'header: {}'.format(header))

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


    def verify_assumptions_parse_file_h1_p_h3_ul_pre(self):
        '''Verify assumptions made in parse_file_h1_h4_p_div.'''
        assumptions = None
        if self.body:
            intro = (Intro(logger=self.logger,options=self.options,body=self.body)
                     if self.logger and self.options and self.body else None)
            assumptions = (
                intro.verify_assumptions_parse_file_h1_p_h3_ul_pre(body=self.body)
                if intro and self.body else None)
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_file_h1_p_h3_ul_pre. ' +
                'self.body: {}.'.format(self.body))
        if not assumptions: self.ready = False
        return assumptions

    def get_table_rows_pre(self,table=None):
        '''Get table rows from the <table> tag.'''
        table_rows = dict()
        if self.ready:
            pre = table.find('pre') if table else None
            if pre:
                rows = self.util.get_string(node=pre).split('\n')
                if rows:
                    for (position,row) in enumerate(rows):
                        if self.ready:
                            table_row = self.get_table_row_1(row=row)
                            if table_row:
                                table_rows[position] = table_row
                            else:
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

    def get_table_row_1(self,row=None):
        '''Set the header keyword-value pairs for the given row.'''
        table_row = list()
        if self.ready:
            if row:
                regex0 = '^\s{5,}'
                regex1 = '^\*'
                regex2 = ('^[A-Z]+\d*\_[A-Z]+\d*\_[A-Z]+\d*\_[A-Z]+\d*\s*\=\s*' + '|'
                          '^[A-Z]+\d*\_[A-Z]+\d*\_[A-Z]+\d*\s*\=\s*'            + '|'
                          '^[A-Z]+\d*\_[A-Z]+\d*\s*\=\s*'                       + '|'
                          '^[A-Z]+\d*\s*\=\s*'
                          )
                regex3 = ('^[A-Z]+\d*\-[A-Z]+\d*\-[A-Z]+\d*\-[A-Z]+\d*\s*\=\s*' + '|'
                          '^[A-Z]+\d*\-[A-Z]+\d*\-[A-Z]+\d*\s*\=\s*'            + '|'
                          '^[A-Z]+\d*\-[A-Z]+\d*\s*\=\s*'                       + '|'
                          '^[A-Z]+\d*\s*\=\s*'
                          )
                regex4 = ('^[A-Z]+\d*\_[A-Z]+\d*\_[A-Z]+\d*\_[A-Z]+\d*' + '|'
                          '^[A-Z]+\d*\_[A-Z]+\d*\_[A-Z]+\d*'            + '|'
                          '^[A-Z]+\d*\_[A-Z]+\d*'                       + '|'
                          '^[A-Z]+\d*'
                          )
                match0 = self.util.check_match(regex=regex0,string=row)
                match1 = self.util.check_match(regex=regex1,string=row.lstrip())
                match2 = self.util.check_match(regex=regex2,string=row.lstrip())
                match3 = self.util.check_match(regex=regex3,string=row.lstrip())
                match4 = self.util.check_match(regex=regex4,string=row.lstrip())
#                print('match0: %r' % match0)
#                print('match1: %r' % match1)
#                print('match2: %r' % match2)
#                print('match3: %r' % match3)
#                print('match4: %r' % match4)
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
                        col0 = col0.replace('=',str()).strip()
                        if   ' / '  in col13: split_char = ' / '
                        elif ' /'   in col13: split_char = ' /'
                        elif '/ '   in col13: split_char = '/ '
                        elif '/'    in col13: split_char = '/'
                        else:                 split_char = None
                        split = col13.split(split_char) if col13 and split_char else None
                        col1  = split[0].strip() if split else None
                        col3  = split[1].strip() if split else None
                        table_row = [col0,col1,None,col3]
                elif match3:
                    row = row.strip()
                    matches = self.util.get_matches(regex=regex3,string=row)
                    match = matches[0] if matches else None
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
                        col1  = split[0].strip() if split else None
                        col3  = split[1].strip() if split else None
                        table_row = [col0,col1,None,col3]
                elif match4:
                    row = row.strip()
                    matches = self.util.get_matches(regex=regex4,string=row)
                    match = matches[0] if matches else None
                    col0 = match if row.startswith(match) else None
                    if col0:
                        col13 = row.split(col0)[1].strip() # = ['',row.replace(col0,'')]
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
                else:
                    self.ready = False
                    self.logger.error('Unable to get_table_row_1. ' +
                                      'no regex match.')


            else:
                self.logger.debug('Unable to get_table_row_1. ' +
                                    'row: {}'.format(row)
                                  )
#        print('row: %r' % row)
#        print('table_row: %r' % table_row)
#        input('pause')

        return table_row



