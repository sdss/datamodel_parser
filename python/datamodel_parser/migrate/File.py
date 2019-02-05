from json import dumps
from bs4 import Tag, NavigableString


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

    def parse_file_intro(self,div=None):
        '''Parse file description content from given division tag.'''
        if self.ready:
            if div:
                self.set_intro_tag_names_and_contents(intro=div)
                print('self.intro_tag_names' + dumps(self.intro_tag_names,indent=1))
                print('self.intro_tag_contents' + dumps(self.intro_tag_contents,indent=1))
                input('pause')
                
                self.set_intro_table_information()
                # This is the information to be dissemenated into db tables
                print('self.intro_heading_orders' + dumps(self.intro_heading_orders,indent=1))
                print('self.intro_heading_levels' + dumps(self.intro_heading_levels,indent=1))
                print('self.intro_heading_titles' + dumps(self.intro_heading_titles,indent=1))
                print('self.intro_descriptions' + dumps(self.intro_descriptions,indent=1))
                input('pause')

            else:
                self.ready = False
                self.logger.error('Unable to parse_file_intro. ' +
                                  'div: {0}'.format(div))

    def set_intro_tag_names_and_contents(self,intro=None):
        '''
            Set the tag names and contents for the children of the
            given division tag.
        '''
        self.intro_tag_names = None
        self.intro_tag_contents = None
        if self.ready:
            number_descendants = self.get_number_descendants(node=intro)
            if intro and number_descendants:
                self.intro_tag_names = list()
                self.intro_tag_contents = list()
                for child in intro.children:
                    if child: # ignore child = '\n'
                        if isinstance(child, NavigableString):
                            self.intro_tag_names.append('')
                            self.intro_tag_contents.append(str(child.string))
                        elif isinstance(child, Tag):
                            (tag_name,tag_contents) = (
                                self.get_tag_name_and_contents(tag=child))
                            print('tag_name: {}'.format(tag_name))
                            print('tag_contents: {}'.format(tag_contents))
                            input('pause')
                        else:
                            self.ready = False
                            self.logger.error(
                                        'Unexpected BeautifulSoup type. ' +
                                        'child: {0}, type(child): {1}'
                                        .format(child,type(child)))
                self.remove_closing_division_tag(
                                    tag_names=self.intro_tag_names,
                                    tag_contents=self.intro_tag_contents)
            else:
                self.ready = False
                self.logger.error(
                            'Unable to set_intro_tag_names_and_contents. ' +
                            'intro: {0}'.format(intro) +
                            'number_descendants: {0}'.format(number_descendants)
                                )

    def get_number_descendants(self,node=None):
        '''Return True if BeautifulSoup object has descendants.'''
        number_descendants = None
        if self.ready:
            if node:
                number_descendants = 0
                if not isinstance(node, NavigableString):
                    for descendant in node.descendants:
                        if descendant: number_descendants += 1
            else:
                self.ready = False
                self.logger.error('Unable to get_number_descendants.' +
                                  'node: {}'.format(node))
        return number_descendants

    def get_string(self,soup_string=None):
        '''Get Python string from BeautifulSoup NavigableString.'''
        string = None
        if self.ready:
            if soup_string and isinstance(soup_string, NavigableString):
                string = str(soup_string.encode('utf-8').decode('utf-8'))
            else:
                self.ready = False
                self.logger.error(
                    'Unable to get_string. ' +
                    'soup_string: {}, '.format(soup_string) +
                    'isinstance(soup_string, NavigableString): {}'
                    .format(isinstance(soup_string, NavigableString))
                    )
        return string

    def remove_closing_division_tag(self,tag_names=None,tag_contents=None):
        '''Remove the contentless, closing division tag from the given lists.'''
        if self.ready:
            if tag_names and tag_contents:
                if tag_names[-1] == 'div':
                    if not tag_contents[-1]:
                        del tag_names[-1]
                        del tag_contents[-1]
                    else:
                        self.ready = False
                        self.logger.error(
                            'Closing div tag has contents. ' +
                            'name: {0}, contents: {1}'
                            .format(tag_names[-1],tag_contents[-1]))
            else:
                self.ready = False
                self.logger.error(
                            'Unable to remove_closing_division_tag. ' +
                            'tag_names: {0}'.format(tag_names) +
                            'contents: {0}'.format(contents)
                                )

    def get_tag_name_and_contents(self,tag=None):
        '''Set the contents of the given node.'''
        tag_name = None
        tag_contents = None
        if self.ready:
            heading_tags = ['h1','h2','h3','h4','h5','h6']
            paragraph_tags = ['p']
            anchor_tags = ['a']
            tag_name = tag.name if tag else None
            if tag_name in heading_tags + paragraph_tags + anchor_tags:
                tag_name = tag.name
                print('tag_name: {}'.format(tag_name))
                if tag_name in paragraph_tags + heading_tags:
                    tag_contents = self.get_text_content_tag_contents(tag=tag)
        
                
                
            
            
            
            
            
            
            else:
                self.ready = False
                self.logger.error('Unable to get_tag_name_and_contents. ' +
                                  'tag: {}, '.format(tag) +
                                  'tag.name: {}, '.format(tag.name) +
                                  'tag_names: {}, '.format(tag_names))
        print('tag_name: {}'.format(tag_name))
        print('tag_contents: {}'.format(tag_contents))
#        input('pause')
        return (tag_name,tag_contents)

    def get_text_content_tag_contents(self,tag=None):
        '''Get the tag contents from the given tag with text content.'''
        print('HI get_text_content_tag_contents.')
        ## This method assumes the tag has text contents only.
        ## if sub-tags other than
        contents = tag.contents if tag else list()
        print('contents: {}'.format( contents))
        print('len(contents): {}'.format( len(contents)))
        if len(contents) == 1:
            ## string contents
            content = contents[0]
            if isinstance(content, NavigableString):
                tag_contents = str(content)
            elif isinstance(tag, Tag):
                print('type(tag): {}'.format(type(tag)))
                print('tag.strings: {}'.format(tag.strings))
                print('tag.string: {}'.format(tag.string))
                input('pause')
        elif len(contents) > 1:
            ## string contents with formatting
            tag_contents = ''
#                input('pause')
            for tag in contents:
                number_descendants = (
                                self.get_number_descendants(tag=tag))
                print('\ntag: {}'.format(tag))
                print('number_descendants: {}'.format(number_descendants))
#                    input('pause')
                if number_descendants == 0:
                    tag_contents += self.get_string(soup_string=tag)
                elif number_descendants == 1:
                    if isinstance(tag, Tag):
                        tag_name = tag.name if tag else None
                        tag_string = tag.string if tag else None
                        tag_string = (
                                    self.get_string(soup_string=tag_string)
                                    if tag_string else None)
                        string = ('<' + tag_name + '>' +
                                  tag_string +
                                  '<'+'/'+tag_name+'>')
                        tag_contents += string
                    else:
                        self.ready = False
                        self.logger.error('Expected a Tag for tag.' +
                                          'Received: {}'.format(tag))
                else:
                    self.ready = False
                    self.logger.error(
                        'Expected a NavigableString or Tag for tag. ' +
                        'However, tag.number_descendants > 1.' +
                        'number_descendants: '
                        .format(number_descendants))


    def set_intro_table_information(self):
        '''Set the heading names and descriptions for the intro table.'''
        self.intro_heading_orders  = list()
        self.intro_heading_levels = list()
        self.intro_heading_titles = list()
        self.intro_descriptions   = list()
        if self.ready:
            if self.intro_tag_names and self.intro_tag_contents:
                names = self.intro_tag_names
                contents = self.intro_tag_contents
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
                    'Unable to set_intro_table_information. ' +
                    'self.intro_tag_names: {0}, self.intro_tag_contents: {1}'
                    .format(self.intro_tag_names,self.intro_tag_contents)
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

