from datamodel_parser.models.datamodel import Intro, File, Hdu, Header, Keyword
from os.path import join, exists
from os import environ
import yaml


class Content:

    def __init__(self, name = None, htmlname = None):
        self.name = name
        self.htmlname = htmlname
        self.set_yaml_dir()
        self.set_yaml_file()
        self.set_cache_from_yaml_file()
        self.set_file_id()
        self.set_data()
        self.set_hdu_list()        

    def set_yaml_dir(self):
        try: self.yaml_dir = join(environ['DATAMODEL_DIR'], 'datamodel', 'products', 'yaml')
        except: self.yaml_dir = None

    def set_yaml_file(self):
        self.yaml_file = join(self.yaml_dir, '%s.yaml' % self.name) if self.name and self.yaml_dir else None
        if self.yaml_file and exists(self.yaml_file): print('Found %s' % self.yaml_file)
        else: 
            print('Cannot find %r' % self.yaml_file)
            self.yaml_file = None
            
    def write_cache_to_yaml_file(self):
        temp_file = '%s.temp' % self.yaml_file #We will eventually remove once we have this save working right
        if self.yaml_file and exists(self.yaml_file):
            '''with open(temp_file, 'w') as file:
                yaml.dump(self.cache, file, default_flow_style=False)'''
            with open(temp_file, 'w') as f: f.write(yaml.dump(cache, sort_keys=False))
            print('Updated %s' % self.yaml_file)
        else: 
            print('Failed to update %r' % self.yaml_file)
            self.yaml_file = None
            
    def set_cache_from_yaml_file(self):
        if self.yaml_file:
            with open(self.yaml_file, 'r') as file:
                try:
                    self.cache = yaml.safe_load(file)
                except yaml.YAMLError as e:
                    print(e)
                    self.cache = None

    def set_file_id(self):
        #select id from file where name ilike 'manga-rss%';
        try: self.file = File.query.filter(File.name.ilike('%s%%' % self.htmlname)).one() if self.htmlname else None
        except: self.file = None
        self.file_id = self.file.id if self.file else None

    def set_intro_for_heading_title(self, heading_title = None):
        try: self.intro = Intro.query.filter(Intro.file_id==self.file_id).filter(Intro.heading_title == heading_title).one() if self.file_id and heading_title else None
        except: self.intro = None

    def set_hdu_list(self):
        self.hdu_list = Hdu.query.filter(Hdu.file_id==self.file_id).order_by(Hdu.number).all() if self.file_id else None
        
    def set_header_from_hdu(self):
        self.header = Header.query.filter(Header.hdu_id==self.hdu.id).one() if self.hdu else None

    def set_keywords_from_header(self):
        self.keywords = Keyword.query.filter(Keyword.header_id==self.header.id).order_by(Keyword.position).all() if self.header else None

    def test(self): #I create a loop instead of test
        self.hdu = self.hdu_list[1]
        self.set_header_from_hdu()
        self.set_keywords_from_header()
        for keyword in self.keywords:
            print('keyword=%r' % keyword.comment)

    def set_data(self):
        self.data = {}
        self.set_description_from_intro()
        self.set_generated_by_from_intro()
        self.set_naming_convention_from_intro()

    def set_description_from_intro(self):
        self.set_intro_for_heading_title(heading_title = 'General Description')
        self.data['description'] = self.intro.description
        
    def set_generated_by_from_intro(self):
        self.set_intro_for_heading_title(heading_title = 'Generated by Product')
        self.data['generated_by'] = self.intro.description
        
    def set_naming_convention_from_intro(self):
        self.set_intro_for_heading_title(heading_title = 'Naming Convention')
        self.data['naming_convention'] = self.intro.description
        
        
