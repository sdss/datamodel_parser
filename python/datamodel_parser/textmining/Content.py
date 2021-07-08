from datamodel_parser.models.datamodel import Intro, File, Hdu, Header, Keyword, Data, Column, Location, Env
from os.path import join, exists
from os import environ
import yaml


class Content:

    def __init__(self, name = None, htmlname = None, env = None, verbose = False):
        self.name = name
        self.htmlname = htmlname
        self.env = env
        self.verbose = verbose
        self.general_keywords = ['SIMPLE', 'BITPIX', 'NAXIS', 'NAXIS1', 'NAXIS2', 'EXTEND']
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
                if len(self.hdu_list) > 0: self.set_yaml_hdu_descriptions()
                self.write_cache_to_yaml_file()
                print('Uncomment write cache to yaml file when testing over')
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
            env = Env.query.filter(Env.variable == self.env).one()
            file = File.query.join(Location, File.location_id == Location.id).filter(File.name.like('%s.html'%self.htmlname)).filter(Location.env_id == env.id)
            if file.count() == 1:
                self.file = file.one()
                self.append_to_log('Loaded File ID: %s'%self.file.id, 'success')
            elif file.count() > 1:
                for index, f in enumerate(file.all()):
                    loc = Location.query.get(f.location_id)
                    env = Env.query.get(loc.env_id)
                    print('FILE>', index, 'Name', f.name, 'Location', loc.path, 'Env', env.variable)
                select = int(input('Select 0,1,etc for correct file:'))
                self.file = file.all()[select]
                self.append_to_log('Loaded File ID: %s'%self.file.id, 'success')
            else:
                self.file = None
                self.append_to_log('Failed to load File: %s'%self.htmlname, 'failed')
        self.file_id = self.file.id if self.file else None

    def set_hdu_list(self):
        """Set HDU list related to datamodel"""
        self.hdu_list = Hdu.query.filter(Hdu.file_id==self.file_id).order_by(Hdu.number).all() if self.file_id else None
        if len(self.hdu_list) == 0: self.append_to_log('HDUs not in database', 'failed')

    def set_database_descriptions(self):
        """Set overall, HDU, keyword, and column descriptions"""
        self.database_data = {'general':{}, 'hdus':{}, 'hdu_keywords':{}}
        self.set_description_from_intro()
        self.set_generated_by_from_intro()
        self.set_naming_convention_from_intro()
        if len(self.hdu_list) > 0: self.set_descriptions_from_hdu()

    def set_description_from_intro(self):
        """Set general description from database"""
        self.set_intro_for_heading_title(heading_title = 'General Description')
        if self.intro is None: self.set_intro_for_heading_title(heading_title = 'General description', final_pass = True)
        self.database_data['general']['description'] = self.intro.description if self.intro is not None and self.intro.description not in ['', None] else input('Copy "General Description" from HTML page and paste here. If cannot for some reason, input "migration: not in database. Needs update":')

    def set_intro_for_heading_title(self, heading_title = None, final_pass = False):
        """Retrieve datamodel introduction descriptions"""
        try: self.intro = Intro.query.filter(Intro.file_id==self.file_id).filter(Intro.heading_title == heading_title).one() if self.file_id and heading_title else None
        except Exception as e:
            self.intro = None
            if final_pass: self.append_to_log('Failed to retrieve Intro of "%s": %s'%(heading_title, e), 'failed')
        
    def set_generated_by_from_intro(self):
        """Set generated by description from database"""
        self.set_intro_for_heading_title(heading_title = 'Generated by Product')
        if self.intro is None: self.set_intro_for_heading_title(heading_title = 'Written by products')
        if self.intro is None: self.set_intro_for_heading_title(heading_title = 'Written by Products', final_pass = True)
        self.database_data['general']['generated_by'] = self.intro.description if self.intro is not None and self.intro.description not in ['', None] else input('Copy "Generated by Product" from HTML page and paste here. If cannot for some reason, input "migration: not in database. Needs update":')
        
    def set_naming_convention_from_intro(self):
        """Set naming convention description from database"""
        self.set_intro_for_heading_title(heading_title = 'Naming Convention')
        if self.intro is None: self.set_intro_for_heading_title(heading_title = 'Naming convention', final_pass = True)
        self.database_data['general']['naming_convention'] = self.intro.description if self.intro is not None and self.intro.description not in ['', None] else input('Copy "Naming Convention" from HTML page and paste here. If cannot for some reason, input "migration: not in database. Needs update":')

    def set_descriptions_from_hdu(self):
        """Loop to retrieve all HDU, keyword, and column descriptions from database"""
        self.set_external_keywords()
        for self.hdu in self.hdu_list:
            self.hdu_title = self.hdu.title.split(': ')[-1] if self.hdu.title is not None and self.hdu.title.split(': ')[-1] != '' else 'HDU %s'%self.hdu.number
            self.set_hdu_description()
            self.set_header_from_hdu()
            if self.header: self.set_keywords_from_header()
            self.set_data_from_hdu()
            if self.data: self.set_columns_from_header()
            self.append_externals_and_generals()

    def append_externals_and_generals(self):
        if self.hdu_title not in self.database_data['hdu_keywords']: self.database_data['hdu_keywords'][self.hdu_title] = {}
        for external_keyword in self.external_keywords.keys():
            if external_keyword not in self.database_data['hdu_keywords'][self.hdu_title]: self.database_data['hdu_keywords'][self.hdu_title][external_keyword] = self.external_keywords[external_keyword]
        for general_keyword in self.general_keywords:
            if general_keyword not in self.database_data['hdu_keywords'][self.hdu_title] or self.database_data['hdu_keywords'][self.hdu_title][general_keyword]['description'] is None or 'migration' in self.database_data['hdu_keywords'][self.hdu_title][general_keyword]['description']: self.database_data['hdu_keywords'][self.hdu_title][general_keyword] = {'description':'', 'unit':''}

    def set_hdu_description(self):
        """Retrieve HDU description from database"""
        self.database_data['hdus'][self.hdu_title] = self.hdu.description if self.hdu.description is not None else ''

    def set_header_from_hdu(self):
        """Retrieve header in database"""
        self.header = Header.query.filter(Header.hdu_id==self.hdu.id) if self.hdu else None
        self.header = self.header.one() if self.header is not None and self.header.count() else None

    def set_keywords_from_header(self):
        """Retrieve list of keywords and their descriptions from database"""
        self.keywords = Keyword.query.filter(Keyword.header_id==self.header.id).order_by(Keyword.position).all() if self.header else None
        self.database_data['hdu_keywords'][self.hdu_title] = {keyword.keyword.strip().split('[')[0]:{'description':keyword.comment} for keyword in self.keywords if keyword.keyword not in [None, '']}
        for keyword in self.keywords:
            if keyword.keyword not in [None, ''] and keyword.keyword.strip().split('[')[0].upper() not in self.database_data['hdu_keywords'][self.hdu_title]: self.database_data['hdu_keywords'][self.hdu_title][keyword.keyword.strip().split('[')[0].upper()] = {'description':keyword.comment}

    def set_data_from_hdu(self):
        """Retrieve data related to columns from database"""
        self.data = Data.query.filter(Data.hdu_id==self.hdu.id) if self.hdu else None
        self.data = self.data.one() if self.data is not None and self.data.count() else None

    def set_columns_from_header(self):
        """Retrieve column descriptions"""
        self.columns = Column.query.filter(Column.data_id==self.data.id).order_by(Column.position).all() if self.data else None
        self.database_data['hdu_keywords'][self.hdu_title] = {}
        for column in self.columns:
            if column.name in [None, '']:
                self.append_to_log(['Column', column.name, 'with description', column.description, 'in database is None for HDU ID:', self.hdu.id, ', number', self.hdu.number, ', title', self.hdu.title], 'failed')
                continue
            if column.units is not None: unit = str(column.units)
            else:
                unit = self.get_buest_guess(column.description)
                if unit != '':
                    user_input = input('Hit enter if "' + unit + '" correct for name: "' + column.name + '" and description: "' + column.description + '". Otherwise, type "n" to enter new unit from list or any other key to set unit as "".')
                    unit = unit if user_input == '' else self.get_custom_key() if user_input == 'n' else 'migration: unit of keyword/column not found. Needs update'
            if column.name.strip().split('[')[0] not in self.database_data['hdu_keywords'][self.hdu_title]: self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0]] = {'description':column.description if column.description else '', 'unit':unit}
            else: self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0]]['unit'] = unit
            if column.description not in [None, ''] and self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0]]['description'] in [None, '']: self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0]]['description'] = column.description

            if column.name.strip().split('[')[0].upper() not in self.database_data['hdu_keywords'][self.hdu_title]: self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0].upper()] = {'description':column.description if column.description else '', 'unit':unit}
            else: self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0].upper()]['unit'] = unit
            if column.description not in [None, ''] and self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0].upper()]['description'] in [None, '']: self.database_data['hdu_keywords'][self.hdu_title][column.name.strip().split('[')[0].upper()]['description'] = column.description

        for keyword in self.database_data['hdu_keywords'][self.hdu_title].keys():
            if self.database_data['hdu_keywords'][self.hdu_title][keyword]['description'] in [None, '']: self.database_data['hdu_keywords'][self.hdu_title][keyword]['description'] = 'migration: description of keyword/column not found. Needs update' if keyword not in self.general_keywords else ''

    def set_external_keywords(self):
        """Lots of files can link to keywords/columns in another HTML. Thus this section retrieves external keywords"""

        self.external_keywords = {}
        while True:
            print('\nExternal keywords to consider with HDUs')
            html_name = input('\nImport any external html names? To skip, simply hit enter. ')
            if html_name == '': break
            env = input('And the environmental variable related to file?')

            env = Env.query.filter(Env.variable == env).one()
            file = File.query.join(Location, File.location_id == Location.id).filter(File.name.like('%s.html'%html_name)).filter(Location.env_id == env.id)
            if file.count() > 1:
                for index, f in enumerate(file.all()): print(f)
                choice = int(input('Choose index of right file:'))
                file = file.all()[choice]
            else: file = file.one()

            for hdu in Hdu.query.filter(Hdu.file_id == file.id).all():
                header = Header.query.filter(Header.hdu_id==hdu.id)
                if header.count():
                    for keyword in Keyword.query.filter(Keyword.header_id==header.one().id).order_by(Keyword.position).all():
                        if keyword.keyword in [None, '']: continue
                        if keyword.keyword.strip().split('[')[0] not in self.external_keywords: self.external_keywords[keyword.keyword.strip().split('[')[0]] = {'description': keyword.comment, 'unit':'migration: unit of keyword/column not found. Needs update'}
                        elif self.external_keywords[keyword.keyword.strip().split('[')[0]]['description'] in [None, '']: self.external_keywords[keyword.keyword.strip().split('[')[0]]['description'] = keyword.comment
                        if 'unit' not in self.external_keywords[keyword.keyword.strip().split('[')[0]]: self.external_keywords[keyword.keyword.strip().split('[')[0]]['unit'] = 'migration: unit of keyword/column not found. Needs update'

                        if keyword.keyword.strip().split('[')[0].upper() not in self.external_keywords: self.external_keywords[keyword.keyword.strip().split('[')[0].upper()] = {'description': keyword.comment, 'unit':'migration: unit of keyword/column not found. Needs update'}
                        elif self.external_keywords[keyword.keyword.strip().split('[')[0].upper()]['description'] in [None, '']: self.external_keywords[keyword.keyword.strip().split('[')[0].upper()]['description'] = keyword.comment
                        if 'unit' not in self.external_keywords[keyword.keyword.strip().split('[')[0].upper()]: self.external_keywords[keyword.keyword.strip().split('[')[0].upper()]['unit'] = 'migration: unit of keyword/column not found. Needs update'
                data = Data.query.filter(Data.hdu_id==hdu.id)
                if data.count():
                    for column in Column.query.filter(Column.data_id==data.one().id).order_by(Column.position).all():
                        if column.name in [None, '']: continue
                        if column.units is not None: unit = str(column.units)
                        else:
                            unit = self.get_buest_guess(column.description)
                            if unit != '':
                                user_input = input('Hit enter if "' + unit + '" correct for name: "' + column.name + '" and description: "' + column.description + '". Otherwise, type "n" to enter new unit from list or any other key to set unit as "".')
                                unit = unit if user_input == '' else self.get_custom_key() if user_input == 'n' else 'migration: unit of keyword/column not found. Needs update'
                        if column.name.strip().split('[')[0] not in self.external_keywords: self.external_keywords[column.name.strip().split('[')[0]] = {'description':column.description if column.description else '', 'unit':unit}
                        else: self.external_keywords[column.name.strip().split('[')[0]]['unit'] = unit
                        if column.description not in [None, ''] and self.external_keywords[column.name.strip().split('[')[0]]['description'] in [None, '']: self.external_keywords[column.name.strip().split('[')[0]]['description'] = column.description
                        if column.name.strip().split('[')[0].upper() not in self.external_keywords: self.external_keywords[column.name.strip().split('[')[0].upper()] = {'description':column.description if column.description else '', 'unit':unit}
                        else: self.external_keywords[column.name.strip().split('[')[0].upper()]['unit'] = unit
                        if column.description not in [None, ''] and self.external_keywords[column.name.strip().split('[')[0].upper()]['description'] in [None, '']: self.external_keywords[column.name.strip().split('[')[0].upper()]['description'] = column.description
            for keyword in self.external_keywords:
                if self.external_keywords[keyword]['description'] in [None, '']: self.external_keywords[keyword]['description'] = 'migration: description of keyword/column not found. Needs update' if keyword not in self.general_keywords else ''

    def get_buest_guess(self, description):
        if description is None: return ''
        des = description.lower()
        return 'Arcsecond' if 'arcsec' in des else 'Arcminute' if 'arcmin' in des else 'Degrees (J2000)' if 'ascention' in des or 'declination' in des or 'j2000' in des else 'Degrees' if 'degree' in des else 'HH:MM:SS' if 'hh:mm:ss' in des else 'H:M:S' if 'h:m:s' in des else '10^-17 erg/s/cm^2/Ang' if 'flux' in des or 'uncert' in des or ('-17' in des and 'erg' in des) else 'mm' if '(mm)' in des else 'Angstroms' if '(ang)' in des or 'angstrom' in des or 'wave' in des else '1/(10^-17 erg/s/cm^2/Ang)^2' if 'inverse' in des or 'ivar' in des else 'Celsius' if 'celsius' in des or 'temp' in des else 'Hg' if 'hg ' in des or 'pressure' in des else 'radians' if 'angle' in des else ''

    def get_custom_key(self):
        units = {0:'migration: keyword/column cannot be validated. Needs update.', 1:'Degrees (J2000)', 2:'Degrees', 3:'Arcsecond', 4:'Arcminute', 5:'HH:MM:SS', 6:'H:M:S', 7:'10^-17 erg/s/cm^2/Ang', 8:'1/(10^-17 erg/s/cm^2/Ang)^2', 9:'Celsius', 10:'Hg', 11:'radians', 12:'Angstroms', 13: 'Other (specify)', 14:''}
        choice = units[int(input('Choose integer id from: ' + str(units)))]
        if 'Other' in choice: choice = input('What is unit? (type only "?" for not validated")')
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
            for self.yaml_hdu in self.cache['releases'][self.yaml_release]['hdus'].keys():
                self.hdu_title = self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name']
                if self.hdu_title not in self.database_data['hdu_keywords'] and self.hdu_title == 'PRIMARY' and 'HDU 0' in self.database_data['hdu_keywords']: self.hdu_title = 'HDU 0'
                if self.hdu_title not in self.database_data['hdu_keywords']: self.set_hdu_via_inspection()
                if self.hdu_title in self.database_data['hdu_keywords']:
                    self.set_yaml_hdu_description()
                    if 'header' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu].keys(): self.set_yaml_hdu_keywords()
                    if 'columns' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu].keys(): self.set_yaml_hdu_columns()
                else: self.append_to_log(['HDU identifier:', self.hdu_title, 'does not relate to any HDU of file in database'], 'failed')

    def set_hdu_via_inspection(self):
        "Identify the yaml hdu that is most like a database hdu and use inspection if fail to verify via hdu header title"""
        previous_score = 0
        previous_keywords = []
        most_likely_hdu = ''
        keywords_list = []
        keywords = {}
        for hdu in self.hdu_list:
            score = 0
            if hdu.title.split(': ')[-1] == self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name']: score = 9999
            if self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name'] is not None and hdu.title is not None and 'primary' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name'].lower() and 'primary' in hdu.title.split(': ')[-1].lower(): score += 9999
            if int(self.yaml_hdu.replace('hdu','')) == hdu.number: score += 1
            header = Header.query.filter(Header.hdu_id == hdu.id)
            if header.count() > 0: keywords = [k.keyword.strip().split('[')[0] for k in Keyword.query.filter(Keyword.header_id == header.one().id).all()]
            data = Data.query.filter(Data.hdu_id == hdu.id)
            if data.count() > 0:
                if header.count() == 0: keywords = [c.name.strip().split('[')[0] for c in Column.query.filter(Column.data_id == data.one().id).all() if c.name not in [None, '']]
                else:
                    for c in Column.query.filter(Column.data_id == data.one().id).all():
                        if c.name not in [None, ''] and c.name.strip().split('[')[0] not in keywords: keywords.append(c.name.strip().split('[')[0]) 
            if 'header' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]:
                for yaml_header in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header']:
                    if yaml_header['key'] not in [None, ''] and yaml_header['key'].strip().split('[')[0] in keywords: score += 1
            if 'columns' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]:
                for yaml_column in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns']:
                    if yaml_column not in [None, ''] and yaml_column.strip().split('[')[0] in keywords: score += 1
            keywords_list.append(keywords)
            if score > previous_score:
                previous_score = score*1
                most_likely_hdu = [hdu][0] #Extra precaution on array to avoid python pointer issue
                previous_keywords = [keywords][0]
                if score > 9999: break
        if most_likely_hdu == '': self.hdu_title = None
        elif previous_score < 9999:
            print('\n>Keywords in Yaml', [y['key'] for y in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header']] if 'header' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu] else '', [y for y in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns']] if 'columns' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu] else '')
            print('>AUTO GUESS:', self.yaml_hdu, '"%s"'%self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name'], '=', 'hdu%s'%most_likely_hdu.number, '"%s"'%most_likely_hdu.title, '\nScore:', previous_score, '\nDatabase Description:', most_likely_hdu.description.split('<b>')[0] if most_likely_hdu.description is not None else 'migration: Intro info not in database. Needs update', 'Keywords:', previous_keywords)
            approve = input('Hit enter if Yaml vs Database Hdu match. Else, enter "n" if change or unsure:')
            if approve == 'n':
                print('HDUs in Database\n>', '\n>'.join(['index %s HDU (Number, title, description, keywords): %s, %s, %s, %s'%(index, h.number, h.title, h.description.split('<b>')[0] if h.description is not None else None, keywords_list[index]) for index, h in enumerate(self.hdu_list)]))
                choice = int(input('Choose index number from above list or -1 for no match'))
                if choice != -1: self.hdu_title = self.hdu_list[choice].title.split(': ')[-1] if most_likely_hdu.title is not None and self.hdu_list[choice].title.split(': ')[-1] != '' else 'HDU %s'%self.hdu_list[choice].number
                else:
                    self.hdu_title = None
                    test = input('Is this a primary header that is being ignored in HTML (y/n)')
                    if test == 'y':
                        if 'columns' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]:
                            for column in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns']:
                                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['description'] = ''
                                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['unit'] = ''
                        if 'header' in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]:
                            for header_index, keyword in enumerate(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header']):
                                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment'] = ''###########
                        self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['description'] = ''
                    
            else: self.hdu_title = most_likely_hdu.title.split(': ')[-1] if most_likely_hdu.title is not None and most_likely_hdu.title.split(': ')[-1] != '' else 'HDU %s'%most_likely_hdu.number
        else: self.hdu_title = most_likely_hdu.title.split(': ')[-1] if most_likely_hdu.title is not None and most_likely_hdu.title.split(': ')[-1] != '' else 'HDU %s'%most_likely_hdu.number

    def set_yaml_hdu_description(self):
        """Set Yaml HDU description from database"""
        print('>>>Saved description for yaml HDU:', self.yaml_hdu, 'from database HDU:', self.hdu_title)
        if self.hdu_title in self.database_data['hdus']:
            self.append_to_log(['HDU:', self.hdu_title, '|', self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['description'], '>', self.database_data['hdus'][self.hdu_title]], 'success')
            self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['description'] = self.database_data['hdus'][self.hdu_title]
        else:
            self.append_to_log(['HDU:', self.hdu_title, 'not present in database'], 'failed')
            self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['description'] = 'migration: Intro info not in database. Needs update'

    def set_yaml_hdu_keywords(self):
        """Set Yaml HDU keywords from database"""
        for header_index, keyword in enumerate(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header']):
            if keyword['key'] in self.database_data['hdu_keywords'][self.hdu_title]:
                self.append_to_log(['HDU:', self.hdu_title, ', keyword:', keyword['key'], '|', str(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment']), '>', self.database_data['hdu_keywords'][self.hdu_title][keyword['key']]['description']], 'success')
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment'] = self.database_data['hdu_keywords'][self.hdu_title][keyword['key']]['description']
            elif keyword['key'] in self.general_keywords: self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment'] = ''
            else:
                self.append_to_log(['HDU:', self.hdu_title, ', keyword:', keyword['key'], 'not present in database'], 'failed')
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['header'][header_index]['comment'] = 'migration: description of keyword/column not found. Needs update'

    def set_yaml_hdu_columns(self):
        """Set Yaml HDU columns from database"""
        hdu_title = self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['name']
        for column in self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'].keys():
            if column in self.database_data['hdu_keywords'][self.hdu_title]:
                self.append_to_log(['HDU:', hdu_title, ', column:', column, '|', str(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['description']), '>', self.database_data['hdu_keywords'][self.hdu_title][column]['description'], '| and unit:', str(self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['unit']), '>', self.database_data['hdu_keywords'][self.hdu_title][column]['unit']], 'success')
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['description'] = self.database_data['hdu_keywords'][self.hdu_title][column]['description']
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['unit'] = self.database_data['hdu_keywords'][self.hdu_title][column]['unit']
            elif column in self.general_keywords:
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['description'] = ''
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['unit'] = ''
            else:
                self.append_to_log(['HDU:', self.hdu_title, ', column:', column, 'not present in database'], 'failed')
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['description'] = 'migration: description of keyword/column not found. Needs update'
                self.cache['releases'][self.yaml_release]['hdus'][self.yaml_hdu]['columns'][column]['unit'] = 'migration: unit of keyword/column not found. Needs update'

    def write_cache_to_yaml_file(self):
        """Overwrite old Yaml file"""
        if self.yaml_file and exists(self.yaml_file):
            save = input('SAVE YAML (simply hit enter if yes, otherwise hit any key first to bypass)?:')
            if save == '':
                with open(self.yaml_file, 'w') as f: f.write(yaml.dump(self.cache, sort_keys=False))
                self.append_to_log('Updated %s' % self.yaml_file, 'success')
        else: 
            self.append_to_log('Failed to update %r' % self.yaml_file, 'failed')
            self.yaml_file = None

    def write_yaml_database_success_or_fail_specifics(self):
        """Write a database to Yaml sucess or failure log file"""
        test_file = '%s.database_to_yaml_log' % self.yaml_file
        with open(test_file, 'w') as f: f.write(yaml.dump(self.log, sort_keys=False))


        
        
