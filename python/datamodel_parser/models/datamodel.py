from datamodel_parser import db, logger
from sqlalchemy.orm import relationship, backref
from datetime import datetime
from pytz import timezone

class Tree(db.Model):
    __tablename__ = 'tree'
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    edition = db.Column(db.String(32), nullable = False, unique = True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(edition = None):
        if edition:
            try: tree = Tree.query.filter(Tree.edition==edition).one()
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    tree_id = db.Column(db.Integer,
                        db.ForeignKey('sdss.tree.id'),
                        nullable = False)
    variable = db.Column(db.String(32), nullable = False, unique = True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(tree_id=None,variable = None):
        if tree_id and variable:
            try: env = (Env.query
                           .filter(Env.tree_id==tree_id)
                           .filter(Env.variable==variable)
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    env_id = db.Column(db.Integer,
                       db.ForeignKey('sdss.env.id'),
                       nullable = False)
    path = db.Column(db.String(64), nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(env_id=None,path=None):
        if env_id and path:
            try: location = (Location.query
                                    .filter(Location.env_id==env_id)
                                    .filter(Location.path==path)
                                    .one())
            except: location = None
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('sdss.location.id'),
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
                              .filter(Directory.depth==depth).one())
            except: directory = None
        else:
            directory = None
        return directory

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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('sdss.location.id'),
                            nullable = False)
    name = db.Column(db.String(64), nullable = False, unique = True)
    extension_count = db.Column(db.Integer, nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(location_id=None,name=None):
        if name:
            try: file = File.query.filter(File.name==name).one()
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey('sdss.file.id'),
                        nullable = False)
    heading_order = db.Column(db.Integer, nullable = False)
    heading_level = db.Column(db.Integer, nullable = False)
    heading_title = db.Column(db.String(64), nullable = False, unique = True)
    description = db.Column(db.String(1024))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(file_id=None,heading_title=None):
        if file_id and heading_title:
            try: intro = (Intro.query.filter(Intro.file_id==file_id)
                                     .filter(Intro.heading_title==heading_title)
                                     .one())
            except: intro = None
        else:
            intro = None
        return intro
    
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey('sdss.file.id'),
                        nullable = False)
    hdu_number = db.Column(db.Integer, nullable = False)
    hdu_name = db.Column(db.String(32), nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(file_id=None,hdu_number=None,hdu_name=None):
        if file_id and hdu_number!=None and hdu_name:
            try: section = (Section.query.filter(Section.file_id==file_id)
                                         .filter(Section.hdu_number==hdu_number)
                                         .filter(Section.hdu_name==hdu_name)
                                         .one())
            except: section = None
        else:
            section = None
        return section
    
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


class Extension(db.Model):
    __tablename__ = 'extension'
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey('sdss.file.id'),
                        nullable = False)
    hdu_number = db.Column(db.Integer, nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(file_id=None,hdu_number=None):
        if file_id and hdu_number!=None:
            try: extension = (Extension.query
                                       .filter(Extension.file_id==file_id)
                                       .filter(Extension.hdu_number==hdu_number)
                                       .one())
            except: extension = None
        else:
            extension = None
        return extension
    
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    extension_id = db.Column(db.Integer,
                             db.ForeignKey('sdss.extension.id'),
                             nullable = False)
    title = db.Column(db.String(32), nullable = False, unique = True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)
    @staticmethod
    def load(extension_id = None):
        if extension_id:
            try: header = Header.query.filter(Header.extension_id==extension_id).one()
            except: header = None
        else:
            header = None
        return header
    
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    header_id = db.Column(db.Integer,
                          db.ForeignKey('sdss.header.id'),
                          nullable = False)
    keyword = db.Column(db.String(32), nullable = False)
    value = db.Column(db.String(80), nullable = False)
    type = db.Column(db.String(80), nullable = False)
    comment = db.Column(db.String(256), nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load_all(header_id = None):
        if header_id:
            try: keywords = Keyword.query.filter(Keyword.header_id==header_id).all()
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    extension_id = db.Column(db.Integer,
                             db.ForeignKey('sdss.extension.id'),
                             nullable = False)
    is_image = db.Column(db.Boolean, nullable = False, default = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)
                         
    @staticmethod
    def load(extension_id=None):
        if extension_id:
            try: data = Data.query.filter(Data.extension_id==extension_id).one()
            except: data = None
        else:
            data = None
        return data
    
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
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    data_id = db.Column(db.Integer,
                        db.ForeignKey('sdss.data.id'),
                        nullable = False)
    header_title = db.Column(db.String(32), nullable = False)
    datatype = db.Column(db.String(64), nullable = False)
    size = db.Column(db.String(32), nullable = False)
    description = db.Column(db.String(128))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

    @staticmethod
    def load(data_id=None):
        if data_id:
            try: column = Column.query.filter(Column.data_id==data_id).one()
            except: column = None
        else:
            column = None
        return column
    
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

