from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.migrate import Util


class Intro:
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
        self.intro_heading_orders = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        self.section_hdu_names    = dict()
        if self.ready:
            if self.body:
                # process different intro types
                # body all div tags
                if self.util.children_all_one_tag_type(node = self.body,
                                                       tag_name = 'div'):
                    self.parse_file_div()
                else:
                    self.ready = False
                    self.logger.error('Unexpected intro type encountered ' +
                                      'in parse_file.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_data. ' +
                                  'self.body: {0}'.format(self.body))

    def parse_file_div(self):
        '''Parse the HTML of the given BeautifulSoup div tag object.'''
        if self.ready:
            if self.body:
                # Find intro div
                for div in [div for div in self.body
                            if not self.util.get_string(node=div).isspace()
                            and self.util.ready]:
                    # Found intro div
                    self.intro_div = None
                    if div['id'] == 'intro':
                        self.intro_div = div
                        child_names = set(self.util.get_child_names(node=div))
                        
#                        print('child_names: %r' % child_names)
#                        input('pause')

                        
                        # process different div intro types
                        if child_names == {'h1', 'h4', 'p','div'}:
                            self.parse_file_h1_h4_p_div()
                        elif child_names == {'h1','dl'}:
                            self.parse_file_h1_dl()
                        else:
                            self.ready = False
                            self.logger.error(
                                'Unexpected child_names encountered ' +
                                'in parse_file_div.')
                        break
                    if not self.intro_div:
                        self.ready = False
                        self.logger.error('Intro div tag not found.' +
                                          'self.intro_div: {0}'
                                            .format(self.intro_div))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_data. ' +
                                  'self.body: {0}'.format(self.body))

    def parse_file_h1_h4_p_div(self):
        '''Parse the HTML of the given BeautifulSoup div tag object with
            children: h1, h4 and p.'''
        if self.ready:
            if self.intro_div and self.verify_assumptions_parse_file_h1_h4_p_div():
                heading_order = -1
                for child in [child for child in self.intro_div.children
                              if not self.util.get_string(node=child).isspace()
                              and self.util.ready]:
                    string = self.util.get_string(node=child)
                    self.ready = self.ready and self.util.ready
                    if self.ready:
                        # file page name
                        if child.name == 'h1':
                            heading_order += 1
                            self.intro_heading_orders.append(heading_order)
                            self.intro_heading_levels.append(1)
                            self.intro_heading_titles.append(string)
                            self.intro_descriptions.append('')
                        # file heading_titles
                        elif child.name == 'h4':
                            heading_order += 1
                            self.intro_heading_orders.append(heading_order)
                            self.intro_heading_levels.append(4)
                            self.intro_heading_titles.append(string)
                        # file heading descriptions
                        elif child.name == 'p':
                            self.intro_descriptions.append(string)
                        # file table of contents
                        elif child.name == 'div':
                            self.parse_section(node=child)
                        else:
                            self.ready = False
                            self.logger.error(
                                    'Unexpected tag name. ' +
                                    'child.name: {} '.format(child.name) +
                                    "must be in {'h1','h4','p','div'}")
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_h1_h4_p_div. ' +
                                  'self.intro_div: {0}'.format(self.intro_div))

    def verify_assumptions_parse_file_h1_h4_p_div(self):
        '''Verify assumptions made in parse_file_h1_h4_p_div.'''
        assumptions = True
        child_names = self.util.get_child_names(node=self.intro_div)
        # Assume child_names.count('h1') == 1
        if child_names.count('h1') != 1:
            assumptions = False
            self.logger.error("Invalid assumption: child_names.count('h1') == 1")
        # Assume child_names.count('div') == 1
        if child_names.count('div') != 1:
            assumptions = False
            self.logger.error("Invalid assumption: child_names.count('div') == 1")
        # Assume child_names[0] == 'h1'
        if child_names[0] != 'h1':
            assumptions = False
            self.logger.error("Invalid assumption: child_names[0] == 'h1'")
        # Assume child_names[-1] == 'div'
        if child_names[-1] != 'div':
            assumptions = False
            self.logger.error("Invalid assumption: child_names[-1] == 'div'")
        # Assume (h4,p) pairs, i.e., length is even
        if not (len(child_names) % 2) == 0:
            assumptions = False
            self.logger.error("Invalid assumption: len(child_names) is even")
        else:
            for i in range( (len(child_names) - 2)//2):
                child_names.remove('h4')
                child_names.remove('p')
            # Assume child_names=['h1'] + ['h4', 'p']*n + ['div'] for some n
            if child_names != ['h1','div']:
                assumptions = False
                self.logger.error(
                    "Invalid assumption: " +
                    "child_names=['h1'] + ['h4', 'p']*n + ['div'] for some n")
        if not assumptions: self.ready = False
        return assumptions

    def parse_section(self,node=None):
        '''Get extension names from the intro Section.'''
        if self.ready:
            if node:
                child_names = set(self.util.get_child_names(node=node))
                if child_names == {'h4','ul'}:
                    self.parse_section_h4_ul(node=node)
                else:
                    self.ready = False
                    self.logger.error('Unexpected child_names encountered ' +
                                      'in parse_file_div.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_section.' +
                                  'node: {}'.format(node))

    def parse_section_h4_ul(self,node=None):
        '''Get extension names from the intro Section.'''
        if self.ready:
            if node and self.verify_assumptions_parse_section_h4_ul(node=node):
                for string in [item for item in node.strings if item != '\n']:
                    if 'HDU' in string:
                        split = string.split(':')
                        extension = split[0].lower().strip() if split else None
                        hdu_number = (int(extension.replace('hdu',''))
                                      if extension else None)
                        hdu_name   = split[1].lower().strip() if split else None
                        if hdu_number is not None and hdu_name:
                            self.section_hdu_names[hdu_number] = hdu_name
                        else:
                            self.ready = False
                            self.logger.error(
                                    'Unable to set_section_hdu_names.' +
                                    'hdu_number: {}'.format(hdu_number) +
                                    'hdu_name: {}'.format(hdu_name))
            else:
                self.ready = False
                self.logger.error('Unable to parse_section_h4_ul.' +
                                  'node: {}'.format(node))

    def verify_assumptions_parse_section_h4_ul(self,node=None):
        '''Verify assumptions made in parse_file_h1_h4_p_div.'''
        assumptions = True
        child_names = self.util.get_child_names(node=node)
        # Assume child_names.count('h4') == 1
        if child_names.count('h4') != 1:
            assumptions = False
            self.logger.error("Invalid assumption: child_names.count('h4') == 1")
        # Assume child_names.count('ul') == 1
        if child_names.count('ul') != 1:
            assumptions = False
            self.logger.error("Invalid assumption: child_names.count('ul') == 1")
        # Assume child_names[0] == 'h4'
        if child_names[0] != 'h4':
            assumptions = False
            self.logger.error("Invalid assumption: child_names[0] == 'h4'")
        # Assume child_names[-1] == 'ul'
        if child_names[-1] != 'ul':
            assumptions = False
            self.logger.error("Invalid assumption: child_names[-1] == 'ul'")
        # Asume all children of the <ul> tag are <li> tags
        ul = node.find_next('ul')
        if not self.util.children_all_one_tag_type(node=ul,tag_name='li'):
            assumptions = False
            self.logger.error(
                    "Invalid assumption: " +
                    "children_all_one_tag_type(node=ul,tag_name='li') == True")
        else:
            for li in [li for li in ul.children
                       if not self.util.get_string(node=li).isspace()
                       and self.util.ready]:
                for child in [child for child in li.children
                             if not self.util.get_string(node=child).isspace()
                             and self.util.ready]:
                    if child.name != 'a':
                        assumptions = False
                        self.logger.error("Invalid assumption: child.name == 'a'")
                    string = self.util.get_string(node=child)
                    if 'HDU' not in string:
                        assumptions = False
                        self.logger.error("Invalid assumption: 'HDU' in string")
                    if ':' not in string:
                        assumptions = False
                        self.logger.error("Invalid assumption: ':' in string")
        if not assumptions: self.ready = False
        return assumptions

    def parse_file_h1_dl(self):
        '''Parse the HTML of the given BeautifulSoup div tag object with
            children: h1, h4 and p.'''
        if self.ready:
            if self.intro_div and self.verify_assumptions_parse_file_h1_dl():
                headings = list()
                descriptions = list()
                
                # page title
                h1 = self.intro_div.find_next('h1')
                heading_title = self.util.get_string(node=h1).lower()
                intro_description = ''
                headings.append(heading)
                descriptions.append('')
                self.intro_heading_titles.append(heading_title)
                self.intro_descriptions.append(intro_description)
                
                # page intro
                dl = self.intro_div.find_next('dl')
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
                        self.set_section_hdu_names(section_title = section_title,
                                               sections      = sections)

    def verify_assumptions_parse_file_h1_dl(self):
        '''Verify assumptions made in parse_file_h1_dl.'''
        assumptions = True
        child_names = self.util.get_child_names(node=self.intro_div)
        # Assume child_names.count('h1') == 1
        if child_names.count('h1') != 1:
            assumptions = False
            self.logger.error("Invalid assumption: child_names.count('h1') == 1")
        # Assume child_names.count('dl') == 1
        if child_names.count('dl') != 1:
            assumptions = False
            self.logger.error("Invalid assumption: child_names.count('dl') == 1")
        # dl assumptions
        dl = self.intro_div.find_next('dl')
        child_names = self.util.get_child_names(node=dl)
        # Assume child_names == ['dt','dd']*4 or child_names == ['dt','dd']*5
        if not (child_names != ['dt','dd']*4 or child_names != ['dt','dd']*5):
            assumptions = False
            self.logger.error("Invalid assumption: "
                "child_names == ['dt','dd']*4 or child_names == ['dt','dd']*5")
        else:
            if child_names == ['dt','dd']*5:
                for dd in dl.find_all('dd'): pass # get last dd
                child_names = self.util.get_child_names(node=dd)
                # Assume child_names == ['ul']
                if child_names != ['ul']:
                    assumptions = False
                    self.logger.error("Invalid assumption: child_names.count('h1') == ['ul']")
                else:
                    # Asume all children of the <ul> tag are <li> tags
                    ul = dd.find_next('ul')
                    if not self.util.children_all_one_tag_type(node=ul,tag_name='li'):
                        assumptions = False
                        self.logger.error(
                                "Invalid assumption: " +
                                "children_all_one_tag_type(node=ul,tag_name='li') == True")
#        print('assumptions: %r' % assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

