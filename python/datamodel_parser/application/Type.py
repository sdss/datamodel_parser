from datamodel_parser.application import Util
from re import search, compile, match
import inspect
from json import dumps



class Type(object):
    '''Parse intro of file HTML.'''

    def __init__(self,logger=None,options=None):
        self.initialize(logger=logger,options=options)
        self.set_ready()
        self.set_attributes()

    def initialize(self,logger=None,options=None):
        '''Initialize utility class, logger, and command line options.'''
        self.util = Util(logger=logger,options=options)
        if self.util and self.util.ready:
            self.logger  = self.util.logger  if self.util.logger  else None
            self.options = self.util.options if self.util.options else None
            self.ready   = bool(self.logger)
        else:
            self.ready = False
            print('ERROR: Unable to initialize. self.util: {}'.format(self.util))

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.ready   and
                          self.util    and
                          self.logger
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options  else None
            self.heading_tag_names   = self.util.heading_tag_names

    def check_tag_has_only_text_content(self,tag=None):
        '''Check children of given tag is None, <code>, <b>, or <a>.'''
        tag_has_text_content = False
        if tag:
            child_names = self.util.get_child_names(node=tag)
            if ((not child_names) or
                set(child_names).issubset({'a','b','code','i','em','sub','sup','tt','var'})
                ):
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
                    children = self.util.get_children(node=node)
                    for child in children:
                        if self.correct_type and child.name in tag_names:
                            if not self.check_tag_has_only_text_content(tag=child):
                                self.correct_type = False
                                self.logger.debug("not tags have only text content " +
                                                  "for tag_names: {}, ".format(tag_names) +
                                                  "child: {}".format(child)
                                                  )
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

    def check_heading_tag_assumptions_1(self,node=None):
        '''Check heading tag assumptions.'''
        if self.ready:
            if node:
                # check heading tag only has text content
                if self.correct_type:
                    self.check_tags_have_only_text_content(node=node,
                                                           tag_names=self.heading_tag_names)
                # check first child of node is heading tag
                if self.correct_type:
                    children = self.util.get_children(node=node)
                    if not children and children[0].name in self.heading_tag_names:
                        self.correct_type = False
                        self.logger.debug("not first child of node is heading tag")

                # check additional headings indicate header and binary table
                if self.correct_type:
                    heading_tag_names = self.util.get_heading_tag_child_names(node=node)
                    l = len(heading_tag_names)
                    if l > 1:
                        heading_nodes = node.find_all(heading_tag_names)
                        heading_strings = [self.util.get_string(node=heading_node)
                                           for heading_node in heading_nodes]
                        found_binary_table = False
                        for heading_string in heading_strings:
                            regex = '(?i)Binary\s*' + '|' + '(?i)Field\s*'
                            match = self.util.check_match(regex=regex,string=heading_string)
                            if match:
                                found_binary_table = True
                                break
                        if not found_binary_table:
                            self.correct_type = False
                            self.logger.debug("not additional headings indicate header and binary table")
            else:
                self.ready = False
                self.logger.error('Unable to check_heading_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_heading_tag_assumptions_2(self,node=None,toggle_found_hdu=False):
        '''Check heading tag assumptions.'''
        if self.ready:
            if node and isinstance(toggle_found_hdu,bool):
                # check heading tag only has text content
                if self.correct_type:
                    self.check_tags_have_only_text_content(node=node,
                                                           tag_names=self.heading_tag_names)
                # check there is a heading tag with HDU title
                if self.correct_type:
                    found_hdu = False
                    heading_tags = self.util.get_heading_tag_children(node=node)
                    for tag in heading_tags:
                        strings = [s.strip().replace(':','').lower()
                                   for s in tag.strings if s and not s.isspace()]
                        # check only one string in tag
                        string = strings[0] if strings and len(strings) == 1 else None
                        # check HDU title in heading tag
                        if string:
                            regex = self.util.get_table_title_regex_4()
#                            regex = ('(?i)hdu\s*\d+' + '|'
#                                    '(?i)primary\s*header' + '|'
#                                    '(?i)sample\s*header' + '|'
#                                    '(?i)primary\s*hdu')
                            if self.util.check_match(regex=regex,string=string):
                                found_hdu = True
                                break
                    if toggle_found_hdu: found_hdu = not found_hdu
                    if not found_hdu:
                        self.correct_type = False
                        self.logger.debug("not HDU title in heading tag")
            else:
                self.ready = False
                self.logger.error('Unable to check_heading_tag_assumptions_2. ' +
                                  'node: {}.'.format(node) +
                                  'isinstance(toggle_found_hdu,bool): {}'
                                    .format(isinstance(toggle_found_hdu,bool))
                                  )

    def check_heading_tag_assumptions_3(self,node=None):
        '''Check heading tag assumptions.'''
        if self.ready:
            if node:
                # check heading tag only has text content
                if self.correct_type:
                    self.check_tags_have_only_text_content(node=node,
                                                           tag_names=self.heading_tag_names)
                # check node has zero or one heading tag
                if self.correct_type:
                    heading_tag_names = self.util.get_heading_tag_child_names(node=node)
                    l = len(heading_tag_names)
                    if not (l == 0 or l == 1 or l == 2):
                        self.correct_type = False
                        self.logger.debug("not node has only one heading tag")
                # check first child of node is heading tag
                if self.correct_type:
                    children = self.util.get_children(node=node)
                    if not children and children[0].name in self.heading_tag_names:
                        self.correct_type = False
                        self.logger.debug("not first child of node is heading tag")
                # if l ==2 check last child of node is heading tag
                if self.correct_type:
                    if l == 2:
                        children = self.util.get_children(node=node)
                        if not children and children[-1].name in self.heading_tag_names:
                            self.correct_type = False
                            self.logger.debug("not last child of node is heading tag")
            else:
                self.ready = False
                self.logger.error('Unable to check_heading_tag_assumptions_3. ' +
                                  'node: {}.'.format(node))

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
                    dl = node.find('dl')
                    child_names = set(self.util.get_child_names(node=dl))
                    if not child_names == dl_child_names:
                        self.correct_type = False
                        self.logger.debug("not children of dl are {}"
                                            .format(dl_child_names) )
            else:
                self.ready = False
                self.logger.error('Unable to check_dl_tag_assumptions_1. ' +
                                  'node: {}.'.format(node) +
                                  'dl_child_names: {}.'.format(dl_child_names))

    def check_ul_tag_assumptions_1(self,node=None,toggle=False):
        '''Check hdu <ul> tag assumptions.'''
        if self.ready:
            if node and isinstance(toggle,bool):
                # check 'ul' in tag_names
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'ul' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'ul' in tag_names")
                # check all <ul> tags have only <li> tag children
                if self.correct_type:
                    for ul in node.find_all('ul'):
                        if self.correct_type:
                            if not self.util.children_all_one_tag_type(node=ul,
                                                                       tag_name='li'):
                                self.correct_type = False
                                self.logger.debug("not all <ul> tags have only <li> tag children")
                        if self.correct_type:
                            is_first_li = True
                            for li in ul.find_all('li'):
                                # check <ul> <li> tags after first <li> tag contains a bold tag
                                if self.correct_type:
                                    tag_names = set(self.util.get_child_names(node=li))
                                    bold_in_tag_names = tag_names & {'b'}
                                    if toggle: bold_in_tag_names = not bold_in_tag_names
                                    if not bold_in_tag_names:
#                                        print('li: %r'% li)
#                                        input('pause')
                                        if is_first_li:
                                            is_first_li = False
                                        else:
                                            self.correct_type = False
                                            self.logger.debug(
                                                "not <ul> <li> tags after first <li> tag contains a bold tag.")
            else:
                self.ready = False
                self.logger.error('Unable to check_ul_tag_assumptions_1. ' +
                                  'node: {}.'.format(node) +
                                  'isinstance(toggle,bool): {}.'.format(isinstance(toggle,bool))
                                  )

    def check_ul_tag_assumptions_2(self,node=None):
        '''Check hdu <ul> tag assumptions.'''
        if self.ready:
            if node:
                # check 'ul' in tag_names
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'ul' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'ul' in tag_names")
                # check there's only one <ul> tag with only <li> tag children
                if self.correct_type:
                    uls = node.find_all('ul') if node else None
                    if not uls or len(list(uls)) > 1:
                        self.correct_type = False
                        self.logger.debug("not there's only one <ul> tag.")
                    else:
                        # check the one <ul> tag has only <li> tag children
                        ul = list(uls)[0]
                        lis = ul.find_all('li') if ul else list()
                        if not lis:
                            self.correct_type = False
                            self.logger.debug("not <ul> tag has only <li> tag children.")
#                        else:
#                            # check lis contain file names
#                            for li in lis:
#                                if self.correct_type:
#                                    if not self.util.check_node_string_is_filename(node=li):
#                                        self.correct_type = False
#                                        self.logger.debug("not <li> string is filename.")
            else:
                self.ready = False
                self.logger.error('Unable to check_ul_tag_assumptions_2. ' +
                                  'ul: {}.'.format(ul))

    def check_ul_tag_assumptions_3(self,node=None):
        '''Check hdu <ul> tag assumptions.'''
        if self.ready:
            if node:
                # check 'ul' in tag_names
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'ul' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'ul' in tag_names")
                # check all <ul> tags have only <li> tag children
                if self.correct_type:
                    for ul in node.find_all('ul'):
                        if self.correct_type:
                            if not self.util.children_all_one_tag_type(node=ul,
                                                                       tag_name='li'):
                                self.correct_type = False
                                self.logger.debug("not all <ul> tags have only <li> tag children")
            else:
                self.ready = False
                self.logger.error('Unable to check_ul_tag_assumptions_3. ' +
                                  'ul: {}.'.format(ul))

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
            else:
                self.ready = False
                self.logger.error('Unable to check_p_tag_assumptions_1. ' +
                                  'node: {}.'.format(node))

    def check_p_tag_assumptions_2(self,node=None):
        '''Check <p> tag assumptions.'''
        if self.ready:
            if node:
                self.check_tags_have_only_text_content(node=node,tag_names = ['p'])
                # check last <p> tag has hdu table information
                if self.correct_type:
                    for p in node.find_all('p'): pass  # get last p tag
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

    def check_p_tag_assumptions_3(self,node=None,toggle_found_table_title=False):
        '''Check <p> tag assumptions.'''
        if self.ready:
            if node and isinstance(toggle_found_table_title,bool):
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                if self.correct_type:
                    found_table_title = False
                    for p in node.find_all('p'):
                        # check a <p> tag contains a table title
                        if self.correct_type:
                            b = p.find('b')
                            if b and b.strings:
                                strings = [s.strip().replace(':','').lower()
                                           for s in b.strings if s and not s.isspace()]
                                # check only one string in <b> tag
                                string = strings[0] if strings and len(strings) == 1 else None
                                if string:
                                    regex = self.util.get_table_title_regex_1()
                                    match = self.util.check_match(regex=regex,string=string)
                                    if match: found_table_title = True
                    if toggle_found_table_title: found_table_title = not found_table_title
                    if not found_table_title:
                        self.correct_type = False
                        self.logger.debug("not there is a header table or data table " +
                                            "title in a <p> tag")
            else:
                self.ready = False
                self.logger.error('Unable to check_p_tag_assumptions_3. ' +
                                  'node: {}.'.format(node)+
                                  'isinstance(toggle_found_table_title,bool): {}'
                                    .format(isinstance(toggle_found_table_title,bool))
                                  )

    def check_p_tag_assumptions_4(self,node=None):
        '''Check <p> tag assumptions.'''
        if self.ready:
            if node:
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                if self.correct_type:
                    table = node.find('table') # find File Contents table
                    previous_siblings = [s for s in table.previous_siblings if s and not str(s).isspace()]
                    for sibling in previous_siblings:
                        # check all <p> tags before File Contents table have <b> tag children
                        if self.correct_type:
                            if sibling.name == 'p':
                                child_names = self.util.get_child_names(node=sibling)
                                if child_names and not 'b' in child_names:
                                    self.correct_type = False
                                    self.logger.debug("all <p> tags before File Contents " +
                                                      "table have <b> tag children")
            else:
                self.ready = False
                self.logger.error('Unable to check_p_tag_assumptions_4. ' +
                                  'node: {}.'.format(node))

    def check_p_tag_assumptions_5(self,node=None):
        '''Check <p> tag assumptions.'''
        if self.ready:
            if node:
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                # check <p> tag has zero or one <b> tag child
                if self.correct_type:
                    for p in node.find_all('p'):
                        if self.correct_type:
                            child_names = self.util.get_child_names(node=p)
                            if child_names and 'b' in child_names:
                                b = p.find('b')
                                if len(list(b.strings)) > 1:
                                    self.correct_type = False
                                    self.logger.debug("not <p> tag has one <b> tag child")
            else:
                self.ready = False
                self.logger.error('Unable to check_p_tag_assumptions_5. ' +
                                  'node: {}.'.format(node))

    def check_p_tag_assumptions_6(self,node=None,toggle=None):
        '''Check <p> tag assumptions.'''
        if self.ready:
            if node and isinstance(toggle,bool):
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                if self.correct_type:
                    found_table_title = False
                    for p in node.find_all('p'):
                        # check there is a header table or data table title in a <p> tag
                        if self.correct_type:
                            b = p.find('b')
                            if b and b.strings:
                                strings = [s.strip().replace(':','').lower()
                                           for s in b.strings if s and not s.isspace()]
                                # check only one string in <b> tag
                                string = strings[0] if strings and len(strings) == 1 else None
                                if string:
                                    regex = self.util.get_table_title_regex_1()
#                                    regex = ('(?i)required(.*?)keywords' + '|'
#                                             '(?i)optional(.*?)keywords' + '|'
#                                             '(?i)required(.*?)column'   + '|'
#                                             '(?i)optional(.*?)column'   + '|'
#                                             '(?i)sample(.*?)header'
#                                             )
                                    match = self.util.check_match(regex=regex,string=string)
                                    if match: found_table_title = True
                    found_table_title = not found_table_title if toggle else found_table_title
                    if not found_table_title:
                        self.correct_type = False
                        self.logger.debug("not there is a header table or data table " +
                                            "title in a <p> tag")
            else:
                self.ready = False
                self.logger.error('Unable to check_p_tag_assumptions_6. ' +
                                  'node: {}.'.format(node))

    def check_pre_tag_assumptions_1(self,node=None):
        '''Check <pre> tag assumptions.'''
        if self.ready:
            if node:
                # check node has <pre> tags
                if self.correct_type:
                    child_names = set(self.util.get_child_names(node=node))
                    if not 'pre' in child_names:
                        self.correct_type = False
                        self.logger.debug("not node has <pre> tags")
                self.check_tags_have_only_text_content(node=node,tag_names=['pre'])
                if self.correct_type:
                    pres = node.find_all('pre')
                    # check two or less pre tags
                    if len(pres) > 2:
                        self.correct_type = False
                        self.logger.error("not two or less pre tags")
                    else:
                        for pre in pres:
                            # check pre tag is a string with rows separated by '\n'
                            if self.correct_type:
                                rows = self.util.get_string(node=pre).split('\n')
                                if not rows:
                                    self.correct_type = False
                                    self.logger.error("not pre tag is a string with rows separated by '\n'")
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
                    if not 'pre' in child_names:
                        self.correct_type = False
                        self.logger.debug("not node has <pre> tags")
                self.check_tags_have_only_text_content(node=node,tag_names=['pre'])
                if self.correct_type:
                    pres = node.find_all('pre')
                    for pre in pres:
                        # check pre tag is a string with rows separated by '\n'
                        if self.correct_type:
                            rows = self.util.get_string(node=pre).split('\n')
                            if not rows:
                                self.correct_type = False
                                self.logger.error("not pre tag is a string with rows separated by '\n'")
            else:
                self.ready = False
                self.logger.error('Unable to check_pre_tag_assumptions_2. ' +
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
                    dl = node.find('dl')
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
                        if not (child_names == {'caption','thead','tbody'}
                                or
                                child_names == {'thead','tbody'}
                            ):
                            self.correct_type = False
                            self.logger.debug(
                                "not table.children = {caption,thead,tbody}"
                                " or {thead,tbody}")
                        # check <thead> has only one child <tr>,
                        # and all children of the <tr> tag are <th> tags
                        self.check_thead_tag_assumptions_1(table=table)
                        # check all children of the <tbody> tag are <tr> tags,
                        # all children of the <tr> tag are <td> tags,
                        # and each <tr> tag as exactly 4 <td> tag children
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
                        if not (child_names == {'caption','tr'}         or
                                child_names == {'tr'}                   or
                                child_names == {'caption','tr','tfoot'} or
                                child_names == {'tr','tfoot'}
                            ):
                            self.correct_type = False
                            self.logger.debug(
                                "not table.children = {caption,tr}")
                        # check all <tr> tag children are <th> or <td> tags
                        self.check_tr_tag_assumptions_1(table=table)
            else:
                self.ready = False
                self.logger.error('Unable to check_table_tag_assumptions_2. ' +
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
                    thead = table.find('thead')
                    child_names = self.util.get_child_names(node=thead)
                    if not child_names == ['tr']:
                        self.correct_type = False
                        self.logger.debug("not <thead> has only one child <tr>")
                # check all children of the <tr> tag are <th> tags
                if self.correct_type:
                    tr = thead.find('tr')
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
                    tbody = table.find('tbody')
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
                            self.logger.debug("not all children of the <tr> tag are <td> tags")
                # check each <tr> tag as exactly 4 <td> tag children
                if self.correct_type:
                    for tr in [tr for tr in tbody.children
                               if not self.util.get_string(node=tr).isspace()]:
                        if self.correct_type:
                            if not len(tr.find_all('td')) == 4:
#                                print('tr: %r' % tr)
#                                input('pause')
                                self.correct_type = False
                                self.logger.debug("not each <tr> tag as exactly 4 <td> tag children")
            else:
                self.ready = False
                self.logger.error('Unable to check_tbody_tag_assumptions_1. ' +
                                  'table: {}.'.format(table))

    def check_tbody_tag_assumptions_2(self,table=None):
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
                    tbody = table.find('tbody')
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
                            self.logger.debug("not all children of the <tr> tag are <td> tags")
            else:
                self.ready = False
                self.logger.error('Unable to check_tbody_tag_assumptions_2. ' +
                                  'table: {}.'.format(table))

    def check_tr_tag_assumptions_1(self,table=None):
        '''Check tbody tag assumptions for the given BeautifulSoup table.'''
        if self.ready:
            if table:
                # check all <tr> tag children are <th> or <td> tags
                if self.correct_type:
                    for node in [node for node in table.find_all('tr')
                                 if not self.util.get_string(node=node).isspace()]:
                        if self.correct_type:
                            tag_names = set(self.util.get_child_names(node=node))
                            if not (tag_names == {'td'} or tag_names == {'th'}):
                                self.correct_type = False
                                self.logger.debug("not all <tr> tag children are " +
                                                  "<th> or <td> tags" )
            else:
                self.ready = False
                self.logger.error('Unable to check_tr_tag_assumptions_1. ' +
                                  'table: {}.'.format(table))


class Intro_type(Type):
    '''Determine the class Intro type of the given node.'''
    def __init__(self,logger=None,options=None):
        Type.__init__(self,logger=logger,options=options)

    def get_intro_type(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        intro_type = None
        if self.ready:
            if node and node.name:
#                tag_names = set(self.util.get_child_names(node=node))
#                print('tag_names: %r' % tag_names)
#                input('pause')
                if   self.check_intro_type_1(node=node): intro_type = 1
                elif self.check_intro_type_2(node=node): intro_type = 2
                elif self.check_intro_type_3(node=node): intro_type = 3
                elif self.check_intro_type_4(node=node): intro_type = 4
                elif self.check_intro_type_5(node=node): intro_type = 5
                elif self.check_intro_type_6(node=node): intro_type = 6
                elif self.check_intro_type_7(node=node): intro_type = 7
                elif self.check_intro_type_8(node=node): intro_type = 8
                elif self.check_intro_type_9(node=node): intro_type = 9
                elif self.check_intro_type_10(node=node): intro_type = 10
                else:
                    self.ready = False
                    self.logger.error('Unable to get_intro_type. '
                                      'Unexpected intro_type.')
            if self.verbose: print('intro_type: %r' % intro_type )
        return intro_type

    def check_intro_type_1(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_1:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")
                # check tag_names = {h,p,div}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','div'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,div}")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.heading_tag_names)
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                self.check_middle_tags_h_p_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_1. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_2(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_2:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")

                # check tag_names = {h,dl}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'dl'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,dl}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check children of <dl> are <dt> and <dd>, which come in pairs
                self.check_dl_tag_assumptions_1(node=node,
                                                dl_child_names={'dt','dd','ul'})
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_2. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_3(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_3:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")
                # check tag_names = {h,dl}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'dl'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,dl}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check children of <dl> are <dt> and <dd>, which come in pairs
                self.check_dl_tag_assumptions_1(node=node,
                                                dl_child_names={'dt','dd'})
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_3. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_4(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_4:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")
                # check tag_names = {h,p,ul}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'ul','p'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,ul}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check all <ul> tags have only <li> tag children, containing a bold tag
                self.check_ul_tag_assumptions_1(node=node)
                # check a <p> tag contains a table title
                self.check_p_tag_assumptions_3(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_4. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_5(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_5:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")
                # check tag_names = {h,p,pre,table}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','pre','table'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,pre,table}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check two or less pre tags -- strings with rows separated by '\n'
                self.check_pre_tag_assumptions_1(node=node)
                # check <p> tag has zero or one <b> tag child
                self.check_p_tag_assumptions_5(node=node)
                # check <table> contains <tbody>,
                self.check_table_tag_assumptions_4(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_5. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_6(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_6:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")
                # check tag_names = {h,p,ul}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','ul'}
                            or
                            set_tag_names == (set_tag_names & self.heading_tag_names)
                                                | {'p'}
                        ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,ul}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                if 'ul' in tag_names:
                    # check lis contain file names
                    self.check_ul_tag_assumptions_2(node=node)
                # check <p> tag has zero or one <b> tag child
                self.check_p_tag_assumptions_5(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_6. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_7(self,node=None):
        '''Determine class File_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                children = node.children
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_7:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = list()
                if self.correct_type:
                    if not tag_names == list():
                        self.correct_type = False
                        self.logger.debug("not tag_names = list()")
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_7. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_8(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_8:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,p,table}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','table'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,table}")
                # check heading tag only has text content
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.heading_tag_names)
                # check all <p> tags before File Contents table have <b> tag children
                self.check_p_tag_assumptions_4(node=node)
                # check previous sibling of <table> is heading with text 'file contents'
                self.check_table_tag_assumptions_3(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_8. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_9(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_9:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")
                # check tag_names = {h,p,ul}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','ul','div'}
                        ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,ul}")
                # check heading tags only have text content
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.heading_tag_names)
                if 'ul' in tag_names:
                    # check all <ul> tags have only <li> tag children
                    self.check_ul_tag_assumptions_3(node=node)
                # check <p> tags only have text content
                self.check_tags_have_only_text_content(node=node,tag_names=['p'])
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_9. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_intro_type_10(self,node=None):
        '''Determine intro_type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_intro_type_10:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names is non-empty
                if self.correct_type:
                    if not tag_names:
                        self.correct_type = False
                        self.logger.debug("not tag_names is non-empty")
                # check tag_names = {h,p,pre}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','pre'}
                        ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,pre}")
                print
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check two or less pre tags -- strings with rows separated by '\n'
                self.check_pre_tag_assumptions_1(node=node)
                # check <p> tag has zero or one <b> tag child
                self.check_p_tag_assumptions_5(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_intro_type_10. ' +
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
                    if not (middle_tags == (middle_tags & self.heading_tag_names)
                                            | {'p'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not middle tags {h,p}, " +
                                          "allowing for [h,p], [h,p,p], etc.")
            else:
                self.ready = False
                self.logger.error('Unable to check_middle_tags_h_p_1. ' +
                                  'node: {}.'.format(node))

    def check_table_tag_assumptions_3(self,node=None):
        '''Check table tag assumptions for the given BeautifulSoup node.'''
        if self.ready:
            if node:
                # check 'table' in tag_names
                if self.correct_type:
                    tag_names = set(self.util.get_child_names(node=node))
                    if not 'table' in tag_names:
                        self.correct_type = False
                        self.logger.debug("not 'table' in tag_names")
                # check previous sibling of <table> is heading with text 'file contents'
                if self.correct_type:
                    table = node.find('table')
                    previous_siblings = [s for s in table.previous_siblings if s.name]
                    previous_sibling = previous_siblings[0] if previous_siblings else None
                    # check previous sibling of <table> is heading
                    if not (previous_sibling and previous_sibling.name in self.heading_tag_names):
                        self.correct_type = False
                        self.logger.debug(
                            "not previous sibling of <table> is heading")
                    else:
                        # check heading text is 'file contents'
                        strings = list(previous_sibling.strings)
                        string = strings[0] if len(strings) == 1 else str()
                        regex = '(?i)file contents'
                        if not (string and self.util.check_match(regex=regex,string=string)):
                            self.correct_type = False
                            self.logger.debug(
                                "not previous sibling of <table> is heading")
            else:
                self.ready = False
                self.logger.error('Unable to check_table_tag_assumptions_3. ' +
                                  'node: {}.'.format(node))

    def check_table_tag_assumptions_4(self,node=None):
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
                        if not (child_names == {'tr'}
                            ):
                            self.correct_type = False
                            self.logger.debug(
                                "not table.children = {caption,thead,tbody}"
                                " or {thead,tbody}")
                        # check all <tr> tag children are <th> or <td> tags
                        self.check_tr_tag_assumptions_1(table=table)
            else:
                self.ready = False
                self.logger.error('Unable to check_table_tag_assumptions_4. ' +
                                  'node: {}.'.format(node))



class Hdu_type(Type):
    '''Determine the class Hdu_type of the given node.'''
    def __init__(self,logger=None,options=None):
        Type.__init__(self,logger=logger,options=options)

    def get_hdu_type(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        hdu_type = None
        if self.ready:
            if node:
                # found in file_type=1, with divs
                tag_names = set(self.util.get_child_names(node=node))
                if   self.check_hdu_type_1(node=node): hdu_type = 1
                elif self.check_hdu_type_2(node=node): hdu_type = 2
                elif self.check_hdu_type_3(node=node): hdu_type = 3
                elif self.check_hdu_type_4(node=node): hdu_type = 4
                elif self.check_hdu_type_5(node=node): hdu_type = 5
                elif self.check_hdu_type_6(node=node): hdu_type = 6
                elif self.check_hdu_type_7(node=node): hdu_type = 7
                elif self.check_hdu_type_8(node=node): hdu_type = 8
                elif self.check_hdu_type_9(node=node): hdu_type = 9
                elif self.check_hdu_type_10(node=node): hdu_type = 10
                elif self.check_hdu_type_11(node=node): hdu_type = 11
                elif self.check_hdu_type_12(node=node): hdu_type = 12
                else:
                    self.ready = False
                    self.logger.error('Unable to get_hdu_type. '
                                      'Unexpected hdu_type.')

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
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','dl','table'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,ul,table}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check node has only one <p> tag
                self.check_p_tag_assumptions_1(node=node)
                if 'dl' in tag_names:
                    # check children of <dl> are <dt> and <dd>, which come in pairs
                    self.check_dl_tag_assumptions_1(node=node,
                                                    dl_child_names={'dt','dd'})
                    # check 'hdu', 'type' and 'size' are in the list elements of dts
                    self.check_hdu_dl_tag_assumptions_1(node=node)
                # check <table> contains <caption>, <thead> and <tbody>
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
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','table'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,table}")
                # check first child of node is heading tag,
                # and additional headings indicate header and binary table
                self.check_heading_tag_assumptions_1(node=node)
                # check last <p> tag has hdu table information
                self.check_p_tag_assumptions_2(node=node)
                # check <table> contains <caption>, <thead> and <tbody>
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
                self.logger.debug("First inconsistency for check_hdu_type_3:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,pre} or {h,pre}
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','pre'}
                        or
                        tag_names == (tag_names & self.heading_tag_names)
                                     | {'pre'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,pre} or {h,pre}")
                # check first child of node is heading tag,
                # and additional headings indicate header and binary table
                self.check_heading_tag_assumptions_1(node=node)
                if 'p' in tag_names:
                    self.check_tags_have_only_text_content(node=node,tag_names=['p'])
                # check two or less pre tags -- strings with rows separated by '\n'
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
                if not ((tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','table'})
                        or
                        (tag_names == (tag_names & self.heading_tag_names)
                                     | {'table'})
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,table} or {h,table}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check <table> contains <caption> and <tbody>
                self.check_table_tag_assumptions_2(node=node)
                if 'p' in tag_names:
                    self.check_tags_have_only_text_content(node=node,tag_names=['p'])
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
                # check tag_names = {h,p} or {h}
                if not ((tag_names == (tag_names & self.heading_tag_names)
                                     | {'p'})
                        or
                        tag_names == (tag_names & self.heading_tag_names)
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p} or {h}")
                self.check_tags_have_only_text_content(node=node,
                                                       tag_names=self.heading_tag_names)
                if 'p' in tag_names:
                    self.check_tags_have_only_text_content(node=node,tag_names=['p'])
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_5. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_6(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_6:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,ul,table}
                if not ((tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','ul','table'})
                         or
                         (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','ul'})
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,ul,table}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check there is NOT a header table or data table title in a <p> tag
                self.check_p_tag_assumptions_6(node=node,toggle=True)
                # check <ul> <li> tags after first <li> tag DOES NOT contain a bold tag
                self.check_ul_tag_assumptions_1(node=node,toggle=True)
                if 'table' in tag_names:
                    # check <table> contains <caption> and <tbody>
                    self.check_table_tag_assumptions_2(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_6. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_7(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = None
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_7:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,ul} or {h,ul}
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','ul'}
                        or
                        tag_names == (tag_names & self.heading_tag_names)
                                     | {'ul'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,ul} or {h,ul}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check there is a header table or data table title in a <p> tag
                self.check_p_tag_assumptions_6(node=node,toggle=False)
                # check <ul> <li> tags after first <li> tag DOES NOT contain a bold tag
                self.check_ul_tag_assumptions_1(node=node,toggle=False)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_7. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_8(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_8:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,table}
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','ul','table'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,table}")
                
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check last <p> tag has hdu table information
                self.check_p_tag_assumptions_2(node=node)
                # check all <ul> tags have only <li> tag children
                self.check_ul_tag_assumptions_3(node=node)
                # check <table> contains <caption>, <thead> and <tbody>
                self.check_table_tag_assumptions_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_8. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_9(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_9:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,table}
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','table'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,table}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check last <p> tag has hdu table information
                self.check_p_tag_assumptions_2(node=node)
                # check <table> contains <caption>, <thead> and <tbody>
                self.check_table_tag_assumptions_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_9. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_10(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = None
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_10:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,pre} or {h,pre}
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','pre'}
                        or
                        tag_names == (tag_names & self.heading_tag_names)
                                     | {'pre'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,pre} or {h,pre}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                if 'p' in tag_names:
                    # check there is NOT a header table or data table title in a <p> tag
                    self.check_p_tag_assumptions_6(node=node,toggle=True)
                # check two or less pre tags -- strings with rows separated by '\n'
                self.check_pre_tag_assumptions_1(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_10. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_11(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = None
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_11:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,pre} or {h,pre}
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','pre'}
                        or
                        tag_names == (tag_names & self.heading_tag_names)
                                     | {'pre'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,pre} or {h,pre}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check there is a header table or data table title in a <p> tag
                self.check_p_tag_assumptions_6(node=node,toggle=False)
                # check pre tag is a string with rows separated by '\n'
                self.check_pre_tag_assumptions_2(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_11. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_hdu_type_12(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_hdu_type_12:")
                tag_names = set(self.util.get_child_names(node=node))
                # check tag_names = {h,p,ul,table}
                if not (tag_names == (tag_names & self.heading_tag_names)
                                     | {'p','ul'}
                        ):
                    self.correct_type = False
                    self.logger.debug("not tag_names = {h,p,ul,table}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check there is NOT a header table or data table title in a <p> tag
                self.check_p_tag_assumptions_6(node=node,toggle=True)
                # check <ul> <li> tags after first <li> tag does contain a bold tag
                self.check_ul_tag_assumptions_1(node=node,toggle=False)
            else:
                self.ready = False
                self.logger.error('Unable to check_hdu_type_12. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

class File_type(Type):
    '''Determine the class File type of the given node.'''
    def __init__(self,logger=None,options=None):
        Type.__init__(self,logger=logger,options=options)

    def get_file_type(self,node=None):
        '''Determine class Hdu template type from the given BeautifulSoup node.'''
        file_type = None
        if self.ready:
            if node:
                if   self.check_file_type_1(node=node): file_type = 1
                elif self.check_file_type_2(node=node): file_type = 2
                elif self.check_file_type_3(node=node): file_type = 3
                elif self.check_file_type_4(node=node): file_type = 4
                elif self.check_file_type_5(node=node): file_type = 5
                elif self.check_file_type_6(node=node): file_type = 6
                else:
                    self.ready = False
                    self.logger.error('Unable to get_file_type. '
                                      'Unexpected file_type.')


            if self.verbose: print('file_type: %r' % file_type )
#            input('pause')
        return file_type

    def check_file_type_1(self,node=None):
        '''Determine class File_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_file_type_1:")
                # check if all children of node are <div> tags
                if not self.util.children_all_one_tag_type(node=node,tag_name='div'):
                    self.correct_type = False
                    self.logger.debug("not all children of node are <div> tags")
            else:
                self.ready = False
                self.logger.error('Unable to check_file_type_1. ' +
                                  'node: {}.'.format(node))
        return self.correct_type


    def check_file_type_2(self,node=None):
        '''Determine class File_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_file_type_2:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,p,ul}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','ul'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,ul}")
                # check node has zero or one heading tag
                self.check_heading_tag_assumptions_3(node=node)
                # check a <p> tag contains a table title
                self.check_p_tag_assumptions_3(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_file_type_2. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_file_type_3(self,node=None):
        '''Determine class File_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_file_type_3:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,p,pre,ul,table}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','pre','table'}
                            or
                            set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','pre'}
                            or
                            set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p'}
                            or
                            set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','pre','ul'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p,pre,ul,table}")
                # check HDU title in heading tag
                self.check_heading_tag_assumptions_2(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to check_file_type_3. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_file_type_4(self,node=None):
        '''Determine class File_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_file_type_4:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,p} or {h,p,ul} or {h,p,pre}
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p'}
                            or
                            set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','ul'}
                            or
                            set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','pre'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p} or {h,p,ul} or {h,p,pre}")
                # check there is NOT a heading tag with HDU title
                self.check_heading_tag_assumptions_2(node=node,toggle_found_hdu=True)
                # check there is NOT a header table or data table title in a <p> tag
                self.check_p_tag_assumptions_3(node=node,toggle_found_table_title=True)
            else:
                self.ready = False
                self.logger.error('Unable to check_file_type_4. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_file_type_5(self,node=None):
        '''Determine class File_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                children = node.children
                self.correct_type = True
                self.logger.debug("First inconsistency for check_file_type_5:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names == list()
                if self.correct_type:
                    if not tag_names == list():
                        self.correct_type = False
                        self.logger.debug("not tag_names = list()")
            else:
                self.ready = False
                self.logger.error('Unable to check_file_type_5. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

    def check_file_type_6(self,node=None):
        '''Determine class File_type template from the given BeautifulSoup node.'''
        self.correct_type = False
        if self.ready:
            if node:
                self.correct_type = True
                self.logger.debug("First inconsistency for check_file_type_6:")
                tag_names = self.util.get_child_names(node=node)
                # check tag_names = {h,p} 
                if self.correct_type:
                    set_tag_names = set(tag_names)
                    if not (set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p'}
                            or
                            set_tag_names == (set_tag_names & self.heading_tag_names)
                                              | {'p','pre'}
                            ):
                        self.correct_type = False
                        self.logger.debug("not tag_names = {h,p}")
                # check there is NOT a heading tag with HDU title
                self.check_heading_tag_assumptions_2(node=node,toggle_found_hdu=True)
                # check there is a header table or data table title in a <p> tag
                self.check_p_tag_assumptions_3(node=node,toggle_found_table_title=False)
            else:
                self.ready = False
                self.logger.error('Unable to check_file_type_6. ' +
                                  'node: {}.'.format(node))
        return self.correct_type

