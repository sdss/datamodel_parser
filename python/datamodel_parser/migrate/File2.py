from json import dumps
from bs4 import Tag, NavigableString


class File2:
    '''
        
    '''

    def __init__(self,logger=None,options=None,body=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_divs(body=body)
        self.set_ready()
        self.set_attributes()
    
######### Same as File1

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

    def set_divs(self,body=None):
        '''Set the divs class attribute.'''
        self.divs = None
        if self.ready:
            divs = body.children if body else None
            self.divs = [div for div in divs if div != '\n'] if divs else None
            if not self.divs:
                self.ready = False
                self.logger.error('Unable to set_divs. ' +
                                  'body: {0}'.format(body))

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger  and
                          self.options and
                          self.divs)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None

    def parse_file(self):
        '''Parse the HTML of the given division tags.'''
        if self.ready:
            if self.divs:
                # define these lists here so they're not overwritten in for loop
                self.file_extension_data    = list()
                self.file_extension_headers = list()
                for div in self.divs:
                    div_id = str(div['id'])
                    if div_id == 'intro':   self.parse_file_intro(intro=div)
                    elif ('hdu' in div_id): self.parse_file_extension(div=div)
                    else:
                        self.ready = False
                        self.logger.error('Unknown div_id: {0}'.format(div_id))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. ' +
                                  'self.div_ids: {0}'.format(self.divs))

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

############

    def parse_file_intro(self,intro=None):
        '''Set the tag names and contents for the children of the given tag.'''
        if self.ready:
            # Make sure intro has children
            number_descendants = self.get_number_descendants(node=intro)
            if intro and number_descendants:
                headings = list()
                descriptions = list()
                
                # page title
                heading = intro.find_next('h1').string
                headings.append(heading)
                descriptions.append('')
                
                # page intro
                dl = intro.find_next('dl')
                dt_list = dl.find_all('dt')
                dd_list = dl.find_all('dd')
                if len(dt_list)==len(dd_list):
                    section_title = dt_list[-1]
                    sections      = dd_list[-1]
                    # if number_descendants > 1: then there's a section list
                    # else there's no section list
                    number_descendants = self.get_number_descendants(node=sections)
                    dt_headings      = (dt_list[:-1]
                                     if number_descendants > 1 else dt_list)
                    dd_descriptions  = (dd_list[:-1]
                                     if number_descendants > 1 else dd_list)
                                     
                    # Intro table
                    headings.extend(dt_headings)
                    descriptions.extend(dd_descriptions)
                    self.set_intro_table_information(headings     = headings,
                                                     descriptions = descriptions)

                    # Section table
                    section_title = (section_title
                                     if number_descendants > 1 else '')
                    sections      = (sections
                                     if number_descendants > 1 else list())
                    self.set_section_hdu_names(section_title = section_title,
                                               sections      = sections)
                else:
                    self.ready = False
                    self.logger.error(
                                'Unable to parse_file_intro. ' +
                                'len(dt_list)!=len(dd_list). ' +
                                'len(dt_list): {0}, '.format(len(dt_list)) +
                                'len(dd_list): {0}, '.format(len(dd_list)))
            else:
                self.ready = False
                self.logger.error(
                            'Unable to parse_file_intro. ' +
                            'intro: {0}'.format(intro) +
                            'number_descendants: {0}'.format(number_descendants)
                                )

    def set_intro_table_information(self,headings=None,descriptions=None):
        '''Set file introduction headings and descriptions.'''
        self.intro_heading_orders = list()
        self.intro_heading_levels = list() # Not used for this template
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if headings and descriptions:
                if len(headings)==len(descriptions):
                    for (heading,description) in list(zip(headings,descriptions)):
                        heading_title = (self.get_string(node=heading)
                                         if heading else '')
                        intro_description = (self.get_string(node=description)
                                             if description else '')
                        self.intro_heading_titles.append(heading_title)
                        self.intro_descriptions.append(intro_description)
                    number_headings = len(headings)
                    self.intro_heading_orders = list(range(number_headings))
                    self.intro_heading_levels = [None] * number_headings
                else:
                    self.ready = False
                    self.logger.error(
                                'Unable to set_intro_table_information. ' +
                                'len(headings)!=len(descriptions). '      +
                                'len(headings): {0}, '.format(len(headings))          +
                                'len(descriptions): {0}.'.format(len(descriptions)))

            else:
                self.ready = False
                self.logger.error(
                            'Unable to set_intro_table_information. ' +
                            'headings: {0}'.format(headings) +
                            'descriptions: {0}'.format(descriptions))

    def get_string(self,node=None):
        string = None
        if self.ready:
            if node:
                if isinstance(node,str):
                    string = node
                else:
                    n = self.get_number_descendants(node=node)
                    if n > 1:                    string = str(node)
                    elif n == 1 and node.string: string = str(node.string)
                    else:                        string = None
            else:
                self.ready = None
                self.logger.error('Unable to get_string. ' +
                                  'node: {0}'.format(node))
        return string

    def set_section_hdu_names(self,section_title=None,sections=None):
        '''Get the extension names from the intro Section.'''
        self.section_hdu_names = dict() # if no section this stays empty
        if self.ready:
            if not (section_title and sections):
                self.section_hdu_names[' '] = ' '
            else:
                hdu_numbers = list()
                extension_hdu_names = list()
                section_title = str(section_title.string)
                sections = sections.find_next('ul').find_all('li')
                for section in sections:
                    for string in section.strings:
                        if 'hdu' in string.lower():
                            hdu_number = (
                                        string.lower().replace('hdu','').strip()
                                        if string else None)
                            hdu_number = int(hdu_number)
                            hdu_numbers.append(hdu_number)
                        elif string.strip()[0] == ':':
                            name = string.split(':')[1].strip()
                            extension_hdu_names.append(name)
                    if (hdu_numbers and extension_hdu_names and
                        len(hdu_numbers)==len(extension_hdu_names)):
                        self.section_hdu_names = dict(zip(hdu_numbers,
                                                          extension_hdu_names))
                    else:
                        self.ready = False
                        self.logger.error(
                                'Unable to set_section_hdu_names.'      +
                                'hdu_numbers: {}'
                                    .format(hdu_numbers)      +
                                'section_hdu_names: {}'
                                    .format(section_hdu_names)          +
                                'len(hdu_numbers): {}'
                                    .format(len(hdu_numbers)) +
                                'len(section_hdu_names): {}'
                                    .format(len(section_hdu_names)))

    def parse_file_extension(self,div=None):
        '''Parse file extension content from given division tag.'''
        if self.ready:
            self.parse_file_extension_data(div=div)
            self.parse_file_extension_header(div=div)

    def parse_file_extension_data(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if div:
                self.check_valid_assumptions(div=div)
                if self.ready:
                    # extension.hdu_number and header.title
                    heading = div.find_next('h2').string
                    split = heading.split(':') if heading else None
                    if split:
                        hdu_number   = int(split[0].lower().replace('hdu',''))
                        header_title = split[1].lower().strip()
                    else:
                        self.ready = False
                        self.logger.error("Expected ':' in heading." +
                                          'heading: {}'.format(heading))
                    # data.is_image
                    header = div.find_next('pre').string
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
                                  'div: {0}'.format(div))

    def parse_file_extension_header(self,div=None):
        '''Parse file description content from given division tag.'''
        hdu_header = dict()
        if self.ready:
            if div:
                self.check_valid_assumptions(div=div)
                if self.ready:
                    # table caption
                    table_caption = None
                    # table column headers
                    table_keywords = ['key','value','type','comment']
                    # table values
                    table_rows = dict()
                    header = div.find_next('pre').string
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

    def check_valid_assumptions(self,div=None):
        '''Verify that all of my assumptions are valid'''
        if self.ready:
            if div:
                self.set_child_names(node=div)
                if not bool('h2' and 'pre' in self.child_names):
                    self.ready = None
                    self.logger.error("Invalid assumption: " +
                                      "self.child_names = ['h2','pre']")
            else:
                self.ready = False
                self.logger.error('Unable to check_valid_assumptions. ' +
                                  'div: {0}.'.format(div))

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
