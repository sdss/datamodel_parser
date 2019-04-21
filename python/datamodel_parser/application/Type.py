from datamodel_parser.application import Util
import inspect
from json import dumps


class Type(object):
    '''Parse intro of file HTML.'''

    def __init__(self,logger=None,options=None):
#        self.calling_class = inspect.stack()[1][0].f_locals["self"].__class__.__name__
        self.initialize(logger=logger,options=options)
        self.set_ready()
        self.set_attributes()

    def initialize(self,logger=None,options=None):
        self.util = Util(logger=logger,options=options)
        self.logger  = self.util.logger  if self.util.logger  else None
        self.options = self.util.options if self.util.options else None
        self.ready   = self.util and self.util.ready if self.util else None

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.ready   and
                          self.util    and
                          self.logger  and
                          self.options)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.heading_tags        = self.util.heading_tags
            self.paragraph_tags      = self.util.paragraph_tags
            self.bold_tags           = self.util.bold_tags
            self.unordered_list_tags = self.util.unordered_list_tags

    def check_tag_has_only_text_content(self,tag=None):
        '''Check children of given tag is None, <code>, <b>, or <a>.'''
        tag_has_text_content = False
        if tag:
            child_names = self.util.get_child_names(node=tag)
            if not child_names or set(child_names).issubset({'a','b','code','i','em'}):
                tag_has_text_content = True
            else:
                tag_has_text_content = False
        else:
            self.logger.error('Unable to check_tag_has_only_text_content. ' +
                              'tag: {}.'.format(tag))
        return tag_has_text_content

    def check_tags_have_only_text_content(self,node=None,tag_names=None):
        '''Check the tags of the given BeautifulSoup node with given tag_names
        have only text content'''
        if self.ready:
            if node and tag_names:
                if self.correct_type:
                    # check heading tags have only text content
                    for child in self.util.get_children(node=node):
                        if self.correct_type and child.name in tag_names:
                            if not self.check_tag_has_only_text_content(tag=child):
                                self.correct_type = False
                                self.logger.debug("not tags have only text content " +
                                                  "for tag_names: {}".format(tag_names))
            else:
                self.logger.error('Unable to check_tags_have_only_text_content. ' +
                                  'node: {}.'.format(node) +
                                  'tag_names: {}.'.format(tag_names))

    def check_tag_type_of_first_child_tag(self,
                                          node=None,
                                          tag_name=None,
                                          child_tag_type=None):
        '''Check all the tags of the node with the given tag_name have
            first child tag of the given child_tag_type.'''
        if self.ready:
            if node and tag_name and child_tag_type:
                if self.correct_type:
                    for tag in node.find_all(tag_name):
                        if self.correct_type:
                            child_names = self.util.get_child_names(node=tag)
                            if not (child_names and child_names[0] in child_tag_type):
                                self.correct_type = False
                                self.logger.debug(
                                    "not all the tags of the given node with " +
                                    "tag_name: {} have first child tag".format(tag_name) +
                                    "of child_tag_type.: {}.".format(child_tag_type))
            else:
                self.ready = False
                self.logger.error('Unable to check_tag_type_of_first_child_tag. ' +
                                  'node: {}.'.format(node) +
                                  'tag_name: {}.'.format(tag_name) +
                                  'child_tag_type: {}.'.format(child_tag_type) )

    def check_dl_tag_assumptions_1(self,node=None,dl_child_names=None):
        '''Check hdu <dl> tag assumptions.'''
        if self.ready:
            if node and dl_child_names:
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
                    if not child_names == dl_child_names:
                        self.correct_type = False
                        self.logger.debug("not children of dl are {}"
                                            .format(dl_child_names) )
                # check <dt> and <dd> come in pairs
                if self.correct_type:
                    dts = list(dl.find_all('dt'))
                    dds = list(dl.find_all('dd'))
                    # Need to remove this from check_intro_2
                    # remove sections dt from dts
                    if (dl_child_names == {'dt','dd','ul'} and
                        dts[-1].string.lower() == 'sections'):
                        dts.pop()
                    if not (len(dts) == len(dds)):
                        self.correct_type = False
                        self.logger.debug("not <dt> and <dd> come in pairs")
            else:
                self.ready = False
                self.logger.error('Unable to check_dl_tag_assumptions_1. ' +
                                  'node: {}.'.format(node) +
                                  'dl_child_names: {}.'.format(dl_child_names))


class Intro_type(Type):
    '''Determine the class Intro type of the given node.'''
    def __init__(self,logger=None,options=None,node=None):
        Type.__init__(self,logger=logger,options=options)

    def get_intro_type(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        intro_type = None
        if self.ready:
            if node:
                if   self.check_intro_type_1(node=node): intro_type = 1
                elif self.check_intro_type_2(node=node): intro_type = 2
                elif self.check_intro_type_3(node=node): intro_type = 3
                elif self.check_intro_type_4(node=node): intro_type = 4
                else:
                    self.ready = False
                    self.logger.error('Unable to get_intro_type. '
                                      'Unexpected intro_type')
                if self.verbose: print('intro_type: %r' % intro_type )
#                input('pause')
        return intro_type

    def check_intro_type_1(self,node=None):
        '''Determine class Intro_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_1:")
                tag_names = self.util.get_child_names(node=node)
                
                # check tag_names = {h,p,div}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.util.heading_tags)
                                              | {'p','div'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,div}")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.util.heading_tags)
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                self.check_middle_tags_h_p_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_1. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_2(self,node=None):
        '''Determine class Intro_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_2:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,dl}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.util.heading_tags)
                                              | {'dl'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,dl}")
                # check node has only one heading tag
                if self.correct_type:
                    heading_tag_names = self.util.get_heading_tag_children(node=node)
                    l = len(heading_tag_names)
                    if not l == 1:
                        self.correct_type = False
                        self.logger.debug("not node has only one heading tag")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.util.heading_tags)
                self.check_dl_tag_assumptions_1(node=node,
                                                     dl_child_names={'dt','dd','ul'})
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_2. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_3(self,node=None):
        '''Determine class Intro_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_3:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,dl}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.util.heading_tags)
                                              | {'dl'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,dl}")
                # check node has only one heading tag
                if self.correct_type:
                    heading_tag_names = self.util.get_heading_tag_children(node=node)
                    l = len(heading_tag_names)
                    if not l == 1:
                        self.correct_type = False
                        self.logger.debug("not node has only one heading tag")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.util.heading_tags)
                self.check_dl_tag_assumptions_1(node=node,
                                                     dl_child_names={'dt','dd'})
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_3. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_4(self,node=None):
        '''Determine class Intro_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_4:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,p}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.util.heading_tags)
                                              | {'p'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p}")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.util.heading_tags)
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                self.check_tag_type_of_first_child_tag(
                                                node=node,
                                                tag_name='p',
                                                child_tag_type=['b'])
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_4. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_middle_tags_h_p_1(self,node=None):
        '''check middle tags {h,p}, allowing for [h,p], [h,p,p], etc.,
            for the given BeautifulSoup node.'''
        if self.ready:
            if node:
                if self.correct_type:
                    tag_names = self.util.get_child_names(node=node)
                    middle_tags = set(tag_names[1:-1])
                    if not (middle_tags == (middle_tags & self.util.heading_tags)
                                            | {'p'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not middle tags {h,p}, " +
                                          "allowing for [h,p], [h,p,p], etc.")
            else:
                self.ready = False
                self.logger.error('Unable to check_middle_tags_h_p_1. ' +
                                  'node: {}.'.format(node))



class Hdu_type(Type):
    '''Determine the class Hdu_type of the given node.'''
    def __init__(self,logger=None,options=None,node=None):
        Type.__init__(self,logger=logger,options=options)

    def get_hdu_type(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        hdu_type = None
        if self.ready:
            if node:
                if   self.check_hdu_type_1(node=node): hdu_type = 1
                elif self.check_hdu_type_2(node=node): hdu_type = 2
                elif self.check_hdu_type_3(node=node): hdu_type = 3
                elif self.check_hdu_type_4(node=node): hdu_type = 4
                elif self.check_hdu_type_5(node=node): hdu_type = 5
                else:
                    self.ready = False
                    self.logger.error('Unable to get_hdu_type. '
                                      'Unexpected hdu_type')
                if self.verbose: print('hdu_type: %r' % hdu_type )
#                input('pause')
        return hdu_type

    def check_hdu_type_1(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_1:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,ul,table}
                if not (tag_names == (tag_names & self.util.heading_tags)
                                     | {'p','dl','table'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,ul,table}")
                self.check_heading_tag_assumptions_1(node=node)
                self.check_p_tag_assumptions_1(node=node)
                self.check_dl_tag_assumptions_1(node=node,
                                                dl_child_names={'dt','dd'})
                self.check_hdu_dl_tag_assumptions_1(node=node)
                self.check_table_tag_assumptions_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_1. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_2(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_2:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,table}
                if not (tag_names == (tag_names & self.util.heading_tags)
                                     | {'p','table'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,table}")
                self.check_heading_tag_assumptions_1(node=node)
                self.check_p_tag_assumptions_2(node=node)
                self.check_table_tag_assumptions_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_2. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_3(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = None
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("Inconsistencies for check_hdu_type_3:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,pre}
                if not (tag_names == (tag_names & self.util.heading_tags)
                                     | {'pre'}
                        ):
                    self.correct_type = False
                    self.logger.debug("tag_names = {h,pre}")
                self.check_heading_tag_assumptions_1(node=node)
                self.check_pre_tag_assumptions_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_3. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_4(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_4:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,table}
                if not (tag_names == (tag_names & self.util.heading_tags)
                                     | {'p','table'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,table}")
                self.check_heading_tag_assumptions_1(node=node)
                self.check_p_tag_assumptions_1(node=node)
                self.check_table_tag_assumptions_2(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_4. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_5(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_5:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p}
                if not (tag_names == (tag_names & self.util.heading_tags)
                                     | {'p'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p}")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.util.heading_tags)
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_5. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_7(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_7:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,pre}
                if not (tag_names == (tag_names & self.util.heading_tags)
                                     | {'p','pre'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,pre}")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.util.heading_tags)
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                self.check_tags_have_only_text_content(node=node,tag_names=['pre'])
                self.check_pre_tag_assumptions_2(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_7. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_heading_tag_assumptions_1(self,node=None):
        '''Check heading tag assumptions.'''
        if self.ready:
            if node:
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.util.heading_tags)
                # check node has either one or three heading tags
                if self.correct_type:
                    heading_tag_names = self.util.get_heading_tag_children(node=node)
                    l = len(heading_tag_names)
                    if not ( l == 1 or l == 3):
                        self.correct_type = False
                        self.logger.debug("not node has either one or three heading tags")
                # check additional headings indicate header and binary table
                if self.correct_type:
                    if l == 3:
                        heading_nodes = node.find_all(heading_tag_names)
                        heading_strings = [self.util.get_string(heading_node)
                                           for heading_node in heading_nodes]
                        if not (heading_strings[1].lower() == 'header' and
                                heading_strings[2].lower() == 'binary table'):
                            self.correct_type = False
                            self.logger.debug("not additional headings indicate header and binary table")
                # check heading starts with hdu or primary
                if self.correct_type:
                    h = node.find_next(heading_tag_names[0])
                    string = self.util.get_string(node=h)
                    string = string.lower() if string else str()
                    if not (string.startswith('hdu')        or
                            string.startswith('primary')
                            ):
                        self.correct_type = False
                        self.logger.error("not heading starts with hdu or primary")
                # if heading starts with hdu,
                # then check next character is a digit or whitespace then a digit
                if self.correct_type:
                    if string.startswith('hdu'):
                        if not string[3].isdigit(): # hdu0, hdu1, ...
                            split = string.split()
                            if not( split                    and
                                    isinstance(split[1],str) and
                                    split[1][0].isdigit()
                                    ):
                                self.correct_type = False
                                self.logger.error("not next character is a digit or whitespace then a digit")
            else:
                self.ready = False
                self.logger.error('Unable to check_heading_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_p_tag_assumptions_1(self,node=None):
        '''Check <p> tag assumptions.'''
        if self.ready:
            if node:
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                # check node has only one <p> tag
                if self.correct_type:
                    child_names = self.util.get_child_names(node=node)
                    if not child_names.count('p') == 1:
                        self.correct_type = False
                        self.logger.debug("not node has only one <p> tag")
                if self.correct_type:
                    p = node.find_next('p')
                    if not self.check_tag_has_only_text_content(tag=p):
                        self.correct_type
                        self.logger.debug("not p tag has text content")
            else:
                self.ready = False
                self.logger.error('Unable to check_p_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_p_tag_assumptions_2(self,node=None):
        '''Check <p> tag assumptions.'''
        if self.ready:
            if node:
                # check node has two or more <p> tags
                if self.correct_type:
                    child_names = self.util.get_child_names(node=node)
                    if not child_names.count('p') > 1:
                        self.correct_type = False
                        self.logger.debug("not node has two or more <p> tags")
                self.check_tags_have_only_text_content(node=node,tag_names = ['p'])
                # check last <p> tag has hdu table information
                if self.correct_type:
                    for p in node.find_all('p'): pass  # get second p tag
                    strings = self.util.get_all_strings(node=p)
                    if not ('hdu type' in strings[0].lower() and
                            'hdu size' in strings[2].lower()
                            ):
                        self.correct_type = False
                        self.logger.debug("not second <p> tag has hdu table information")
            else:
                self.ready = False
                self.logger.error('Unable to check_p_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_hdu_dl_tag_assumptions_1(self,node=None):
        '''Check hdu <dl> tag assumptions.'''
        if self.ready:
            if node:
                # check 'dl' in tag_names
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'dl' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'dl' in tag_names")
                # check 'hdu', 'type' and 'size' are in the list elements of dts
                if self.correct_type:
                    dl = node.find_next('dl')
                    (dts,dds) = self.util.get_dts_and_dds_from_dl(dl=dl)
                    in_dt = lambda s: bool([dt for dt in dts if s in dt.lower()])
                    if not (in_dt('hdu') and in_dt('type') and in_dt('size')):
                        self.correct_type = False
                        self.logger.debug("not 'hdu', 'type' and 'size' " +
                                          "are in the list elements of dts")
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_dl_tag_assumptions_1. ' +
                                  'dl: {}.'.format(dl))

    def check_table_tag_assumptions_1(self,node=None):
        '''Check table tag assumptions for the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # check <table> in node
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'table' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'table' in tag_names")
                # check <table> contains <caption>, <thead> and <tbody>
                if self.correct_type:
                    tables = node.find_all('table')
                    for table in tables:
                        child_names = set(self.util.get_child_names(node=table))
                        if not child_names == {'caption','thead','tbody'}:
                            self.correct_type = False
                            self.logger.debug(
                                "not table.children = {caption,thead,tbody}")
                        self.check_thead_tag_assumptions_1(table=table)
                        self.check_tbody_tag_assumptions_1(table=table)
            else:
                self.ready = False
                self.logger.error('Unable to check_table_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_table_tag_assumptions_2(self,node=None):
        '''Check table tag assumptions for the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # check <table> in node
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'table' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'table' in tag_names")
                # check <table> contains <caption> and <tbody>
                if self.correct_type:
                    tables = node.find_all('table')
                    for table in tables:
                        child_names = set(self.util.get_child_names(node=table))
                        if not child_names == {'caption','tr'}:
                            self.correct_type = False
                            self.logger.debug(
                                "not table.children = {caption,tbody}")
                        self.check_tr_tag_assumptions_1(table=table)
            else:
                self.ready = False
                self.logger.error('Unable to check_table_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_thead_tag_assumptions_1(self,table=None):
        '''Check thead tag assumptions for the given BeautifulSoup table.'''
        if self.ready:
            if table:
                # check <thead> in <table>
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=table))
                    if not 'thead' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'thead' in tag_names")
                # check <thead> has only one child <tr>
                if self.correct_type:
                    thead = table.find_next('thead')
                    child_names = self.util.get_child_names(node=thead)
                    if not child_names == ['tr']:
                        self.correct_type = False
                        self.logger.debug("not <thead> has only one child <tr>")
                # check all children of the <tr> tag are <th> tags
                if self.correct_type:
                    tr = thead.find_next('tr')
                    if not self.util.children_all_one_tag_type(node=tr,tag_name='th'):
                        self.correct_type = False
                        self.logger.debug("not all children of the tr tag are th tags")
            else:
                self.ready = False
                self.logger.error('Unable to check_thead_tag_assumptions_1. ' +
                                  'table: {}.'.format(table))

    def check_tbody_tag_assumptions_1(self,table=None):
        '''Check tbody tag assumptions for the given BeautifulSoup table.'''
        if self.ready:
            if table:
                # check <tbody> in <table>
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=table))
                    if not 'tbody' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'tbody' in tag_names")
                # check all children of the <tbody> tag are <tr> tags
                if self.correct_type:
                    tbody = table.find_next('tbody')
                    if not self.util.children_all_one_tag_type(node=tbody,
                                                               tag_name='tr'):
                        self.correct_type = False
                        self.logger.debug("not all children of the <tbody> tag are <tr> tags")
                # check all children of the <tr> tag are <td> tags
                if self.correct_type:
                    for tr in [tr for tr in tbody.children
                               if not self.util.get_string(node=tr).isspace()]:
                        if not self.util.children_all_one_tag_type(node=tr,
                                                                   tag_name='td'):
                            self.correct_type = False
                            self.logger.debug("not all children of the <tr> tag are <th> tags")
                # check each <tr> tag as exactly 4 <td> tag children
                if self.correct_type:
                    for tr in [tr for tr in tbody.children
                               if not self.util.get_string(node=tr).isspace()]:
                        if not len(tr.find_all('td')) == 4:
                            self.correct_type = False
                            self.logger.debug("not each <tr> tag as exactly 4 <td> tag children")
            else:
                self.ready = False
                self.logger.error('Unable to check_tbody_tag_assumptions_1. ' +
                                  'table: {}.'.format(table))

    def check_tr_tag_assumptions_1(self,table=None):
        '''Check tbody tag assumptions for the given BeautifulSoup table.'''
        if self.ready:
            if table:
                # check children of the <table> tag are <caption> and <tr> tags
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=table))
                    if not tag_names == {'caption','tr'}:
                        self.correct_type = False
                        self.logger.debug("not children of the <table> tag are "
                                          "<caption> and <tr> tags")
                # check all <tr> tag children are <th> or <td> tags
                if self.correct_type:
                    for node in [node for node in table.find_all('tr')
                                 if not self.util.get_string(node=node).isspace()]:
                        if self.correct_type:
                            tag_names = set(self.util.get_child_names(node=node))
                            if not (tag_names == {'td'} or tag_names == {'th'}):
                                self.correct_type = False
                                self.logger.debug("not all <tr> tag children are "
                                                  "<th> or <td> tags")
                # check first <tr> tag children are <th> tags
                if self.correct_type:
                    tr = table.find_next('tr') # get first tr tag
                    if not self.util.children_all_one_tag_type(node = tr,
                                                           tag_name = 'th'):
                        self.correct_type = False
                        self.logger.debug("not first <tr> tag children are <th> tags")
                # check after first <tr> tag children are <td> tags
                if self.correct_type:
                    siblings = tr.next_siblings # get next siblings of first tr tag
                    for sibling in [s for s in siblings if s.name]:
                        if self.correct_type:
                            if not self.util.children_all_one_tag_type(node = sibling,
                                                                   tag_name = 'td'):
                                self.correct_type = False
                                self.logger.debug("not after first <tr> tag children are <td> tags")

            else:
                self.ready = False
                self.logger.error('Unable to check_tr_tag_assumptions_1. ' +
                                  'table: {}.'.format(table))


    def check_pre_tag_assumptions_1(self,node=None):
        '''Check <pre> tag assumptions.'''
        if self.ready:
            if node:
                # check node has <pre> tags
                if self.correct_type:
                    child_names = set(self.util.get_child_names(node=node))
                    if not child_names & {'pre'}:
                        self.correct_type = False
                        self.logger.debug("not node has only two <pre> tags")
                if self.correct_type:
                    pres = node.find_all('pre')
                    for pre in pres:
                        # check pre tag is a string with rows separated by '\n'
                        if self.correct_type:
                            rows = self.util.get_string(node=pre).split('\n')
                            if not rows:
                                self.correct_type = False
                                self.logger.error("not pre tag is a string with rows separated by '\n'")
                        # check none of the list entries of rows are empty
                        if self.correct_type:
                            rows1 = [row for row in rows if row]
                            if len(rows) != len(rows1):
                                self.correct_type = False
                                self.logger.error("none of the list entries of rows are empty")
                        # check rows contain either '=' for data or 'HISTORY' or 'END'
                        if self.correct_type:
                            for row in rows:
                                if self.correct_type:
                                    if not ('=' in row or 'HISTORY' in row or 'END' in row):
                                        self.correct_type = False
                                        self.logger.error("the rows contain either '=' " +
                                                          "for data or 'HISTORY' or 'END'")
            else:
                self.ready = False
                self.logger.error('Unable to check_pre_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_pre_tag_assumptions_2(self,node=None):
        '''Check <pre> tag assumptions.'''
        if self.ready:
            if node:
                # check node has <pre> tags
                if self.correct_type:
                    child_names = set(self.util.get_child_names(node=node))
                    if not child_names & {'pre'}:
                        self.correct_type = False
                        self.logger.debug("not node has only two <pre> tags")
                if self.correct_type:
                    pres = node.find_all('pre')
                    for pre in pres:
                        # check pre tag is a string with rows separated by '\n'
                        if self.correct_type:
                            rows = self.util.get_string(node=pre).split('\n')
                            if not rows:
                                self.correct_type = False
                                self.logger.error("not pre tag is a string with rows separated by '\n'")
                        # check none of the list entries of rows are empty
                        if self.correct_type:
                            rows1 = [row for row in rows if row]
                            if len(rows) != len(rows1):
                                self.correct_type = False
                                self.logger.error("none of the list entries of rows are empty")
            else:
                self.ready = False
                self.logger.error('Unable to check_pre_tag_assumptions_2. ' +
                                  'node: {}.'.format(node))


