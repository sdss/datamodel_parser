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
        self.file_extension_data   = list()
        self.file_extension_headers = list()
        if self.ready:
            if self.divs:
                for div in self.divs:
                    div_id = str(div['id'])
                    if div_id == 'intro': self.parse_file_intro(intro=div)
                    elif ('hdu' in div_id): self.parse_file_extension(div=div)
                    else:
                        self.ready = False
                        self.logger.error('Unknown div_id: {0}'.format(div_id))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. self.div_ids: {0}'
                                    .format(self.divs))

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

############

    def parse_file_intro(self,intro=None):
        '''Set the tag names and contents for the children of the given tag.'''
        if self.ready:
            # Make sure intro has children
            number_descendants = self.get_number_descendants(node=intro)
            if intro and number_descendants:
                dl = intro.find_next('dl')
                dt_list = dl.find_all('dt')
                dd_list = dl.find_all('dd')
                if len(dt_list)==len(dd_list):
                    self.set_intro_table_information(
                                                    headings     = dt_list[:-1],
                                                    descriptions = dd_list[:-1])
                    self.section_hdu_names(section_title = dt_list[-1],
                                           sections      = dd_list[-1])
                    print('self.intro_heading_orders: {}'.format(self.intro_heading_orders))
                    print('self.intro_heading_levels: %r' % self.intro_heading_levels)
                    print('self.intro_heading_titles: {}'.format(self.intro_heading_titles))
                    print('self.intro_descriptions: {}'.format(self.intro_descriptions))
                    print('self.section_extension_names: {}'.format(self.section_extension_names))
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
                         self.append_intro_heading_title(heading=heading)
                         self.append_intro_description(description=description)
                    number_headings = len(headings)
                    self.intro_heading_orders = list(range(number_headings))
                    self.intro_heading_levels = [''] * number_headings
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

    def append_intro_heading_title(self,heading=None):
        '''Append heading title to self.intro_heading_titles.'''
        if self.ready:
            if heading:
                number_descendants = self.get_number_descendants(node=heading)
                if heading.string:       string = str(heading.string)
                elif number_descendants: string = str(heading)
                else:                    string = ''
                self.intro_heading_titles.append(string)
            else:
                self.ready = False
                self.logger.error('Unable to set_intro_table_information. ' +
                                  'heading: {0}'.format(heading))

    def append_intro_description(self,description=None):
        '''Append description title to self.intro_descriptions.'''
        if self.ready:
            if description:
                number_descendants = (
                    self.get_number_descendants(node=description))
                if description.string:   string = str(description.string)
                elif number_descendants: string = str(description)
                else:                    string = ''
                self.intro_descriptions.append(string)
            else:
                self.ready = False
                self.logger.error('Unable to append_intro_description. ' +
                                  'description: {0}'.format(description))

    def section_hdu_names(self,section_title=None,sections=None):
        '''Get the extension names from the intro Section.'''
        self.section_extension_names = dict()
        if self.ready:
            if section_title and sections:
                extension_hdu_numbers = list()
                extension_hdu_names = list()
                section_title = str(section_title.string)
                sections = sections.find_next('ul').find_all('li')
                for section in sections:
                    for string in section.strings:
                        if 'hdu' in string.lower():
                            extension_hdu_number = (
                                        string.lower().replace('hdu','').strip()
                                        if string else None)
                            extension_hdu_numbers.append(extension_hdu_number)
                        elif string.strip()[0] == ':':
                            name = string.split(':')[1].strip()
                            extension_hdu_names.append(name)
                    if (extension_hdu_numbers and extension_hdu_names and
                        len(extension_hdu_numbers)==len(extension_hdu_names)):
                        self.section_extension_names = dict(zip(
                                                        extension_hdu_numbers,
                                                        extension_hdu_names))
                    else:
                        self.ready = False
                        self.logger.error(
                                'Unable to section_hdu_names.' +
                                'extension_hdu_numbers: {}'
                                    .format(extension_hdu_numbers)       +
                                'section_extension_names: {}'
                                    .format(section_extension_names)     +
                                'len(extension_hdu_numbers): {}'
                                    .format(len(extension_hdu_numbers))       +
                                'len(section_extension_names): {}'
                                    .format(len(section_extension_names)))
            else:
                self.ready = False
                self.logger.error('Unable to section_hdu_names.' +
                                  'section_title: {}, '.format(section_title) +
                                  'sections: {}.'.format(sections))

    def parse_file_extension(self,div=None):
        '''Parse file extension content from given division tag.'''
        if self.ready:
#            self.parse_file_extension_data(div=div)
            self.parse_file_extension_header(div=div)

    def parse_file_extension_header(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if div:
                self.check_valid_assumptions(div=div)
                if self.ready:
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

                    print('extension_hdu_number: %r' % extension_hdu_number)
                    print('header_title: %r' % header_title)
                    header = div.find_next('pre').string
                    self.parse_header(header=header)
            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_data. ' +
                                  'div: {0}'.format(div))

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

    def parse_header(self,header=None):
        '''Parse file description content from given header string.'''
        hdu_header = dict()
        if self.ready:
            if header:
                    print('header: %r' % header)
                    input('pause')

            else:
                self.ready = False
                self.logger.error('Unable to parse_file_extension_header. ' +
                                  'header: {0}'.format(header))


###########################################################################
################       Use for list style file intros
#####################################################################

    def parse_extensions(self):
        self.extensions = list()
        if self.ready:
            if self.soup:
                another_hdu = True
                hdu_number = -1
                while another_hdu:
                    if hdu_number > 5e4:
                        self.ready = False
                        self.logger.error(
                            'Runaway while loop in parse_extensions')
                        break
                    hdu_number += 1
                    hdu = 'hdu' + str(hdu_number)
                    div = (self.soup.find('div',id=hdu)
                            if self.soup and hdu else None)
                    if div:
                        self.set_header_title_div(div=div)
                        self.set_keywords_values_comments_div(div=div)
                        extension = {
                            'hdu_number'               :
                                hdu_number,
                            'header_title'             :
                                self.header_title,
                            'keywords_values_comments' :
                                self.keywords_values_comments
                                    }
                        self.extensions.append(extension)
                    else: another_hdu = False
                self.extension_count = len(self.extensions)
            else:
                self.ready = False
                self.logger.error('Unable to parse_extensions. self.soup: {0}'
                                    .format(self.soup))

    def set_header_title_div(self,div=None):
        '''Set the header title.'''
        self.header_title = None
        if self.ready:
            if div:
                self.header_title = (div.h2.string.split(' ')[1]
                                     if div and div.h2 and div.h2.string and
                                        div.h2.string.split(' ') and
                                        len(div.h2.string.split(' '))==2
                                     else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_header_title_div. ' +
                                    'div: {0}'.format(div))


    def set_keywords_values_comments_div(self,div=None):
        self.keywords_values_comments = list()
        '''Set keyword/value pairs with description if present.'''
        if self.ready:
            if div:
                pre = div.pre if div else None
                string = str(pre.string) if pre else None
                keyword_value_list = string.split('\n') if string else None
                if keyword_value_list:
                    for keyword_value in keyword_value_list:
                        if keyword_value:
                            split = keyword_value.split('=')
                            keyword = split[0].strip() if split else ''
                            split = (split[1].split('/')
                                     if split and len(split)>1 else None)
                            value = split[0].strip() if split else ''
                            comment = (split[1].strip()
                                       if split and len(split)>1 else '')
                            keyword_value_comment = {
                                'keyword' : keyword,
                                'value'   : value,
                                'comment' : comment,
                                                    }
                            self.keywords_values_comments.append(
                                keyword_value_comment)
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to set_title_and_keyword_columns. ' +
                        'keyword_value_list: {0}'.format(keyword_value_list))
            else:
                self.ready = False
                self.logger.error('Unable to set_title_and_keyword_columns. ' +
                                    'div: {0}'.format(div))

def set_intro_list_strings(self,intro=None):
        dl = intro.dl if intro else None
        if dl:
#            print('dl.strings: {0}'.format(dl.strings))
#            input('pause')
            self.initialize_description()
            columns = [c.replace('_',' ').title()
                       for c in self.description.keys()]
            find_value = False
            for string in dl.strings:
                if string in columns:
                    key = string.lower().replace(' ','_')
                    find_value = True
                    continue
                if find_value:
                    if string != '\n':
                        self.description[key] = string
                        find_value = False
        else:
            self.ready = None
            self.logger.error('Unable to set_description. ' +
                                'dl: {0}'.format(dl))

