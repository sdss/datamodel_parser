from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.migrate import Util


class File1:
    '''
        
    '''

    def __init__(self,logger=None,options=None,body=None):
        self.initialize(logger=logger,options=options)
        self.set_divs(body=body)
        self.set_ready()
        self.set_attributes()

    def initialize(self,logger=None,options=None):
        self.util = Util(logger=logger,options=options)
        self.logger  = self.util.logger  if self.util.logger  else None
        self.options = self.util.options if self.util.options else None
        self.ready   = self.util and self.util.ready if self.util else None

    def set_divs(self,body=None):
        '''Set the divs class attribute.'''
        self.divs = None
        if self.ready:
            divs = body.children if body else None
            self.divs = [div for div in divs if div != '\n'] if divs else None
            if not self.divs:
                self.ready = False
                self.logger.error('Unable to set_divs. ' +
                                  'body: {}.'.format(body))

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.ready   and
                          self.util    and
                          self.logger  and
                          self.options and
                          self.divs)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.heading_tags        = self.util.heading_tags
            self.paragraph_tags      = self.util.paragraph_tags
            self.bold_tags           = self.util.bold_tags
            self.unordered_list_tags = self.util.unordered_list_tags

    def parse_file(self):
        '''Parse the HTML of the given division tags.'''
        if self.ready:
            if self.divs:
                # define these lists here so they're not overwritten in for loop
                self.file_hdu_info    = list()
                self.file_hdu_tables = list()
                for div in self.divs:
                    div_id = div['id']
                    if div_id == 'intro': self.parse_file_intro(intro=div)
                    elif 'hdu' in div_id: self.parse_file_hdu(div=div)
                    else:
                        self.ready = False
                        self.logger.error('Unknown div_id: {}.'.format(div_id))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. ' +
                                  'self.div_ids: {}.'.format(self.divs))

    def parse_file_intro(self,intro=None):
        '''Parse file intro table content from given tag.'''
        if self.ready:
            if intro:
                self.set_intro_tag_names_and_contents(intro=intro)
                self.set_intro_table_information()
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_intro. ' +
                                  'intro: {}.'.format(intro))

    def set_intro_tag_names_and_contents(self,intro=None):
        ''' Set the tag names and contents for the children of the given tag.'''
        self.intro_tag_names = None
        self.intro_tag_contents = None
        if self.ready:
            # Make sure intro has children
            number_descendants = self.util.get_number_descendants(node=intro)
            self.ready = self.ready and self.util.ready
            # Process intro
            if self.ready and intro and number_descendants:
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
                            self.set_section_hdu_titles(div=child)
                        else:
                            # Parse intro titles and contents
                            tag_contents = self.get_tag_contents(tag=child)
                            self.intro_tag_names.append(tag_name)
                            self.intro_tag_contents.append(tag_contents)
                    else:
                        self.ready = False
                        self.logger.error('Unexpected BeautifulSoup type. ' +
                                          'child: {}, '.format(child) +
                                          'type(child): {}.'.format(type(child)))
                self.remove_closing_division_tag(
                                        tag_names=self.intro_tag_names,
                                        tag_contents=self.intro_tag_contents)
            else:
                self.ready = False
                self.logger.error(
                            'Unable to set_intro_tag_names_and_contents. ' +
                            'intro: {}'.format(intro) +
                            'number_descendants: {}'.format(number_descendants) 
                                )

    def set_section_hdu_titles(self,div=None):
        '''Get the hdu names from the intro Section.'''
        self.section_hdu_titles = dict()
        if self.ready:
            if div:
                for string in [item for item in div.strings if item != '\n']:
                    if 'HDU' in string:
                        split = string.split(':')
                        hdu = split[0].lower().strip() if split else None
                        hdu_number = (int(hdu.replace('hdu',''))
                                      if hdu else None)
                        hdu_title   = split[1].lower().strip() if split else None
                        if hdu_number is not None and hdu_title:
                            self.section_hdu_titles[hdu_number] = hdu_title
                        else:
                            self.ready = False
                            self.logger.error(
                                    'Unable to set_section_hdu_titles.' +
                                    'hdu_number: {}'.format(hdu_number) +
                                    'hdu_title: {}'.format(hdu_title))
            else:
                self.ready = False
                self.logger.error('Unable to set_section_hdu_titles.' +
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
                            'tag_names: {}'.format(tag_names) +
                            'contents: {}'.format(contents)
                                )

    def set_intro_table_information(self):
        '''Set the heading names and descriptions for the intro table.'''
        self.intro_positions = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if self.intro_tag_names and self.intro_tag_contents:
                names = self.intro_tag_names
                contents = self.intro_tag_contents
                self.check_valid_assumptions(names=names,contents=contents)
                if self.ready:
                    position = -1
                    for (idx,name) in enumerate(names):
                        if name in self.paragraph_tags: continue
                        if name in self.heading_tags:
                            position += 1
                            self.intro_positions.append(position)
                            level = int(name.replace('h',''))
                            self.intro_heading_levels.append(level)
                            self.intro_heading_titles.append(contents[idx])
                            if names[idx+1] in self.paragraph_tags:
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
                # Check that the lists have the same length
                if len(names) != len(contents):
                    self.ready = False
                    self.logger.error(
                        'Invalid assumption: len(names) = len(contents). ' +
                        'len(names): {0}, len(contents): {1}'
                        .format(len(names),len(contents))
                                      )
                # Check that the first name is a heading tag
                if names[0] not in self.heading_tags:
                    self.ready = False
                    self.logger.error(
                        'Invalid assumption: File intro starts with a heading.')

                # Check that the names are either heading or paragraph tags
                for name in names:
                    unexpected_tag_names = list()
                    if name not in self.heading_tags and name not in self.paragraph_tags:
                        unexpected_tag_names.append(name)
                    if unexpected_tag_names:
                        self.ready = False
                        self.logger.error(
                            'Invalid assumption: ' +
                            'names are either heading or paragraph tags.' +
                            'unexpected_tag_names: {}.'
                            .format(unexpected_tag_names))
            else:
                self.ready = False
                self.logger.error(
                    'Unable to check_valid_assumptions. ' +
                    'names: {0}, contents: {1}'.format(names,contents))

    def parse_file_hdu(self,div=None):
        '''Parse file hdu content from given division tag.'''
        if self.ready:
            self.parse_file_hdu_info(div=div)
            self.parse_file_hdu(div=div)

    def parse_file_hdu_info(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if div:
                # hdu.hdu_number and header.title
                heading = div.find_next('h2').string
                split = heading.split(':')
                if split:
                    hdu_number   = int(split[0].lower().replace('hdu',''))
                    hdu_title = split[1].lower().strip()
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
                is_image = bool('image' in descriptions)
                
                hdu_info = dict()
                hdu_info['hdu_number']         = hdu_number
                hdu_info['hdu_title']       = hdu_title
                hdu_info['is_image']           = is_image
                hdu_info['column_datatype']    = column_datatype
                hdu_info['column_size']        = column_size
                hdu_info['column_description'] = column_description
                self.file_hdu_info.append(hdu_info)
                self.hdu_count = len(self.file_hdu_info)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_info. ' +
                                  'div: {}'.format(div))

    def parse_file_hdu(self,div=None):
        '''Parse file description content from given division tag.'''
        hdu = dict()
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
                    if not self.ready: break
                    row_data = list()
                    for data in row.find_all('td'):
                        string = self.util.get_string(node=data)
                        self.ready = self.ready and self.util.ready
                        if self.ready: row_data.append(string)
                        else: break
                    table_rows[row_order]  = row_data
                hdu['table_caption']  = table_caption
                hdu['table_keywords'] = table_keywords
                hdu['table_rows']     = table_rows
                self.file_hdu_tables.append(hdu)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu. ' +
                                  'div: {}'.format(div))
