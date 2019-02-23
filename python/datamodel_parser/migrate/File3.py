from json import dumps
from bs4 import Tag, NavigableString


class File3:
    '''
        
    '''

    def __init__(self,logger=None,options=None,body=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_body(body=body)
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
        self.ready = bool(self.logger  and
                          self.options and
                          self.body)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None

    def parse_file(self):
        '''Parse the HTML of the given division tags.'''
        self.file_extension_data    = list()
        self.file_extension_headers = list()
        if self.ready:
            if self.body:
                self.set_child_names(node=self.body)
                self.set_child_strings(node=self.body)
                print('self.child_names: \n' + dumps( self.child_names,indent=1))
                print('self.child_strings: \n' + dumps( self.child_strings,indent=1))
                input('pause')
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. self.body: {0}'
                                    .format(self.divs))


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

    def set_child_strings(self,node=None):
        '''Set a list of child for the given BeautifulSoup node.'''
        self.intro_heading_orders = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        find_paragraphs = True
        if self.ready:
            if node:
                heading_tags = ['h1','h2','h3','h4','h5','h6']
                for child in node.children:
                    child_name = child.name
                    if child_name:
                        print('\n\n\nchild: %r' % child)

                        # Don't look for anymore intro heading_titles
                        # and heading_descriptions
                        if child_name == 'pre': find_paragraphs = False
                        # Heading tags
                        if child_name in heading_tags:
                            string = str(child.string)
                            split = string.split(':') if string else None
                            if split:
                                heading_title = split[0].strip()
                                description   = split[1].strip()
                                if heading_title:
                                    self.intro_heading_titles.append(heading_title)
                                if description:
                                    self.intro_descriptions.append(description)
                        # heading_title and heading_description
                        if child_name == 'p' and find_paragraphs:
                            b = child.find_next('b')
                            heading_title = str(b.string).strip() if b else None
                            print('\nheading_title: %r' % heading_title)
#                            input('pause')
                            description = ''
                            for child_string in child.strings:
                                string = str(child_string).strip()
                                if string and string!=heading_title:
                                    description += string.strip()
                                    print('description: %r' % description)
#                                    input('pause')
                            if heading_title:
                                self.intro_heading_titles.append(heading_title)
                            if description:
                                self.intro_descriptions.append(description)

                        print('self.intro_heading_titles: \n' + dumps(self.intro_heading_titles,indent=1))
                        print('self.intro_descriptions: \n' + dumps( self.intro_descriptions,indent=1))
                        input('pause')
                        
            else:
                self.ready = None
                self.logger.error('Unable to set_child_strings. ' +
                                  'node: {0}'.format(node))

    def set_heading_tag_names(self,child_names=None):
        '''Set a list of child for the given BeautifulSoup child_names.'''
        self.heading_tag_names = list()
        if self.ready:
            if child_names:
                heading_tags = ['h1','h2','h3','h4','h5','h6']
                for name in child_names:
                    if name and name in heading_tags:
                        self.heading_tag_names.append(str(name))
            else:
                self.ready = None
                self.logger.error('Unable to set_child_names. ' +
                                  'child_names: {0}'.format(child_names))
