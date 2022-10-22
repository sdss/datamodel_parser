from datamodel_parser.models.datamodel import Intro, File, Hdu, Header, Keyword, Data, Column, Location, Env
from os.path import join, exists
from os import environ

class Summary:

    def __init__(self, name = None, verbose = None):
        self.name = name
        self.verbose = verbose
        self.set_file()
        self.set_hdu()
        self.set_header()
        self.set_keyword()
        
    def set_keyword(self):
        if self.header:
            self.keyword = Keyword.query.filter(Keyword.header_id.in_([header.id for header in self.header]))
            self.keyword = self.keyword.all()
            if self.verbose: print("Summary> Found %r Headers" % len(self.header))

    def set_header(self):
        if self.hdu:
            self.header = Header.query.filter(Header.hdu_id.in_([hdu.id for hdu in self.hdu]))
            self.header = self.header.all()
            if self.verbose: print("Summary> Found %r Headers" % len(self.header))

    def set_hdu(self):
        if self.file:
            self.hdu = Hdu.query.filter(Hdu.file_id==self.file.id).order_by(Hdu.number).all()
            if self.verbose: print("Summary> Found %r HDUs" % len(self.hdu))

    def set_file(self):
        if self.name:
            try: self.file = File.query.filter(File.name.ilike('%s%%' % self.name)).one()
            except: self.file = None
        if self.verbose: print("Summary> %r" % self.file)

