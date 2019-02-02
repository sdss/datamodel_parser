from json import dumps
from bs4 import Tag, NavigableString, unicode


class File:
    '''
        
    '''

    def __init__(self,logger=None,options=None,divs=None):
        self.set_logger(logger=logger)
        self.set_options(options=options)
        self.set_divs(divs=divs)
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

    def set_divs(self, divs=None):
        '''Set the divs class attribute.'''
        self.divs = None
        if self.ready:
            self.divs = divs if divs else None
            if not self.divs:
                self.ready = False
                self.logger.error('Unable to set_divs.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger  and
                          self.options and
                          self.divs)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None
            self.path    = self.options.path    if self.options else None

    def parse_file(self):
        '''Parse the HTML of the given division tags.'''
        if self.ready:
            if self.divs:
                self.set_extension_count()
                for div in self.divs:
                    div_id = div['id']
                    if div_id == 'intro':      self.parse_file_intro(div=div)
                    elif div_id == 'sections': self.parse_file_sections(div=div)
                    elif 'hdu' in div_id:      self.parse_file_extension(div=div)
                    else:
                        self.ready = False
                        self.logger.error('Unknown div_id: {0}'.format(div_id))
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. self.div_ids: {0}'
                                    .format(self.divs))

    def set_extension_count(self):
        '''Set the file extension count.'''
        self.extension_count = 0
        if self.ready:
            if self.divs:
                for div in self.divs:
                    div_id = div['id']
                    if div_id and 'hdu' in div_id: self.extension_count += 1
            else:
                self.ready = False
                self.logger.error('Unable to set_extension_count. ' +
                                  'self.div_ids: {0}'.format(self.divs))

    def set_div_ids(self):
        '''Set a list of division tag id's.'''
        self.div_ids = list()
        if self.ready:
            if self.divs:
                for div in self.divs:
                    div_id = div['id']
                    if div_id: self.div_ids.append(div['id'])
            else:
                self.ready = False
                self.logger.error('Unable to set_div_ids. self.divs: {0}'
                                    .format(self.divs))

    def parse_file_intro(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if div:
                self.set_div_children_names_and_contents(div=div)
                self.set_intro_table_information()
                print('self.intro_heading_order' + dumps(self.intro_heading_order,indent=1))
                print('self.intro_heading_levels' + dumps(self.intro_heading_levels,indent=1))
                print('self.intro_heading_titles' + dumps(self.intro_heading_titles,indent=1))
                print('self.intro_descriptions' + dumps(self.intro_descriptions,indent=1))
                input('pause')

            else:
                self.ready = False
                self.logger.error('Unable to parse_file_intro. ' +
                                  'div: {0}'.format(div))

    def set_div_children_names_and_contents(self,div=None):
        '''
            Set the tag names and contents for the children
            of the given division tag.
        '''
        self.div_children_names = list()
        self.div_children_contents = list()
        if self.ready:
            if div and self.get_number_of_descendants(item=div):
                for child in div.children:
                    # child.string can be '\n' with child.name = None
                    if not child.name: continue
                    name = child.name
                    self.div_children_names.append(name)
                    self.set_children_contents(child=child)

                # Remove closing division tag </div>
                if self.div_children_names[-1] == 'div':
                    if not self.div_children_contents[-1]:
                        del self.div_children_names[-1]
                        del self.div_children_contents[-1]
                    else:
                        self.ready = False
                        self.logger.error(
                            'Closing div tag has contents. ' +
                            'name: {0}, contents: {1}'
                            .format(self.div_children_names[-1],
                                    self.div_children_contents[-1]))
            else:
                self.ready = False
                self.logger.error(
                            'Unable to set_div_children_names_and_contents. ' +
                            'div: {0}'.format(div) +
                            'div.children: {0}'.format(div.children)
                                )

    def get_number_of_descendants(self,item=None):
        '''Return True if BeautifulSoup object has descendants.'''
        number_of_descendants = None
        if self.ready:
            if item:
                number_of_descendants = 0
                if not isinstance(item, NavigableString):
                    for descendant in item.descendants:
                        if descendant: number_of_descendants += 1
                    print('number_of_descendants: {}'
                          .format(number_of_descendants))
            else:
                self.ready = False
                self.logger.error('Unable to get_number_of_descendants.' +
                                  'item: {}'.format(item))
        return number_of_descendants

    def set_child_contents(self,child=None):
        '''Set the contents of the given child.'''
        if self.ready:
            contents = child.contents if child else list()
            print('contents: {}'.format( contents))
            input('pause')
            if len(contents) == 1:
                if isinstance(contents[0], NavigableString):
                    string = self.get_string(NavigableString=contents[0])
    #                            print('string: {}'.format( string))
            elif len(contents) > 1:
                string = list()
                for item in contents:
                    ###### I'M HERE !!!!!!!!!!! ########
                    ## Test if item has descendants
                    ## If it doesn't, get a string from the NavigableString
                    ## and append it to the string list
                    ## If it does, find out if it's only one descendant.
                    ## If so, extract the string.
                    ## If not, throw an error and log.
                    number_of_descendants = self.get_number_of_descendants(item=item)
                    print('item: {}'.format(item))
                    print('number_of_descendants: {}'.format(number_of_descendants))
                   
                    input('pause')
            else:
                self.ready = False
                self.logger.error(
                    'Unable to set_div_children_names_and_contents.' +
                    'contents: {}'.format(contents))

            self.div_children_contents.append(string)
    #                        input('pause')

    def get_string(self,NavigableString=None):
        '''Get Python string from BeautifulSoup NavigableString.'''
        string = None
        if self.ready:
            if NavigableString:
                string = str(
                    NavigableString[0].encode('utf-8').decode('utf-8').strip())
            else:
                self.ready = False
                self.logger.error('Unable to get_string.' +
                                  'NavigableString: {}'.format(NavigableString))
        return string

    def set_intro_table_information(self):
        '''Set the heading names and descriptions for the intro table.'''
        self.intro_heading_order  = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if self.div_children_names and self.div_children_contents:
                names = self.div_children_names
                contents = self.div_children_contents
                print('names: ' + dumps(names,indent=1))
                print('contents: ' + dumps(contents,indent=1))
                self.check_valid_assumptions(names=names,contents=contents)
                if self.ready:
                    heading_tags = ['h1','h2','h3','h4','h5','h6']
                    paragraph_tags = ['p']
                    order = -1
                    for (idx,name) in enumerate(names):
                        if name in paragraph_tags: continue
                        if name in heading_tags:
                            order += 1
                            self.intro_heading_order.append(order)
                            level = int(name.replace('h',''))
                            self.intro_heading_levels.append(level)
                            self.intro_heading_titles.append(contents[idx])
                            if names[idx+1] in paragraph_tags:
                                self.intro_descriptions.append(contents[idx+1])
                            else:
                                self.intro_descriptions.append('')
            else:
                self.ready = False
                self.logger.error(
                    'Unable to parse_file_intro. ' +
                    'self.div_children_names: {0}, self.div_children_contents: {1}'
                    .format(self.div_children_names,self.div_children_contents)
                                  )

    def check_valid_assumptions(self,names=None,contents=None):
        '''Verify that all of my assumptions are valid'''
        if self.ready:
            if names and contents:
                heading_tags = ['h1','h2','h3','h4','h5','h6']
                paragraph_tags = ['p']
                # Check that the lists have the same length
                if len(names) != len(contents):
                    self.ready = False
                    self.logger.error(
                        'Invalid assumption: len(names) = len(contents). ' +
                        'len(names): {0}, len(contents): {1}'
                        .format(len(names),len(contents))
                                      )
                # Check that the first name is a heading tag
                if names[0] not in heading_tags:
                    self.ready = False
                    self.logger.error(
                        'Invalid assumption: File intro starts with a heading.')

                # Check that the names are either heading or paragraph tags
                for name in names:
                    unexpected_tag_names = list()
                    if name not in heading_tags and name not in paragraph_tags:
                        unexpected_tag_names.append(name)
                    if unexpected_tag_names:
                        self.ready = False
                        self.logger.error(
                            'Invalid assumption: ' +
                            'names are either heading or paragraph tags.' +
                            'unexpected_tag_names: {0}.'
                            .format(unexpected_tag_names))
            else:
                self.ready = False
                self.logger.error(
                    'Unable to check_valid_assumptions. ' +
                    'names: {0}, contents: {1}'.format(names,contents)
                                  )


    def set_parent_names(self,div=None):
        '''Set a list of parent for the given division tag.'''
        self.parent_names = list()
        if self.ready:
            if div:
                for parent in div.parents:
                    if parent.name: self.parent_names.append(parent.name)
            else:
                self.ready = None
                self.logger.error('Unable to set_parent_names. ' +
                                  'div: {0}'.format(div))

    def set_child_names(self,div=None):
        '''Set a list of child for the given division tag.'''
        self.child_names = list()
        if self.ready:
            if div:
                for child in div.children:
                    if child.name:
                        self.child_names.append(child.name)
            else:
                self.ready = None
                self.logger.error('Unable to set_child_names. ' +
                                  'div: {0}'.format(div))

    def parse_file_sections(self,div=None):
        print('HI parse_file_sections')

    def parse_file_extension(self,div=None):
        print('HI parse_file_extension')

    def set_header_levels(self):
        print('HI parse_file_sections')

    def parse_extensions(self):
        self.extensions = list()
        if self.ready:
            if self.soup:
                another_hdu = True
                hdu_number = -1
                while another_hdu:
                    if hdu_number > 5e4:
                        self.ready = False
                        self.logger.error(
                            'Runaway while loop in parse_extensions')
                        break
                    hdu_number += 1
                    hdu = 'hdu' + str(hdu_number)
                    div = (self.soup.find('div',id=hdu)
                            if self.soup and hdu else None)
                    if div:
                        self.set_header_title_div(div=div)
                        self.set_keywords_values_comments_div(div=div)
                        extension = {
                            'hdu_number'               :
                                hdu_number,
                            'header_title'             :
                                self.header_title,
                            'keywords_values_comments' :
                                self.keywords_values_comments
                                    }
                        self.extensions.append(extension)
                    else: another_hdu = False
                self.extension_count = len(self.extensions)
            else:
                self.ready = False
                self.logger.error('Unable to parse_extensions. self.soup: {0}'
                                    .format(self.soup))

    def set_header_title_div(self,div=None):
        '''Set the header title.'''
        self.header_title = None
        if self.ready:
            if div:
                self.header_title = (div.h2.string.split(' ')[1]
                                     if div and div.h2 and div.h2.string and
                                        div.h2.string.split(' ') and
                                        len(div.h2.string.split(' '))==2
                                     else None)
            else:
                self.ready = False
                self.logger.error('Unable to set_header_title_div. ' +
                                    'div: {0}'.format(div))


    def set_keywords_values_comments_div(self,div=None):
        self.keywords_values_comments = list()
        '''Set keyword/value pairs with description if present.'''
        if self.ready:
            if div:
                pre = div.pre if div else None
                string = str(pre.string) if pre else None
                keyword_value_list = string.split('\n') if string else None
                if keyword_value_list:
                    for keyword_value in keyword_value_list:
                        if keyword_value:
                            split = keyword_value.split('=')
                            keyword = split[0].strip() if split else ''
                            split = (split[1].split('/')
                                     if split and len(split)>1 else None)
                            value = split[0].strip() if split else ''
                            comment = (split[1].strip()
                                       if split and len(split)>1 else '')
                            keyword_value_comment = {
                                'keyword' : keyword,
                                'value'   : value,
                                'comment' : comment,
                                                    }
                            self.keywords_values_comments.append(
                                keyword_value_comment)
                else:
                    self.ready = False
                    self.logger.error(
                        'Unable to set_title_and_keyword_columns. ' +
                        'keyword_value_list: {0}'.format(keyword_value_list))
            else:
                self.ready = False
                self.logger.error('Unable to set_title_and_keyword_columns. ' +
                                    'div: {0}'.format(div))

#########
# Use for list style file intros
#########
def set_intro_list_strings(self,intro=None):
        dl = intro.dl if intro else None
        if dl:
            print('dl.strings: {0}'.format(dl.strings))
            input('pause')
            self.initialize_description()
            columns = [c.replace('_',' ').title()
                       for c in self.description.keys()]
            find_value = False
            for string in dl.strings:
                if string in columns:
                    key = string.lower().replace(' ','_')
                    find_value = True
                    continue
                if find_value:
                    if string != '\n':
                        self.description[key] = string
                        find_value = False
        else:
            self.ready = None
            self.logger.error('Unable to set_description. ' +
                                'dl: {0}'.format(dl))

