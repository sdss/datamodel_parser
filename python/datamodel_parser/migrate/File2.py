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

######### Same as File1

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
                    self.set_section_extension_names(section_title = dt_list[-1],
                                                 sections      = dd_list[-1])
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
                for (heading,description) in list(zip(headings,descriptions)):
                    number_descendants = self.get_number_descendants(node=
                                                                     heading)
                    if heading.string:       string = str(heading.string)
                    elif number_descendants: string = str(heading)
                    else:                    string = ''
                    self.intro_heading_titles.append(string)

                    number_descendants = self.get_number_descendants(node=
                                                                     description)
                    if description.string:   string = str(description.string)
                    elif number_descendants: string = str(description)
                    else:                    string = ''
                    self.intro_descriptions.append(string)
            else:
                self.ready = False
                self.logger.error(
                            'Unable to set_intro_table_information. ' +
                            'headings: {0}'.format(headings) +
                            'descriptions: {0}'.format(descriptions))

    def set_section_extension_names(self,section_title=None,sections=None):
        '''Get the extension names from the intro Section.'''
        self.section_extension_names = dict()
        if self.ready:
            if section_title and sections:
                section_title = str(section_title.string)
                sections = sections.find_next('ul').find_all('li')
                for section in sections:
                    print('section: %r' % section)
                    strings = section.strings
                    for string in strings:
                        print('string: %r' % string)
                        if 'HDU' in string:
                            pass
                    
                    
                input('pause')
                print('section_title: %r' % section_title)
                print('sections: %r' % sections)
                input('pause')
            else:
                self.ready = False
                self.logger.error('Unable to set_section_extension_names.' +
                                  'section_title: {}, '.format(section_title) +
                                  'sections: {}.'.format(sections))

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

