
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
                                  'self.body: {0}'.format(self.body))

    def parse_file_div(self):
        '''Parse the HTML of the given BeautifulSoup div tag object.'''
        if self.ready:
            if self.body:
                # Find extension div
                for div in [div for div in self.body
                            if not self.util.get_string(node=div).isspace()
                            and self.util.ready]:
                    # Found intro div
                    if 'hdu' in div['id']: self.parse_file_extension_div(div=div)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_div. ' +
                                  'self.body: {0}'.format(self.body))

    def parse_file_extension_div(self,div=None):
        '''Parse file extension content from given division tag.'''
        if self.ready:
            if div:
                child_names = set(self.util.get_child_names(node=div))
                # process different div extension types
                if child_names == {'h2','p','dl','table'}:
                    self.parse_file_data_p_h2_dl_table(div=div)
                    self.parse_file_header_p_h2_dl_table(div=div)
                else:
                    self.ready = False
                    self.logger.error('Unexpected child_names encountered ' +
                                      'in parse_file_extension_div.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_div. ' +
                                  'div: {0}'.format(div))

    def parse_file_data_p_h2_dl_table(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if (div and
                self.verify_assumptions_parse_file_p_h2_dl_table(div=div)):
                # extension.hdu_number and header.title
                heading = div.find_next('h2').string
                split = heading.split(':')
                hdu_number   = int(split[0].lower().replace('hdu',''))
                header_title = split[1].lower().strip()
                # column.description
                column_description = div.find_next('p').string

                # data.is_image, column.datatype, column.size
                data = div.find_next('dl')
                dt = data.find_all('dt')
                dd = data.find_all('dd')
                definitions  = list()
                descriptions = list()
                for definition in dt:
                    definitions.append(definition.string.lower())
                for description in dd:
                    descriptions.append(description.string.lower())
                for (definition,description) in list(zip(definitions,descriptions)):
                    if 'type' in definition: column_datatype = description
                    if 'size' in definition: column_size     = description
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
                self.logger.error('Unable to parse_file_data_p_h2_dl_table. ' +
                                  'div: {0}'.format(div))

    def parse_file_header_p_h2_dl_table(self,div=None):
        '''Parse file description content from given division tag.'''
        hdu_header = dict()
        if self.ready:
            if (div and
                self.verify_assumptions_parse_file_p_h2_dl_table(div=div)):
                table = div.find_next('table')
                # table caption
                table_caption = table.find_next('caption').string
                # table column headers
                table_keywords = list()
                for string in table.find_next('thead').stripped_strings:
                    table_keywords.append(string.lower())
                # table values
                body = table.find_next('tbody')
                rows = body.find_all('tr')
                table_rows = dict()
                for (row_order,row) in enumerate(rows):
                    if not self.ready: break
                    row_data = list()
                    for data in row.find_all('td'):
                        string = self.util.get_string(node=data)
                        self.ready = self.ready and self.util.ready
                        if self.ready: row_data.append(string)
                        else: break
                    table_rows[row_order]  = row_data
                hdu_header['table_caption']  = table_caption
                hdu_header['table_keywords'] = table_keywords
                hdu_header['table_rows']     = table_rows
                self.file_extension_headers.append(hdu_header)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_header_p_h2_dl_table. ' +
                                  'div: {0}'.format(div))

    def verify_assumptions_parse_file_p_h2_dl_table(self,div=None):
        '''Verify assumptions made in parse_file_data_p_h2_dl_table.'''
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
            # Assume 'HDUn:' is in the h2 heading for some n = 0,1,2,...
            h2 = div.find_next('h2')
            string = self.util.get_string(node=h2)
            if not ('HDU' in string and ':' in string):
                assumptions = False
                self.logger.error("Invalid assumption: HDU:' in h2 heading")
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
            for dt in dts: dts_strings.append(self.util.get_string(node=dt))
            # Assume 'HDU Type' in dts_strings
            if 'HDU Type' not in dts_strings:
                assumptions = False
                self.logger.error("Invalid assumption: HDU Type' in dts_strings")
            # Assume 'HDU Size' in dts_strings
            if 'HDU Size' not in dts_strings:
                assumptions = False
                self.logger.error("Invalid assumption: HDU Size' in dts_strings")
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
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_file_p_h2_dl_table. ' +
                'div: {0}'.format(div))
        if not assumptions: self.ready = False
        return assumptions


