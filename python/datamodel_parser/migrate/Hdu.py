
from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.migrate import Util
from datamodel_parser.migrate import Intro


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

    def parse_file(self):
        '''Parse the HTML of the given BeautifulSoup object.'''
        self.hdu_count = None
        self.file_hdu_info = list()
        self.file_hdu_tables = list()
        if self.ready:
            if self.body:
                # process different hdu types
                # self.body all div tags
                if self.util.children_all_one_tag_type(node = self.body,
                                                       tag_name = 'div'):
                    self.parse_file_div()
                else:
                    # self.body not all div tags
                    child_names = set(self.util.get_child_names(node=self.body))
                    if child_names == {'h1','p','h3','ul','pre'}:
                        self.parse_file_h1_p_h3_ul_pre()
                    else:
                        self.ready = False
                        self.logger.error('Unexpected intro type encountered ' +
                                          'in parse_file.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. ' +
                                  'self.body: {}.'.format(self.body))

    def parse_file_div(self):
        '''Parse the HTML of the given BeautifulSoup div tag object.'''
        if self.ready:
            if self.body:
                # Find hdu div
                for div in [div for div in self.body
                            if not self.util.get_string(node=div).isspace()]:
                    # Found hdu div
                    if 'hdu' in div['id']: self.parse_file_hdu_div(div=div)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_div. ' +
                                  'self.body: {}.'.format(self.body))

    def parse_file_hdu_div(self,div=None):
        '''Parse file hdu content from given division tag.'''
        if self.ready:
            if div:
                child_names = set(self.util.get_child_names(node=div))
                # process different div hdu types
                if child_names == {'h2','p','dl','table'}:
                    self.parse_file_hdu_intro_h2_p_dl_table(div=div)
                    self.parse_file_hdu_tables_h2_p_dl_table(div=div)
                elif child_names == {'h2','pre'}:
                    self.parse_file_hdu_intro_h2_pre(div=div)
                    self.parse_file_hdu_tables_h2_pre(div=div)
                else:
                    self.ready = False
                    self.logger.error('Unexpected child_names encountered ' +
                                      'in parse_file_hdu_div.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_div. ' +
                                  'div: {}.'.format(div))

    def parse_file_hdu_intro_h2_p_dl_table(self,div=None):
        '''Parse file hdu data content from given division tag.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h2_p_dl_table(div=div)
            if div and assumptions:
                # hdu.hdu_number and header.title
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(
                                                        node=div,
                                                        header_tag_name='h2'))
                # column.description
                p = div.find_next('p')
                column_description = self.util.get_string(node=p)
                
                # data.is_image, column.datatype, column.size
                dl = div.find_next('dl')
                (definitions,descriptions) = self.util.get_dts_and_dds_from_dl(dl=dl)
                for (definition,description) in list(zip(definitions,descriptions)):
                    if 'hdu type' in definition.lower(): column_datatype = description
                    if 'hdu size' in definition.lower(): column_size     = description
                is_image = bool('image' in [x.lower() for x in descriptions])

                hdu_info = dict()
                hdu_info['is_image']           = is_image
                hdu_info['hdu_number']         = hdu_number
                hdu_info['hdu_title']          = hdu_title
                hdu_info['column_size']        = column_size
                hdu_info['column_description'] = column_description
                hdu_info['column_datatype']    = column_datatype
                self.file_hdu_info.append(hdu_info)
                self.hdu_count = len(self.file_hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_h2_p_dl_table. ' +
                                  'div: {}, '.format(div) +
                                  'assumptions: {}'.format(assumptions)
                                  )

    def parse_file_hdu_tables_h2_p_dl_table(self,div=None):
        '''Parse file hdu keyword/value/type/comment content
        from given division tag.'''
        hdu_tables = list()
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h2_p_dl_table(div=div)
            if div and assumptions:
                tables = div.find_all('table')
                for table in tables:
                    hdu_table = dict()
                    # table caption
                    caption = table.find_next('caption')
                    table_caption = self.util.get_string(node=caption)
                    # table column headers
                    tr = table.find_next('thead').find_next('tr')
                    table_keywords = list()
                    for th in [th for th in tr.children
                               if not self.util.get_string(node=th).isspace()]:
                        string = self.util.get_string(node=th)
                        table_keywords.append(string)
                    # table values
                    body = table.find_next('tbody')
                    rows = body.find_all('tr')
                    table_rows = dict()
                    for (row_order,row) in enumerate(rows):
                        row_data = list()
                        for data in row.find_all('td'):
                            string = self.util.get_string(node=data)
                            row_data.append(string)
                        table_rows[row_order]  = row_data
                    # Put it all together
                    s = set([x.lower() for x in table_keywords])
                    is_header = (s == {'key','value','type','comment'})
                    hdu_table['is_header']      = is_header
                    hdu_table['table_caption']  = table_caption
                    hdu_table['table_keywords'] = table_keywords
                    hdu_table['table_rows']     = table_rows
                    hdu_tables.append(hdu_table)
                self.file_hdu_tables.append(hdu_tables)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_h2_p_dl_table. ' +
                                  'div: {}, '.format(div) +
                                  'assumptions: {}.'.format(assumptions))

    def verify_assumptions_parse_file_h2_p_dl_table(self,div=None):
        '''Verify assumptions made in parse_file_hdu_intro_h2_p_dl_table.'''
        assumptions = None
        if div:
            assumptions = True
            child_names = self.util.get_child_names(node=div)
            # Assume child_names.count('h2') == 1
            if child_names.count('h2') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('h2') == 1")
            # Assume child_names.count('p') == 1
            if child_names.count('p') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('p') == 1")
            # Assume child_names.count('dl') == 1
            if child_names.count('dl') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('dl') == 1")
            # Assume child_names.count('table') == 1 or child_names.count('table') == 2
            if not (child_names.count('table') == 1 or child_names.count('table') == 2):
                assumptions = False
                self.logger.error("Invalid assumption: " +
                    "child_names.count('table') == 1 or " +
                    "child_names.count('table') == 2")
            # h2 tag assumptions
            # Assume 'HDUn: HduTitle' is the h2 heading for some digit n
            h2 = div.find_next('h2')
            string = self.util.get_string(node=h2).lower()
            if not ('hdu' in string and
                    ':' in string   and
                    string.split(':')[0].lower().replace('hdu','').isdigit()):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "div.find_next('h2') = 'HDUn: HduTitle', " +
                        "where n is a digit")
            # dl tag assumptions
            dl = div.find_next('dl')
            child_names = self.util.get_child_names(node=dl)
            # Assume child_names.count('dt') == 2
            if child_names.count('dt') != 2:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('dt') == 2")
            # Assume child_names.count('dd') == 2
            if child_names.count('dd') != 2:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('dd') == 2")
            # dt tags assumptions
            dts = dl.find_all('dt')
            dts_strings = list()
            for dt in dts:
                string = self.util.get_string(node=dt).lower()
                dts_strings.append(string)
            # Assume 'HDU Type' in dts_strings
            if 'hdu type' not in dts_strings:
                assumptions = False
                self.logger.error("Invalid assumption: 'HDU Type' in dts_strings")
            # Assume 'HDU Size' in dts_strings
            if 'hdu size' not in dts_strings:
                assumptions = False
                self.logger.error("Invalid assumption: 'HDU Size' in dts_strings")
            # table tag assumptions
            table = div.find_next('table')
            child_names = self.util.get_child_names(node=table)
            # Assume child_names.count('caption') == 1
            if child_names.count('caption') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('caption') == 1")
            # Assume child_names.count('thead') == 1
            if child_names.count('thead') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('thead') == 1")
            # Assume child_names.count('tbody') == 1
            if child_names.count('tbody') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('tbody') == 1")
            # thead tag assumptions
            thead = table.find_next('thead')
            child_names = self.util.get_child_names(node=thead)
            # Assume child_names.count('tr') == 1
            if child_names.count('tr') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('tr') == 1")
            # Asume all children of the <ul> tag are <th> tags
            tr = thead.find_next('tr')
            if not self.util.children_all_one_tag_type(node=tr,tag_name='th'):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "children_all_one_tag_type(node=tr,tag_name='th') == True")
            # tbody tag assumptions
            # Asume all children of the <tbody> tag are <tr> tags
            tbody = table.find_next('tbody')
            if not self.util.children_all_one_tag_type(node=tbody,tag_name='tr'):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "children_all_one_tag_type(node=tbody,tag_name='tr') == True")
            # Asume all children of the <tbody> child <tr> tags are <td> tags
            for tr in [tr for tr in tbody.children
                       if not self.util.get_string(node=tr).isspace()]:
                if not self.util.children_all_one_tag_type(node=tr,tag_name='td'):
                    assumptions = False
                    self.logger.error(
                            "Invalid assumption: " +
                            "children_all_one_tag_type(node=tr,tag_name='td')")
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_file_h2_p_dl_table. ' +
                'div: {}.'.format(div))
#        print(assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

    def parse_file_hdu_intro_h2_pre(self,div=None):
        '''Parse file hdu data content from given division tag.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h2_pre(div=div)
            if div and assumptions:
                # hdu.hdu_number and header.title
                (hdu_number,hdu_title) = (
                    self.util.get_hdu_number_and_hdu_title(
                                                        node=div,
                                                        header_tag_name='h2'))
                # data.is_image
                header = div.find_next('pre').string
                rows = header.split('\n') if header else list()
                image_row = [row for row in rows
                        if row and 'XTENSION' in row and 'IMAGE' in row]
                is_image = bool(image_row)
                # combine in a dict
                hdu_info = dict()
                hdu_info['is_image']           = is_image
                hdu_info['hdu_number']         = hdu_number
                hdu_info['hdu_title']       = hdu_title
                # This template type has no data
                hdu_info['column_size']        = None
                hdu_info['column_description'] = None
                hdu_info['column_datatype']    = None
                self.file_hdu_info.append(hdu_info)
                self.hdu_count = len(self.file_hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_intro_h2_pre. ' +
                                  'div: {}, '.format(div) +
                                  'assumptions: {}.'.format(assumptions))

    def parse_file_hdu_tables_h2_pre(self,div=None):
        '''Parse file hdu data content from given division tag.'''
        hdu = dict()
        
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h2_pre(div=div)
            if div and assumptions:
                # table caption
                table_caption = None
                # table column headers
                table_keywords = ['Key','Value','Type','Comment']
                # table values
                pre = div.find_next('pre')
                rows = self.util.get_string(node=pre).split('\n')
                table_rows = dict()
                for (row_order,row) in enumerate(rows):
                    table_rows[row_order] = self.get_row_data_h2_pre(row=row)
                # Put it all together
                hdu['table_caption']  = table_caption
                hdu['table_keywords'] = table_keywords
                hdu['table_rows']     = table_rows
                self.file_hdu_tables.append(hdu)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables_h2_pre. ' +
                                  'div: {}, '.format(div) +
                                  'assumptions: {}'.format(assumptions))

    def get_row_data_h2_pre(self,row=None):
        '''Set the header keyword-value pairs for the given row.'''
        row_data = list()
        if self.ready:
            if row:
                keyword = None
                value = None
                type = None # This is not used in this template type
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
                            'Unable to set_row_data_h2_pre. ' +
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
                        split = value_comment.split(split_char) if split_char else None
                        value   = split[0]         if split else None
                        comment = split[1].strip() if split else None
                row_data = ([keyword,value,type,comment]
                                if keyword or value or type or comment
                                else list())
            else:
                self.ready = False
                self.logger.error('Unable to get_row_data_h2_pre. ' +
                                  'row: {}'.format(row))
        return row_data

    def verify_assumptions_parse_file_h2_pre(self,div=None):
        '''Verify assumptions made in parse_file_hdu_intro_h2_p_dl_table.'''
        assumptions = None
        if div:
            assumptions = True
            child_names = self.util.get_child_names(node=div)
            # Assume child_names.count('h2') == 1
            if child_names.count('h2') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('h2') == 1")
            # Assume child_names.count('pre') == 1
            if child_names.count('pre') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('pre') == 1")
            # h2 tag assumptions
            # Assume 'HDUn: HduTitle' is the h2 heading for some digit n
            h2 = div.find_next('h2')
            string = self.util.get_string(node=h2).lower()
            if not ('hdu' in string and
                    ':' in string   and
                    string.split(':')[0].lower().replace('hdu','').isdigit()):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "div.find_next('h2') = 'HDUn: HduTitle', " +
                        "where n is a digit")
            # pre tag assumptions
            pre = div.find_next('pre')
            rows = self.util.get_string(node=pre).split('\n')
            # Assume the pre tag is a string with rows separated by '\n'
            if not rows:
                assumptions = False
                self.logger.error(
                              "Invalid assumption: " +
                              "pre tag is a string with rows separated by '\n'")
            # Assume none of the list entries of rows are empty
            rows1 = [row for row in rows if row]
            if len(rows) != len(rows1):
                assumptions = False
                self.logger.error("Invalid assumption: " +
                                  "none of the list entries of rows are empty")
            # Assume the rows contain either '=' for data or 'HISTORY' or 'END'
            for row in rows:
                if not ('=' in row or 'HISTORY' in row or 'END' in row):
                    assumptions = False
                    self.logger.error(
                        "Invalid assumption: " +
                        "the rows contain either '=' for data or 'HISTORY' or 'END'")
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_file_h2_pre. ' +
                'div: {}.'.format(div))
#        print(assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

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
                                            .replace(':',''))
                        self.ready = self.ready and self.util.ready
                        if self.ready:
                            header = list()
                            for pre_tag in pre_tags:
                                string = self.util.get_string(node=pre_tag)
                                self.ready = self.ready and self.util.ready
                                if self.ready: header.append(string)
                                else: break
                            header = '\n' + '\n'.join(header)
                            self.parse_file_hdu_tables(header=header)
                            self.parse_file_hdu_info(hdu_title = hdu_title,
                                                     header       = header)
                        else: break
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to parse_file_hdu_tables. ' +
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
                for child in self.body.children:
                    child_name = child.name if child else None
                    if child_name and child_name in self.heading_tags:
                        string = self.util.get_string(node=child)
                        self.ready = self.ready and self.util.ready
                        if self.ready:
                            if string and 'HDU' in string:
                                found_hdu_tags = True
                                self.hdu_tags = (previous_child.next_siblings
                                                       if previous_child else None)
                                break
                        else: break
                    if not found_hdu_tags:
                        previous_child = child if child else None
            else:
                self.ready = None
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
                for tag in self.hdu_tags:
                    name = tag.name
                    if name:
                        string = self.util.get_string(node=tag)
                        self.ready = self.ready and self.util.ready
                        if self.ready:
                            if name in self.heading_tags and 'HDU' in string:
                                self.hdu_headings.append(tag)
                                if first_hdu:
                                    first_hdu = False
                                else:
                                    self.hdu_pres.append(pres)
                                    pres = list()
                            elif name == 'pre':
                                pres.append(tag)
                            else: # Do nothing; only processing heading and pre tags
                                pass
                        else: break
                self.hdu_pres.append(pres)
            else:
                self.ready = None
                self.logger.error('Unable to set_hdu_headings_and_pres. ' +
                                  'self.hdu_tags: {}'
                                  .format(self.hdu_tags))

    def parse_file_hdu_info(self,hdu_title=None,header=None):
        '''Parse file description content from given hdu_titleision tag.'''
        if self.ready:
            if hdu_title and header:
                if self.ready:
                    # hdu.hdu_number and header.title
                    hdu_number = (
                        [int(s) for s in list(hdu_title) if s.isdigit()][0])
                    # data.is_image
                    rows = header.split('\n') if header else list()
                    rows = [row for row in rows
                            if row and 'XTENSION' in row and 'IMAGE' in row]
                    is_image = bool(rows)
                    hdu_info = dict()
                    hdu_info['is_image']           = is_image
                    hdu_info['hdu_number']         = hdu_number
                    hdu_info['hdu_title']       = hdu_title
                    hdu_info['column_size']        = None
                    hdu_info['column_description'] = None
                    hdu_info['column_datatype']    = None
                    self.file_hdu_info.append(hdu_info)
                    self.hdu_count = len(self.file_hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_info. ' +
                                  'hdu_title: {}'.format(hdu_title) +
                                  'header: {}'.format(header))

    def parse_file_hdu_tables(self,header=None):
        '''Parse file description content from given headerision tag.'''
        hdu = dict()
        if self.ready:
            if header:
                # table caption
                table_caption = None
                # table column headers
                table_keywords = ['key','value','type','comment']
                # table values
                table_rows = dict()
                rows = header.split('\n') if header else list()
                rows = [row for row in rows if row]
                if rows:
                    for (row_order,row) in enumerate(rows):
                        self.set_row_data(row=row)
                        table_rows[row_order] = (self.row_data
                                                 if self.row_data else None)
                    hdu['table_caption']  = table_caption
                    hdu['table_keywords'] = table_keywords
                    hdu['table_rows']     = table_rows
                    self.file_hdu_tables.append(hdu)
                else:
                    self.ready = False
                    self.logger.error(
                                'Unable to parse_file_hdu_tables. ' +
                                'rows: {}'.format(rows))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_tables. ' +
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
                    value_comment = row.replace('HISTORY','')
                elif '=' in row:
                    split = row.split('=')
                    keyword       = split[0].strip() if split else None
                    value_comment = split[1]         if split else None
                elif 'END' in row:
                    keyword = 'END'
                    value_comment = row.replace('END','')
                else:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_row_data. ' +
                            "The strings 'HISTORY', 'END' and '=' " +
                            'not found in row. ' +
                            'row: {}'.format(row))
                if value_comment and '/' in value_comment:
                    split = value_comment.split('/')
                    value   = split[0]         if split else None
                    comment = split[1].strip() if split else None
                else:
                    value = value_comment
                    comment = None
                self.row_data = ([keyword,value,type,comment]
                                if keyword or value or type or comment
                                else list())
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
                self.ready = None
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



