from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.migrate import Util


class File2:
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
                                  'body: {}'.format(body))

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
                    div_id = str(div['id'])
                    if div_id == 'intro':   self.parse_file_intro(intro=div)
                    elif ('hdu' in div_id): self.parse_file_hdu(div=div)
                    else:
                        self.ready = False
                        self.logger.error('Unknown div_id: {}'.format(div_id))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. ' +
                                  'self.div_ids: {}'.format(self.divs))

    def parse_file_intro(self,intro=None):
        '''Set the tag names and contents for the children of the given tag.'''
        if self.ready:
            # Make sure intro has children
            number_descendants = self.util.get_number_descendants(node=intro)
            self.ready = self.ready and self.util.ready
            if self.ready and intro and number_descendants:
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
                    number_descendants = self.util.get_number_descendants(node=sections)
                    self.ready = self.ready and self.util.ready
                    if self.ready:
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
                        self.set_section_hdu_titles(section_title = section_title,
                                               sections      = sections)
                else:
                    self.ready = False
                    self.logger.error(
                                'Unable to parse_file_intro. ' +
                                'len(dt_list)!=len(dd_list). ' +
                                'len(dt_list): {}, '.format(len(dt_list)) +
                                'len(dd_list): {}, '.format(len(dd_list)))
            else:
                self.ready = False
                self.logger.error(
                            'Unable to parse_file_intro. ' +
                            'intro: {}'.format(intro) +
                            'number_descendants: {}'.format(number_descendants)
                                )

    def set_intro_table_information(self,headings=None,descriptions=None):
        '''Set file introduction headings and descriptions.'''
        self.intro_positions = list()
        self.intro_heading_levels = list() # Not used for this template
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if headings and descriptions:
                if len(headings)==len(descriptions):
                    for (heading,description) in list(zip(headings,descriptions)):
                        heading_title = (self.util.get_string(node=heading)
                                         if heading else '')
                        self.ready = self.ready and self.util.ready
                        intro_description = (self.util.get_string(node=description)
                                             if description else '')
                        self.ready = self.ready and self.util.ready
                        if self.ready:
                            self.intro_heading_titles.append(heading_title)
                            self.intro_descriptions.append(intro_description)
                        else: break
                    if self.ready:
                        number_headings = len(headings)
                        self.intro_positions = list(range(number_headings))
                        self.intro_heading_levels = [1]
                        self.intro_heading_levels.extend([4] * (number_headings - 1))
                else:
                    self.ready = False
                    self.logger.error(
                                'Unable to set_intro_table_information. ' +
                                'len(headings)!=len(descriptions). '      +
                                'len(headings): {}, '.format(len(headings))          +
                                'len(descriptions): {}.'.format(len(descriptions)))

            else:
                self.ready = False
                self.logger.error(
                            'Unable to set_intro_table_information. ' +
                            'headings: {}'.format(headings) +
                            'descriptions: {}'.format(descriptions))

    def set_section_hdu_titles(self,section_title=None,sections=None):
        '''Get the hdu names from the intro Section.'''
        self.section_hdu_titles = dict() # if no section this stays empty
        if self.ready:
            if section_title and sections:
                hdu_numbers = list()
                hdu_hdu_titles = list()
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
                            hdu_hdu_titles.append(name)
                    if (hdu_numbers and hdu_hdu_titles and
                        len(hdu_numbers)==len(hdu_hdu_titles)):
                        self.section_hdu_titles = dict(zip(hdu_numbers,
                                                          hdu_hdu_titles))
                    else:
                        self.ready = False
                        self.logger.error(
                                'Unable to set_section_hdu_titles.'      +
                                'hdu_numbers: {}'
                                    .format(hdu_numbers)      +
                                'section_hdu_titles: {}'
                                    .format(section_hdu_titles)          +
                                'len(hdu_numbers): {}'
                                    .format(len(hdu_numbers)) +
                                'len(section_hdu_titles): {}'
                                    .format(len(section_hdu_titles)))
            else: pass # Do nothing, it is possible to not have a section list


    def parse_file_hdu(self,div=None):
        '''Parse file hdu content from given division tag.'''
        if self.ready:
            self.parse_file_hdu_info(div=div)
            self.parse_file_hdu(div=div)

    def parse_file_hdu_info(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if div:
                self.check_valid_assumptions(div=div)
                if self.ready:
                    # hdu.hdu_number and header.title
                    heading = div.find_next('h2').string
                    split = heading.split(':') if heading else None
                    if split:
                        hdu_number   = int(split[0].lower().replace('hdu',''))
                        hdu_title = split[1].lower().strip()
                    else:
                        self.ready = False
                        self.logger.error("Expected ':' in heading." +
                                          'heading: {}'.format(heading))
                    # data.is_image
                    header = div.find_next('pre').string
                    rows = header.split('\n') if header else list()
                    rows = [row for row in rows
                            if row and 'XTENSION' in row and 'IMAGE' in row]
                    is_image = bool(rows)
                    hdu_info = dict()
                    hdu_info['hdu_number']         = hdu_number
                    hdu_info['hdu_title']       = hdu_title
                    hdu_info['is_image']           = is_image
                    hdu_info['column_datatype']    = None
                    hdu_info['column_size']        = None
                    hdu_info['column_description'] = None
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
                self.check_valid_assumptions(div=div)
                if self.ready:
                    # table caption
                    table_caption = None
                    # table column headers
                    table_column_names = ['Key','Value','Type','Comment']
                    # table values
                    table_rows = dict()
                    header = div.find_next('pre').string
                    rows = header.split('\n') if header else list()
                    rows = [row for row in rows if row]
                    if rows:
                        for (position,row) in enumerate(rows):
                            self.set_row_data(row=row)
                            table_rows[position] = (self.row_data
                                                     if self.row_data else None)
                        hdu['table_caption']  = table_caption
                        hdu['table_column_names'] = table_column_names
                        hdu['table_rows']     = table_rows
                        self.file_hdu_tables.append(hdu)
                    else:
                        self.ready = False
                        self.logger.error(
                                    'Unable to parse_file_hdu. ' +
                                    'rows: {}'.format(rows))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu. ' +
                                  'header: {}'.format(header))

    def check_valid_assumptions(self,div=None):
        '''Verify that all of my assumptions are valid'''
        if self.ready:
            if div:
                child_names = self.util.get_child_names(node=div)
                self.ready = self.ready and self.util.ready
                if not (self.ready and bool('h2' and 'pre' in child_names)):
                    self.ready = None
                    self.logger.error("Invalid assumption that " +
                                      "child_names = ['h2','pre']" +
                                      'However, child_names: {}'
                                        .format(child_names))
            else:
                self.ready = False
                self.logger.error('Unable to check_valid_assumptions. ' +
                                  'div: {}.'.format(div))

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
                if value_comment and ' /' in value_comment:
                    split = value_comment.split(' /')
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
