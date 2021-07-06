from datamodel_parser.models.datamodel import Intro, File, Hdu, Header, Keyword, Data, Column, Location, Env
from os.path import join, exists
from os import environ
import yaml


class Content:

    def __init__(self, name = None, htmlname = None, verbose = False):
        self.name = name
        self.htmlname = htmlname
        self.verbose = verbose
        self.log = {'success':[], 'failed':[]}
        self.set_yaml_dir()
        self.set_yaml_file()
        self.set_cache_from_yaml_file()
        self.check_cache()
        if self.cache_format_as_expected:
            self.set_file_id()
            self.set_hdu_list()
            self.set_database_descriptions()
            #self.check_database_loaded()
            #if self.database_entries_loaded:
            if True:
                self.set_yaml_description()
                self.set_yaml_generated_by()
                self.set_yaml_naming_convention()
                self.set_yaml_hdu_descriptions()
                self.write_cache_to_yaml_file()
                self.write_yaml_database_success_or_fail_specifics()
            else: self.append_to_log('Skipped since data not correctly loaded', 'failed')
        else: self.append_to_log('Skipped due to no cache loaded', 'failed')

    def set_yaml_dir(self):
        """Set Yaml dir"""
        try: self.yaml_dir = join(environ['DATAMODEL_DIR'], 'datamodel', 'products', 'yaml')
        except Exception as e:
            self.yaml_dir = None
            self.append_to_log('ERROR> Failed setting directory: %s'%e, 'failed')

    def set_yaml_file(self):
        """Set Yaml file"""
        self.yaml_file = join(self.yaml_dir, '%s.yaml' % self.name) if self.name and self.yaml_dir else None
        if self.yaml_file and exists(self.yaml_file): self.append_to_log('Found %s' % self.yaml_file, 'success')
        else: 
            self.append_to_log('ERROR> Cannot find yaml file %r' % self.yaml_file, 'failed')
            self.yaml_file = None
            
    def set_cache_from_yaml_file(self):
        """Retrieve data from Yaml file"""
        if self.yaml_file:
            with open(self.yaml_file, 'r') as file:
                try:
                    self.cache = yaml.safe_load(file)
                except yaml.YAMLError as e:
                    self.append_to_log('Yaml Failed to load cache: %s' %e, 'failed')
                    self.cache = None

    def check_cache(self):
        """Check Yaml load exists and meets expected format"""
        self.cache_format_as_expected = self.cache is not None and 'general' in self.cache and 'releases' in self.cache and len(self.cache['releases']) > 0
        if self.cache is None: self.append_to_log('FAIL> Yaml file is not loaded', 'failed')
        elif 'general' not in self.cache: self.append_to_log('FAIL> Yaml file format is incorrect as "general" is not a top level key', 'failed')
        elif 'releases' not in self.cache: self.append_to_log('FAIL> Yaml file format is incorrect as "releases" is not a top level key', 'failed')
        elif len(self.cache['releases']) == 0: self.append_to_log('FAIL> Yaml file lacks release data', 'failed')

    def set_file_id(self):
        """Set datamodel file identifier from database"""
        if self.htmlname is None: self.append_to_log('Failed to load File: HTMLNAME is None', 'failed')
        else:
            file = File.query.filter(File.name.like('%s'% (self.htmlname+r'%')))
            if file.count() == 1: self.file = file.one()
            elif file.count() > 1:
                for index, f in enumerate(file.all()):
                    loc = Location.query.get(f.location_id)
                    env = Env.query.get(loc.env_id)
                    print('FILE>', index, 'Name', f.name, 'Location', loc.path, 'Env', env.variable)
                select = int(input('Select 0,1,etc for correct file:'))
                self.file = file.all()[select]
            else:
                self.file = None
                self.append_to_log('Failed to load File: %s' %e, 'failed')
        self.file_id = self.file.id if self.file else None

    def set_hdu_list(self):
        """Set HDU list related to datamodel"""
        self.hdu_list = Hdu.query.filter(Hdu.file_id==self.file_id).order_by(Hdu.number).all() if self.file_id else None
        if self.hdu_list is None:
            self.append_to_log('HDUs not in database', 'failed')
            self.weights = []
        else: self.weight_hdu_list()

    def weight_hdu_list(self):
        "Weight the likelyness that each cache hdu is a certain hdu recorded in the database"""
        self.hdu_weight = {}
        for cache_release in self.cache['releases'].keys():
            for cache_hdu in self.cache['releases'][cache_release]['hdus'].keys():
                for hdu in self.hdu_list:
                    if cache_release not in self.hdu_weight: self.hdu_weight[cache_release] = {cache_hdu:{hdu.title.split(': ')[-1]:0}}
                    if hdu.title.split(': ')[-1] == self.cache['releases'][cache_release]['hdus'][cache_hdu]['name']:
                        self.hdu_weight[cache_release][cache_hdu][hdu.title.split(': ')[-1]] = 9999
                        break
                    if int(cache_hdu.replace('hdu','')) == hdu.number: self.hdu_weight[cache_release][cache_hdu][hdu.title.split(': ')[-1]]+=1
                    score = 0
                    for cache_header in self.cache['releases'][cache_release]['hdus'][cache_hdu]['header']:
                        header = Header.query.filter(Header.hdu_id == hdu.id)
                        if header.count() == 0: break
                        for keyword in Keyword.query.filter(Keyword.header_id == header.id).all():
                            if keyword.strip() == cache_header['key']: self.hdu_weight[cache_release][cache_hdu][hdu.title.split(': ')[-1]]+=1
                    for cache_column in self.cache['releases'][cache_release]['hdus'][cache_hdu]['column']:
                        data = Data.query.filter(Data.hdu_id == hdu.id)
                        if data.count() == 0: break
                        for column in Column.query.filter(Column.data_id == data.id).all():
                            if column.strip() == cache_column['name']: self.hdu_weight[cache_release][cache_hdu][hdu.title.split(': ')[-1]]+=1
       self.set_highest_scored_hdu_converter(self):

    def set_highest_scored_hdu_converter(self):                    
        """Set a key that converts database->cache hdu from database-recorded hdu of highest score to cache hdu"""
        for release in self.hdu_weight.keys():
            for hdu in self.hdu_weight[release].keys():
                hdu_winner = ''
                score = 0
                for candidate_hdu in self.hdu_weight[release][hdu].keys():
                    if self.hdu_weight[release][hdu][candidate_hdu] > score:
                        score = self.hdu_weight[release][hdu][candidate_hdu]
                        hdu_winner = candidate_hdu
                self.winner_hdu[release][hdu] = hdu_winner

    def set_database_descriptions(self):
        """Set overall, HDU, keyword, and column descriptions"""
        self.database_data = {'general':{}, 'hdus':{}, 'hdu_keywords':{}, 'hdu_columns':{}}
        self.set_description_from_intro()
        self.set_generated_by_from_intro()
        self.set_naming_convention_from_intro()
        self.set_descriptions_from_hdu()

    def set_description_from_intro(self):
        """Set general description from database"""
        self.set_intro_for_heading_title(heading_title = 'General Description')
        if self.intro is None: self.set_intro_for_heading_title(heading_title = 'General description')
        self.database_data['general']['description'] = self.intro.description if self.intro else None

    def set_intro_for_heading_title(self, heading_title = None):
        """Retrieve datamodel introduction descriptions"""
        try: self.intro = Intro.query.filter(Intro.file_id==self.file_id).filter(Intro.heading_title == heading_title).one() if self.file_id and heading_title else None
        except Exception as e:
            self.intro = None
            self.append_to_log('Failed to retrieve Intro: %s'%e, 'failed')
        
    def set_generated_by_from_intro(self):
        """Set generated by description from database"""
        self.set_intro_for_heading_title(heading_title = 'Generated by Product')
        if self.intro is None: self.set_intro_for_heading_title(heading_title = 'Written by products')
        self.database_data['general']['generated_by'] = (self.intro.description if self.intro.description else '') if self.intro else None
        
    def set_naming_convention_from_intro(self):
        """Set naming convention description from database"""
        self.set_intro_for_heading_title(heading_title = 'Naming Convention')
        if self.intro is None: self.set_intro_for_heading_title(heading_title = 'Naming convention')
        self.database_data['general']['naming_convention'] = (self.intro.description if self.intro.description else '') if self.intro else None

    def set_descriptions_from_hdu(self):
        """Loop to retrieve all HDU, keyword, and column descriptions from database"""
        for self.hdu in self.hdu_list:
            self.set_hdu_description()
            self.set_header_from_hdu()
            if self.header: self.set_keywords_from_header()
            self.set_data_from_hdu()
            if self.data: self.set_columns_from_header()

    def set_hdu_description(self):
        """Retrieve HDU description from database"""
        self.database_data['hdus'][self.hdu.title.split(': ')[-1]] = self.hdu.description if self.hdu.description is not None else ''

    def set_header_from_hdu(self):
        """Retrieve header in database"""
        self.header = Header.query.filter(Header.hdu_id==self.hdu.id) if self.hdu else None
        self.header = self.header.one() if self.header is not None and self.header.count() else None

    def set_keywords_from_header(self):
        """Retrieve list of keywords and their descriptions from database"""
        self.keywords = Keyword.query.filter(Keyword.header_id==self.header.id).order_by(Keyword.position).all() if self.header else None
        self.database_data['hdu_keywords'][self.hdu.title.split(': ')[-1]] = {keyword.keyword.strip():{'comment':keyword.comment if keyword.comment else ''} for keyword in self.keywords}

    def set_data_from_hdu(self):
        """Retrieve data related to columns from database"""
        self.data = Data.query.filter(Data.hdu_id==self.hdu.id) if self.hdu else None
        self.data = self.data.one() if self.data is not None and self.data.count() else None

    def set_columns_from_header(self):
        """Retrieve column descriptions"""
        self.columns = Column.query.filter(Column.data_id==self.data.id).order_by(Column.position).all() if self.data else None
        self.database_data['hdu_columns'][self.hdu.title.split(': ')[-1]] = {}
        for column in self.columns:
            if column.units is not None: unit = str(column.units)
            else:
                unit = ''
                """unit = self.get_buest_guess(column.description)
                if unit != '':
                    user_input = input('Hit enter if "' + unit + '" correct for name: "' + column.name + '" and description: "' + column.description + '". Otherwise, type "n" to enter new unit from list or any other key to set unit as "".')
                    unit = unit if user_input == '' else self.get_custom_key() if user_input == 'n' else ''"""
            try: self.database_data['hdu_columns'][self.hdu.title.split(': ')[-1]][column.name.strip()] = {'description':column.description if column.description else '', 'unit':unit}
            except Exception as e: print('FAILED!!!!!!!!!!!!!!', e, column)

    def get_buest_guess(self, description):
        des = description.lower()
        return 'Arcsecond' if 'arcsec' in des else 'Arcminute' if 'arcmin' in des else 'Degrees (J2000)' if 'ascention' in des or 'declination' in des or 'j2000' in des else 'Degrees' if 'degree' in des else 'HH:MM:SS' if 'hh:mm:ss' in des else 'H:M:S' if 'h:m:s' in des else '10^-17 erg/s/cm^2/Ang' if 'flux' in des or 'uncert' in des or ('-17' in des and 'erg' in des) else 'mm' if '(mm)' in des else 'Angstroms' if '(ang)' in des or 'angstrom' in des or 'wave' in des else '1/(10^-17 erg/s/cm^2/Ang)^2' if 'inverse' in des or 'ivar' in des else 'Celsius' if 'celsius' in des or 'temp' in des else 'Hg' if 'hg ' in des or 'pressure' in des else 'radians' if 'angle' in des else ''

    def get_custom_key(self):
        units = {1:'Degrees (J2000)', 2:'Degrees', 3:'Arcsecond', 4:'Arcminute', 5:'HH:MM:SS', 6:'H:M:S', 7:'10^-17 erg/s/cm^2/Ang', 8:'1/(10^-17 erg/s/cm^2/Ang)^2', 9:'Celsius', 10:'Hg', 11:'radians', 12:'Angstroms', 13: 'Other (specify)', 14:''}
        choice = units[int(input('Choose integer id from: ' + str(units)))]
        if 'Other' in choice: choice = input('What is unit? ')
        return choice
        
    def check_database_loaded(self):
        """Check overal and HDU related descriptions exists in database"""
        self.database_entries_loaded = self.database_data['general']['description'] is not None
        if self.database_data['general']['description'] is None: self.append_to_log('FAIL> Database entry does not exist', 'failed')
        elif self.hdu_list is None: self.append_to_log('No HDU list retrieved by database', 'failed')

    def append_to_log(self, message, process):
        """Append a message to the log file and state if proccess is a success or failure"""
        if isinstance(message, list): message = ' '.join([str(m) for m in message])
        self.log[process].append(message + r'\n')
        if self.verbose: print(message)

    def set_yaml_description(self):
        """Set Yaml general description from database"""
        self.append_to_log(["General desciption|", self.cache['general']['description'], '>', self.database_data['general']['description']], 'success')
        self.cache['general']['description'] = self.database_data['general']['description']
        self.cache['general']['short'] = 'migrated from old datamodel - needs update'

    def set_yaml_generated_by(self):
        """Set Yaml generated by description from database"""
        self.append_to_log(["Generated by|", self.cache['general']['generated_by'], '>', self.database_data['general']['generated_by']], 'success')
        self.cache['general']['generated_by'] = self.database_data['general']['generated_by']

    def set_yaml_naming_convention(self):
        """Set Yaml naming convention description from database"""
        self.append_to_log(["naming convention|", self.cache['general']['naming_convention'], '>', self.database_data['general']['naming_convention']], 'success')
        self.cache['general']['naming_convention'] = self.database_data['general']['naming_convention']

    def set_yaml_hdu_descriptions(self):
        """Set Yaml HDU, keyword, and columns descriptions from database"""
        for self.yaml_release in self.cache['releases'].keys():
            #if len(self.cache['releases'][self.yaml_release]['hdus'].keys()) <= 2 and self.database_data['hdus'] <= 2:
            for self.yaml_hdu in self.cache['releases'][self.yaml_release]['hdus'].keys():
                self.hdu_title = self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name']
                if self.hdu_title not in self.database_data['hdu_keywords'] and self.hdu_title == 'PRIMARY' and 'HDU 0' in self.database_data['hdu_keywords']: self.hdu_title = 'HDU 0'
                if self.hdu_title in self.database_data['hdu_keywords']:
                    self.set_yaml_hdu_description()
                    if 'header' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu].keys(): self.set_yaml_hdu_keywords()
                    if 'columns' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu].keys(): self.set_yaml_hdu_columns()
                else:
                    self.append_to_log(['HDU:', self.hdu_title, ' not present in database'], 'failed')

    def set_yaml_hdu_description(self):
        """Set Yaml HDU description from database"""
        print('>>>>>>>', self.yaml_hdu, self.hdu_title)
        if self.hdu_title in self.database_data['hdus']:
            self.append_to_log(['HDU:', self.hdu_title, '|', self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['description'], '>', self.database_data['hdus'][self.hdu_title]], 'success')
            self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['description'] = self.database_data['hdus'][self.hdu_title]
        else: self.append_to_log(['HDU:', self.hdu_title, 'not present in database'], 'failed')

    def set_yaml_hdu_keywords(self):
        """Set Yaml HDU keywords from database"""
        for header_index, keyword in enumerate(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header']):
            if keyword['key'] in self.database_data['hdu_keywords'][self.hdu_title]:
                self.append_to_log(['HDU:', self.hdu_title, ', keyword:', keyword['key'], '|', str(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment']), '>', self.database_data['hdu_keywords'][self.hdu_title][keyword['key']]['comment']], 'success')
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment'] = self.database_data['hdu_keywords'][self.hdu_title][keyword['key']]['comment']
            else: self.append_to_log(['HDU:', self.hdu_title, ', keyword:', keyword['key'], ' not present in database'], 'failed')

    def set_yaml_hdu_columns(self):
        """Set Yaml HDU columns from database"""
        hdu_title = self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name']
        for column in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'].keys():
            if column in self.database_data['hdu_columns'][hdu_title]:
                self.append_to_log(['HDU:', self.hdu_title, ', column:', column, '|', str(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['description']), '>', self.database_data['hdu_columns'][hdu_title][column]['description'], '| and unit:', str(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['unit']), '>', self.database_data['hdu_columns'][hdu_title][column]['unit']], 'success')
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['description'] = self.database_data['hdu_columns'][hdu_title][column]['description']
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['unit'] = self.database_data['hdu_columns'][hdu_title][column]['unit']
            else: self.append_to_log(['HDU:', self.hdu_title, ', column:', column, 'not present in database'], 'failed')

    def write_cache_to_yaml_file(self):
        """Overwrite old Yaml file"""
        if self.yaml_file and exists(self.yaml_file):
            with open(self.yaml_file, 'w') as f: f.write(yaml.dump(self.cache, sort_keys=False))
            self.append_to_log('Updated %s' % self.yaml_file, 'success')
        else: 
            self.append_to_log('Failed to update %r' % self.yaml_file, 'failed')
            self.yaml_file = None

    def write_yaml_database_success_or_fail_specifics(self):
        """Write a database to Yaml sucess or failure log file"""
        test_file = '%s.database_to_yaml_log' % self.yaml_file
        with open(test_file, 'w') as f: f.write(yaml.dump(self.log, sort_keys=False))


        
        
