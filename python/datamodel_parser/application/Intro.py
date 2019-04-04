from json import dumps
from bs4 import Tag, NavigableString
from datamodel_parser.application import Util


class Intro:
    '''Parse intro of file HTML.'''

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
        self.intro_positions = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        self.section_hdu_titles   = dict()
        if self.ready:
            if self.body:
                # process different intro types
                # self.body all div tags
                child_names = self.util.get_child_names(node=self.body)
#                print('self.body: %r'% self.body)
#                print('child_names: %r'% child_names)
#                input('pause')
                if self.util.children_all_one_tag_type(node = self.body,
                                                       tag_name = 'div'):
                    self.parse_file_div()
                else:
                    # self.body not all div tags
                    child_names = set(self.util.get_child_names(node=self.body))
                    if child_names == {'h1','p','h3','ul','pre'}:
                        self.parse_file_h1_p_h3_ul_pre()
                    elif child_names == {'h1','p','h2','table','h3','pre'}:
                        self.parse_file_h1_p_h2_table_h3_pre()
                    else:
                        self.ready = False
                        self.logger.error('Unexpected HTML body type encountered ' +
                                          'in Intro.parse_file.')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_info. ' +
                                  'self.body: {}'.format(self.body))

    def parse_file_div(self):
        '''Parse the HTML of the given BeautifulSoup div tag object.'''
        if self.ready:
            if self.body:
                # Find intro div
                for div in [div for div in self.body
                            if not self.util.get_string(node=div).isspace()]:
                    # Found intro div
                    self.intro_div = None
                    if div['id'] == 'intro':
                        self.intro_div = div
                        child_names = set(self.util.get_child_names(node=div))
                        # process different div intro types
                        if child_names == {'h1','h4','p','div'}:
                            self.parse_file_h1_h4_p_div()
                        elif child_names == {'h1','dl'}:
                            self.parse_file_h1_dl()
                        else:
                            self.ready = False
                            self.logger.error(
                                'Unexpected child_names encountered ' +
                                'in Intro.parse_file_div().')
                        break
                    if not self.intro_div:
                        self.ready = False
                        self.logger.error('Intro div tag not found.' +
                                          'self.intro_div: {}'
                                            .format(self.intro_div))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_hdu_info. ' +
                                  'self.body: {}'.format(self.body))

    def parse_file_h1_h4_p_div(self):
        '''Parse the HTML of the given BeautifulSoup div tag object with
            children: h1, h4 and p.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h1_h4_p_div()
            if self.intro_div and assumptions:
                position = -1
                for child in [child for child in self.intro_div.children
                              if not self.util.get_string(node=child).isspace()]:
                    string = self.util.get_string(node=child)
                    self.ready = self.ready and self.util.ready
                    if self.ready:
                        # file page name
                        if child.name == 'h1':
                            position += 1
                            self.intro_positions.append(position)
                            self.intro_heading_levels.append(1)
                            self.intro_heading_titles.append(string)
                            self.intro_descriptions.append('')
                        # file heading_titles
                        elif child.name == 'h4':
                            position += 1
                            self.intro_positions.append(position)
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
                                  'self.intro_div: {}'.format(self.intro_div) +
                                  'assumptions: {}'.format(assumptions))

    def verify_assumptions_parse_file_h1_h4_p_div(self):
        '''Verify assumptions made in parse_file_h1_h4_p_div.'''
        assumptions = None
        if self.intro_div:
            assumptions = True
            child_names = self.util.get_child_names(node=self.intro_div)
            repeated_h4_p = False
            for n in range(1,20):
                if child_names == ['h1'] + ['h4','p']*n + ['div']:
                    repeated_dt_dd = True
                    break
            if not repeated_dt_dd:
                assumptions = False
                self.logger.error("Invalid assumption: " +
                    "child_names == ['h1'] + ['h4','p']*n + ['div'] for some n")
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_file_h1_h4_p_div. ' +
                'self.intro_div: {}.'.format(self.intro_div))
#        print('assumptions: %r' % assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

    def parse_file_h1_dl(self):
        '''Parse the HTML of the given BeautifulSoup div tag object with
            children: h1, h4 and p.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h1_dl()
            if self.intro_div and assumptions:
                # page title
                h1 = self.intro_div.find_next('h1')
                title = self.util.get_string(node=h1)
                description = '' # no description for page title
                self.intro_heading_titles.append(title)
                self.intro_descriptions.append(description)
                
                # page intro
                dl = self.intro_div.find_next('dl')
                (titles,descriptions) = self.util.get_dts_and_dds_from_dl(dl=dl)
                # extract section list if present
                for dd in dl.find_all('dd'): pass # get last dd in dl
                child_names = self.util.get_child_names(node=dd)
                if child_names == ['ul']: # section list in last dd
                    titles.pop()          # remove section title
                    descriptions.pop()    # remove section list
                    self.parse_section(node=dd)
                self.intro_heading_titles.extend(titles)
                self.intro_descriptions.extend(descriptions)
                number_headings = len(self.intro_heading_titles)
                self.intro_positions = list(range(number_headings))
                self.intro_heading_levels = [1]
                self.intro_heading_levels.extend([4] * (number_headings - 1))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_h1_h4_p_div. ' +
                                  'self.intro_div: {}'.format(self.intro_div) +
                                  'assumptions: {}'.format(assumptions))

    def verify_assumptions_parse_file_h1_dl(self):
        '''Verify assumptions made in parse_file_h1_dl.'''
        assumptions = None
        if self.intro_div:
            assumptions = True
            child_names = self.util.get_child_names(node=self.intro_div)
            if not child_names == ['h1','dl']:
                assumptions = False
                self.logger.error("Invalid assumption: child_names == ['h1','dl']")
            # dl assumptions
            dl = self.intro_div.find_next('dl')
            child_names = self.util.get_child_names(node=dl)
            repeated_dt_dd = False
            for n in range(1,20):
                if child_names == ['dt','dd']*n:
                    repeated_dt_dd = True
                    break
            if not repeated_dt_dd:
                assumptions = False
                self.logger.error("Invalid assumption: "
                                  "repeated_dt_dd")
            for dd in dl.find_all('dd'): pass # get last dd
            child_names = self.util.get_child_names(node=dd)
            # Assume child_names == ['ul']
            if child_names == ['ul']:
                # Asume all children of the <ul> tag are <li> tags
                ul = dd.find_next('ul')
                if not self.util.children_all_one_tag_type(node=ul,tag_name='li'):
                    assumptions = False
                    self.logger.error(
                        "Invalid assumption: " +
                        "children_all_one_tag_type(node=ul,tag_name='li') == True")
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_file_h1_dl. ' +
                'self.intro_div: {}.'.format(self.intro_div))
#        print('assumptions: %r' % assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

    def parse_section(self,node=None):
        '''Get hdu names from the intro Section.'''
        if self.ready:
            if node:
                child_names = set(self.util.get_child_names(node=node))
                if child_names == {'h4','ul'}:
                    self.parse_section_h4_ul(node=node)
                elif child_names == {'ul'}:
                    self.parse_section_ul(node=node)
                else:
                    self.ready = False
                    self.logger.error('Unexpected child_names encountered ' +
                                      'Intro.in parse_file_div().')
            else:
                self.ready = False
                self.logger.error('Unable to parse_section.' +
                                  'node: {}'.format(node))

    def parse_section_h4_ul(self,node=None):
        '''Get hdu names from the intro Section.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_section_h4_ul(node=node)
            if node and assumptions:
                for string in [item for item in node.strings if item != '\n']:
                    if 'HDU' in string:
                        split = string.split(':')
                        hdu = split[0].strip() if split else None
                        hdu_number = (int(hdu.lower().replace('hdu',''))
                                      if hdu else None)
                        hdu_title   = split[1].strip() if split else None
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
                self.logger.error('Unable to parse_section_h4_ul.' +
                                  'node: {}'.format(node) +
                                  'assumptions: {}'.format(assumptions))

    def verify_assumptions_parse_section_h4_ul(self,node=None):
        '''Verify assumptions made in parse_file_h1_h4_p_div.'''
        assumptions = None
        if node:
            assumptions = True
            child_names = self.util.get_child_names(node=node)
            if not child_names == ['h4','ul']:
                assumptions = False
                self.logger.error("Invalid assumption: child_names == ['h4','ul']")
            # Asume all children of the <ul> tag are <li> tags
            ul = node.find_next('ul')
            if not self.util.children_all_one_tag_type(node=ul,tag_name='li'):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "children_all_one_tag_type(node=ul,tag_name='li') == True")
            else:
                for li in [li for li in ul.children
                           if not self.util.get_string(node=li).isspace()]:
                    for child in [child for child in li.children
                                 if not self.util.get_string(node=child).isspace()]:
                        if not child.name == 'a':
                            assumptions = False
                            self.logger.error("Invalid assumption: child.name == 'a'")
                        string = self.util.get_string(node=child)
                        if not 'HDU' in string:
                            assumptions = False
                            self.logger.error("Invalid assumption: 'HDU' in string")
                        if not ':' in string:
                            assumptions = False
                            self.logger.error("Invalid assumption: ':' in string")
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_section_h4_ul. ' +
                'node: {}.'.format(node))
#        print('assumptions: %r' % assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

    def parse_section_ul(self,node=None):
        '''Get hdu names from the intro Section.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_section_ul(node=node)
            if node and assumptions:
                hdu_hdu_titles = list()
                for li in [li for li in node.find_all('li')
                           if not self.util.get_string(node=li).isspace()]:
                    section_name = li.contents[1].replace(':','').strip()
                    hdu_hdu_titles.append(section_name)
                hdu_numbers = list(range(len(hdu_hdu_titles)))
                self.section_hdu_titles = dict(zip(hdu_numbers,hdu_hdu_titles))
            else:
                self.ready = False
                self.logger.error('Unable to parse_section_ul.' +
                                  'node: {}'.format(node) +
                                  'assumptions: {}'.format(assumptions))

    def verify_assumptions_parse_section_ul(self,node=None):
        '''Verify assumptions made in parse_file_h1_h4_p_div.'''
        assumptions = None
        if node:
            assumptions = True
            child_names = self.util.get_child_names(node=node)
            if not child_names == ['ul']:
                assumptions = False
                self.logger.error("Invalid assumption: child_names == ['ul']")
            # ul assumptions
            # Asume all children of the <ul> tag are <li> tags
            ul = node.find_next('ul') if node else None
            if not self.util.children_all_one_tag_type(node=ul,tag_name='li'):
                assumptions = False
                self.logger.error(
                        "Invalid assumption: " +
                        "children_all_one_tag_type(node=ul,tag_name='li') == True")
            # li assumptions
            # Assume the only child of each <li> tag is an <a> tag
            lis = ul.find_all('li')
            for li in lis:
                child_names = self.util.get_child_names(node=li)
                if not child_names == ['a']:
                    assumptions = False
                    self.logger.error("Invalid assumption: child_names == ['a']")
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_section_ul. ' +
                'node: {}.'.format(node))
#        print('assumptions: %r' % assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

    def parse_file_h1_p_h3_ul_pre(self):
        '''Parse the HTML of the given BeautifulSoup div tag object with
            children: h1, p, h3, ul, and pre.'''
        if self.ready:
            assumptions = self.verify_assumptions_parse_file_h1_p_h3_ul_pre()
            if self.body and assumptions:
                position = -1
                found_format_notes = False
                append_discussions = False

#                for child in [child for child in self.body.children if child != '\n']:
#                    if not child.name: print('child: %r' % child)
#                    input('pause')

                for child in [child for child in self.body.children if child != '\n']:
                    child_name = child.name if child else None
                    string = self.util.get_string(node=child)
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
                        title = self.util.get_string(node=child)
                        # page title
                        if child_name == 'h1':
                            self.intro_descriptions.append('')
                        # multiple non-nested tags
                        if 'Format notes' in title:
                            found_format_notes = True
                            title = title.replace(':','')
                        self.intro_heading_titles.append(title)
                    # intro non-heading tags containing headings and descriptions
                    elif (child_name in self.paragraph_tags or
                          child_name in self.unordered_list_tags
                        ):
                        contents = child.contents
                        for content in [content for content in contents if content != '\n']:
                            # heading content
                            if content.name in self.bold_tags:
                                position += 1
                                title = (self.util.get_string(node=content)
                                            .replace(':',''))
                                self.intro_positions.append(position)
                                self.intro_heading_levels.append(3)
                                self.intro_heading_titles.append(title)
                            # descriptions
                            else:
                                string = str(content)
                                if not append_discussions:
                                    self.intro_descriptions.append(string.strip())
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
                self.ready = False
                self.logger.error('Unable to parse_file_h1_p_h3_ul_pre. ' +
                                  'self.body: {}'.format(self.body) +
                                  'assumptions: {}'.format(assumptions))

    def verify_assumptions_parse_file_h1_p_h3_ul_pre(self,body=None):
        '''Verify assumptions made in parse_file_h1_h4_p_div.'''
        assumptions = None
        body = body if body else self.body
        if body:
            assumptions = True
            child_names = self.util.get_child_names(node=body)
            if not child_names == ['h1','p','p','p','p','p','p','h3','p',
                                   'ul','p','h3','pre','p','pre','p','pre']:
                assumptions = False
                self.logger.error("Invalid assumption: " +
                    "child_names == ['h1','p','p','p','p','p','p','h3','p'," +
                                    "'ul','p','h3','pre','p','pre','p','pre']")
        else:
            self.ready = False
            self.logger.error(
                'Unable to verify_assumptions_parse_file_h1_p_h3_ul_pre. ' +
                'body: {}.'.format(body))
#        print('assumptions: %r' % assumptions)
#        input('pause')
        if not assumptions: self.ready = False
        return assumptions

    def parse_file_h1_p_h2_table_h3_pre(self):
        '''Parse the HTML of the given BeautifulSoup div tag object with
            children: h1, p, h3, ul, and pre.'''
        if self.ready:
#            assumptions = self.verify_assumptions_parse_file_h1_p_h3_ul_pre()
            if self.body:# and assumptions:
                child_names = self.util.get_child_names(node=self.body)
                print('child_names: %r' % child_names)

                for child in child_names:
                    self.body.find_next(child)
                    if child in self.util.heading_tags:
                        hdu_titles = self.util.get_all_possible_hdu_titles()
                        print('hdu_titles: %r'% hdu_titles)
                        input('pause')

                    print('child: %r' % child)
                    input('pause')

            else:
                self.ready = False
                self.logger.error('Unable to parse_file_h1_p_h3_ul_pre. ' +
                                  'self.body: {}'.format(self.body) +
                                  'assumptions: {}'.format(assumptions))
