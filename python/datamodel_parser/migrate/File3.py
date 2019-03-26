from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.migrate import Util


class File3:
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
        '''Parse the HTML of the given division tags.'''
        self.file_hdu_info    = list()
        self.file_hdu_tables = list()
        if self.ready:
            if self.body:
                self.parse_file_intro()
                self.parse_file_hdu_tables()
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. self.body: {}'
                                    .format(self.body))

    def parse_file_intro(self):
        '''Parse file intro content from given body tag.'''
        self.intro_positions = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if self.body and self.body.children:
                position = -1
                found_format_notes = False
                append_discussions = False
                for child in self.body.children:
                    child_name = child.name if child else None
                    string = self.util.get_string(node=child)
                    self.ready = self.ready and self.util.ready
                    if self.ready and child_name: # skip child = '\n'
                        # found hdu tags
                        if (child_name in self.heading_tags and 'HDU' in string):
                            break
                        # intro heading tags
                        elif child_name in self.heading_tags:
                            # page title
                            position += 1
                            self.intro_positions.append(position)
                            level = int(child_name.replace('h',''))
                            self.intro_heading_levels.append(level)
                            title = self.util.get_string(node=child).replace(':','')
                            self.ready = self.ready and self.util.ready
                            if self.ready:
                                self.intro_heading_titles.append(title)
                                # page title
                                if child_name == 'h1':
                                    self.intro_descriptions.append('')
                                # multiple non-nested tags
                                if title == 'Format notes':
                                    found_format_notes = True
                            else: break
                        # intro non-heading tags containing headings and descriptions
                        elif (child_name in self.paragraph_tags or
                              child_name in self.unordered_list_tags
                            ):
                            contents = child.contents
                            for content in contents:
                                title = (self.util.get_string(node=content)
                                            .replace(':',''))
                                self.ready = self.ready and self.util.ready
                                if self.ready and not title.isspace():  # skip '\n'
                                    # heading content
                                    if content.name in self.bold_tags:
                                        position += 1
                                        self.intro_positions.append(position)
                                        self.intro_heading_levels.append(3)
                                        self.intro_heading_titles.append(title)
                                    # descriptions
                                    else:
                                        string = self.util.get_string(node=content)
                                        self.ready = self.ready and self.util.ready
                                        if self.ready and string:
                                            if not append_discussions:
                                                self.intro_descriptions.append(string)
                                            else:
                                                self.intro_descriptions[-1] += ' ' + string
                                            if found_format_notes:
                                                append_discussions = True
                                        else: break
                        else:
                            self.ready = False
                            self.logger.error('Unable to parse_file_intro. ' +
                                              'Unexpected tag type: {}'
                                                .format(child_name))
                            break
            else:
                self.ready = None
                self.logger.error('Unable to parse_file_intro. ' +
                                  'self.body: {}'.format(self.body) +
                                  'self.body.children: {}'
                                    .format(self.body.children))

    def parse_file_hdu_tables(self):
        '''Parse file hdu content from given body tag.'''
        self.section_hdu_titles = dict() # if no section this stays empty
        if self.ready:
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
                        self.parse_file_hdu(header=header)
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
                                  'hdu_title: {}'.format(hdu_title) +
                                  'header: {}'.format(header))

    def parse_file_hdu(self,header=None):
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
                                'Unable to parse_file_hdu. ' +
                                'rows: {}'.format(rows))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu. ' +
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
