from pgpasslib import getpass

def get_database_uri(user='sdss', host='', database='datamodel', port=5432):
    try: password = ':' + getpass(host, port, database, user)
    except: password = ''
    return "postgres://{user}{password}@{host}/{database}".format(
            user=user, password=password, host=host, database=database)

class common(object):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    #SQLALCHEMY_ECHO = True

class development(common):
    SQLALCHEMY_DATABASE_URI = get_database_uri()


