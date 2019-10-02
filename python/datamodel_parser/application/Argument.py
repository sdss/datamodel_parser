from argparse import ArgumentParser
from os import getenv

class Argument:
    
    def __init__(self, name=None):
        self.get_options = globals()[name] if name in globals().keys() else None
        self.options = self.get_options() if self.get_options else None
        self.options._name = name if self.options else None

def inverse_parse_html():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', help='file path', metavar='PATH')
    parser.add_argument('-s', '--string', help='search string', metavar='STRING')
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-f', '--force', help='skip caveats', action='store_true')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def filespec_db():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def filespec_db():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def filespec_archive():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    parser.add_argument('-t', '--test', action='store_true', dest='test',
        help='Test mode.  Do not actually populate database.')
    parser.add_argument('-p', '--path', help='datamodel file path', metavar='PATH')
    parser.add_argument('-s', '--start', help='datamodel file path start', metavar='START')
    parser.add_argument('-o', '--location', help='example location path', metavar='LOCATION')
    parser.add_argument('-m', '--limit', help='limit number of SQL queries', metavar='limit')
    parser.add_argument('-f', '--failed', action='store_true', dest='failed',
        help='run only files in all_failed_datamodels.yaml.')
    parser.add_argument('-e', '--tree_ids', nargs='+', help='space separated list of tree_id values', metavar='tree_ids')
    return parser.parse_args()

def filespec_init():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def parse_html():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', help='file path', metavar='PATH')
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-f', '--force', help='skip caveats', action='store_true')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def populate_path_tables():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', help='file path', metavar='PATH')
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-f', '--force', help='skip caveats', action='store_true')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def template_html():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', help='file path', metavar='PATH')
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-f', '--force', help='skip caveats', action='store_true')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def parse_stub():
    parser = ArgumentParser()
    parser.add_argument('-b', '--basename', help='file path basename', metavar='BASE')
    parser.add_argument('-p', '--path', help='datamodel file path', metavar='PATH')
    parser.add_argument('-f', '--fits', help='fits file name', metavar='FITS')
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def datamodel_template():
    parser = ArgumentParser()
    parser.add_argument('-p', '--path', help='file path', metavar='PATH')
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def parse_paths():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def percent_completed():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

def find_svn_products():
    parser = ArgumentParser()
    parser.add_argument('-l', '--level', help='set logging level', metavar='LEVEL', choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument('-n', '--nolog', help='set nolog variable', action='store_true')
    parser.add_argument('-v', '--verbose', help='set verbose logging', action='store_true')
    return parser.parse_args()

