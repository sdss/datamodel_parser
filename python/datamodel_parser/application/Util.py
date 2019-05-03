from bs4 import BeautifulSoup, Tag, NavigableString
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
            self.heading_tags = {'h1','h2','h3','h4','h5','h6'}
            self.paragraph_tags = {'p'}
            self.bold_tags = {'b'}
            self.unordered_list_tags = {'ul'}
            self.description_list_tags ={'dl'}
            self.table_tags = {'table'}
            self.sections_strings = {'sections','file contents'}
            self.header_table_column_names = {}

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
                for child in self.get_children(node=node):
                    if child.name and child.name != tag_name:
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
                dt_tags = dl.find_all('dt')
                dd_tags = dl.find_all('dd')
                for dt in dt_tags:
                    string = self.get_string(node=dt).strip()
                    dts.append(string)
                for dd in dd_tags:
                    string = self.get_string(node=dd).strip()
                    # this way kills <code> and <a> tags
#                    contents = [self.get_string(node=x).strip() for x in dd.contents]
#                    string = str().join(contents) if len(contents) > 1 else contents[0]
                    dds.append(string)
            else:
                self.ready = False
                self.logger.error('Unable to get_dts_and_dds_from_dl. ' +
                                  'dl: {}'.format(dl))
        return (dts,dds)

    def get_hdu_number_and_hdu_title(self,node=None):
        '''Get hdu_number and hdu_title from first heading tag in BeautifulSoup node.'''
        (hdu_number,hdu_title) = (None,None)
        if self.ready:
            if node:
                child_names = self.get_child_names(node=node)
                heading_tag_names = [name for name in child_names
                                    if name in self.heading_tags]
                heading_tag_name = heading_tag_names[0]       if heading_tag_names else None
                header_tag = node.find_next(heading_tag_name) if heading_tag_name else None
                heading = self.get_string(node=header_tag)    if header_tag else None
                if heading:
                    node_id = (node.attrs['id']
                               if node.attrs and 'id' in node.attrs else None)
                    if node_id:
                        # hdu_number
                        # hdu_number from node['id']
                        id_hdu_number = None
                        if node_id and node_id.lower().startswith('hdu'):
                            id_hdu_number = node_id[3:].strip()
                            id_hdu_number = (int(id_hdu_number)
                                             if id_hdu_number.isdigit()
                                             else None)
                        # hdu_number from hdu_title
                        heading_hdu_number = None
                        split = heading.split(':')
                        if (split and split[0].lower().startswith('hdu')):
                            heading_hdu_number = split[0].lower().replace('hdu',str())
                            heading_hdu_number = (int(heading_hdu_number)
                                                  if heading_hdu_number.isdigit()
                                                  else None)
                        # put hdu_number together
                        hdu_number = (id_hdu_number
                                        if id_hdu_number is not None
                                      else heading_hdu_number
                                        if heading_hdu_number is not None
                                      else None)
                        # hdu_title
                        hdu_title = (split[1].strip() if split and len(split) > 1
                                     else heading.strip())
                    elif (heading.lower().startswith('primary') or
                        heading.lower().startswith('the primary')
                        ):
                        hdu_number = 0
                        split = heading.split(':')
                        hdu_title = (split[1].strip() if split and len(split) > 1
                                     else heading.strip())
                    else:
                        self.ready = False
                        self.logger.error("Unable to get_hdu_number_and_hdu_title "
                                          "from node.attrs['id'] or 'header_tag'.")
                else:
                    self.ready = False
                    self.logger.error('Unable to get_hdu_number_and_hdu_title. ' +
                                      'heading: {}'.format(heading))

        return (hdu_number,hdu_title)

    def get_all_possible_hdu_titles(self):
        '''Generate a list of hdu n where n is an integer.'''
        hdu_titles = list()
        if self.ready:
            for n in range(100):
                hdu_titles.append('hdu ' + str(n))
        return hdu_titles

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

    def get_heading_tag_siblings(self,node=None):
        '''Get a list of heading tags, which are siblings of the given node.'''
        heading_tags = list()
        if self.ready:
            if node:
                siblings = set(self.get_sibling_names(node=node))
                heading_tags = list(set(self.heading_tags) & siblings)
            else:
                self.ready = False
                self.logger.error('Unable to get_heading_tag_siblings. ' +
                                  'node: {0}'.format(node))
        return heading_tags

    def get_heading_tag_children(self,node=None):
        '''Get a list of heading tags, which are children of the given node.'''
        heading_tags = list()
        if self.ready:
            if node:
                children = self.get_child_names(node=node)
                heading_tags = [child for child in children
                                if child in self.heading_tags]
            else:
                self.ready = False
                self.logger.error('Unable to get_heading_tag_children. ' +
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
        (datatype,hdu_size)=(None,None)
        if self.ready:
            if node:
                all_strings = self.get_all_strings(node=node)
                if 'hdu type' in all_strings[0].lower(): datatype = all_strings[1]
                if 'hdu size' in all_strings[2].lower(): hdu_size = all_strings[3]
            else:
                self.ready = False
                self.logger.error('Unable to get_datatype_and_hdu_size. ' +
                                  'node: {0}'.format(node))
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

    def get_children(self,node=None,name=None):
        '''Get the children from the BeautifulSoup node, excluding line endings.'''
        children = None
        if self.ready:
            if node:
#                children = [child for child in node.children
#                              if not self.get_string(node=child).isspace()]
                children = ([child for child in node.children if child.name == name]
                            if name else
                            [child for child in node.children if child.name])
            else:
                self.ready = False
                self.logger.error('Unable to get_children. ' +
                                  'node: {0}'.format(node))
        return children

    def get_intro(self,node=None):
        '''Get a new BeautifulSoup object comprised of the intro tags
            of the given BeautifulSoup node.'''
        intro = None
        if self.ready:
            if node:
                # get previous_siblings of the end of intro heading tag
                previous_siblings = None
                heading_tags = self.get_heading_tag_children(node=node)
                for heading_tag in heading_tags:
                    h = node.find_next(heading_tag)
                    string = h.string.lower()
                    # find the end of the intro (the file contents or first hdu)
                    if (string.replace(':','') in self.sections_strings or
                        'hdu' in string
                        ):
                        previous_siblings = h.previous_siblings
                        break
                # reverse the order of the previous_siblings
                if previous_siblings:
                    intro_tags = list()
                    for sibling in [s for s in previous_siblings if s.name]:
                        intro_tags.append(sibling)
                    intro_tags.reverse()
                    
                    # create new BeautifulSoup object out of the intro_tags text
                    tag_text = '\n'.join([str(tag) for tag in intro_tags])
                    intro = BeautifulSoup(tag_text, 'html.parser')
                else:
                    self.ready = False
                    self.logger.error('Unable to get_intro. ' +
                                      'previous_siblings: {}'.format(previous_siblings))
            else:
                self.ready = False
                self.logger.error('Unable to get_intro. ' +
                                  'node: {}'.format(node))
        return intro

    def get_hdus(self,node=None):
        '''Get the hdu tags from the given BeautifulSoup node.'''
        hdus = None
        if self.ready:
            if node:
                # get next_siblings if the first hdu heading tag
                next_siblings = None
                heading_tags = self.get_heading_tag_children(node=node)
                for heading_tag in heading_tags:
                    h = node.find_next(heading_tag)
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
        column_names = None
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


#    def get_hdus(self,node=None):
#        '''Get the hdu tags from the given BeautifulSoup node.'''
#        hdus = None
#        if self.ready:
#            if node:
#                # get next_siblings if the first hdu heading tag
#                next_siblings = None
#                heading_tags = self.get_heading_tag_children(node=node)
#                for heading_tag in heading_tags:
#                    h = node.find_next(heading_tag)
#                    string = h.string.lower()
#                    # find the beginning of the hdus
#                    if string.startswith('hdu'):
#                        next_siblings = h.previous_sibling.next_siblings
#                        break
#                # create new BeautifulSoup object out of the next_siblings text
#                if next_siblings:
#                    hdu_number = 0
#                    new_hdu = False
#                    hdus = list()
#                    tag_text = list()
#                    for sibling in [s for s in next_siblings if s.name]:
#                        # get hdu number
#                        if hdu_number == 0:
#                            new_hdu = True
#                        if sibling.name in heading_tags:
#                            string = self.get_string(node=sibling)
#                            spaceless_string = ''.join(string.split()).lower()
#                            find_hdunum = spaceless_string.find('hdu'+str(hdu_number))
#                            find_primaryhdu = spaceless_string.find('primaryhdu')
#                            if find_hdunum >= 0 or find_primaryhdu >=0:
#                                n
#                            print('string: %r' % string)
#                            print('find_hdunum: %r' % find_hdunum)
#                            print('find_primaryhdu: %r' % find_primaryhdu)
#                            input('pause')
#                        if not first_heading and sibling.name in heading_tags:
#                            tag_text = ''.join(tag_text)
#                            hdus.append(BeautifulSoup(tag_text, 'html.parser'))
#                            hdu_number += 1
#                            tag_text = list()
#                            tag_text.append(str(sibling))
#                        else:
#                            if sibling.name in heading_tags:
#                                first_heading = False
#                            tag_text.append(str(sibling))
#                        print('tag_text: %r' % tag_text)
#                        print('sibling: %r' % sibling)
#                        input('pause')
#
#                    print('hdus: %r' % hdus)
#                    input('pause')
#
#
#                    for sibling in [s for s in next_siblings if s.name]:
#                        tag_text.append(str(sibling))
#                    tag_text = ''.join(tag_text)
#                    hdus = BeautifulSoup(tag_text, 'html.parser')
#                else:
#                    self.ready = False
#                    self.logger.error('Unable to get_intro. ' +
#                                      'next_siblings: {}'.format(next_siblings))
#
#            else:
#                self.ready = False
#                self.logger.error('Unable to get_hdus. ' +
#                                  'node: {}'.format(node))
#        return hdus
























































