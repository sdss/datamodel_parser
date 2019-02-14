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

    def parse_file(self):
        '''Parse the HTML of the given division tags.'''
        print('HI File2.parse_file(). self.template_type = 2')
        input('pause')
