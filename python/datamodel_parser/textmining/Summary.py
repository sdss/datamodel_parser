from datamodel_parser.models.datamodel import Intro, File, Hdu, Header, Keyword, Data, Column, Location, Env
from os.path import join, exists
from os import environ

class Summary:

    def __init__(self, name = None, verbose = None):
        self.name = name
        self.verbose = verbose
        self.set_file()
        self.set_yaml_dir()
        self.set_yaml_file()

    def set_file(self):
        if self.name:
            try: self.file = File.query.filter(File.name.ilike('%s%%' % self.name)).one()
            except: self.file = None
        print("Summary> %r" % self.file)

    def set_yaml_dir(self):
        try:
            self.yaml_dir = join(environ['DATAMODEL_DIR'], 'datamodel', 'products', 'yaml')
            if self.verbose: print("Summary> Yaml %r" % self.yaml_dir )
        except Exception as e:
            self.yaml_dir = None
            print("Summary> Yaml %r" % e )

    def set_yaml_file(self):
        self.yaml_file = join(self.yaml_dir, '%s.yaml' % self.name) if self.name and self.yaml_dir else None
        if self.yaml_file and not exists(self.yaml_file):
            print("Summary> Nonexistent Path %r" % self.yaml_file )
        if self.verbose: print("Summary> Yaml File %r" % self.yaml_file )
