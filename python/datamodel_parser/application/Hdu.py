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
            self.heading_tags        = self.util.heading_tags
            self.paragraph_tags      = self.util.paragraph_tags
            self.bold_tags           = self.util.bold_tags
            self.unordered_list_tags = self.util.unordered_list_tags
            self.file_hdu_info   = list()
            self.file_hdu_tables = list()
            self.hdu_type = None

    def parse_file(self):
        '''Parse the HTML of the given BeautifulSoup object.'''
        self.hdu_count = None
        if self.ready:
            # process different hdu types
            if self.body:
                # self.body all div tags
                if self.util.children_all_one_tag_type(node = self.body,
                                                       tag_name = 'div'):
                    print('***** All divs *****')
                    divs = self.util.get_hdu_divs(node=self.body)
                    for (self.hdu_number,div) in enumerate(divs):
                        if self.ready: self.parse_file_hdu_div(node=div)
                else:
                    hdus = self.util.get_hdus(node=self.body)
                    self.parse_file_hdus(node=hdus)
                self.set_hdu_count()
#                print('self.file_hdu_info: %r' % self.file_hdu_info)
#                print('self.file_hdu_tables: %r' % self.file_hdu_tables)
#                input('pause')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. ' +
                                  'self.body: {}.'.format(self.body))

    def parse_file_hdu_div(self,node=None):
        '''Parse file hdu content from given BeautifulSoup division node.'''
        if self.ready:
            if node:
                child_names = set(self.util.get_child_names(node=node)) # REMOVE
                type = Hdu_type(logger=self.logger,options=self.options)
                self.hdu_type = type.get_hdu_type(node=node)

#                print('self.hdu_type: %r' % self.hdu_type)
#                input('pause')

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
                    else:
                        self.ready = False
                        self.logger.error('Unexpected child_names encountered ' +
                                          'in Hdu.parse_file_hdu_div().')
                else:
                    self.ready = False
                    child_names = set(self.util.get_child_names(node=node))
                    self.logger.error('Unable to parse_file_hdu_div. ' +
                                      'self.hdu_type: {}, '.format(self.hdu_type) +
                                      'child_names: {}.'.format(child_names))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_div. ' +
                                  'node: {}.'.format(node))

    def parse_file_hdus(self,node=None):
        '''Parse file hdu content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                child_names = set(self.util.get_child_names(node=node)) # REMOVE
#                type = Hdu_type(logger=self.logger,options=self.options)
#                self.hdu_type = type.get_hdu_type(node=node)
#                print('self.hdu_type: %r' % self.hdu_type)
#                input('pause')

#                if self.hdu_type == 5:
#                    self.parse_file_hdu_intro_type_5(node=node)
#                    self.parse_file_hdu_tables_type_5(node=node)

                
                if child_names == {'h1','p','h3','ul','pre'}:
                    self.parse_file_h1_p_h3_ul_pre()
                else:
                    self.ready = False
                    self.logger.error('Unexpected HTML body type encountered ' +
                                      'in Hdu.parse_file.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdus. ' +
                                  'node: {}.'.format(node))

    def set_hdu_count(self):
        '''Set the class attribute hdu_count.'''
        if self.ready:
            if self.file_hdu_info and self.file_hdu_tables:
                if len(self.file_hdu_info) == len(self.file_hdu_tables):
                    self.hdu_count = len(self.file_hdu_info)
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to parse_file. ' +
                        'len(self.file_hdu_info) != len(self.file_hdu_tables). ' +
                        'len(self.file_hdu_info): {}, '.format(len(self.file_hdu_info)) +
                        'len(self.file_hdu_tables): {}.'.format(len(self.file_hdu_tables)))
            else:
                self.ready = False
                self.logger.error('Unable to set_hdu_count. ' +
                                  'self.file_hdu_info: {}, '.format(self.file_hdu_info) +
                                  'self.file_hdu_tables: {}.'.format(self.file_hdu_tables))

    def parse_file_hdu_intro_1(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # Get hdu_number and header_title from (the first) heading tag
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # hdu_description
                p = node.find_next('p')
                hdu_description = self.util.get_string(node=p)
                
                # datatype and hdu_size
                dl = node.find_next('dl')
                (datatype,hdu_size) = self.util.get_datatype_and_hdu_size(node=dl)

                # is_image
                tables = node.find_all('table')
                is_image = (     True  if len(tables) == 1
                            else False if len(tables) == 2
                            else None)

                # put it all together
                hdu_info = dict()
                hdu_info['is_image']        = is_image
                hdu_info['hdu_number']      = hdu_number
                hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                hdu_info['hdu_size']        = hdu_size
                hdu_info['hdu_description'] = hdu_description
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_1. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_intro_2(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # Get hdu_number and header_title from (the first) heading tag
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # hdu.description
                ps = list()
                for p in node.find_all('p'): ps.append(p)
                ps.pop() # remove last p tag containing datatype and hdu_size
                hdu_description = '\n'.join([self.util.get_string(node=p) for p in ps])
                
                # datatype and hdu_size
                for p in node.find_all('p'): pass # get last p tag
                (datatype,hdu_size) = self.util.get_datatype_and_hdu_size(node=p)

                # is_image
                tables = node.find_all('table')
                is_image = (     True  if len(tables) == 1
                            else False if len(tables) == 2
                            else None)

                # put it all together
                hdu_info = dict()
                hdu_info['is_image']        = is_image
                hdu_info['hdu_number']      = hdu_number
                hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                hdu_info['hdu_size']        = hdu_size
                hdu_info['hdu_description'] = hdu_description
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_2. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_intro_3(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        if self.ready:
            if node:
                # Get hdu_number and header_title from (the first) heading tag
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))

                # is_image
                pres = node.find_all('pre')
                is_image = (True       if len(pres) == 1
                            else False if len(pres) == 2
                            else None)

                # put it all together
                hdu_info = dict()
                hdu_info['is_image']        = is_image
                hdu_info['hdu_number']      = hdu_number
                hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                hdu_info['hdu_size']        = None
                hdu_info['hdu_description'] = None
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

                # is_image
                tables = node.find_all('table')
                is_image = (True       if len(tables) == 1
                            else False if len(tables) == 2
                            else None)

                # put it all together
                hdu_info = dict()
                hdu_info['is_image']        = is_image
                hdu_info['hdu_number']      = hdu_number
                hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                hdu_info['hdu_size']        = None
                hdu_info['hdu_description'] = hdu_description
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
                hdu_description = '\n'.join([self.util.get_string(node=p) for p in ps])

                # put it all together
                hdu_info = dict()
                hdu_info['is_image']        = None
                hdu_info['hdu_number']      = hdu_number
                hdu_info['hdu_title']       = hdu_title if hdu_title else ' '
                hdu_info['hdu_size']        = None
                hdu_info['hdu_description'] = hdu_description
                self.file_hdu_info.append(hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_5. ' +
                                  'node: {}, '.format(node) )

    def parse_file_hdu_tables_1(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                tables = node.find_all('table')
                # double check is_image consistentcy
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(node=node))
                is_image = self.file_hdu_info[hdu_number]['is_image']
                if (is_image and len(tables) == 2):
                    self.ready = False
                    self.logger.error('Inconsistent is_image.')
                # check that HDU0 has only one table
                if hdu_number == 0 and len(tables) > 1:
                    if self.options.force:
                        tables = [tables[0]]
                        self.file_hdu_info[hdu_number]['is_image'] = True
                    else:
                        self.ready = False
                        self.logger.error('HDU0 only allowed one table. ' +
                                          'len(tables): {}'.format(len(tables)))
                # parse table(s)
                if self.ready:
                    for table in tables:
                        hdu_table = dict()
                        # table caption
                        caption = table.find_next('caption')
                        table_caption = self.util.get_string(node=caption)
                        # table_column_names
                        table_column_names = list(table.find_next('thead')
                                                       .find_next('tr').strings)
                        # is_header
                        s = set([x.lower() for x in table_column_names])
                        is_header = (s == {'key','value','type','comment'})
                        # table keyword/values
                        trs = table.find_next('tbody').find_all('tr')
                        table_rows = dict()
                        for (position,tr) in enumerate(trs):
                            table_row = list()
                            for td in tr.find_all('td'):
                                string = self.util.get_string(node=td)
                                table_row.append(string)
                            table_rows[position]  = table_row
                        
                        # put it all together
                        hdu_table['is_header']          = is_header
                        hdu_table['table_caption']      = table_caption
                        hdu_table['table_column_names'] = table_column_names
                        hdu_table['table_rows']         = table_rows
                        hdu_tables.append(hdu_table)
                    self.file_hdu_tables.append(hdu_tables)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_1. ' +
                                  'node: {}, '.format(node))

    def parse_file_hdu_tables_2(self,node=None):
        '''Parse file hdu data content from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                # table caption
                table_caption = None
                # table keyword/values
                pres = node.find_all('pre')
                assert(len(pres)<=2)
            
                # hdu header
                hdu_table = dict()
                pre = pres[0]
                rows = self.util.get_string(node=pre).split('\n')
                table_rows = dict()
                for (position,row) in enumerate(rows):
                    table_rows[position] = self.get_table_row_pre_1(row=row)
                # put it all together
                hdu_table['is_header']          = True
                hdu_table['table_caption']      = table_caption
                hdu_table['table_column_names'] = ['Key','Value','Type','Comment']
                hdu_table['table_rows']         = table_rows
                hdu_tables.append(hdu_table)
                
                # hdu data table
                if len(pres) == 2:
                    hdu_table = dict()
                    pre = pres[1]
                    rows = self.util.get_string(node=pre).split('\n')
                    table_rows = dict()
                    for (position,row) in enumerate(rows):
                        table_rows[position] = self.get_table_row_pre_1(row=row)
                    # put it all together
                    hdu_table['is_header']          = True
                    hdu_table['table_caption']      = table_caption
                    hdu_table['table_column_names'] = ['Name','Type','Unit','Description']
                    hdu_table['table_rows']         = table_rows
                    hdu_tables.append(hdu_table)
                self.file_hdu_tables.append(hdu_tables)

            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_2. ' +
                                  'node: {}, '.format(node) +
                                  'assumptions: {}'.format(assumptions))

    def get_table_row_pre_1(self,row=None):
        '''Set the header keyword-value pairs for the given row.'''
        table_row = list()
        if self.ready:
            if row:
                keyword = None
                value = None
                datatype = None # This is not used in this template datatype
                comment = None
                value_comment = None
                # determine keyword
                if 'HISTORY' in row or row.strip() == 'END':
                    if   'HISTORY AP3D:' in row: keyword = 'HISTORY AP3D:'
                    elif 'HISTORY' in row:       keyword = 'HISTORY'
                    else:                        keyword = 'END'
                    value_comment = row.replace(keyword,'')
                    keyword = keyword.replace(':','')
                elif '=' in row:
                    split = row.split('=')
                    keyword       = split[0].strip() if split else None
                    value_comment = split[1]         if split else None
                else:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_table_row_h2_pre. ' +
                            "The strings 'HISTORY', 'END' and '=' " +
                            'not found in row. ' +
                            'row: {}'.format(row))
                # determine value and comment
                if self.ready:
                    if 'HISTORY' in row or 'END' in row:
                        value = None
                        comment = value_comment
                    elif '=' in row:
                        if   ' / '  in value_comment: split_char = ' / '
                        elif ' /'   in value_comment: split_char = ' /'
                        elif '/ '   in value_comment: split_char = '/ '
                        elif '/'    in value_comment: split_char = '/'
                        else:                         split_char = None
                        split   = (value_comment.split(split_char)
                                   if split_char else None)
                        value   = split[0]         if split else None
                        comment = split[1].strip() if split else None
                table_row = [keyword,value,datatype,comment]
            else:
                self.ready = False
                self.logger.error('Unable to get_table_row_pre_1. ' +
                                  'row: {}'.format(row))
        return table_row

    def parse_file_hdu_tables_3(self,node=None):
        '''Parse file hdu keyword/value/type/comment content
        from given BeautifulSoup node.'''
        hdu_tables = list()
        if self.ready:
            if node:
                tables = node.find_all('table')
                for (table_number,table) in enumerate(tables):
                    if self.ready:
                        # table caption
                        caption = table.find_next('caption')
                        table_caption = self.util.get_string(node=caption)
                        
                        # parse table
                        trs = [tr for tr in table.find_all('tr')
                               if not self.util.get_string(node=tr).isspace()]
                        
                        # table_column_names from <th> children of first <tr> tag
                        column_names = str()
                        if self.util.children_all_one_tag_type(node=trs[0],tag_name='th'):
                            ths = trs[0]
                            trs = trs[1:]
                            column_names = list([s.lower() for s in ths.strings
                                                    if not s.isspace()])

                        # table keyword/values
                        hdu_table = dict()
                        table_rows = dict()
                        for (position,tr) in enumerate(trs):
                            if self.ready:
                                if column_names:
                                    is_header = (False
                                                if ('unit' in column_names
                                                    or 'units' in column_names)
                                                else True)
                                    table_row = self.get_table_row_tr_1(
                                                            table_number=table_number,
                                                            column_names=column_names,
                                                            node=tr)
                                else:
                                    column_names = (['key','value','type','comment']
                                                    if table_number == 0 else
                                                    ['name','type','unit','description'])
                                    is_header = True if table_number == 0 else False
                                    table_row = list()
                                    for td in tr.find_all('td'):
                                        string = self.util.get_string(node=td)
                                        table_row.append(string)
                                table_rows[position]  = table_row
                        
                        # put it all together
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

    def get_table_row_tr_1(self,table_number=None,column_names=None,node=None):
        '''Get table row from the <td> children of the given BeautifulSoup node.'''
        table_row = [None,None,None,None]
        if self.ready:
            if table_number is not None and column_names and node:
                is_header = (False if ('unit' in column_names or 'units' in column_names)
                            else True)
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
                                   'type'         : 1,
                                   'unit'         : 2,
                                   'units'        : 2,
                                   'comment'      : 3,
                                   'description'  : 3,
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
        
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_4. ' +
                                  'table_number: {}, '.format(table_number) +
                                  'table_column_names: {}, '.format(table_column_names) +
                                  'node: {}.'.format(node) )
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
                    self.file_hdu_info.append(hdu_info)
                    self.hdu_count = len(self.file_hdu_info)
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
                table_column_names = ['key','value','type','comment']
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
                    hdu_table['table_column_names'] = table_column_names
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



