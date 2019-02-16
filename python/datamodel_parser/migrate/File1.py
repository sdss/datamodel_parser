from json import dumps
from bs4 import Tag, NavigableString


class File1:
    '''
        
    '''

    def __init__(self,logger=None,options=None,body=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_divs(body=body)
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
        self.file_extension_data   = list()
        self.file_extension_headers = list()
        if self.ready:
            if self.divs:
                for div in self.divs:
                    div_id = div['id']
                    if div_id == 'intro': self.parse_file_intro(intro=div)
                    elif 'hdu' in div_id: self.parse_file_extension(div=div)
                    else:
                        self.ready = False
                        self.logger.error('Unknown div_id: {0}'.format(div_id))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. self.div_ids: {0}'
                                    .format(self.divs))

    def parse_file_intro(self,intro=None):
        '''Parse file description content from given tag.'''
        if self.ready:
            if intro:
                self.set_intro_tag_names_and_contents(intro=intro)
                self.set_intro_table_information()
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_intro. ' +
                                  'intro: {0}'.format(intro))

    def set_intro_tag_names_and_contents(self,intro=None):
        ''' Set the tag names and contents for the children of the given tag.'''
        self.intro_tag_names = None
        self.intro_tag_contents = None
        if self.ready:
            # Make sure intro has children
            number_descendants = self.get_number_descendants(node=intro)
            if intro and number_descendants:
                self.intro_tag_names = list()
                self.intro_tag_contents = list()
                for child in [item for item in intro.children if item != '\n']:
                    if isinstance(child, NavigableString):
                        self.intro_tag_names.append('')
                        self.intro_tag_contents.append(str(child.string))
                    elif isinstance(child, Tag):
                        tag_name = child.name
                        if tag_name == 'div':
                            # Parse intro section hdu names
                            self.set_section_hdu_names(div=child)
                            self.extension_count = len(
                                                self.section_hdu_names.keys())
                        else:
                            # Parse intro titles and contents
                            tag_contents = self.get_tag_contents(tag=child)
                            self.intro_tag_names.append(tag_name)
                            self.intro_tag_contents.append(tag_contents)
                    else:
                        self.ready = False
                        self.logger.error('Unexpected BeautifulSoup type. ' +
                                          'child: {0}, type(child): {1}'
                                          .format(child,type(child)))
                self.remove_closing_division_tag(
                                        tag_names=self.intro_tag_names,
                                        tag_contents=self.intro_tag_contents)
            else:
                self.ready = False
                self.logger.error(
                            'Unable to set_intro_tag_names_and_contents. ' +
                            'intro: {0}'.format(intro) +
                            'number_descendants: {0}'.format(number_descendants)
                                )

    def get_number_descendants(self,node=None):
        '''Return True if BeautifulSoup object has descendants.'''
        number_descendants = None
        if self.ready:
            if node:
                number_descendants = 0
                if not isinstance(node, NavigableString):
                    for descendant in node.descendants:
                        if descendant: number_descendants += 1
            else:
                self.ready = False
                self.logger.error('Unable to get_number_descendants.' +
                                  'node: {}'.format(node))
        return number_descendants

    def set_section_hdu_names(self,div=None):
        '''Get the extension names from the intro Section.'''
        self.section_hdu_names = dict()
        if self.ready:
            if div:
                for string in [item for item in div.strings if item != '\n']:
                    if 'HDU' in string:
                        split = string.split(':')
                        extension = split[0].lower().strip() if split else None
                        hdu_number = (extension.replace('hdu','')
                                                if extension else None)
                        hdu_name   = split[1].lower().strip() if split else None
                        if hdu_number and hdu_name:
                            self.section_hdu_names[hdu_number] = hdu_name
                        else:
                            self.ready = False
                            self.logger.error(
                                    'Unable to set_section_hdu_names.' +
                                    'hdu_number: {}'
                                        .format(hdu_number) +
                                    'hdu_name: {}'.format(hdu_name))
            else:
                self.ready = False
                self.logger.error('Unable to set_section_hdu_names.' +
                                  'div: {}'.format(div))

    def get_tag_contents(self,tag=None):
        '''Get the tag contents from the given tag with text content.'''
        tag_contents = None
        if self.ready:
            if tag:
                contents = tag.contents
                if len(contents) == 1:
                    tag_contents = str(contents[0])
                elif len(contents) > 1:
                    tag_contents = ''
                    for item in contents:
                        tag_contents += str(item)
            else:
                self.ready = False
                self.logger.error('Unable to get_tag_contents.' +
                                  'tag: {}'.format(tag))
        return tag_contents

    def remove_closing_division_tag(self,tag_names=None,tag_contents=None):
        '''Remove the contentless, closing division tag from the given lists.'''
        if self.ready:
            if tag_names and tag_contents:
                if tag_names[-1] == 'div':
                    if not tag_contents[-1]:
                        del tag_names[-1]
                        del tag_contents[-1]
                    else:
                        self.ready = False
                        self.logger.error(
                            'Closing div tag has contents. ' +
                            'name: {0}, contents: {1}'
                            .format(tag_names[-1],tag_contents[-1]))
            else:
                self.ready = False
                self.logger.error(
                            'Unable to remove_closing_division_tag. ' +
                            'tag_names: {0}'.format(tag_names) +
                            'contents: {0}'.format(contents)
                                )

    def set_intro_table_information(self):
        '''Set the heading names and descriptions for the intro table.'''
        self.intro_heading_orders = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if self.intro_tag_names and self.intro_tag_contents:
                names = self.intro_tag_names
                contents = self.intro_tag_contents
                self.check_valid_assumptions(names=names,contents=contents)
                if self.ready:
                    heading_tags = ['h1','h2','h3','h4','h5','h6']
                    paragraph_tags = ['p']
                    order = -1
                    for (idx,name) in enumerate(names):
                        if name in paragraph_tags: continue
                        if name in heading_tags:
                            order += 1
                            self.intro_heading_orders.append(order)
                            level = int(name.replace('h',''))
                            self.intro_heading_levels.append(level)
                            self.intro_heading_titles.append(contents[idx])
                            if names[idx+1] in paragraph_tags:
                                self.intro_descriptions.append(contents[idx+1])
                            else:
                                self.intro_descriptions.append('')
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_intro_table_information. ' +
                    'self.intro_tag_names: {0}, self.intro_tag_contents: {1}'
                    .format(self.intro_tag_names,self.intro_tag_contents)
                                  )

    def check_valid_assumptions(self,names=None,contents=None):
        '''Verify that all of my assumptions are valid'''
        if self.ready:
            if names and contents:
                heading_tags = ['h1','h2','h3','h4','h5','h6']
                paragraph_tags = ['p']
                # Check that the lists have the same length
                if len(names) != len(contents):
                    self.ready = False
                    self.logger.error(
                        'Invalid assumption: len(names) = len(contents). ' +
                        'len(names): {0}, len(contents): {1}'
                        .format(len(names),len(contents))
                                      )
                # Check that the first name is a heading tag
                if names[0] not in heading_tags:
                    self.ready = False
                    self.logger.error(
                        'Invalid assumption: File intro starts with a heading.')

                # Check that the names are either heading or paragraph tags
                for name in names:
                    unexpected_tag_names = list()
                    if name not in heading_tags and name not in paragraph_tags:
                        unexpected_tag_names.append(name)
                    if unexpected_tag_names:
                        self.ready = False
                        self.logger.error(
                            'Invalid assumption: ' +
                            'names are either heading or paragraph tags.' +
                            'unexpected_tag_names: {0}.'
                            .format(unexpected_tag_names))
            else:
                self.ready = False
                self.logger.error(
                    'Unable to check_valid_assumptions. ' +
                    'names: {0}, contents: {1}'.format(names,contents))

    def set_parent_names(self,div=None):
        '''Set a list of parent for the given division tag.'''
        self.parent_names = list()
        if self.ready:
            if div:
                for parent in div.parents:
                    if parent.name: self.parent_names.append(parent.name)
            else:
                self.ready = None
                self.logger.error('Unable to set_parent_names. ' +
                                  'div: {0}'.format(div))

    def parse_file_extension(self,div=None):
        '''Parse file extension content from given division tag.'''
        if self.ready:
            self.parse_file_extension_data(div=div)
            self.parse_file_extension_header(div=div)

    def parse_file_extension_data(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if div:
                # extension.hdu_number and header.title
                heading = div.find_next('h2').string
                split = heading.split(':')
                if split:
                    extension_hdu_number = int(
                                            split[0].lower().replace('hdu',''))
                    header_title =   split[1].lower()
                else:
                    self.ready = False
                    self.logger.error("Expected ':' in heading")
                
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
                hdu_data['extension_hdu_number'] = extension_hdu_number
                hdu_data['header_title']         = header_title
                hdu_data['data_is_image']        = data_is_image
                hdu_data['column_datatype']      = column_datatype
                hdu_data['column_size']          = column_size
                hdu_data['column_description']   = column_description
                self.file_extension_data.append(hdu_data)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_data. ' +
                                  'div: {0}'.format(div))

    def parse_file_extension_header(self,div=None):
        '''Parse file description content from given division tag.'''
        hdu_header = dict()
        if self.ready:
            if div:
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
                    row_data = list()
                    for data in row.find_all('td'):
                        number_descendants = self.get_number_descendants(node=data)
                        if data.string:          data_string = str(data.string)
                        elif number_descendants: data_string = str(data)
                        else:                    data_string = ''
                        row_data.append(data_string)
                    table_rows[row_order]  = row_data
                hdu_header['table_caption']  = table_caption
                hdu_header['table_keywords'] = table_keywords
                hdu_header['table_rows']     = table_rows
                self.file_extension_headers.append(hdu_header)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_header. ' +
                                  'div: {0}'.format(div))



