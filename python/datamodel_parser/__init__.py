# encoding: utf-8

from __future__ import absolute_import, division, print_function, unicode_literals

import os

import yaml


# Inits the logging system. Only shell logging, and exception and warning catching.
# File logging can be started by calling log.start_file_logger(name).
#from .utils import log


def merge(user, default):
    """Merges a user configuration with the default one."""

    if isinstance(user,dict) and isinstance(default,dict):
        for kk, vv in default.items():
            if kk not in user:
                user[kk] = vv
            else:
                user[kk] = merge(user[kk], vv)

    return user


NAME = 'datamodel_parser'


# Loads config
config = yaml.load(open(os.path.dirname(__file__) + '/etc/{0}.yml'.format(NAME)))

# If there is a custom configuration file, updates the defaults using it.
custom_config_fn = os.path.expanduser('~/.{0}/{0}.yml'.format(NAME))
if os.path.exists(custom_config_fn):
    config = merge(yaml.load(open(custom_config_fn)), config)


__version__ = '0.1.0dev'

########

import logging
logger = logging.getLogger('datamodel_parser')
logger.setLevel(logging.WARNING)

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

try: configname = os.environ['DATAMODEL_PARSER_CONFIG']
except: configname = "development"

app = Flask(__name__)
app.config.from_object('{0}_config.{1}'.format(__name__,configname))

db = SQLAlchemy(app)

#####

try:
    schema = os.environ['DATAMODEL_PARSER_SCHEMA']
except:
    schema = 'sdss'

