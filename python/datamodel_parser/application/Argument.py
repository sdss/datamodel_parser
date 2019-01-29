from argparse import ArgumentParser
from os import getenv

class Argument:
    
    def __init__(self, name=None):
        self.get_options = globals()[name] if name in globals().keys() else None
        self.options = self.get_options() if self.get_options else None
        self.options._name = name if self.options else None

def parse_html():
    parser = ArgumentParser()
    parser.add_argument("-u", "--url", help="file URL", metavar="URL", default='')
    parser.add_argument("-e", "--edition", help="data release edition", metavar="EDITION", default='')
    parser.add_argument("-l", "--level", help="set logging level", metavar="LEVEL", choices=['debug','info','warning','error','critical'], default='info')
    parser.add_argument("-n", "--nolog", help="set nolog variable", action="store_true")
    parser.add_argument("-v", "--verbose", help="set verbose logging", action="store_true")
    return parser.parse_args()


