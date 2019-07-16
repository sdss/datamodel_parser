from datamodel_parser import db, logger, schema
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

class Tree(db.Model):
    __tablename__ = 'tree'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    edition = db.Column(db.String(32), nullable = False, unique = True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(edition=None,tree_id=None):
        if edition:
            try: tree = Tree.query.filter(Tree.edition==edition).one()
            except: tree = None
        elif tree_id:
            try: tree = Tree.query.filter(Tree.id==tree_id).one()
            except: tree = None
        else:
            tree = None
        return tree
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print) 
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Env(db.Model):
    __tablename__ = 'env'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    tree_id = db.Column(db.Integer,
                        db.ForeignKey(schema + '.tree.id'),
                        nullable = False)
    variable = db.Column(db.String(32), nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(tree_id=None,variable=None,env_id=None):
        if tree_id and variable:
            try: env = (Env.query
                           .filter(Env.tree_id==tree_id)
                           .filter(Env.variable==variable)
                           .one())
            except: env = None
        elif env_id:
            try: env = (Env.query
                           .filter(Env.id==env_id)
                           .one())
            except: env = None
        else:
            env = None
        return env
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Location(db.Model):
    __tablename__ = 'location'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    env_id = db.Column(db.Integer,
                       db.ForeignKey(schema + '.env.id'),
                       nullable = False)
    path = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(env_id=None,path=None,location_id=None):
        if env_id: # path can be None
            try:
                location = (Location.query
                                    .filter(Location.env_id==env_id)
                                    .filter(Location.path==path)
                                    .one())
            except:
                location = None
        elif location_id:
            try: location = (Location.query
                                     .filter(Location.id==location_id)
                                     .one())
            except:
                location = None
        else:
            location = None
        return location
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Directory(db.Model):
    __tablename__ = 'directory'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey(schema + '.location.id'),
                            nullable = False)
    name = db.Column(db.String(64), nullable = False)
    depth = db.Column(db.Integer, nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)
    @staticmethod
    def load(location_id=None,name=None,depth=None):
        if location_id and name and depth!=None:
            try: directory = (Directory.query
                              .filter(Directory.location_id==location_id)
                              .filter(Directory.name==name)
                              .filter(Directory.depth==depth)
                              .one())
            except: directory = None
        else:
            directory = None
        return directory

    @staticmethod
    def load_all(location_id=None):
        if location_id:
            try: directories = (Directory.query
                              .filter(Directory.location_id==location_id)
                              .order_by(Directory.depth)
                              .all())
            except: directories = None
        else:
            directories = None
        return directories

    @staticmethod
    def load_directories():
        try: directories = Directory.query.order_by(Directory.id).all()
        except: directories = None
        return directories

    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))

    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))

    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class File(db.Model):
    __tablename__ = 'file'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey(schema + '.location.id'),
                            nullable = False)
    name = db.Column(db.String(64), nullable = False)
    status = db.Column(db.String(16), nullable = False,default='pending')
    intro_type = db.Column(db.Integer)
    file_type = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(location_id=None,name=None,file_id=None):
        if location_id and name:
            try: file = (File.query
                            .filter(File.location_id==location_id)
                            .filter(File.name==name)
                            .one())
            except: file = None
        elif file_id:
            try: file = (File.query
                            .filter(File.id==file_id)
                            .one())
            except: file = None
        else:
            file = None
        return file

    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Intro(db.Model):
    __tablename__ = 'intro'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey(schema + '.file.id'),
                        nullable = False)
    position = db.Column(db.Integer, nullable = False)
    heading_level = db.Column(db.Integer)
    heading_title = db.Column(db.String(128))
    description = db.Column(db.String(4096))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(file_id=None,position=None):
        if file_id and position is not None:
            try: intro = (Intro.query.filter(Intro.file_id==file_id)
                                     .filter(Intro.position==position)
                                     .one())
            except: intro = None
        elif file_id:
            try: intro = (Intro.query.filter(Intro.file_id==file_id).one())
            except: intro = None
        else:
            intro = None
        return intro
    
    @staticmethod
    def load_all(file_id=None,description_substring=None):
        if file_id:
            try: intros = (Intro.query.filter(Intro.file_id==file_id)
                                .order_by(Intro.position)
                                .all())
            except: intros = None
        elif description_substring:
            try: intros = (Intro.query.filter(Intro.description.contains(description_substring))
                                .all())
            except: intros = None
        else:
            intros = None
        return intros
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Filespec(db.Model):
    __tablename__ = 'filespec'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey(schema + '.file.id'),
                        nullable = False)
    env_label = db.Column(db.String(32))
    location = db.Column(db.String(512))
    name = db.Column(db.String(128))
    ext = db.Column(db.String(16))
    note = db.Column(db.String(512))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(file_id=None):
        if file_id:
            try: filespec = (Filespec.query.filter(Filespec.file_id==file_id).one())
            except: filespec = None
        else:
            filespec = None
        return filespec
    
    @staticmethod
    def load_all(file_id=None):
        if file_id:
            try: filespecs = (Filespec.query.filter(Filespec.file_id==file_id)
                                .order_by(Filespec.file_id)
                                .all())
            except: filespecs = None
        else:
            filespecs = None
        return filespecs
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])

class Section(db.Model):
    __tablename__ = 'section'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey(schema + '.file.id'),
                        nullable = False)
    hdu_number = db.Column(db.Integer)
    hdu_title = db.Column(db.String(32))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(file_id=None,hdu_number=None,hdu_title=None):
        if file_id and hdu_number is not None and hdu_title:
            try: section = (Section.query.filter(Section.file_id==file_id)
                                         .filter(Section.hdu_number==hdu_number)
                                         .filter(Section.hdu_title==hdu_title)
                                         .one())
            except: section = None
        elif file_id:
            try: section = Section.query.filter(Section.file_id==file_id).one()
            except: section = None
        else:
            section = None
        return section
    
    @staticmethod
    def load_all(file_id=None):
        if file_id:
            try: sections = (Section.query
                                  .filter(Section.file_id==file_id)
                                  .order_by(Section.hdu_number)
                                  .all())
            except: sections = None
        else:
            sections = None
        return sections
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Hdu(db.Model):
    __tablename__ = 'hdu'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey(schema + '.file.id'),
                        nullable = False)
    is_image = db.Column(db.Boolean)
    number = db.Column(db.Integer)
    title = db.Column(db.String(128))
    size = db.Column(db.String(64))
    description = db.Column(db.String(4096))
    hdu_type = db.Column(db.Integer)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(file_id=None,number=None):
        if file_id and number is not None:
            try: hdu = (Hdu.query.filter(Hdu.file_id==file_id)
                                 .filter(Hdu.number==number)
                                 .one())
            except: hdu = None
        elif file_id:
            try: hdu = (Hdu.query.filter(Hdu.file_id==file_id)
                                 .one())
            except: hdu = None
        else:
            hdu = None
        return hdu
    
    @staticmethod
    def load_all(file_id=None):
        if file_id:
            try: hdus = (Hdu.query.filter(Hdu.file_id==file_id)
                                .order_by(Hdu.number)
                                .all())
            except: hdus = None
        else:
            hdus = None
        return hdus
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Header(db.Model):
    __tablename__ = 'header'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    hdu_id = db.Column(db.Integer,
                             db.ForeignKey(schema + '.hdu.id'),
                             nullable = False)
    hdu_number = db.Column(db.Integer, nullable = False)
    table_caption = db.Column(db.String(1024))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)
    @staticmethod
    def load(hdu_id=None):
        if hdu_id:
            try: header = (Header.query
                                .filter(Header.hdu_id==hdu_id)
                                .one())
            except: header = None
        else:
            header = None
        return header
    
    @staticmethod
    def load_all(hdus=None,hdu_id=None):
        '''Create a list of all header rows with id's in the given hdu list.'''
        if hdus:
            headers = dict()
            for hdu in hdus:
                try:
                    header = (Header.query
                                    .filter(Header.hdu_id==hdu.id)
                                    .one())
                    headers[header.hdu_number] = header
                except: pass # do nothing
        elif hdu_id:
            try: headers = (Header.query.filter(Header.hdu_id==hdu_id)
                                .order_by(Header.hdu_number)
                                .all())
            except: headers = None
        else:
            headers = None
        return headers
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Keyword(db.Model):
    __tablename__ = 'keyword'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    header_id = db.Column(db.Integer,
                          db.ForeignKey(schema + '.header.id'),
                          nullable = False)
    position = db.Column(db.Integer, nullable = False)
    keyword = db.Column(db.String(64))
    value = db.Column(db.String(256))
    datatype = db.Column(db.String(80))
    comment = db.Column(db.String(16384))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(header_id=None,position=None):
        if header_id and position is not None:
            try: header = (Keyword.query
                                .filter(Keyword.header_id==header_id)
                                .filter(Keyword.position==position)
                                .one())
            except: header = None
        else:
            header = None
        return header
    
    @staticmethod
    def load_all(header_id=None):
        if header_id:
            try: keywords = (Keyword.query
                                  .filter(Keyword.header_id==header_id)
                                  .order_by(Keyword.position)
                                  .all())
            except: keywords = None
        else:
            keywords = None
        return keywords
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Data(db.Model):
    __tablename__ = 'data'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    hdu_id = db.Column(db.Integer,
                             db.ForeignKey(schema + '.hdu.id'),
                             nullable = False)
    hdu_number = db.Column(db.Integer, nullable = False)
    table_caption = db.Column(db.String(1024))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)
                         
    @staticmethod
    def load(hdu_id=None):
        if hdu_id:
            try: data = Data.query.filter(Data.hdu_id==hdu_id).one()
            except: data = None
        else:
            data = None
        return data
    
    @staticmethod
    def load_all(hdus=None,hdu_id=None):
        '''Create a list of all data rows with id's in the given hdu list.'''
        if hdus:
            datas = dict()
            for hdu in hdus:
                try:
                    data = (Data.query
                                .filter(Data.hdu_id==hdu.id)
                                .one())
                    datas[data.hdu_number] = data
                except: pass
        elif hdu_id:
            try: datas = (Data.query.filter(Data.hdu_id==hdu_id)
                              .order_by(Data.hdu_number)
                              .all())
            except: datas = None
        else:
            datas = None
        return datas
    
    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])


class Column(db.Model):
    __tablename__ = 'column'
    __table_args__ = {'schema':schema}
    id = db.Column(db.Integer, primary_key = True)
    data_id = db.Column(db.Integer,
                        db.ForeignKey(schema + '.data.id'),
                        nullable = False)
    position = db.Column(db.Integer, nullable = False)
    name = db.Column(db.String(128))
    datatype = db.Column(db.String(128))
    units = db.Column(db.String(128))
    description = db.Column(db.String(2048))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(data_id=None,position=None):
        if data_id and position is not None:
            try: column = (Column.query
                                .filter(Column.data_id==data_id)
                                .filter(Column.position==position)
                                .one())
            except: column = None
        else:
            column = None
        return column

    @staticmethod
    def load_all(data_id=None):
        if data_id:
            try: columns = (Column.query
                                  .filter(Column.data_id==data_id)
                                  .order_by(Column.position)
                                  .all())
            except: columns = None
        else:
            columns = None
        return columns

    def update_if_needed(self, columns = None, skip_keys = []):
        self.updated = False
        for key,column in columns.items():
            if key not in skip_keys:
                if getattr(self,key) != column:
                    setattr(self,key,column)
                    if not self.updated: self.updated = True
        if self.updated: self.commit()

    def add(self):
        try: db.session.add(self)
        except Exception as e:
            print("{0} ADD> {1}".format(self.__tablename__, e))
    
    def commit(self):
        try: db.session.commit()
        except Exception as e:
            print("{0} COMMIT> {1}".format(self.__tablename__, e))
    
    def __repr__(self): # representation (pretty print)
        return "\n".join(["{0}: {1}".format(
                                        column.key,
                                        getattr(self,column.key))
                                        for column in self.__table__.columns])

