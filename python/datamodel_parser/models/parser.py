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
    variable = db.Column(db.String(16), nullable = False, unique = True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

class Location(db.Model):
    __tablename__ = 'location'
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    env_id = db.Column(db.Integer,
                       db.ForeignKey('sdss.env.id'),
                       nullable = False)
    path = db.Column(db.String(64), nullable = False, unique = True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

class Directory(db.Model):
    __tablename__ = 'directory'
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    location_id = db.Column(db.Integer,
                            db.ForeignKey('sdss.location.id'),
                            nullable = False)
    name = db.Column(db.String(64), nullable = False, unique = True)
    depth = db.Column(db.Integer, nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

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

class Description(db.Model):
    __tablename__ = 'description'
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    file_id = db.Column(db.Integer,
                        db.ForeignKey('sdss.file.id'),
                        nullable = False)
    sas_path = db.Column(db.String(128), nullable = False, unique = True)
    general_description = db.Column(db.String(256), nullable = False,
                                    unique = True)
    naming_convention = db.Column(db.String(128), nullable = False, unique = True)
    approximate_size = db.Column(db.String(32), nullable = False, unique = True)
    file_type = db.Column(db.String(32), nullable = False, unique = True)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

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

class Keyword(db.Model):
    __tablename__ = 'keyword'
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    header_id = db.Column(db.Integer,
                          db.ForeignKey('sdss.header.id'),
                          nullable = False)
    keyword = db.Column(db.String(32), nullable = False)
    value = db.Column(db.String(80), nullable = False)
    comment = db.Column(db.String(80), nullable = False)
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

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

class Column(db.Model):
    __tablename__ = 'column'
    __table_args__ = {'schema':'sdss'}
    id = db.Column(db.Integer, primary_key = True)
    data_id = db.Column(db.Integer,
                        db.ForeignKey('sdss.data.id'),
                        nullable = False)
    name = db.Column(db.String(32), nullable = False)
    value = db.Column(db.String(64), nullable = False)
    length = db.Column(db.Integer, nullable = False)
    description = db.Column(db.String(80))
    created = db.Column(db.DateTime, default=datetime.now)
    modified = db.Column(db.DateTime,
                         default=datetime.now,
                         onupdate=datetime.now)

