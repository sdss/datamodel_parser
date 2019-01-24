from bs4 import BeautifulSoup
from json import dumps
from requests import get as requests_get


class Page:
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

    def parse_page(self):
        '''
            Parse the HTML of the given URL
            and disseminate it in various formats.
        '''
        if self.ready:
            self.set_html_text()
            self.set_soup()
            self.parse_description()
            self.parse_extensions()

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

    def parse_description(self):
        '''Parse the discription of the page and dessimenate the information.'''
        self.set_description_columns()
        self.populate_description_table()
#        print('self.description_columns:\n' + dumps(self.description_columns,indent=1))
#        input('pause')

    def set_description_columns(self):
        '''Set the columns of the description table.'''
        if self.ready:
            if self.soup:
                intro = self.soup.find('div',id='intro') if self.soup else None
                dl = intro.dl if intro else None
                if dl:
                    self.initialize_description_columns()
                    columns = [c.replace('_',' ').title()
                               for c in self.description_columns.keys()]
                    find_value = False
                    for string in dl.strings:
                        if string in columns:
                            key = string.lower().replace(' ','_')
                            find_value = True
                            continue
                        if find_value:
                            if string != '\n':
                                self.description_columns[key] = string
                                find_value = False
                else:
                    self.ready = None
                    self.logger.error('Unable to set_description_columns. ' +
                                        'dl: {0}'.format(dl))
            else:
                self.ready = False
                self.logger.error('Unable to set_description_columns. ' +
                                    'self.soup: {0}'.format(self.soup))

    def initialize_description_columns(self):
        '''Initialize the columns of the description table.'''
        self.description_columns = None
        if self.ready:
            self.description_columns = {
                'general_description' : '',
                'naming_convention'   : '',
                'approximate_size'    : '',
                'file_type'           : '',
                }

    def populate_description_table(self):
        '''Update/Create description table row.'''
        print('self.description_columns:\n' +
                dumps(self.description_columns,indent=1))
#        if self.ready:
#            self.set_description()
#            if self.description: self.update_row()
#            else:                self.create_row()

    def parse_extensions(self):
        '''Parse the extensions of the page and dessimenate the information.'''
        self.set_extensions()

    def set_extensions(self):
        '''Set the columns of the extension table.'''
        self.extensions = list()
        if self.ready:
            if self.soup:
                another_hdu = True
                self.hdu_number = -1
                while another_hdu:
                    if self.hdu_number > 5e4:
                        self.ready = False
                        self.logger.error(
                            'Runaway while loop in parse_extensions')
                        break
                    self.hdu_number += 1
                    hdu = 'hdu' + str(self.hdu_number)
                    div = (self.soup.find('div',id=hdu)
                            if self.soup and hdu else None)
                    if div: self.set_title_and_keyword_columns(div=div)
                    else:   another_hdu = False
            else:
                self.ready = False
                self.logger.error('Unable to set_extensions. self.soup: {0}'
                                    .format(self.soup))
                    
    def set_title_and_keyword_columns(self,div=None):
        self.header_title = None
        self.keyword_columns = dict()
        '''
            Set the header title
            as well as keyword/value pairs with description if present.
        '''
        if self.ready:
            if div:
                self.header_title = (div.h2.string.split(' ')[1]
                                     if div and div.h2 and div.h2.string and
                                        div.h2.string.split(' ') and
                                        len(div.h2.string.split(' '))==2
                                     else None)
                pre = div.pre
                if pre and pre.string:
                    string = unicode(pre.string)
                    print('string: %r' % string)
                    print('type(pre.string): %r' % type(pre.string))
                    input('pause')
#
#                    for string in pre.strings
#                        print('string: %r' % string)
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to set_title_and_keyword_columns. ' +
                        'pre: {0}'.format(pre))
            else:
                self.ready = False
                self.logger.error('Unable to set_title_and_keyword_columns. ' +
                                    'div: {0}'.format(div))

