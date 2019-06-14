from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.application import Util
from datamodel_parser.application.Type import Intro_type
from re import search, compile, match


class Intro:
    '''Parse intro of file HTML.'''

    def __init__(self,logger=None,options=None,body=None):
        self.initialize(logger=logger,options=options)
        self.set_body(body=body)
        self.set_ready()
        self.set_attributes()

    def initialize(self,logger=None,options=None):
        '''Initialize utility class, logger, and command line options.'''
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
            self.heading_tags        = self.util.heading_tag_names
            self.paragraph_tags      = self.util.paragraph_tags
            self.bold_tags           = self.util.bold_tags
            self.unordered_list_tags = self.util.unordered_list_tags
            self.intro_positions      = list()
            self.intro_heading_levels = list()
            self.intro_heading_titles = list()
            self.intro_descriptions   = list()
            self.intro_type = None

    def parse_file(self,node=None):
        '''Parse the HTML of the given BeautifulSoup object.'''
        if self.ready:
            if node:
                type = Intro_type(logger=self.logger,options=self.options)
                self.intro_type = type.get_intro_type(node=node)
                
#                print('node: %r'% node)
#                print('self.intro_type: %r'% self.intro_type)
#                input('pause')

                if self.intro_type:
                    if   self.intro_type == 1: self.parse_file_type_1(node=node)
                    elif self.intro_type == 2: self.parse_file_type_2(node=node)
                    elif self.intro_type == 3: self.parse_file_type_3(node=node)
                    elif self.intro_type == 4: self.parse_file_type_4(node=node)
                    elif self.intro_type == 5: self.parse_file_type_5(node=node)
                    elif self.intro_type == 6: self.parse_file_type_6(node=node)
                    elif self.intro_type == 7: self.parse_file_type_7(node=node)
                    elif self.intro_type == 8: self.parse_file_type_8(node=node)
                    elif self.intro_type == 9: self.parse_file_type_9(node=node)
                    else:
                        self.ready = False
                        self.logger.error(
                            'Unexpected self.intro_type encountered ' +
                            'in Intro.parse_file_intro_div().')

#                    print('self.intro_positions: {}'.format(self.intro_positions))
#                    print('self.intro_heading_levels: %r' % self.intro_heading_levels)
#                    print('self.intro_heading_titles: {}'.format(self.intro_heading_titles))
#                    print('self.intro_descriptions: {}'.format(self.intro_descriptions))
#                    print('self.ready: {}'.format(self.ready))
#                    input('pause')

                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file. ' +
                                      'self.intro_type: {}'.format(self.intro_type))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. ' +
                                  'node: {}.'.format(node))

    def parse_file_type_1(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                first_heading = True
                description = str()
                for child in self.util.get_children(node=node):
                    string = self.util.get_string(node=child)
                    # self.intro_heading_levels
                    # self.intro_heading_titles
                    if child.name in self.heading_tags:
                        digit = self.util.get_single_digit(string=child.name)
                        heading_level = digit if digit else 4
                        self.intro_heading_levels.append(heading_level)
                        self.intro_heading_titles.append(string)
                        if first_heading:
                            first_heading = False
                            description = str() # no description for page title
                            self.intro_descriptions.append(description)
                    # self.intro_descriptions
                    elif child.name == 'p':
                        description += string
                        next_sibling = self.util.get_sibling_names(node=child)[0]
                        if next_sibling not in self.paragraph_tags:
                            self.intro_descriptions.append(description)
                            description = str()
                        else:
                            description += '\n'
                    # file table of contents
                    elif child.name == 'div':
                        pass # don't do this anymore
#                        self.parse_section(node=child)
                    else:
                        self.ready = False
                        self.logger.error('Unexpected tag name. ' +
                                          'child.name: {} '.format(child.name) )
                # self.intro_positions,
                self.intro_positions = list(range(len(self.intro_heading_titles)))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_1. ' +
                                  'node: {}'.format(node))

    def parse_file_type_2(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # page title
                heading_tag_name = self.util.get_heading_tag_child_names(node=node)[0]
                h = node.find(heading_tag_name)
                title = self.util.get_string(node=h)
                description = str() # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                dl = node.find('dl')
                (titles,descriptions) = self.util.get_dts_and_dds_from_dl(dl=dl)
                if titles[-1].lower() == 'sections': titles.pop()
                assert(len(titles)==len(descriptions))
                
                # check if errors have occurred
                self.ready = self.ready and self.util.ready

                # put it all together
                if self.ready:
                    self.intro_heading_titles.extend(titles)
                    self.intro_descriptions.extend(descriptions)
                    number_headings = len(self.intro_heading_titles)
                    self.intro_positions = list(range(number_headings))
                    self.intro_heading_levels = [1]
                    self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_2. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_3(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # page title
                heading_tag_name = self.util.get_heading_tag_child_names(node=node)[0]
                h = node.find(heading_tag_name)
                title = self.util.get_string(node=h)
                description = str() # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                dl = node.find('dl')
                (titles,descriptions) = self.util.get_dts_and_dds_from_dl(dl=dl)
                if (titles[-1].lower() == 'sections' or
                    titles[-1].lower() == 'file contents'
                    ):
                    titles.pop()          # remove section title
                    descriptions.pop()    # remove section list
                assert(len(titles)==len(descriptions))

                # check if errors have occurred
                self.ready = self.ready and self.util.ready

                # put it all together
                if self.ready:
                    self.intro_heading_titles.extend(titles)
                    self.intro_descriptions.extend(descriptions)
                    number_headings = len(self.intro_heading_titles)
                    self.intro_positions = list(range(number_headings))
                    self.intro_heading_levels = [1]
                    self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_3. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_4(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # page title
                heading_tag_name = self.util.get_heading_tag_child_names(node=node)[0]
                h = node.find(heading_tag_name) if heading_tag_name else None
                title = self.util.get_string(node=h) if h else str()
                description = str() # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                (titles,descriptions) = (
                    self.util.get_titles_and_descriptions_from_ps_1(node=node))
                
                # check if errors have occurred
                self.ready = self.ready and self.util.ready
                
                # put it all together
                if self.ready:
                    self.intro_heading_titles.extend(titles)
                    self.intro_descriptions.extend(descriptions)
                    number_headings = len(self.intro_heading_titles)
                    self.intro_positions = list(range(number_headings))
                    self.intro_heading_levels = [1]
                    self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_4. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_5(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                self.ready = False
                self.logger.error('Under construction.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_5. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_6(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # page title
                heading_tag_name = self.util.get_heading_tag_child_names(node=node)[0]
                h = node.find(heading_tag_name) if heading_tag_name else None
                title = self.util.get_string(node=h) if h else str()
                description = str() # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                (titles,descriptions) = (
                    self.util.get_titles_and_descriptions_from_ps_2(node=node,sibling_tag_name='ul'))
                    
                # check if errors have occurred
                self.ready = self.ready and self.util.ready
                
                # put it all together
                if self.ready:
                    self.intro_heading_titles.extend(titles)
                    self.intro_descriptions.extend(descriptions)
                    number_headings = len(self.intro_heading_titles)
                    self.intro_positions = list(range(number_headings))
                    self.intro_heading_levels = [1]
                    self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_6. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_7(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # this file type just consists of a string with no tags
                strings = node.strings if node else list()
                string = ' '.join(strings).strip() if strings else str()
            
                self.intro_positions      = [1]
                self.intro_heading_levels = [1]
                self.intro_heading_titles = [' ']
                self.intro_descriptions   = [string]
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_7. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_8(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # page title
                heading_tag_name = self.util.get_heading_tag_child_names(node=node)[0]
                h = node.find(heading_tag_name) if heading_tag_name else None
                title = self.util.get_string(node=h) if h else str()
                description = str() # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                table = node.find('table')
                if table:
                    # ps before File Contents table
                    previous_siblings = [s for s in table.previous_siblings
                                        if str(s) and not str(s).isspace()]
                    soup = self.util.get_soup_from_iterator(iterator=previous_siblings,
                                                       reverse=True)
                    (titles,descriptions) = (
                        self.util.get_titles_and_descriptions_from_ps_1(node=soup))
                    self.intro_heading_titles.extend(titles)
                    self.intro_descriptions.extend(descriptions)

                    # ps after File Contents table (Notes)
                    # remove FITS Header Keywords heading if present
                    header_keywords_string = str()
                    next_siblings = [s for s in table.next_siblings if s.name]
                    if next_siblings:
                        last_sibling = next_siblings[-1]
                        if last_sibling.name in self.util.heading_tag_names:
                            regex = '(?i)\s*FITS Header Keywords\s*'
                            header_keywords_string = str(last_sibling.string)
                            if self.util.check_match(regex=regex,string=header_keywords_string):
                                next_siblings.pop()
                    soup = self.util.get_soup_from_iterator(iterator=next_siblings)

                    # check for heading tag with Note or Notes
                    heading_tag_names = self.util.get_heading_tag_child_names(node=soup)
                    h = (soup.find(heading_tag_names[0])
                         if heading_tag_names and len(heading_tag_names) == 1 else None)
                    title = self.util.get_string(node=h) if h else str()
                    if title:
                        regex = '(?i)\s*Note\s*' + '|' '(?i)\s*Notes\s*'
                        if self.util.check_match(regex=regex,string=title):
                            ps = soup.find_all('p')
                            if ps:
                                descriptions = [self.util.get_string(node=p) for p in ps
                                                if str(p) and not str(p).isspace()]
                                description = '\n\n'.join(descriptions)
                                self.intro_heading_titles.append(title)
                                self.intro_descriptions.append(description)
                            else:
                                self.ready = False
                                self.logger.error('Unable to parse_file_type_8. ' +
                                                  'Anticipated <p> tags. ' +
                                                  'ps: {}'.format(ps))
                        else:
                            self.ready = False
                            self.logger.error('Unable to parse_file_type_8. ' +
                                              'Anticipated Note or Notes in title. ' +
                                              'title: {}'.format(title))
                    # get Note or Notes from ps
                    else:
                        (titles,descriptions) = (
                            self.util.get_titles_and_descriptions_from_ps_1(node=soup))
                        if titles:
                            if len(titles) > 1:
                                regex = '(?i)\s*Note\s*' + '|' '(?i)\s*Notes\s*'
                                if (self.util.check_match(regex=regex,string=titles[0])
                                    and not [t for t in titles[1:] if t]
                                    ):
                                    title = titles[0]
                                    description = '\n\n'.join(descriptions)
                                    self.intro_heading_titles.append(title)
                                    self.intro_descriptions.append(description)
                                else:
                                    self.ready = False
                                    self.logger.error('Unable to parse_file_type_8. ' +
                                                      'Anticipated one Note title ' +
                                                      'and multiple <p> tags ' +
                                                      'soup: {}'.format(soup))
                            else:
                                title = titles[0]
                                description = descriptions[0]
                                self.intro_heading_titles.append(title)
                                self.intro_descriptions.append(description)
                    if header_keywords_string:
                        self.intro_heading_titles.append(header_keywords_string.strip())
                        self.intro_descriptions.append(str())


                else:
                    self.ready = False
                    self.logger.error('Unable to parse_file_type_8. ' +
                                      'Expected table. ' +
                                      'table: {}.'.format(table)
                                      )

                # check if errors have occurred
                self.ready = self.ready and self.util.ready
                
                # put it all together
                if self.ready:
                    # Already done above
#                    self.intro_heading_titles.extend(titles)
#                    self.intro_descriptions.extend(descriptions)
                    number_headings = len(self.intro_heading_titles)
                    self.intro_positions = list(range(number_headings))
                    self.intro_heading_levels = [1]
                    self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_8. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_9(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # page title
                heading_tag_name = self.util.get_heading_tag_child_names(node=node)[0]
                h = node.find(heading_tag_name) if heading_tag_name else None
                title = self.util.get_string(node=h) if h else str()
                description = str() # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                (titles,descriptions) = self.util.get_titles_and_descriptions_1(node=node)
                
                # check if errors have occurred
                self.ready = self.ready and self.util.ready
                
                # put it all together
                if self.ready:
                    self.intro_heading_titles.extend(titles)
                    self.intro_descriptions.extend(descriptions)
                    number_headings = len(self.intro_heading_titles)
                    self.intro_positions = list(range(number_headings))
                    self.intro_heading_levels = [1]
                    self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_9. ' +
                                  'node: {}'.format(node) )

    def parse_file_type_10(self,node=None):
        '''Parse the HTML of the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # page title
                heading_tag_name = self.util.get_heading_tag_child_names(node=node)[0]
                h = node.find(heading_tag_name) if heading_tag_name else None
                title = self.util.get_string(node=h) if h else str()
                description = str() # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                (titles,descriptions) = (
                    self.util.get_titles_and_descriptions_from_ps_2(node=node,sibling_tag_name='pre'))
                # check if errors have occurred
                self.ready = self.ready and self.util.ready
                
                # put it all together
                if self.ready:
                    self.intro_heading_titles.extend(titles)
                    self.intro_descriptions.extend(descriptions)
                    number_headings = len(self.intro_heading_titles)
                    self.intro_positions = list(range(number_headings))
                    self.intro_heading_levels = [1]
                    self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_type_10. ' +
                                  'node: {}'.format(node) )

