from json import dumps
from datamodel_parser.application import Util


class Type:
    '''Parse intro of file HTML.'''

    def __init__(self,logger=None,options=None,node=None):
        self.initialize(logger=logger,options=options)
        self.set_node(node=node)
        self.set_ready()
        self.set_attributes()

    def initialize(self,logger=None,options=None):
        self.util = Util(logger=logger,options=options)
        self.logger  = self.util.logger  if self.util.logger  else None
        self.options = self.util.options if self.util.options else None
        self.ready   = self.util and self.util.ready if self.util else None

    def set_node(self, node=None):
        '''Set the node class attribute.'''
        self.node = None
        if self.ready:
            self.node = node if node else None
            if not self.node:
                self.ready = False
                self.logger.error('Unable to set_node.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.ready   and
                          self.util    and
                          self.logger  and
                          self.options and
                          self.node)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.heading_tags        = self.util.heading_tags
            self.paragraph_tags      = self.util.paragraph_tags
            self.bold_tags           = self.util.bold_tags
            self.unordered_list_tags = self.util.unordered_list_tags


