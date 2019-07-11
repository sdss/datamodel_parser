from bs4 import BeautifulSoup, Tag, NavigableString
from re import search, compile, match
from string import punctuation
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
        self.ready = bool(self.logger       and
                          self.options      
                          )

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.heading_tag_names = {'h1','h2','h3','h4','h5','h6'}
            self.paragraph_tags = {'p'}
            self.bold_tags = {'b'}
            self.unordered_list_tags = {'ul'}
            self.description_list_tags ={'dl'}
            self.table_tags = {'table'}
            self.sections_strings = {'sections','file contents'}
            self.header_table_column_names = {}
            

    def get_table_title_regex_1(self):
        '''Get regex for table title with required/optional keywords/column etc,
            typically found in <p> tags.'''
        regex = ('(?i)required(.*?)keywords'            + '|'
                 '(?i)optional(.*?)keywords'            + '|'
                 '(?i)example\s*header'                 + '|'
                 '(?i)sample(.*?)header'                + '|'
                 '(?i)example(.*?)configuration file'   + '|'
                 '(?i)required(.*?)column'              + '|'
                 '(?i)optional(.*?)column'              + '|'
                 '(?i)column(.*?)name'
                 )
        return regex

    def get_table_title_regex_2(self):
        '''Get regex for table title with required/optional keywords and sample header,
            typically found in <p> tags.'''
        regex = ('(?i)required(.*?)keywords'            + '|'
                 '(?i)optional(.*?)keywords'            + '|'
                 '(?i)example\s*header'                 + '|'
                 '(?i)sample(.*?)header'                + '|'
                 '(?i)example(.*?)configuration file'
                 )
        return regex

    def get_table_title_regex_3(self):
        '''Get regex for table title with required/optional column and column name,
            typically found in <p> tags.'''
        regex = ('(?i)required(.*?)column' + '|'
                 '(?i)optional(.*?)column' + '|'
                 '(?i)column(.*?)name'
                 )
        return regex

    def get_table_title_regex_4(self):
        '''Get regex for table title typically found in heading tags.'''
        regex = ('(?i)primary\s*header' + '|'
                 '(?i)primary\s*hdu' + '|'
                 '(?i)primary\s*hdu\s*\d*' + '|'
                 '(?i)sample\s*header' + '|'
#                 '(?i)table\s*header' + '|'
#                 '(?i)enum\s*header' + '|'
                 '(?i)hdu\s*\d+'
                 )
        return regex

    def get_string(self,node=None):
        string = None
        if self.ready:
            if node:
                if isinstance(node,str):
                    string = node
                else:
                    n = self.get_number_descendants(node=node)
                    if n > 1:
                        node_contents = [str(x) for x in node.contents]
                        string = str().join(node_contents).strip()
#                        string = str(node).strip() # depricated way
                    elif (n == 1 and bool(node.string)):
                        string = str(node.string).strip()
                    else:
                        string = str()
            else:
                self.ready = False
                self.logger.error('Unable to get_string. ' +
                                  'node: {0}'.format(node))
        return string

    def get_number_descendants(self,node=None):
        '''Return True if BeautifulSoup object has descendants.'''
        number_descendants = None
        if self.ready:
            if node:
                number_descendants = 0
                if not (isinstance(node,NavigableString) or isinstance(node,str)):
                    for descendant in node.descendants:
                        if descendant: number_descendants += 1
            else:
                self.ready = False
                self.logger.error('Unable to get_number_descendants.' +
                                  'node: {}'.format(node))
        return number_descendants

    def get_child_names(self,node=None):
        '''Set a list of child for the given BeautifulSoup node.'''
        child_names = list()
        if self.ready:
            if node:
                for child in self.get_children(node=node):
                    if child.name: child_names.append(str(child.name))
                # remove irrelevant <br> tags
                child_names = [name for name in child_names if not name=='br']
            else:
                self.ready = False
                self.logger.error('Unable to get_child_names. ' +
                                  'node: {0}'.format(node))
        return child_names

    def children_all_one_tag_type(self,node=None,tag_name=None):
        '''Check all children of node are only one tag type with tag_name.'''
        all_one_tag_type = None
        if self.ready:
            if node and tag_name:
                all_one_tag_type = True
                children = self.get_children(node=node)
                if children:
                    for child in children:
                        if child.name and child.name != tag_name:
                            all_one_tag_type = False
#                            print('child: %r' % child)
#                            input('pause')
                else:
                    all_one_tag_type = False
            else:
                self.ready = False
                self.logger.error('Unable to children_all_one_tag_type. ' +
                                  'node: {}'.format(node)   +
                                  'tag_name: {}'.format(tag_name)
                                  )
        return all_one_tag_type

    def get_sibling_names(self,node=None):
        '''Set a list of child for the given BeautifulSoup node.'''
        sibling_names = list()
        if self.ready:
            if node:
                for sibling in [sibling for sibling in node.next_siblings if sibling.name]:
                    sibling_names.append(str(sibling.name))
            else:
                self.ready = False
                self.logger.error('Unable to get_sibling_names. ' +
                                  'node: {0}'.format(node))
        return sibling_names

    def get_parent_names(self,node=None):
        '''Set a list of parents for the given BeautifulSoup node.'''
        parent_names = None
        if self.ready:
            if node:
                parent_names = list()
                for parent in node.parents:
                    if parent.name: parent_names.append(parent.name)
            else:
                self.ready = False
                self.logger.error('Unable to set_parent_names. ' +
                                  'node: {0}'.format(node))
        return parent_names

    def get_dts_and_dds_from_dl(self,dl=None):
        '''From the given HTML description list <dl> Beautiful soup object,
        get Python lists for the associated definition tags <dt> and
        description tags <dd>.'''
        dts  = list()
        dds = list()
        if self.ready:
            if dl:
                first_dt = True
                dd = list()
                children = self.get_children(node=dl)
                for child in children:
                    if self.ready:
                        if child.name == 'dt':
                            dts.append(self.get_string(node=child).strip())
                            if first_dt:
                                first_dt = False
                            else:
                                 dds.append('\n'.join(dd))
                                 dd = list()
                        elif child.name == 'dd':
                            dd.append(self.get_string(node=child).strip())
                        else:
                            self.ready = False
                            self.logger.error('Unable to get_dts_and_dds_from_dl. ' +
                                              'Unexpected child.name: {} '.format(child.name))
                dds.append('\n'.join(dd))
            else:
                self.ready = False
                self.logger.error('Unable to get_dts_and_dds_from_dl. ' +
                                  'dl: {}.'.format(dl))
        return (dts,dds)

    def get_titles_and_descriptions_from_ps_1(self,node=None):
        '''From the given list of BeautifulSoup <p> tag objects,
        get Python lists for the associated titles and descriptions
        '''
        titles  = list()
        descriptions = list()
        if self.ready:
            if node:
                ps = node.find_all('p')
                for p in ps:
                    (title,description) = self.get_title_and_description_from_p(p=p)
                    if title or description:
                        titles.append(title)
                        descriptions.append(description)
            else:
                self.ready = False
                self.logger.error('Unable to get_titles_and_descriptions_from_ps_1. ' +
                                  'node: {}'.format(node))
        if not (titles and descriptions) and len(titles)==len(descriptions):
            self.ready = False
            self.logger.error('Unable to get_titles_and_descriptions_from_ps_1. ' +
                              'titles: {}, '.format(titles) +
                              'descriptions: {}, '.format(descriptions) +
                              'len(titles): {}, '.format(len(titles)) +
                              'len(descriptions): {}.'.format(len(descriptions))
                              )
        return (titles,descriptions)

    def get_titles_and_descriptions_from_ps_2(self,node=None,sibling_tag_names=None):
        '''From the given list of BeautifulSoup <p> tag objects,
        get Python lists for the associated titles and descriptions
        '''
        titles  = list()
        descriptions = list()
        if self.ready:
            if node and sibling_tag_names:
                children = self.get_children(node=node)
                is_first_title = True
                desc = list()
                for child in children:
#                    print('\nchild: %r' % child)
#                    input('pause')
                    if child.name in self.heading_tag_names:
                        title = self.get_string(node=child)
                        titles.append(title)
                        descriptions.append(str())
                    elif child.name == 'p':
                        (title,description) = self.get_title_and_description_from_p(p=child)
                        titles.append(title)
                        if is_first_title:
                            is_first_title = False
                            desc.append(description)
                        else:
                            descriptions.append('\n'.join(desc))
                            desc=list()
                            desc.append(description)
                    elif child.name in sibling_tag_names:
                        desc.append(str(child))
#                    print('titles: %r' % titles)
#                    print('desc: %r' % desc)
#                    print('descriptions: %r' % descriptions)
#                    input('pause')
                descriptions.append('\n'.join(desc))
            else:
                self.ready = False
                self.logger.error('Unable to get_titles_and_descriptions_from_ps_2. ' +
                                  'node: {}'.format(node) +
                                  'sibling_tag_names: {}'.format(sibling_tag_names)
                                  )
        if not (titles and descriptions) and len(titles)==len(descriptions):
            self.ready = False
            self.logger.error('Unable to get_titles_and_descriptions_from_ps_2. ' +
                              'titles: {}, '.format(titles) +
                              'descriptions: {}, '.format(descriptions) +
                              'len(titles): {}, '.format(len(titles)) +
                              'len(descriptions): {}.'.format(len(descriptions))
                              )
        return (titles,descriptions)

    def get_title_and_description_from_p(self,p=None):
        '''From the given list of BeautifulSoup <p> tag objects,
        get Python lists for the associated titles and descriptions
        '''
        title = str()
        description = str()
        if p:
            child_names = self.get_child_names(node=p)
            if child_names:
                if child_names[0] == 'b':
                    b = p.find('b')
                    if b:
                        # title
                        title = self.get_string(node=b) if b else str()
                        title = title.replace(':','') if title else str()
                    
                        # description
                        description_list = list()
                        for sibling in b.next_siblings:
                            string = str(sibling).strip()
                            description_list.append(string)
                        description = ' '.join(description_list)
                    else:
                        title = str()
                        description = self.get_string(node=p)
                else:
                    title = str()
                    description = self.get_string(node=p)
            else:
                title = str()
                description = self.get_string(node=p)
        else:
            self.ready = False
            self.logger.error('Unable to get_title_and_description_from_p. ' +
                              'p: {}'.format(p))
        if not (title and description): pass # can be empty if no <b> tag
        return (title,description)

    def get_titles_and_descriptions_1(self,node=None):
        '''From the given BeautifulSoup node, get Python lists for the associated
            titles and descriptions, comprised of the heading strings and the tags
            inbetween the headings, respectively.
        '''
        titles  = list()
        descriptions = list()
        if self.ready:
            if node:
                children = self.get_children(node=node)
                if children:
                    is_first_title = True
                    second_title = True
                    description_list = list()
                    for child in children:
                        if self.ready:
#                            print('\n\n child: %r'%  child)
#                            print('self.ready: %r'%  self.ready)
#                            input('pause')
                            if child.name == 'div': break # don't add Sections div
                            elif child.name in self.heading_tag_names:
                                if is_first_title:
                                    is_first_title = False
                                    continue
                                elif second_title:
                                    second_title = False
                                    title = (self.get_string(node=child)
                                             if child else None)
                                    if title: titles.append(title)
                                else:
                                    description = '\n\n'.join(description_list)
                                    description_list = list()
                                    title = (self.get_string(node=child)
                                             if child else None)
                                    if title: titles.append(title)
                                    if description: descriptions.append(description)
                            else:
                                description_list.append(self.get_string(node=child))
                    if description_list:
                        description = '\n\n'.join(description_list)
                        descriptions.append(description)
                else:
                    self.ready = False
                    self.logger.error('Unable to get_titles_and_descriptions_1. ' +
                                      'children: {}'.format(children))
            else:
                self.ready = False
                self.logger.error('Unable to get_titles_and_descriptions_1. ' +
                                  'node: {}'.format(node))
        if not (titles and descriptions) and len(titles)==len(descriptions):
            self.ready = False
            self.logger.error('Unable to get_titles_and_descriptions_from_ps_1. ' +
                              'titles: {}, '.format(titles) +
                              'descriptions: {}, '.format(descriptions) +
                              'len(titles): {}, '.format(len(titles)) +
                              'len(descriptions): {}.'.format(len(descriptions))
                              )
#        print('titles: %r' % titles)
#        print('descriptions: %r' % descriptions)
#        print('self.ready: %r' % self.ready)
#        input('pause')
        return (titles,descriptions)

    def get_string_from_middle_children_1(self,node=None):
        '''Combine strings of tags into one string, excluding first heading tag
            and table tags.'''
        string = None
        if self.ready:
            if node:
                children = self.get_children(node=node)
                if children:
                    # remove table tags from children
                    children = [c for c in children if c.name != 'table']

                    # remove the first child if heading tag
                    if children[0].name in self.heading_tag_names:
                        children = children[1:]
                    else:
                        self.ready = False
                        self.logger.error('Unable to get_string_from_middle_children_1. ' +
                                          'first tag not in self.heading_tag_names. ' +
                                          'children: {}. '.format(children))
                    if self.ready:
                        string = '\n\n'.join([self.get_string(node=child)
                                              for child in children])
                else:
                    self.ready = False
                    self.logger.error('Unable to get_string_from_middle_children_1. ' +
                                      'children: {}.'.format(children)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_string_from_middle_children_1. ' +
                                  'node: {}.'.format(node)
                                  )
        return string

    def check_found_hdus(self,title=str(),description=str()):
        '''Check if the title and description indicates the hdus have been found.'''
        found_hdus = False
        if title or description:
            split_title = set([s.lower() for s in title.split()])
            description_title = set([s.lower() for s in description.split()])
            string_set = split_title | description_title
            if ({'required','keywords'}.issubset(string_set) or
                {'required','column'}.issubset(string_set)
                ):
                found_hdus = True
        else:
            self.ready = False
            self.logger.error('Unable to check_found_hdus. ' +
                              'title: {}, '.format(title) +
                              'description: {}.'.format(description)
                              )
        return found_hdus

    def get_hdu_number_and_hdu_title_from_heading_tag(self,node=None):
        '''Get hdu_number and hdu_title from first heading tag in BeautifulSoup node.'''
        (hdu_number,hdu_title) = (None,None)
        if self.ready:
            if node:
                child_names = self.get_child_names(node=node) if node else None
                heading_tag_names = [name for name in child_names
                                    if name in self.heading_tag_names] if child_names else None
                heading_tag_name = heading_tag_names[0] if heading_tag_names else None
                heading_tag = node.find(heading_tag_name) if heading_tag_name else None
                heading = self.get_string(node=heading_tag).strip() if heading_tag else None
                if heading_tag and heading:
                    # hdu_number
                    # hdu_number from node['id']
                    node_id = (node.attrs['id']
                               if node.attrs and 'id' in node.attrs else str())
                    regex = '(?i)hdu\s*\d+'
                    matches1 = self.get_matches(regex=regex,string=node_id) if node_id else list()
                    match1 = matches1[0] if matches1 else str()
                    regex = '\d+'
                    matches2 = self.get_matches(regex=regex,string=match1) if match1 else None
                    node_id_hdu_number = int(matches2[0]) if matches2 else None

                    # hdu_number from heading_tag['id']
                    heading_id = (heading_tag.attrs['id']
                               if heading_tag.attrs and 'id' in heading_tag.attrs else str())
                    regex = '(?i)hdu\s*\d+'
                    matches3 = self.get_matches(regex=regex,string=heading_id) if heading_id else list()
                    match2 = matches3[0] if matches3 else str()
                    regex = '\d+'
                    matches4 = self.get_matches(regex=regex,string=match2) if match2 else None
                    heading_id_hdu_number = int(matches4[0]) if matches4 else None

                    # hdu_number from hdu_title
                    regex = '(?i)hdu\s*\d+'
                    matches5 = (self.get_matches(regex=regex,string=heading)
                                if heading else list())
                    heading_hdu_N = matches5[0] if matches5 else str()
                    regex = '\d+'
                    matches6 = (self.get_matches(regex=regex,string=heading_hdu_N)
                                if heading_hdu_N else list())
                    heading_hdu_number = int(matches6[0]) if matches6 else None
                    
                    if heading_hdu_number is None:
                        regex = '(?i)primary'
                        heading_hdu_number = ('0' if self.check_match(regex=regex,string=heading)
                                              else None)

                    # put hdu_number together
                    hdu_number = (node_id_hdu_number
                                    if node_id_hdu_number is not None
                                  else heading_id_hdu_number
                                    if heading_id_hdu_number is not None
                                  else heading_hdu_number
                                    if heading_hdu_number is not None
                                  else None)
                                  
                    # put hdu_title together
                    hdu_title = heading.strip()

#                    print('\nnode_id: %r' % node_id)
#                    print('matches1: %r' % matches1)
#                    print('match1: %r' % match1)
#                    print('matches2: %r' % matches2)
#                    print('node_id_hdu_number: %r' % node_id_hdu_number)
#
#                    print('\nheading_id: %r' % heading_id)
#                    print('matches3: %r' % matches3)
#                    print('match2: %r' % match2)
#                    print('matches4: %r' % matches4)
#                    print('heading_id_hdu_number: %r' % heading_id_hdu_number)
#
#                    print('\nheading: %r' % heading)
#                    print('matches5: %r' % matches5)
#                    print('heading_hdu_N: %r' % heading_hdu_N)
#                    print('matches6: %r' % matches6)
#                    print('heading_hdu_number: %r' % heading_hdu_number)
#
#                    print('\nhdu_number: %r' % hdu_number)
#                    print('hdu_title: %r' % hdu_title)
#                    input('pause')


                else:
                    self.ready = False
                    self.logger.error('Unable to get_hdu_number_and_hdu_title_from_heading_tag from first heading. ' +
                                      'heading_tag: {}, '.format(heading_tag) +
                                      'heading: {}.'.format(heading)
                                      )
                if (hdu_number,hdu_title) == (None,None):
                    self.ready = False
                    self.logger.error('Unable to get_hdu_number_and_hdu_title_from_heading_tag. ' +
                                      'hdu_number: {}, '.format(hdu_number) +
                                      'hdu_title: {}'.format(hdu_title)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_hdu_number_and_hdu_title_from_heading_tag. ' +
                                  'node: {} '.format(node) )
        return (hdu_number,hdu_title)

    def get_hdu_number_and_hdu_title_from_p_tags_1(self,node=None):
        '''Get hdu_number and hdu_title from first heading tag in BeautifulSoup node.'''
        (hdu_number,hdu_title) = (None,None)
        if self.ready:
            if node:
                hdu_numbers = list()
                for p in node.find_all('p'):
                    (title,description) = self.get_title_and_description_from_p(p=p)
                    if title:
                        regex1 = self.get_table_title_regex_1()
#                        regex1 = ('(?i)Required(.*?)keywords' + '|'
#                                 '(?i)Required(.*?)column\s*names' )
                        regex2 = '(?i)hdu\s*\d+'
                        match1 = (self.check_match(regex=regex1,string=title)
                                  if title else None)
                        matches2 = (self.get_matches(regex=regex2,string=title)
                                  if title else None)
                        match2 = matches2[0] if matches2 else None
                        if match1:
                            if not match2:
                                hdu_numbers.append(0)
                            else:
                                regex3 = '\d+'
                                matches3 = (self.get_matches(regex=regex3,string=title)
                                          if title else None)
                                match3 = matches3[0] if matches3 else None
                                if match3:
                                    hdu_numbers.append(match3)
                if len(set(hdu_numbers)) == 1: # if all entries in hdu_numbers are the same
                    hdu_number = hdu_numbers[0]
                    hdu_title = 'HDU' + str(hdu_number)
                if (hdu_number,hdu_title) == (None,None):
                    self.ready = False
                    self.logger.error('Unable to get_hdu_number_and_hdu_title_from_p_tags_1. ' +
                                      'hdu_number: {}, '.format(hdu_number) +
                                      'hdu_title: {}'.format(hdu_title)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_hdu_number_and_hdu_title_from_p_tags_1. ' +
                                  'node: {} '.format(node) )
        return (hdu_number,hdu_title)

    def get_single_digit(self,string=None):
        '''Get single digit 0-9 from the given string.'''
        digit = None
        if self.ready:
            if string:
                digits = list(filter(str.isdigit, string))
                if len(digits) == 1:
                    digit = int(digits[0])
                else:
                    self.ready = False
                    self.logger.error('Unable to get_single_digit. ' +
                                      'len(digits) > 1. ' +
                                      'digits: {}, '.format(digits) +
                                      'string: {}'.format(string))
            else:
                self.ready = False
                self.logger.error('Unable to get_single_digit. ' +
                                  'string: {0}'.format(string))
        return digit

    def get_hdu_divs(self,node=None):
        '''Get a list of divs with id containing 'hdu', from the given node.'''
        hdu_divs = list()
        if self.ready:
            if node:
                divs = node.find_all('div')
                for div in [div for div in divs
                            if not self.get_string(node=div).isspace()]:
                    div_id = (div.attrs['id']
                               if div.attrs and 'id' in div.attrs else None)
                    if div_id and div_id.lower().startswith('hdu'):
                        hdu_divs.append(div)
            else:
                self.ready = False
                self.logger.error('Unable to get_hdu_divs. ' +
                                  'node: {}'.format(node))
        return hdu_divs

    def get_intro_div(self,node=None):
        '''Get a list of divs with id containing 'intro', from the given node.'''
        intro_divs = list()
        if self.ready:
            if node:
                # create intro_divs list
                divs = node.find_all('div')
                for div in [div for div in divs
                            if not self.get_string(node=div).isspace()]:
                    div_id = (div.attrs['id']
                               if div.attrs and 'id' in div.attrs else None)
                    if div_id and div_id.startswith('intro'):
                        intro_divs.append(div)
                # check one and only one intro div
                if not intro_divs:
                    self.ready = False
                    self.logger.error("Unable to get_intro_divs. " +
                                      "Not found: 'intro' in div['id']. " +
                                      "intro_divs: {}".format(intro_divs)
                                      )
                if len(intro_divs) > 1:
                    self.ready = False
                    self.logger.error("Unable to get_intro_divs. " +
                                      "len(intro_divs) > 1. " +
                                      "intro_divs: {}".format(intro_divs)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_div. ' +
                                  'node: {}'.format(node))
        return intro_divs[0] if self.ready else None

    def get_heading_tag_sibling_names(self,node=None):
        '''Get a list of heading tags, which are siblings of the given node.'''
        heading_tags = list()
        if self.ready:
            if node:
                siblings = set(self.get_sibling_names(node=node))
                heading_tags = list(set(self.heading_tag_names) & siblings)
            else:
                self.ready = False
                self.logger.error('Unable to get_heading_tag_sibling_names. ' +
                                  'node: {0}'.format(node))
        return heading_tags

    def get_heading_tag_child_names(self,node=None):
        '''Get a list of heading tags, which are children of the given node.'''
        heading_tag_names = list()
        if self.ready:
            if node:
                children = self.get_child_names(node=node)
                heading_tag_names = [child for child in children
                                if child in self.heading_tag_names]
            else:
                self.ready = False
                self.logger.error('Unable to get_heading_tag_child_names. ' +
                                  'node: {0}'.format(node))
        return heading_tag_names

    def get_heading_tag_children(self,node=None):
        '''Get a list of heading tags, which are children of the given node.'''
        heading_tags = list()
        if self.ready:
            if node:
                heading_tags = [c for c in node.children
                                if c.name and c.name in self.heading_tag_names]
            else:
                self.ready = False
                self.logger.error('Unable to get_heading_tag_child_names. ' +
                                  'node: {0}'.format(node))
        return heading_tags

    def get_all_strings(self,node=None):
        '''Get all strings from the given BeautifulSoup node.'''
        all_strings = list()
        if self.ready:
            if node:
                for string in [str(s) for s in node.strings if not s.isspace()]:
                    all_strings.append(str(string))
            else:
                self.ready = False
                self.logger.error('Unable to get_all_strings. ' +
                                  'node: {0}'.format(node))
        return all_strings

    def get_datatype_and_hdu_size(self,node=None):
        '''Get datatype and hdu_size from the given BeautifulSoup node.'''
        (datatype,hdu_size) = (None,None)
        if self.ready:
            if node:
                all_strings = self.get_all_strings(node=node)
                if self.check_match(regex='(?i)hdu type',string=all_strings[0]):
                    datatype = all_strings[1].strip().strip(punctuation).strip()
                if self.check_match(regex='(?i)hdu size',string=all_strings[2]):
                    hdu_size = all_strings[3].strip().strip(punctuation).strip()
            else:
                self.ready = False
                self.logger.error('Unable to get_datatype_and_hdu_size. ' +
                                  'node: {0}'.format(node))
            if (datatype,hdu_size) == (None,None):
                self.ready = False
                self.logger.error('Unable to get_datatype_and_hdu_size. ' +
                                  'datatype: {0}. '.format(datatype) +
                                  'hdu_size: {0}. '.format(hdu_size)
                                  )
        return (datatype,hdu_size)

    def get_datatype_and_hdu_size_from_dl(self,dl=None):
        '''Get datatype and hdu_size from the given BeautifulSoup dl tag.'''
        (datatype,hdu_size)=(None,None)
        if self.ready:
            if dl:
                (definitions,descriptions) = self.get_dts_and_dds_from_dl(dl=dl)
                for (definition,description) in list(zip(definitions,descriptions)):
                    if 'hdu type' in definition.lower(): datatype = description
                    if 'hdu size' in definition.lower(): hdu_size = description
            else:
                self.ready = False
                self.logger.error('Unable to get_datatype_and_hdu_size_from_dl. ' +
                                  'dl: {0}'.format(dl))
        return (datatype,hdu_size)

    def get_children(self,node=None,names=list()):
        '''Get the children from the BeautifulSoup node, excluding line endings.'''
        children = None
        if self.ready:
            if node:
#                children = ([child for child in node.children if child.name in names]
#                            if names else
#                            [child for child in node.children
#                             if str(child) and not str(child).isspace()]
#                            )
                children = ([child for child in node.children
                             if child.name and child.name in names]
                            if names else
                            [child for child in node.children if child.name])
            else:
                self.ready = False
                self.logger.error('Unable to get_children. ' +
                                  'node: {0}'.format(node))
        return children
    
    def get_intro_and_hdus(self,node=None,file_type=None):
        '''Get new BeautifulSoup objects comprised of the intro tags and hdu tags
            of the given BeautifulSoup node.'''
        (intro,hdus) = (None,None)
        if self.ready:
#            print('file_type: %r' % file_type)
#            input('pause')
            if node and file_type:
                if   file_type == 1: (intro,hdus) = self.get_intro_and_hdus_1(node=node)
                elif file_type == 2: (intro,hdus) = self.get_intro_and_hdus_2(node=node)
                elif file_type == 3: (intro,hdus) = self.get_intro_and_hdus_3(node=node)
                elif file_type == 4: (intro,hdus) = self.get_intro_and_hdus_4(node=node)
                elif file_type == 5: (intro,hdus) = self.get_intro_and_hdus_4(node=node)
                elif file_type == 6: (intro,hdus) = self.get_intro_and_hdus_5(node=node)
                else:
                    self.ready = False
                    self.logger.error('Unable to get_intro_and_hdus. '
                                      'Unexpected file_type.')
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_hdus. ' +
                                  'bool(node): {}, '.format(bool(node)) +
                                  'file_type: {}.'.format(file_type))
        return (intro,hdus)

    def get_intro_and_hdus_1(self,node=None):
        '''Get new BeautifulSoup objects comprised of the intro tags and hdu tags
            of the given BeautifulSoup node.'''
        (intro,hdus) = (None,None)
        if self.ready:
            if node:
                intro = self.get_intro_div(node=node)
                hdus  = self.get_hdu_divs(node=node)
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_hdus_1. ' +
                                  'bool(node): {}, '.format(bool(node))
                                  )
        return (intro,hdus)

    def get_intro_and_hdus_2(self,node=None):
        '''Get new BeautifulSoup objects comprised of the intro tags and hdu tags
            of the given BeautifulSoup node.'''
        (intro,hdus) = (None,None)
        if self.ready:
            if node:
                regex = self.get_table_title_regex_1()
#                regex = ('(?i)required\s+header\s+keywords'     + '|'
#                         '(?i)required\s+column\s+names'        + '|'
#                         '(?i)required\s+hdu\s*\d*\s+keywords'  + '|'
#                         '(?i)required\s+hdu\s*\d*\s+column\s+names'
#                         )
                (intro,combined_hdus) = self.get_intro_and_combined_hdus_2(node=node,regex=regex)
                hdus = self.get_split_hdus_2(node=combined_hdus) if combined_hdus else None
#                print('\nintro: %r' % intro)
#                print('\ncombined_hdus: %r' % combined_hdus)
#                print('hdus: %r' % hdus)
#                print('bool(intro): %r' % bool(intro))
#                print('bool(combined_hdus): %r' % bool(combined_hdus))
#                print('bool(hdus): %r' % bool(hdus))
#                input('pause')
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_hdus_2. ' +
                                  'node: {}, '.format(node)
                                  )
        return (intro,hdus)

    def get_intro_and_hdus_3(self,node=None):
        '''Get new BeautifulSoup objects comprised of the intro tags and hdu tags
            of the given BeautifulSoup node.'''
        (intro,hdus) = (None,None)
        if self.ready:
            if node:
                regex = self.get_table_title_regex_4()
#                regex = ('(?i)primary\s*header' + '|'
#                         '(?i)primary\s*hdu' + '|'
#                         '(?i)primary\s*hdu\s*\d*' + '|'
#                         '(?i)hdu\s*\d+'
#                         )
                (intro,combined_hdus) = self.get_intro_and_combined_hdus_3(node=node,regex=regex)
                hdus = (self.get_split_hdus_3(node=combined_hdus,regex=regex)
                        if combined_hdus and regex else None)
#                print('\nintro: %r' % intro)
#                print('\ncombined_hdus: %r' % combined_hdus)
#                print('hdus: %r' % hdus)
#                print('bool(intro): %r' % bool(intro))
#                print('bool(combined_hdus): %r' % bool(combined_hdus))
#                print('bool(hdus): %r' % bool(hdus))
#                print('!!!!!!!! HI get_intro_and_hdus_3 !!!!!!!!')
#                input('pause')
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_hdus_3. ' +
                                  'node: {}, '.format(node)
                                  )
        return (intro,hdus)

    def get_intro_and_hdus_4(self,node=None):
        '''Get new BeautifulSoup objects comprised of the intro tags and hdu tags
            of the given BeautifulSoup node.'''
        (intro,hdus) = (None,None)
        if self.ready:
            if node:
                intro = node
                hdus = None # There's no hdu's for this file type
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_hdus_4. ' +
                                  'node: {}, '.format(node)
                                  )
        return (intro,hdus)

    def get_intro_and_hdus_5(self,node=None):
        '''Get new BeautifulSoup objects comprised of the intro tags and hdu tags
            of the given BeautifulSoup node.'''
        (intro,hdus) = (None,None)
        if self.ready:
            if node:
                regex = self.get_table_title_regex_1()
#                regex = ('(?i)required(.*?)keywords' + '|'
#                         '(?i)optional(.*?)keywords' + '|'
#                         '(?i)required(.*?)column'   + '|'
#                         '(?i)optional(.*?)column'   + '|'
#                         '(?i)sample(.*?)header'
#                         )
                (intro,combined_hdus) = (self.get_intro_and_combined_hdus_2(node=node,regex=regex)
                                         if node and regex else None)
                hdus = (self.get_split_hdus_3(node=combined_hdus,regex=regex)
                        if combined_hdus and regex else None)
#                print('\nintro: %r' % intro)
#                print('\ncombined_hdus: %r' % combined_hdus)
#                print('hdus: %r' % hdus)
#                print('bool(intro): %r' % bool(intro))
#                print('bool(combined_hdus): %r' % bool(combined_hdus))
#                print('bool(hdus): %r' % bool(hdus))
#                input('pause')
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_hdus_5. ' +
                                  'node: {}, '.format(node)
                                  )
        return (intro,hdus)



    def get_intro_and_combined_hdus_2(self,node=None,regex=None):
        '''Get a new BeautifulSoup object comprised of the intro tags
            of the given BeautifulSoup node.'''
        (intro,combined_hdus) = (None,None)
        if self.ready:
            if node and regex:
                previous_siblings = None
                next_siblings = None
                ps = node.find_all('p')
                for p in ps:
                    (title,description) = self.get_title_and_description_from_p(p=p)
                    if title:
                        if self.check_match(regex=regex,string=title):
                            previous_siblings = p.previous_siblings
                            next_siblings = p.previous_sibling.next_siblings
                            break
                intro = (self.get_soup_from_iterator(iterator=previous_siblings,
                                                        reverse=True)
                        if previous_siblings else None)
                combined_hdus = (self.get_soup_from_iterator(iterator=next_siblings,
                                                             reverse=False)
                                 if next_siblings else None)
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_combined_hdus_2. ' +
                                  'node: {}'.format(node) +
                                  'regex: {}'.format(regex)
                                  )
        return (intro,combined_hdus)

    def get_intro_and_combined_hdus_3(self,node=None,regex=None):
        '''Get a new BeautifulSoup object comprised of the intro tags
            of the given BeautifulSoup node.'''
        (intro,combined_hdus) = (None,None)
        if self.ready:
            if node and regex:
                previous_siblings = None
                next_siblings = None
                heading_tags = self.get_heading_tag_children(node=node)
                for heading_tag in heading_tags:
                    strings=list(heading_tag.strings) if heading_tag else list()
                    string = ' '.join(strings) if strings else str()
                    if string:
                        if self.check_match(regex=regex,string=string):
                            previous_siblings = heading_tag.previous_siblings
                            next_siblings = heading_tag.previous_sibling.next_siblings
                            break
                if previous_siblings and next_siblings:
                    intro = self.get_soup_from_iterator(iterator=previous_siblings,
                                                         reverse=True)
                    combined_hdus = self.get_soup_from_iterator(iterator=next_siblings,
                                                                 reverse=False)
                else:
                    self.ready = False
                    self.logger.error('Unable to get_intro_and_combined_hdus_3. ' +
                                      'previous_siblings: {}, '.format(previous_siblings) +
                                      'combined_hdus: {}.'.format(combined_hdus)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_intro_and_combined_hdus_3. ' +
                                  'node: {}'.format(node) +
                                  'regex: {}'.format(regex)
                                  )
        return (intro,combined_hdus)

    def get_soup_from_iterator(self,iterator=None,reverse=False):
        '''Create a list out of the iterator, reverse the order if reverse==True,
        and create new BeautifulSoup object out of the list text.'''
        soup = None
        if iterator and isinstance(reverse,bool):
            siblings = [str(s) for s in iterator if s and not str(s).isspace()]
            if reverse: siblings.reverse() if siblings else list()
            text = '\n\n'.join(siblings) if siblings else str()
            soup = BeautifulSoup(text, 'html.parser') if text else None
        else:
            self.ready = False
            self.logger.error('Unable to get_soup_from_iterator. ' +
                              'iterator: {}, '.format(iterator) +
                              'isinstance(reverse,bool): {}'
                                .format(isinstance(reverse,bool))
                              )
        return soup

    def get_next_sibling(self,node=None):
        '''Get the next sibling of the given BeautifulSoup node.'''
        next_sibling = None
        if self.ready:
            if node:
                next_siblings = [s for s in node.next_siblings
                                 if s and not str(s).isspace()]
                next_sibling = next_siblings[0] if next_siblings else None
            else:
                self.ready = False
                self.logger.error('Unable to get_next_sibling. ' +
                                  'node: {}'.format(node)
                                  )
        return next_sibling



    def get_split_hdus_2(self,node=None):
        '''Split the node into a list of BeautifulSoup objects containing file HDUs.'''
        hdus = list()
        if self.ready:
            if node:
                children = self.get_children(node=node)
                if children:
                    is_first_title = True
                    hdu = list()
                    for child in children:
                        if self.ready:
#                            print('\n\n@@@@@@@ HI child @@@@@@@')
#                            print('child: %r'%  child)
#                            input('pause')
                            if child.name == 'p':
                                (title,description) = (
                                    self.get_title_and_description_from_p(p=child))
                                if title:
                                    regex1 = self.get_table_title_regex_1()
#                                    regex1 = ('(?i)required(.*?)keywords' + '|'
#                                             '(?i)optional(.*?)keywords' + '|'
#                                             '(?i)required(.*?)column'   + '|'
#                                             '(?i)optional(.*?)column'
#                                             )
                                    regex2 = '(?i)hdu\s*\d+'
                                    match1 = (self.check_match(regex=regex1,string=title)
                                              if title else None)
                                    matches2 = (self.get_matches(regex=regex2,string=title)
                                              if title else None)
                                    match2 = matches2[0] if matches2 else 'no match'
#                                    print('match2: %r' %  match2)
                                    if match1:
                                        if is_first_title:
                                            is_first_title = False
                                            previous_match2 = match2
                                            hdu.append(child)

#                                            print('\n\n^^^^^^^ HI is_first_title ^^^^^^^')
#                                            print('hdu: %r' %  hdu)
#                                            input('pause')
                                        # when same hdu_k for header and data tables
                                        elif previous_match2 == match2:
                                            hdu.append(child)

#                                            print('\n\n%%% HI previous_match2 == match2 %%%%%%')
#                                            print('hdu: %r' %  hdu)
#                                            input('pause')
                                        else:
#                                            print('\n\n****** HI Soup inside loop ******')
#                                            print('hdu: %r' %  hdu)
#                                            input('pause')

                                            soup = self.get_soup_from_iterator(hdu) if hdu else None
                                            if soup:
                                                hdus.append(soup)
                                                hdu = list()
                                                hdu.append(child)
                                                previous_match2 = match2
                                            else:
                                                self.ready = False
                                                self.logger.error('Unable to get_split_hdus_2. ' +
                                                                  'In for loop. ' +
                                                                  'soup: {}.'.format(soup))
                                    # append <p> tags without table title matching regex
                                    else:
                                        hdu.append(child)
                                        
#                                        print('\n\n^^^^^^^ HI not match1 ^^^^^^^')
#                                        print('hdu: %r' %  hdu)
#                                        input('pause')
                                # append <p> tags without table title 
                                else:
                                    hdu.append(child)

#                                    print('\n\n^^^^^^^ HI not title ^^^^^^^')
#                                    print('hdu: %r' %  hdu)
#                                    input('pause')
                            # append non <p> tags
                            else:
                                hdu.append(child)

#                                print('\n\n&&&&& HI no title &&&&&')
#                                print('hdu: %r' % hdu)
#                                input('pause')
                    soup = self.get_soup_from_iterator(hdu) if hdu else None
                    if soup:
#                        print('\n\n****** HI Soup outside loop ******')
#                        print('hdu: %r' %  hdu)
#                        input('pause')

                        hdus.append(soup)
                    else:
                        self.ready = False
                        self.logger.error('Unable to get_split_hdus_2. ' +
                                          'Out of for loop. ' +
                                          'soup: {}.'.format(soup))
                else:
                    self.ready = False
                    self.logger.error('Unable to get_split_hdus_2. ' +
                                      'children: {}'.format(children))
            else:
                self.ready = False
                self.logger.error('Unable to get_split_hdus_3. ' +
                                  'node: {}'.format(node))
#        print('\n\n!!!!!!!! HI end of function !!!!!!!!!')
#        print('hdus: %r' % hdus)
#        input('pause')

        return hdus


    def get_split_hdus_3(self,node=None,regex=None):
        '''Split the node into a list of BeautifulSoup objects containing file HDUs.'''
        hdus = list()
        if self.ready:
            if node and regex:
                children = self.get_children(node=node)
                if children:
                    is_first_title = True
                    title = None
                    hdu = list()
                    for child in children:
                        if self.ready:
#                            print('\n\n child: %r'%  child)
#                            print('self.ready: %r'%  self.ready)
#                            input('pause')
                            if child.name in self.heading_tag_names:
                                strings = [s for s in child.strings
                                           if s and not s.isspace()]
                                # check only one string in tag
                                string = (strings[0]
                                          if strings and len(strings) == 1 else None)
                                title = (self.get_hdu_title(string=string,regex=regex)
                                         if string and regex else None)
#                                print('title: %r' % title)
#                                input('pause')
                                if title:
                                    if is_first_title:
                                        is_first_title = False
                                        previous_title = title
                                        hdu.append(child)
                                    # when same title for header and data tables
                                    elif previous_title == title:
                                        hdu.append(child)
                                    else:
#                                            print('hdu: %r' %  hdu)
#                                            input('pause')
                                        soup = self.get_soup_from_iterator(hdu) if hdu else None
                                        if soup:
                                            hdus.append(soup)
                                            hdu = list()
                                            hdu.append(child)
                                            previous_title = title
                                        else:
                                            self.ready = False
                                            self.logger.error('Unable to get_split_hdus_3. ' +
                                                              'In for loop. ' +
                                                              'soup: {}.'.format(soup))
                                else:
#                                    print('child: %r'%  child)
#                                    print('child.name: %r'%  child.name)
#                                    print('string: %r'%  string)
#                                    input('pause')

                                    self.ready = False
                                    self.logger.error('Unable to get_split_hdus_3. ' +
                                                      'title: {}.'.format(title))
                            else:
                                hdu.append(child)
                    soup = self.get_soup_from_iterator(hdu) if hdu else None
                    if soup:
                        hdus.append(soup)
                        hdu = list()
                        hdu.append(child)
                        previous_title = title
                    else:
                        self.ready = False
                        self.logger.error('Unable to get_split_hdus_3. ' +
                                          'Out of for loop. ' +
                                          'soup: {}.'.format(soup))
#                    print('hdu: %r' % hdu)
#                    input('pause')
                else:
                    self.ready = False
                    self.logger.error('Unable to get_split_hdus_3. ' +
                                      'children: {}'.format(children))
            else:
                self.ready = False
                self.logger.error('Unable to get_split_hdus_3. ' +
                                  'node: {}'.format(node) +
                                  'regex: {}'.format(regex)
                                  )
#        print('hdus: %r' % hdus)
#        input('pause')
        return hdus

    def get_hdu_title(self,string=None,regex=None):
        '''Get HDU title from given string.'''
        hdu_title = None
        if self.ready:
            if string and regex:
                p1 = compile(regex)
                iterator = p1.finditer(string)
                titles = list()
                for match in iterator:
                    text = string[match.start() : match.end()] if match else None
                    if text: titles.append(text)
                if len(titles) == 1:
                    hdu_title = titles[0]
                else:
                    
                    #### DEBUG ####
                    self.logger.error('DEBUG: string: %r'% string)
                    self.logger.error('DEBUG: regex: %r'% regex)
                    self.logger.error('DEBUG: titles: %r'% titles)
#                    input('pause')

                    self.ready = False
                    self.logger.error('Unable to get_hdu_title. ' +
                                      'len(titles) != 1. ' +
                                      'titles: {}'.format(titles)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_hdu_title. ' +
                                  'string: {}'.format(string) +
                                  'regex: {}'.format(regex)
                                  )
        return hdu_title


    def get_hdus(self,node=None):
        '''Get the hdu tags from the given BeautifulSoup node.'''
        hdus = None
        if self.ready:
            if node:
                # get next_siblings if the first hdu heading tag
                next_siblings = None
                heading_tags = self.get_heading_tag_child_names(node=node)
                for heading_tag in heading_tags:
                    h = node.find(heading_tag)
                    string = h.string
                    string = string.lower() if string else str()
                    # find the beginning of the hdus
                    if string.startswith('hdu'):
                        next_siblings = h.previous_sibling.next_siblings
                        break
                # create new BeautifulSoup object out of the next_siblings text
                if next_siblings:
                    tag_text = list()
                    for sibling in [s for s in next_siblings if s.name]:
                        tag_text.append(str(sibling))
                    tag_text = ''.join(tag_text)
                    hdus = BeautifulSoup(tag_text, 'html.parser')
                else:
                    self.ready = False
                    self.logger.error('Unable to get_intro. ' +
                                      'next_siblings: {}'.format(next_siblings))

            else:
                self.ready = False
                self.logger.error('Unable to get_hdus. ' +
                                  'node: {}'.format(node))
        return hdus

    def get_tag_names(self,tag_list=None):
        '''Get a list of tag names from the given BeautifulSoup tag_list.'''
        tag_names = list()
        if self.ready:
            if tag_list:
                for tag in tag_list:
                    tag_names.append(tag.name)
            else:
                self.ready = False
                self.logger.error('Unable to get_tag_names. ' +
                                  'tag_list: {}'.format(tag_list))
        return tag_names

    def get_column_names(self,trs=None):
        '''Get column_names from the <tr> tag with all <th> tag children.'''
        column_names = list()
        if self.ready:
            if trs:
                for tr in trs:
                    if self.children_all_one_tag_type(node=tr,tag_name='th'):
                        column_names = list([s.lower() for s in tr.strings
                                                if not s.isspace()])
                        break
            else:
                self.ready = False
                self.logger.error('Unable to get_column_names. ' +
                                  'trs: {}'.format(trs))
        return column_names

    def check_node_string_is_filename(self,node=None):
        '''Check the sub-string of the <li> tag is a filename with extension
        in ext_list.'''
        is_filename = None
        if self.ready:
            if node:
                string = self.get_string(node=node)
                extension_list=['txt','html','fits','ply']
                is_filename = False
                for extension in extension_list:
                    match = self.check_match(regex=extension,string=string)
                    if match:
                        is_filename = True
                        break
            else:
                self.ready = False
                self.logger.error('Unable to check_node_string_is_filename. ' +
                                  'node: {}'.format(node))
        return is_filename

    def check_match(self,regex=None,string=None):
        '''Use regular exparession pattern to check if there is a match in the given string'''
        match = None
        if self.ready:
            if regex and string:
                match = bool(self.get_matches(regex=regex,string=string))
            else:
                self.ready = False
                self.logger.error('Unable to check_match. ' +
                                  'regex: {}'.format(regex) +
                                  'string: {}'.format(string)
                                  )
        if match is None:
            self.ready = False
            self.logger.error('Unable to check_match. ' +
                              'match: {}. '.format(match)
                              )
        return match

    def get_matches(self,regex=None,string=None):
        matches = None
        if self.ready:
            if regex and string:
                pattern = compile(regex)
                iterator = pattern.finditer(string)
                matches = list()
                for match in iterator:
                    text = string[match.start() : match.end()] if match else None
                    if text: matches.append(text)
            else:
                self.ready = False
                self.logger.error('Unable to check_match. ' +
                                  'regex: {}'.format(regex) +
                                  'string: {}'.format(string)
                                  )
        return matches

    def get_tables_1(self,node=None,table_tag=None):
        '''Test if node contains two tables by table_tag
            and split them into a list of Beautiful soup objects'''
        tables = None
        if self.ready:
            if node and table_tag:
                table_tags = node.find_all(table_tag)
                if table_tags:
                    if len(list(table_tags)) == 1:
                        tables = [node]
                    elif len(list(table_tags)) == 2:
                        # split tables based on table_tag, e.g., pre, ul, etc.
                        children = self.get_children(node=node)
                        if children:
                            previous_siblings = None
                            next_siblings = None
                            for child in children:
                                if child.name == table_tag:
                                    previous_siblings = child.next_sibling.previous_siblings
                                    next_siblings = child.next_siblings
                                    break
                            if previous_siblings and next_siblings:
                                tables = [self.get_soup_from_iterator(
                                                    iterator=previous_siblings,
                                                    reverse=True),
                                              self.get_soup_from_iterator(
                                                    iterator=next_siblings,
                                                    reverse=False)
                                              ]
                        else:
                            self.ready = False
                            self.logger.error('Unable to get_tables_1. ' +
                                              'children: {}, '.format(children)
                                              )
                    else:
                        self.ready = False
                        self.logger.error('Unable to get_tables_1. ' +
                                          'len(list(table_tags)) > 2, '
                                          'len(list(table_tags)): {}, '.format(len(list(table_tags)))
                                          )
                else:
                    self.ready = False
                    self.logger.error('Unable to get_tables_1. ' +
                                      'table_tags: {}, '.format(table_tags)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_tables_1. ' +
                                  'node: {}, '.format(node) +
                                  'table_tag: {}, '.format(table_tag)
                                  )
            if tables is None:
                self.ready = False
                self.logger.error('Unable to get_tables_1. ' +
                                  'tables: {}, '.format(tables)
                                  )
        return tables

    def get_tables_2(self,node=None,table_title_tag_names=None,regex=None):
        '''Test if node contains two tables by table_title_tags with regex match
            and split them into a list of Beautiful soup objects'''
        tables = None
        if self.ready:
            if node and table_title_tag_names and regex:
                # get all children of node with name in table_title_tag_names
                table_title_tags = self.get_children(node=node,
                                                     names=table_title_tag_names)
                # get potential titles from
                table_titles = list()
                for tag in table_title_tags:
                    strings = [s.strip() for s in tag.strings
                               if str(s) and not str(s).isspace()]
                    title = strings[0] if strings else None
                    if title: table_titles.append(title)
                # get titles with regex match
                table_titles = [t for t in table_titles
                                if self.check_match(regex=regex,string=t)]
                if table_titles:
                    if len(list(table_titles)) == 1:
                        tables = [node]
                    elif len(list(table_titles)) == 2:
                        children = self.get_children(node=node)
                        if children:
                            previous_siblings = None
                            next_siblings = None
                            found_first_table_title = False
                            for child in children:
                                if child.name in table_title_tag_names:
                                    if not found_first_table_title:
                                        found_first_table_title = True
                                    else:
                                        previous_siblings = child.previous_siblings
                                        next_siblings = child.previous_sibling.next_siblings
                                        break
                            if previous_siblings and next_siblings:
                                tables = [self.get_soup_from_iterator(
                                                    iterator=previous_siblings,
                                                    reverse=True),
                                              self.get_soup_from_iterator(
                                                    iterator=next_siblings,
                                                    reverse=False)
                                              ]
                        else:
                            self.ready = False
                            self.logger.error('Unable to get_tables_2. ' +
                                              'children: {}, '.format(children)
                                              )
                    else:
                        self.ready = False
                        self.logger.error('Unable to get_tables_2. ' +
                                          'len(list(table_titles)) > 2, '
                                          'len(list(table_titles)): {}, '
                                            .format(len(list(table_titles)))
                                          )
                else:
                    self.ready = False
                    self.logger.error('Unable to get_tables_2. ' +
                                      'table_titles: {}, '.format(table_titles)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_tables_2. ' +
                                  'node: {}, '.format(node) +
                                  'table_title_tag_names: {}, '
                                    .format(table_title_tag_names) +
                                  'regex: {}, '.format(regex)
                                  )
            if tables is None:
                self.ready = False
                self.logger.error('Unable to get_tables_2. ' +
                                  'tables: {}, '.format(tables)
                                  )
        return tables

    def get_tables_3(self,node=None,regex=None):
        '''Test if node contains two tables by table_title_tags with regex match
            and split them into a list of Beautiful soup objects'''
        tables = list()
        if self.ready:
            if node and regex:
                # get all children of node with name 'p'
                table_title_tags = self.get_children(node=node,names=['p'])
                # get potential titles from
                table_titles = list()
                for tag in table_title_tags:
                    strings = [s.strip() for s in tag.strings
                               if str(s) and not str(s).isspace()]
                    title = strings[0] if strings else None
                    if title: table_titles.append(title)
                # get titles with regex match
                table_titles = [t for t in table_titles
                                if self.check_match(regex=regex,string=t)]
#                print('table_titles: %r' % table_titles)
#                input('pause')
                if table_titles:
                    if len(list(table_titles)) == 1:
                        tables = [node]
                    else:
                        children = self.get_children(node=node)
                        if children:
                            is_first_title = True
                            table = list()
                            for child in children:
                                if self.ready:
#                                    print('\n\n@@@@@@@ HI child @@@@@@@')
#                                    print('child: %r'%  child)
#                                    input('pause')
                                    if child.name == 'p':
                                        (title,description) = (
                                            self.get_title_and_description_from_p(p=child))
                                        if title:
                                            match = (self.check_match(regex=regex,string=title)
                                                      if title else None)
                                            if match:
                                                if is_first_title:
                                                    is_first_title = False
                                                    table.append(child)

#                                                    print('\n\n^^^^^^^ HI is_first_title ^^^^^^^')
#                                                    print('table: %r' %  table)
#                                                    input('pause')
                                                else:
#                                                    print('\n\n****** HI Soup inside loop ******')
#                                                    print('table: %r' %  table)
#                                                    input('pause')
                                                    # strip off tags before table title tag
                                                    found_title = False
                                                    for (idx,item) in enumerate(table):
                                                        string=self.get_string(node=item)
                                                        if self.check_match(regex=regex,
                                                                            string=string):
                                                            found_title = True
                                                            break
                                                    table = table[idx:] if found_title else None
                                                    soup = (self.get_soup_from_iterator(table)
                                                            if table else None)
                                                    if soup:
                                                        tables.append(soup)
                                                        table = list()
                                                        table.append(child)
                                                    else:
                                                        self.ready = False
                                                        self.logger.error(
                                                            'Unable to get_tables_3. ' +
                                                            'In for loop. ' +
                                                            'soup: {}.'.format(soup))
                                            # append <p> tags without table title matching regex
                                            else:
                                                table.append(child)
                                        
#                                                print('\n\n^^^^^^^ HI not match ^^^^^^^')
#                                                print('table: %r' %  table)
#                                                input('pause')
                                        # append <p> tags without table title
                                        else:
                                            table.append(child)

#                                            print('\n\n^^^^^^^ HI not title ^^^^^^^')
#                                            print('table: %r' %  table)
#                                            input('pause')
                                    # append non <p> tags
                                    else:
                                        table.append(child)

#                                        print('\n\n&&&&& HI no title &&&&&')
#                                        print('table: %r' % table)
#                                        input('pause')
                        soup = self.get_soup_from_iterator(table) if table else None
                        if soup:
#                            print('\n\n****** HI Soup outside loop ******')
#                            print('table: %r' %  table)
#                            input('pause')

                            tables.append(soup)
                        else:
                            self.ready = False
                            self.logger.error('Unable to get_tables_3. ' +
                                              'Out of for loop. ' +
                                              'soup: {}.'.format(soup))

                else:
                    self.ready = False
                    self.logger.error('Unable to get_tables_3. ' +
                                      'table_titles: {}, '.format(table_titles)
                                      )
            else:
                self.ready = False
                self.logger.error('Unable to get_tables_3. ' +
                                  'node: {}, '.format(node) +
                                  'regex: {}, '.format(regex)
                                  )
            if tables is None:
                self.ready = False
                self.logger.error('Unable to get_tables_3. ' +
                                  'tables: {}, '.format(tables)
                                  )
        return tables












































