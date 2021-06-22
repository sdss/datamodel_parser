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
        self.set_hdu_list()
        self.check_data_loaded()
        if self.data_loaded:
            self.set_database_descriptions()
            self.set_yaml_description()
            self.set_yaml_naming_convention()
            self.set_yaml_generated_by()
            
    
    def check_all_data_loaded(self):
        self.data_loaded = self.cache is not None and 'general' in self.cache and 'releases' in self.cache and len(self.cache['releases']) > 0 and self.intro is not None and self.hdu_list is not None
        if self.data_loaded: print('Yaml file and database are loaded succesfully and yaml file has expected format.')
        elif self.cache is None: print('FAIL> Yaml file is not loaded')
        elif 'general' not in self.cache: print('FAIL> Yaml file format is incorrect as "general" is not a top level key')
        elif 'releases' not in self.cache: print('FAIL> Yaml file format is incorrect as "releases" is not a top level key')
        elif self.intro is None: print('FAIL> Database entry does not exist')
        elif self.hdu_list is None: print('FAIL> No HDU list retrieved by database')
        elif len(self.cache['releases']) == 0: print('FAIL> Yaml file has no releases')
        else: print('FAIL> Check data correctly loaded')

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
            with open(temp_file, 'w') as f: f.write(yaml.dump(self.cache, sort_keys=False))
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

    def set_data_from_hdu(self):
        self.data = Data.query.filter(Data.hdu_id==self.hdu.id).one() if self.hdu else None

    def set_keywords_from_header(self):
        self.keywords = Keyword.query.filter(Keyword.header_id==self.header.id).order_by(Keyword.position).all() if self.header else None
        self.database_data['hdu_keywords'][self.hdu.title.split(': ')[-1]] = {keyword:self.keywords[keyword].comment for keyword in self.keywords}

    def set_columns_from_header(self):
        self.columns = Columns.query.filter(Columns.header_id==self.header.id).order_by(Columns.position).all() if self.header else None
        self.database_data['hdu_columns'][self.hdu.title.split(': ')[-1]] = {column:self.columns[column].description for column in self.columns}

    def set_database_descriptions(self):
        self.database_data = {'general':{}, 'hdus':{}, 'hdu_keywords':{}}
        self.set_description_from_intro()
        self.set_generated_by_from_intro()
        self.set_naming_convention_from_intro()
        self.set_hdu_descriptions_from_hdu()

    def set_description_from_intro(self):
        self.set_intro_for_heading_title(heading_title = 'General Description')
        self.database_data['general']['description'] = self.intro.description
        
    def set_generated_by_from_intro(self):
        self.set_intro_for_heading_title(heading_title = 'Generated by Product')
        self.database_data['general']['generated_by'] = self.intro.description
        
    def set_naming_convention_from_intro(self):
        self.set_intro_for_heading_title(heading_title = 'Naming Convention')
        self.database_data['general']['naming_convention'] = self.intro.description
        
    def set_yaml_description(self):
        self.cache['general']['description'] = self.database_data['general']['description'] 
        
    def set_yaml_naming_convention(self):
        self.cache['general']['naming_convention'] = self.database_data['general']['naming_convention']

    def set_yaml_generated_by(self):
        self.cache['general']['generated_by'] = self.database_data['general']['generated_by']

    def set_hdu_description(self):
        self.database_data['hdus'][self.hdu.title.split(': ')[-1]] = self.hdu.description

    def set_hdu_descriptions_from_hdu(self):
	for self.hdu in self.hdu_list:
            self.set_hdu_description()
            self.set_header_from_hdu()
            self.set_keywords_from_header()
            self.set_data_from_hdu()
            self.set_columns_from_header()

    def set_yaml_hdu_descriptions(self):
        for self.yaml_release in self.cache['releases'].keys():
            for self.yaml_hdu in self.cache['releases'][self.yaml_release]['hdus'].keys():
                self.set_yaml_hdu_description()
                if 'header' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]: self.set_yaml_hdu_keywords()
                if 'columns' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]: self.set_yaml_hdu_columns()


    def set_yaml_hdu_description(self):
        if self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name'] in self.database_data['hdus']: self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['description'] = self.database_data['hdus'][self.yaml_hdu]
        else: print('Did not find', self.yaml_hdu, self.yaml_release, 'in cache to match with database')

    def set_yaml_hdu_keywords(self):
        for header_index, keyword in enumerate(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header']):
            if keyword['name'] in self.database_data['hdu_keywords'][self.yaml_hdu]: self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment'] = self.database_data['hdu_keywords'][self.yaml_hdu][keyword['name']]

    def set_yaml_hdu_columns(self):
        for header_index, column in enumerate(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns']):
            if column['name'] in self.database_data['hdu_keywords'][self.yaml_hdu]: self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['description'] = self.database_data['hdu_keywords'][self.yaml_hdu][column['name']]
                
                
                    


        
        
