
from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.migrate import Util


class Extension:
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
        self.extension_count = None
        self.file_extension_data    = list()
        self.file_extension_headers = list()
        if self.ready:
            if self.body:
                # process different extension types
                # div intro type
                if self.util.children_all_one_tag_type(node = self.body,
                                                       tag_name = 'div'):
                    self.parse_file_div()
                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file. ' +
                                      'Unexpected intro type encountered ' +
                                      'in parse_file().')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. ' +
                                  'self.body: {}.'.format(self.body))

    def parse_file_div(self):
        '''Parse the HTML of the given BeautifulSoup div tag object.'''
        if self.ready:
            if self.body:
                # Find extension div
                for div in [div for div in self.body
                            if not self.util.get_string(node=div).isspace()]:
                    # Found intro div
                    if 'hdu' in div['id']: self.parse_file_extension_div(div=div)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_div. ' +
                                  'self.body: {}.'.format(self.body))

    def parse_file_extension_div(self,div=None):
        '''Parse file extension content from given division tag.'''
        if self.ready:
            if div:
                child_names = set(self.util.get_child_names(node=div))
                # process different div extension types
                if child_names == {'h2','p','dl','table'}:
                    self.parse_file_data_h2_p_dl_table(div=div)
                    self.parse_file_header_h2_p_dl_table(div=div)
                elif child_names == {'h2','pre'}:
                    self.parse_file_data_h2_pre(div=div)
                    self.parse_file_header_h2_pre(div=div)
                else:
                    self.ready = False
                    self.logger.error('Unexpected child_names encountered ' +
                                      'in parse_file_extension_div.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_div. ' +
                                  'div: {}.'.format(div))

    def parse_file_data_h2_p_dl_table(self,div=None):
        '''Parse file extension data content from given division tag.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h2_p_dl_table(div=div)
            if div and assumptions:
                # extension.hdu_number and header.title
                (hdu_number,header_title) = (
                            self.util.get_hdu_number_and_header_title(node=div))

                # column.description
                p = div.find_next('p')
                column_description = self.util.get_string(node=p)

                # data.is_image, column.datatype, column.size
                dl = div.find_next('dl')
                (definitions,descriptions) = self.util.get_dts_and_dds_from_dl(dl=dl)
                for (definition,description) in list(zip(definitions,descriptions)):
                    if 'hdu type' in definition.lower(): column_datatype = description
                    if 'hdu size' in definition.lower(): column_size     = description
                data_is_image = bool('image' in descriptions)
                
                hdu_data = dict()
                hdu_data['hdu_number']         = hdu_number
                hdu_data['header_title']       = header_title
                hdu_data['data_is_image']      = data_is_image
                hdu_data['column_datatype']    = column_datatype
                hdu_data['column_size']        = column_size
                hdu_data['column_description'] = column_description
                self.file_extension_data.append(hdu_data)
                self.extension_count = len(self.file_extension_data)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_data_h2_p_dl_table. ' +
                                  'div: {}, '.format(div) +
                                  'assumptions: {}'.format(assumptions)
                                  )

    def parse_file_header_h2_p_dl_table(self,div=None):
        '''Parse file extension keyword/value/type/comment content
        from given division tag.'''
        hdu_header = dict()
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h2_p_dl_table(div=div)
            if div and assumptions:
                table = div.find_next('table')
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
                hdu_header['table_caption']  = table_caption
                hdu_header['table_keywords'] = table_keywords
                hdu_header['table_rows']     = table_rows
                self.file_extension_headers.append(hdu_header)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_header_h2_p_dl_table. ' +
                                  'div: {}, '.format(div) +
                                  'assumptions: {}.'.format(assumptions))

    def verify_assumptions_parse_file_h2_p_dl_table(self,div=None):
        '''Verify assumptions made in parse_file_data_h2_p_dl_table.'''
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
            # Assume child_names.count('table') == 1
            if child_names.count('table') != 1:
                assumptions = False
                self.logger.error("Invalid assumption: child_names.count('table') == 1")
            # h2 tag assumptions
            # Assume 'HDUn: ExtensionTitle' is the h2 heading for some digit n
            h2 = div.find_next('h2')
            string = self.util.get_string(node=h2).lower()
            if not ('hdu' in string and
                    ':' in string   and
                    string.split(':')[0].lower().replace('hdu','').isdigit()):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "div.find_next('h2') = 'HDUn: ExtensionTitle', " +
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
        if not assumptions:
            print('div: %r' % div)
            self.ready = False
        return assumptions

    def parse_file_data_h2_pre(self,div=None):
        '''Parse file extension data content from given division tag.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h2_pre(div=div)
            if div and assumptions:
                # extension.hdu_number and header.title
                (hdu_number,header_title) = (
                            self.util.get_hdu_number_and_header_title(node=div))
                # data.is_image
                header = div.find_next('pre').string
                rows = header.split('\n') if header else list()
                image_row = [row for row in rows
                        if row and 'XTENSION' in row and 'IMAGE' in row]
                data_is_image = bool(image_row)
                # combine in a dict
                hdu_data = dict()
                hdu_data['hdu_number']         = hdu_number
                hdu_data['header_title']       = header_title
                hdu_data['data_is_image']      = data_is_image
                # This template type has no data
                hdu_data['column_datatype']    = None
                hdu_data['column_size']        = None
                hdu_data['column_description'] = None
                self.file_extension_data.append(hdu_data)
                self.extension_count = len(self.file_extension_data)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_data_h2_pre. ' +
                                  'div: {}, '.format(div) +
                                  'assumptions: {}.'.format(assumptions))

    def parse_file_header_h2_pre(self,div=None):
        '''Parse file extension data content from given division tag.'''
        hdu_header = dict()
        
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
                hdu_header['table_caption']  = table_caption
                hdu_header['table_keywords'] = table_keywords
                hdu_header['table_rows']     = table_rows
                self.file_extension_headers.append(hdu_header)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_header_h2_pre. ' +
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
                if 'HISTORY' in row:
                    keyword = 'HISTORY'
                    value_comment = row.replace('HISTORY','').strip()
                elif '=' in row:
                    split = row.split('=')
                    keyword       = split[0].strip() if split else None
                    value_comment = split[1]         if split else None
                elif 'END' in row:
                    keyword = 'END'
                    value_comment = row.replace('END','').strip()
                else:
                    self.ready = False
                    self.logger.error(
                            'Unable to set_row_data_h2_pre. ' +
                            "The strings 'HISTORY', 'END' and '=' " +
                            'not found in row. ' +
                            'row: {}'.format(row))
                # determine value and comment
                if value_comment:
                    if '=' in row:
                        if   ' / '  in value_comment: split_char = ' / '
                        elif ' /'   in value_comment: split_char = ' /'
                        elif '/'    in value_comment: split_char = '/'
                        else:                         split_char = None
                        split = value_comment.split(split_char) if split_char else None
                        value   = split[0]         if split else None
                        comment = split[1].strip() if split else None
                    else:
                        value = None
                        comment = value_comment
                else:
                    value = value_comment
                    comment = None
                row_data = ([keyword,value,type,comment]
                                if keyword or value or type or comment
                                else list())
            else:
                self.ready = False
                self.logger.error('Unable to get_row_data_h2_pre. ' +
                                  'row: {}'.format(row))
        return row_data

    def verify_assumptions_parse_file_h2_pre(self,div=None):
        '''Verify assumptions made in parse_file_data_h2_p_dl_table.'''
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
            # Assume 'HDUn: ExtensionTitle' is the h2 heading for some digit n
            h2 = div.find_next('h2')
            string = self.util.get_string(node=h2).lower()
            if not ('hdu' in string and
                    ':' in string   and
                    string.split(':')[0].lower().replace('hdu','').isdigit()):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "div.find_next('h2') = 'HDUn: ExtensionTitle', " +
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
#        print(assumptions)
#        input('pause')
        if not assumptions:
            self.ready = False
        return assumptions

