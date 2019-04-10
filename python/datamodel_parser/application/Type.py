from datamodel_parser.application import Util
import inspect
from json import dumps

class Type(object):
    '''Parse intro of file HTML.'''

    def __init__(self,logger=None,options=None,node=None):
#        self.calling_class = inspect.stack()[1][0].f_locals["self"].__class__.__name__
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


class Intro_type(Type):
    '''Determine the class Intro type of the given node.'''
    def __init__(self,logger=None,options=None,node=None):
        Type.__init__(self,logger=logger,options=options,node=node)
        print('HI class Intro_type.')
        input('pause')


class Hdu_type(Type):
    '''Determine the class HDU type of the given node.'''
    def __init__(self,logger=None,options=None,node=None):
        Type.__init__(self,logger=logger,options=options,node=node)

    def get_Hdu_type(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        hdu_type = None
        if self.ready:
            node = node if node else self.node
            if node:
                if   self.check_Hdu_type_1(node=node): hdu_type = 1
                elif self.check_Hdu_type_2(node=node): hdu_type = 2
                elif self.check_Hdu_type_3(node=node): hdu_type = 3
                elif self.check_Hdu_type_4(node=node): hdu_type = 4
#                else:
#                    self.ready = False
#                    self.logger.error('Unable to get_Hdu_type. '
#                                      'Unexpected child_names encountered ' +
#                                      'in Hdu.parse_file_hdu_div(). ')
        return hdu_type

    def check_Hdu_type_1(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = None
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_Hdu_type_1:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,ul,table}
                if not (tag_names.issubset(self.util.heading_tags
                                           | {'p'} | {'dl'} | {'table'})
                                            and tag_names & {'dl'}):
                    self.correct_type = False
                    self.logger.debug("tag_names = {h,p,ul,table}")
                self.check_hdu_heading_tag_assumptions(node=node)
                self.check_hdu_dl_tag_assumptions(node=node)
                self.check_hdu_table_tag_assumptions(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to get_Hdu_type. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_Hdu_type_2(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        if self.ready:
            if node:
                self.logger.debug("First inconsistency for check_Hdu_type_2:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,ul,table}
                if not (tag_names.issubset(self.util.heading_tags
                                           | {'p'} | {'dl'} | {'table'})):
                    self.correct_type = False
                    self.logger.debug("tag_names = {h,p,table}")
                self.check_hdu_table_tag_assumptions(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to get_Hdu_type. ' +
                                  'node: {}.'.format(node))

    def check_Hdu_type_3(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        correct_type = None
        if self.ready:
            if node:
                correct_type = True
                self.logger.debug("Inconsistencies for check_Hdu_type_3:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,pre}
                if not (tag_names.issubset(self.util.heading_tags | {'pre'} )):
                    correct_type = False
                    self.logger.debug("tag_names = {h,pre}")
                else:
                    # heading tag assumptions
                    if self.check_hdu_heading_tag_assumptions(node=node):
                        # pre tag assumptions
                        pre = node.find_next('pre')
                        rows = self.util.get_string(node=pre).split('\n')
                        # Assume the pre tag is a string with rows separated by '\n'
                        if not rows:
                            correct_type = False
                            self.logger.error("pre tag is a string with rows separated by '\n'")
                        else:
                            # Assume none of the list entries of rows are empty
                            rows1 = [row for row in rows if row]
                            if len(rows) != len(rows1):
                                correct_type = False
                                self.logger.error("none of the list entries of rows are empty")
                            else:
                                # Assume the rows contain either '=' for data or 'HISTORY' or 'END'
                                for row in rows:
                                    if not ('=' in row or 'HISTORY' in row or 'END' in row):
                                        correct_type = False
                                        self.logger.error("the rows contain either '=' " +
                                                          "for data or 'HISTORY' or 'END'")
            else:
                self.ready = False
                self.logger.error('Unable to get_Hdu_type. ' +
                                  'node: {}.'.format(node))
#        print('correct_type: %r' % correct_type)
#        input('pause')
        return correct_type

    def check_Hdu_type_4(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        correct_type = None
        if self.ready:
            if node:
                correct_type = True
                self.logger.debug("Inconsistencies for check_Hdu_type_4:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,pre}
                if not (tag_names.issubset(self.util.heading_tags
                                            | {'p'} | {'table'} )):
                    correct_type = False
                    self.logger.debug("tag_names = {h,p,table}")
                # heading tag assumptions
                correct_type = self.check_hdu_heading_tag_assumptions(node=node)
                # pre tag assumptions
                pre = node.find_next('pre')
                rows = self.util.get_string(node=pre).split('\n')
                # Assume the pre tag is a string with rows separated by '\n'
                if not rows:
                    correct_type = False
                    self.logger.error("pre tag is a string with rows separated by '\n'")
                # Assume none of the list entries of rows are empty
                rows1 = [row for row in rows if row]
                if len(rows) != len(rows1):
                    correct_type = False
                    self.logger.error("none of the list entries of rows are empty")
                # Assume the rows contain either '=' for data or 'HISTORY' or 'END'
                for row in rows:
                    if not ('=' in row or 'HISTORY' in row or 'END' in row):
                        correct_type = False
                        self.logger.error("the rows contain either '=' " +
                                          "for data or 'HISTORY' or 'END'")
            else:
                self.ready = False
                self.logger.error('Unable to get_Hdu_type. ' +
                                  'node: {}.'.format(node))
#        print('correct_type: %r' % correct_type)
#        input('pause')
        return correct_type

    def check_hdu_heading_tag_assumptions(self,node=None):
        '''Check hdu heading tag assumptions.'''
        if self.ready:
            if node:
                # check only one heading tag
                if self.correct_type:
                    heading_tag_names = self.util.get_heading_tag_children(node=node)
                    if not len(heading_tag_names) == 1:
                        self.correct_type = False
                        self.logger.debug("not only one heading tag")
                # check heading = 'HDUn: HduTitle', where n is a digit
                if self.correct_type:
                    h = node.find_next(heading_tag_names[0])
                    string = self.util.get_string(node=h).lower()
                    if not ('hdu' in string and
                            ':' in string   and
                            string.split(':')[0].lower().replace('hdu','').isdigit()):
                        self.correct_type = False
                        self.logger.error("not heading = 'HDUn: HduTitle', where n is a digit")
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_heading_tag_assumptions. ' +
                                  'node: {}.'.format(node))

    def check_hdu_dl_tag_assumptions(self,node=None):
        '''Check hdu <dl> tag assumptions.'''
        if self.ready:
            if node:
                # check 'dl' in tag_names
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'dl' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'dl' in tag_names")
                # check children of <dl> are <dt> and <dd>
                if self.correct_type:
                    dl = node.find_next('dl')
                    child_names = set(self.util.get_child_names(node=dl))
                    if not child_names == {'dt','dd'}:
                        self.correct_type = False
                        self.logger.debug("not children of dl are dt and dd")
                # check 'hdu', 'type' and 'size' are in the list elements of dts
                if self.correct_type:
                    (dts,dds) = self.util.get_dts_and_dds_from_dl(dl=dl)
                    in_dt = lambda s: bool([x for x in dts if s in x.lower()])
                    if not (in_dt('hdu') and in_dt('type') and in_dt('size')):
                        self.correct_type = False
                        self.logger.debug("dts list elements")
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_dl_tag_assumptions. ' +
                                  'node: {}.'.format(node))

    def check_hdu_table_tag_assumptions(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # <table> tag assumptions
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'table' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'table' in tag_names")
                # <table> tag contains <caption>, <thead> and <tbody> tags
                if self.correct_type:
                    table = node.find_next('table')
                    child_names = set(self.util.get_child_names(node=table))
                    if not child_names == {'caption','thead','tbody'}:
                        self.correct_type = False
                        self.logger.debug("not table.children == {caption,thead,tbody}")
                # <thead> tag assumptions
                if self.correct_type:
                    thead = table.find_next('thead')
                    child_names = self.util.get_child_names(node=thead)
                    if not child_names == ['tr']:
                        self.correct_type = False
                        self.logger.debug("not child_names == ['tr']")
                # Asume all children of the <tr> tag are <th> tags
                if self.correct_type:
                    tr = thead.find_next('tr')
                    if not self.util.children_all_one_tag_type(node=tr,tag_name='th'):
                        self.correct_type = False
                        self.logger.debug("not all children of the tr tag are th tags")
                # tbody tag assumptions
                if self.correct_type:
                    # Asume all children of the <tbody> tag are <tr> tags
                    tbody = table.find_next('tbody')
                    if not self.util.children_all_one_tag_type(node=tbody,tag_name='tr'):
                        self.correct_type = False
                        self.logger.debug("not all children of the <tbody> tag are <tr> tags")
                if self.correct_type:
                    # Asume all children of the <tbody> child <tr> tags are <td> tags
                    for tr in [tr for tr in tbody.children
                               if not self.util.get_string(node=tr).isspace()]:
                        if not self.util.children_all_one_tag_type(node=tr,tag_name='td'):
                            self.correct_type = False
                            self.logger.debug("all children of the <tbody> " +
                                              "child <tr> tags are <td> tags")
            else:
                self.ready = False
                self.logger.error('Unable to get_Hdu_type. ' +
                                  'node: {}.'.format(node))

