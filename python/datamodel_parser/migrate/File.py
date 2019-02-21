from datamodel_parser.migrate import File1
from datamodel_parser.migrate import File2
from json import dumps


class File:

    def __init__(self,logger=None,options=None,body=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_body(body=body)
        self.set_ready()
        self.set_attributes()
        self.set_file()

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
                self.logger.error('Unable to set_options.')

    def set_body(self, body=None):
        '''
            Set the body class attribute,
            a BeautifulSoup object generated by the datamodel HTML body.
        '''
        self.body = None
        if self.ready:
            self.body = body if body else None
            if not self.body:
                self.ready = False
                self.logger.error('Unable to set_body.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger  and
                          self.options and
                          self.body)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None

    def set_file(self):
        ''' Set class File instance.'''
        self.file = None
        if self.ready:
            self.set_template_type()
            if   self.template_type == 1: self.set_file1()
            elif self.template_type == 2: self.set_file2()
            else:
                self.ready = False
                self.logger.error('Unable to set_file. ' +
                                  'Unable to determine datamodel template_type')

    def set_template_type(self):
        '''Determine the datamodel template type.'''
        self.template_type = None
        self.set_all_divs()
        if self.all_divs: self.set_div_template_type()
        else: pass
            
    def set_all_divs(self):
        '''Check if the HTML body is comprised of only division tags.'''
        self.all_divs = True
        if self.ready:
            if self.body:
                all_div = True
                for child in self.body.children:
                    if child.name and child.name != 'div': self.all_div = False
            else:
                self.ready = False
                self.logger.error('Unable to set_all_divs. ' +
                                  'self.body: '.format(self.body))

    def set_div_template_type(self):
        '''Determine the datamodel template type from the first division tag.'''
        if self.ready:
            if self.body:
                div = self.body.find_next('div')
                div_id = div['id']
                if div_id == 'intro':
                    self.set_child_names(node=div)
                    if 'dl' not in self.child_names:
                        self.template_type = 1
                    else:
                        self.template_type = 2
                        
                else:
                    self.ready = False
                    self.logger.error('Unable to set_all_divs. ' +
                                      "Expedted div_id='intro'." +
                                      'div_id: {0}'.format(div_id))
            else:
                self.ready = False
                self.logger.error('Unable to set_all_divs. ' +
                                  'self.body: '.format(self.body))

    def set_child_names(self,node=None):
        '''Set a list of child for the given BeautifulSoup node.'''
        self.child_names = list()
        if self.ready:
            if node:
                for child in node.children:
                    if child.name:
                        self.child_names.append(child.name)
            else:
                self.ready = None
                self.logger.error('Unable to set_child_names. ' +
                                  'node: {0}'.format(node))

    def set_file1(self):
        '''
            Set instance of File derived class comprised of HTML div's,
            where 'dl' is not a child tag.
        '''
        if self.ready:
            if self.body:
                self.file = (File1(logger=self.logger,
                                   options=self.options,
                                   body=self.body)
                             if self.logger and self.options and self.body
                             else None)
                self.ready = bool(self.file and self.file.ready)
                if not self.ready:
                    self.logger.error(
                        'Unable to set_file1. '             +
                        'self.file: {0}'.format(self.file) +
                        'self.file.ready: {0}'.format(self.file.ready))
            else:
                self.ready = False
                self.logger.error('Unable to set_file1. ' +
                                  'divs: {0}'.format(divs))

    def set_file2(self):
        '''
            Set instance of File derived class comprised of HTML div's,
            where 'dl' is not a child tag.
        '''
        if self.ready:
            if self.body:
                self.file = (File2(logger=self.logger,
                                   options=self.options,
                                   body=self.body)
                             if self.logger and self.options and self.body
                             else None)
                self.ready = bool(self.file and self.file.ready)
                if not self.ready:
                    self.logger.error(
                        'Unable to set_file2. '             +
                        'self.file: {0}'.format(self.file) +
                        'self.file.ready: {0}'.format(self.file.ready))
            else:
                self.ready = False
                self.logger.error('Unable to set_file2. ' +
                                  'divs: {0}'.format(divs))

    def parse_file(self):
        '''Parse the given file using the determined File instance.'''
        self.file.parse_file()
        self.extension_count         = self.file.extension_count
        self.intro_heading_orders    = self.file.intro_heading_orders
        self.intro_heading_levels    = self.file.intro_heading_levels
        self.intro_heading_titles    = self.file.intro_heading_titles
        self.intro_descriptions      = self.file.intro_descriptions
        self.section_hdu_names       = self.file.section_hdu_names
        self.file_extension_data     = self.file.file_extension_data
        self.file_extension_headers  = self.file.file_extension_headers

        print('self.extension_count: {}'.format(self.extension_count))
#        print('self.intro_heading_orders: {}'.format(self.intro_heading_orders))
#        print('self.intro_heading_levels: %r' % self.intro_heading_levels)
#        print('self.intro_heading_titles: {}'.format(self.intro_heading_titles))
#        print('self.intro_descriptions: {}'.format(self.intro_descriptions))
#        print('self.section_hdu_names: {}'.format(self.section_hdu_names))
#        print('self.file_extension_data: \n' + dumps(self.file_extension_data,indent=1))
#        print('self.file_extension_headers: {}'.format(self.file_extension_headers))
#        input('pause')

