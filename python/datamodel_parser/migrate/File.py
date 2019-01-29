from bs4 import BeautifulSoup
from json import dumps
from requests import get as requests_get


class File:
    '''
        
    '''

    def __init__(self, logger=None, options=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_ready()
        self.set_attributes()

    def set_logger(self, logger=None):
        '''Set class logger.'''
        self.logger = logger if logger else None
        self.ready = bool(self.logger)
        if not self.ready: print('ERROR: Unable to set_logger.')

    def set_options(self, options=None):
        '''Set the options class attribute.'''
        self.options = None
        if self.ready:
            self.options = options if options else None
            if not self.options:
                self.ready = False
                self.logger.error('Unable to set_options')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger and
                          self.options)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.url     = self.options.url     if self.options else None

    def parse_url(self):
        self.env_variable = None
        self.location_path = None
        if self.ready:
            if self.url:
                path = self.url.replace(
                    'https://data.sdss.org/datamodel/files/','')
                split = path.split('/')
                self.env_variable = split[0]               if split else None
                self.name = split[-1]                      if split else None
                self.location_path = '/'.join(split[1:-1]) if split else None
                self.directory_names = list()
                self.directory_depths = list()
                for name in split[1:-1]:
                    self.directory_names.append(name)
                    self.directory_depths.append(self.directory_names.index(name))
                self.location_directories = {'names'  : self.directory_names,
                                             'depths' : self.directory_depths,
                                             }
#                print('self.url: %r' % self.url)
#                print('self.env_variable: %r' % self.env_variable)
#                print('self.location_path: %r' % self.location_path)
#                print('self.location_directories:\n' + dumps(self.location_directories,indent=1))
#                print('self.name: %r' % self.name)
            else:
                self.ready = False
                self.logger.error('Unable to set_env_variable. ' +
                                  'self.url: {0}'.format(self.url))

    def parse_file(self):
        '''
            Parse the HTML of the given file URL
            and disseminate it in various formats.
        '''
        if self.ready:
            self.set_html_text()
            self.set_soup()
            
            if self.soup.find('div',id='intro'):
                self.parse_description_div()
                self.parse_extensions_div()
            #
            # Information to be dissemenated into database.
            #
#            print('self.description:\n' + dumps(self.description,indent=1))
#            print('self.extension_count: %r' % self.extension_count)
#            for extension in self.extensions:
#                input('pause')
#                print('extension:\n' + dumps(extension,indent=1))
#            input('pause')

    def set_html_text(self):
        '''Set the HTML text for the given URL.'''
        self.html_text = None
        if self.ready:
            if self.url:
                request_url = requests_get(self.url) if self.url else None
                self.html_text = request_url.text if request_url else None
            else:
                self.logger.error('Unable to set_html_text. self.url: {0}'
                    .format(self.url))

    def set_soup(self):
        '''
            Set a class BeautifulSoup instance
            from the HTML text of the given URL.
        '''
        self.soup = None
        if self.ready:
            self.soup = (BeautifulSoup(self.html_text, 'html.parser')
                         if self.html_text else None)
            if not self.soup:
                self.ready = None
                self.logger.error('Unable to set_soup. self.html_text: {0}'
                                    .format(self.html_text))

    def parse_description_div(self):
        '''Parse the discription of the file.'''
        self.description = None
        if self.ready:
            if self.soup:
                intro = self.soup.find('div',id='intro') if self.soup else None
                dl = intro.dl if intro else None
                if dl:
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
            else:
                self.ready = False
                self.logger.error('Unable to parse_description_div. ' +
                                    'self.soup: {0}'.format(self.soup))

    def initialize_description(self):
        '''Initialize the columns of the description table.'''
        if self.ready:
            self.description = {
                'general_description' : '',
                'naming_convention'   : '',
                'approximate_size'    : '',
                'file_type'           : '',
                }

    def parse_extensions_div(self):
        self.extensions = list()
        if self.ready:
            if self.soup:
                another_hdu = True
                hdu_number = -1
                while another_hdu:
                    if hdu_number > 5e4:
                        self.ready = False
                        self.logger.error(
                            'Runaway while loop in parse_extensions_div')
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
                self.logger.error('Unable to parse_extensions_div. self.soup: {0}'
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

