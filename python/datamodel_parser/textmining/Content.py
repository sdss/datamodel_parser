from datamodel_parser.models.datamodel import Intro, File


class Content:

    def __init__(self, name = None, htmlname = None):
        self.name = name
        self.htmlname = htmlname
        self.set_file_id()
        self.set_intro()

    def set_file_id(self):
        #select id from file where name ilike 'manga-rss%';
        try: self.file = File.query.filter(File.name.ilike('%s%%' % self.htmlname)).one() if self.htmlname else None
        except: self.file = None
        self.file_id = self.file.id if self.file else None

    def set_intro(self):
        self.intro = Intro.query.filter(Intro.file_id==self.file_id).filter(Intro.heading_title==self.heading_title).first() if self.file_id else None
