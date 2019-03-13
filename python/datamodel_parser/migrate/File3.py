from json import dumps
from bs4 import Tag, NavigableString

class File3:
    '''
        
    '''

    def __init__(self,logger=None,options=None,body=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_body(body=body)
        self.set_ready()
        self.set_attributes()
    
    def set_logger(self,logger=None):
        '''Set class logger.'''
        self.logger = logger if logger else None
        self.ready = bool(self.logger)
        if not self.ready: print('ERROR: Unable to set_logger.')

    def set_options(self,options=None):
        '''Set the options class attribute.'''
        self.options = None
        if self.ready:
            self.options = options if options else None
            if not self.options:
                self.ready = False
                self.logger.error('Unable to set_options.')

    def set_body(self,body=None):
        '''Set the body class attribute.'''
        self.body = None
        if self.ready:
            self.body = body if body else None
            if not self.body:
                self.ready = False
                self.logger.error('Unable to set_body.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger  and
                          self.options and
                          self.body)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.heading_tags = ['h1','h2','h3','h4','h5','h6']
            self.paragraph_tags = ['p']
            self.bold_tags = ['b']
            self.unordered_list_tags = ['ul']

    def parse_file(self):
        '''Parse the HTML of the given division tags.'''
        self.file_extension_data    = list()
        self.file_extension_headers = list()
        if self.ready:
            if self.body:
                self.parse_file_intro()
                # print associated results here
#                print('\n\nself.intro_heading_orders: %r' % self.intro_heading_orders)
#                print('self.intro_heading_levels: %r' % self.intro_heading_levels)
#                print('self.intro_heading_titles: %r' % self.intro_heading_titles)
#                print('self.intro_descriptions: %r' % self.intro_descriptions)
#                print('len(self.intro_heading_titles): %r' % len(self.intro_heading_titles))
#                print('len(self.intro_descriptions): %r' % len(self.intro_descriptions))

                self.parse_file_extensions()
#                print('self.file_extension_data: \n' + dumps(self.file_extension_data,indent=1))
#                print('self.file_extension_headers: \n' + dumps(self.file_extension_headers,indent=1))
#                input('pause')

            else:
                self.ready = False
                self.logger.error('Unable to parse_file. self.body: {0}'
                                    .format(self.divs))

    def parse_file_intro(self):
        '''Parse file intro content from given body tag.'''
        self.intro_heading_orders = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if self.body and self.body.children:
                heading_order = -1
                found_format_notes = False
                append_discussions = False
                for child in self.body.children:
                    child_name = child.name if child else None
                    string = self.get_string(node=child)
                    if child_name: # skip child = '\n'
                        # found extension tags
                        if (child_name in self.heading_tags and 'HDU' in string):
                            break
                        # intro heading tags
                        elif child_name in self.heading_tags:
                            # page title
                            heading_order += 1
                            self.intro_heading_orders.append(heading_order)
                            level = int(child_name.replace('h',''))
                            self.intro_heading_levels.append(level)
                            title = self.get_string(node=child).replace(':','')
                            self.intro_heading_titles.append(title)
                            # page title
                            if child_name == 'h1':
                                self.intro_descriptions.append('')
                            # multiple non-nested tags
                            if title == 'Format notes':
                                found_format_notes = True
                        # intro non-heading tags containing headings and descriptions
                        elif (child_name in self.paragraph_tags or
                              child_name in self.unordered_list_tags
                            ):
                            contents = child.contents
                            for content in contents:
                                if not self.get_string(node=content).isspace():  # skip '\n'
                                    # heading content
                                    if content.name in self.bold_tags:
                                        heading_order += 1
                                        self.intro_heading_orders.append(heading_order)
                                        self.intro_heading_levels.append(3)
                                        title = (self.get_string(node=content)
                                                     .replace(':',''))
                                        self.intro_heading_titles.append(title)
                                    # descriptions
                                    else:
                                        string = self.get_string(node=content)
                                        if not append_discussions:
                                            self.intro_descriptions.append(string)
                                        else:
                                            self.intro_descriptions[-1] += ' ' + string
                                        if found_format_notes:
                                            append_discussions = True
                        else:
                            self.ready = False
                            self.logger.error('Unable to parse_file_intro. ' +
                                              'Unexpected tag type: {}'
                                                .format(child_name))
                            break
            else:
                self.ready = None
                self.logger.error('Unable to parse_file_intro. ' +
                                  'self.body: {0}'.format(self.body) +
                                  'self.body.children: {0}'
                                    .format(self.body.children))

    def parse_file_extensions(self):
        '''Parse file extension content from given body tag.'''
        self.section_hdu_names = dict() # if no section this stays empty
        if self.ready:
            self.set_extension_tags()
            self.set_extension_headings_and_pres()
            if (self.ready and
                self.extension_headings and self.extension_pres and
                len(self.extension_headings) == len(self.extension_pres)):
                intro_heading_order = -1
                for (heading_tag,pre_tags) in list(zip(self.extension_headings,
                                                      self.extension_pres)):
                    header_title = (self.get_string(node=heading_tag)
                                        .replace(':',''))
                    header = list()
                    for pre_tag in pre_tags:
                        header.append(self.get_string(node=pre_tag))
                    header = '\n'.join(header)
                    self.parse_file_extension_header(header=header)
                    self.parse_file_extension_data(header_title = header_title,
                                                   header       = header)
            else:
                self.ready = False
                self.logger.error(
                    'Unable to parse_file_extensions. ' +
                    'self.extension_headings: {0}'
                        .format(self.extension_headings) +
                    'self.extension_pres: {0}'
                        .format(self.extension_pres) +
                    'len(self.extension_headings): {0}'
                        .format(len(self.extension_headings)) +
                    'len(self.extension_pres): {0}'
                        .format(len(self.extension_pres)))

    def set_extension_tags(self):
        '''Set extensions from given body tag.'''
        self.extension_tags = None
        if self.ready:
            if self.body and self.body.children:
                previous_child = None
                found_extension_tags = False
                for child in self.body.children:
                    child_name = child.name if child else None
                    if child_name and child_name in self.heading_tags:
                        string = self.get_string(node=child)
                        if string and 'HDU' in string:
                            found_extension_tags = True
                            self.extension_tags = (previous_child.next_siblings
                                                   if previous_child else None)
                            break
                    if not found_extension_tags:
                        previous_child = child if child else None
            else:
                self.ready = None
                self.logger.error('Unable to set_extension_tags. ' +
                                  'self.body: {0}'.format(self.body) +
                                  'self.body.children: {0}'
                                    .format(self.body.children))

    def set_extension_headings_and_pres(self):
        '''Set extension_headings and extension_pres from the extension_tags'''
        if self.ready:
            if self.extension_tags:
                first_extension = True
                self.extension_headings = list()
                self.extension_pres = list()
                pres = list()
                for tag in self.extension_tags:
                    name = tag.name
                    if self.ready and name:
                        string = self.get_string(node=tag)
                        if name in self.heading_tags and 'HDU' in string:
                            self.extension_headings.append(tag)
                            if first_extension:
                                first_extension = False
                            else:
                                self.extension_pres.append(pres)
                                pres = list()
                        elif name == 'pre':
                            pres.append(tag)
                        else: # Do nothing; only processing heading and pre tags
                            pass
                self.extension_pres.append(pres)
            else:
                self.ready = None
                self.logger.error('Unable to set_extension_headings_and_pres. ' +
                                  'self.extension_tags: {0}'
                                  .format(self.extension_tags))

    def parse_file_extension_data(self,header_title=None,header=None):
        '''Parse file description content from given header_titleision tag.'''
        if self.ready:
            if header_title and header:
                if self.ready:
                    # extension.hdu_number and header.title
                    hdu_number = (
                        [int(s) for s in list(header_title) if s.isdigit()][0])
                    # data.is_image
                    rows = header.split('\n') if header else list()
                    rows = [row for row in rows
                            if row and 'XTENSION' in row and 'IMAGE' in row]
                    data_is_image = bool(rows)
                    hdu_data = dict()
                    hdu_data['hdu_number']         = hdu_number
                    hdu_data['header_title']       = header_title
                    hdu_data['data_is_image']      = data_is_image
                    hdu_data['column_datatype']    = None
                    hdu_data['column_size']        = None
                    hdu_data['column_description'] = None
                    self.file_extension_data.append(hdu_data)
                    self.extension_count = len(self.file_extension_data)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_data. ' +
                                  'header_title: {0}'.format(header_title) +
                                  'header: {0}'.format(header))

    def parse_file_extension_header(self,header=None):
        '''Parse file description content from given headerision tag.'''
        hdu_header = dict()
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
                    hdu_header['table_caption']  = table_caption
                    hdu_header['table_keywords'] = table_keywords
                    hdu_header['table_rows']     = table_rows
                    self.file_extension_headers.append(hdu_header)
                else:
                    self.ready = False
                    self.logger.error(
                                'Unable to parse_file_extension_header. ' +
                                'rows: {0}'.format(rows))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_header. ' +
                                  'header: {0}'.format(header))

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
                            'row: {0}'.format(row))
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
                                  'row: {0}'.format(row))

    def set_child_names(self,node=None):
        '''Set a list of child for the given BeautifulSoup node.'''
        self.child_names = list()
        if self.ready:
            if node:
                for child in node.children:
                    if child.name:
                        self.child_names.append(str(child.name))
            else:
                self.ready = None
                self.logger.error('Unable to set_child_names. ' +
                                  'node: {0}'.format(node))

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
                self.logger.error('Unable to set_child_names. ' +
                                  'child_names: {0}'.format(child_names))

    def get_string(self,node=None):
        string = None
        if self.ready:
            if node:
                if isinstance(node,str):
                    string = node
                else:
                    n = self.get_number_descendants(node=node)
                    if n > 1:
                        string = str(node).strip()
                    elif (n == 1) and bool(node.string):
                        string = str(node.string).strip()
                    else:
                        string = None
            else:
                self.ready = None
                self.logger.error('Unable to get_string. ' +
                                  'node: {0}'.format(node))
        return string

    def get_number_descendants(self,node=None):
        '''Return True if BeautifulSoup object has descendants.'''
        number_descendants = None
        if self.ready:
            if node:
                number_descendants = 0
                if not (isinstance(node, NavigableString) or isinstance(node, str)):
                    for descendant in node.descendants:
                        if descendant: number_descendants += 1
            else:
                self.ready = False
                self.logger.error('Unable to get_number_descendants.' +
                                  'node: {}'.format(node))
        return number_descendants

