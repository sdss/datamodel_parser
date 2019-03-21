from bs4 import Tag, NavigableString
from json import dumps


class Util:

    def __init__(self,logger=None,options=None):
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
                self.logger.error('Unable to set_options.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger  and
                          self.options)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.heading_tags = ['h1','h2','h3','h4','h5','h6']
            self.paragraph_tags = ['p']
            self.bold_tags = ['b']
            self.unordered_list_tags = ['ul']

    def get_string(self,node=None):
        string = None
        if self.ready:
            if node:
                if isinstance(node,str):
                    string = node
                else:
                    n = self.get_number_descendants(node=node)
                    if n > 1:
                        string = str(node).strip()
                    elif (n == 1 and bool(node.string)):
                        string = str(node.string).strip()
                    else:
                        string = ''
            else:
                self.ready = None
                self.logger.error('Unable to get_string. ' +
                                  'node: {0}'.format(node))
        return string

    def get_number_descendants(self,node=None):
        '''Return True if BeautifulSoup object has descendants.'''
        number_descendants = None
        if self.ready:
            if node:
                number_descendants = 0
                if not (isinstance(node, NavigableString) or isinstance(node, str)):
                    for descendant in node.descendants:
                        if descendant: number_descendants += 1
            else:
                self.ready = False
                self.logger.error('Unable to get_number_descendants.' +
                                  'node: {}'.format(node))
        return number_descendants

    def get_child_names(self,node=None):
        '''Set a list of child for the given BeautifulSoup node.'''
        child_names = None
        if self.ready:
            if node:
                child_names = list()
                for child in node.children:
                    if child.name: child_names.append(str(child.name))
            else:
                self.ready = None
                self.logger.error('Unable to get_child_names. ' +
                                  'node: {0}'.format(node))
        return child_names

    def children_all_one_tag_type(self,node=None,tag_name=None):
        '''Check all children of node are only one tag type with tag_name.'''
        all_one_tag_type = None
        if self.ready:
            if node and tag_name:
                all_one_tag_type = True
                for child in [child for child in node.children
                              if not self.get_string(node=child).isspace()]:
                    if child.name and child.name != tag_name:
                        all_one_tag_type = False
            else:
                self.ready = False
                self.logger.error('Unable to children_all_one_tag_type. ' +
                                  'node: {}'.format(node)   +
                                  'tag_name: {}'.format(tag_name)
                                  )
        return all_one_tag_type

    def get_parent_names(self,node=None):
        '''Set a list of parents for the given BeautifulSoup node.'''
        parent_names = None
        if self.ready:
            if node:
                parent_names = list()
                for parent in node.parents:
                    if parent.name: parent_names.append(parent.name)
            else:
                self.ready = None
                self.logger.error('Unable to set_parent_names. ' +
                                  'node: {0}'.format(node))
        return parent_names

    def get_dts_and_dds_from_dl(self,dl=None):
        '''From the given HTML description list <dl> Beautiful soup object,
        get Python lists for the associated definition tags <dt> and
        description tags <dd>.'''
        definitions  = list()
        descriptions = list()
        if self.ready:
            if dl:
                dts = dl.find_all('dt')
                dds = dl.find_all('dd')
                for dt in dts:
                    string = self.get_string(node=dt)
                    definitions.append(string)
                for dd in dds:
                    contents = [self.get_string(node=x) for x in dd.contents]
                    string = ' '.join(contents) if len(contents) > 1 else contents[0]
                    descriptions.append(string)
            else:
                self.ready = None
                self.logger.error('Unable to get_dts_and_dds_from_dl. ' +
                                  'dl: {0}'.format(dl))
        return (definitions,descriptions)

    def get_hdu_number_and_header_title(self,node=None,header_tag_name=None):
        '''Get extension.hdu_number and header.title from BeautifulSoup node.'''
        hdu_number = None
        header_title = None
        if self.ready:
            if node and header_tag_name:
                header_tag = node.find_next(header_tag_name)
                heading = self.get_string(node=header_tag)
                split = heading.split(':')
                hdu_number = int(split[0].lower().replace('hdu',''))
                header_title = split[1].strip()
            else:
                self.ready = None
                self.logger.error('Unable to get_hdu_number_and_header_title. ' +
                                  'node: {0}'.format(node) +
                                  'header_tag_name: {0}'.format(header_tag_name))
        return (hdu_number,header_title)

