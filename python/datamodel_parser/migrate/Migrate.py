from datamodel_parser.migrate import File
import logging
from json import dumps

class Migrate:

    def __init__(self, options=None):
        self.set_logger(options=options)
        self.set_options(options=options)
        self.set_ready()
        self.set_attributes()

    def set_logger(self, options=None):
        '''Set class logger.'''
        self.ready = True
        self.logger = None
        if options and logging:
            self.logger = logging.getLogger('datamodel_parser')
            if self.logger:
                if   options.level == 'debug':
                    self.logger.setLevel(logging.DEBUG)
                elif options.level == 'info':
                    self.logger.setLevel(logging.INFO)
                elif options.level == 'warning':
                    self.logger.setLevel(logging.WARNING)
                elif options.level == 'error':
                    self.logger.setLevel(logging.ERROR)
                elif options.level == 'critical':
                    self.logger.setLevel(logging.CRITICAL)
                else: self.logger.setLevel(logging.DEBUG)
                handler = logging.StreamHandler()
                if options.level == 'debug':
                    formatter = logging.Formatter("%(name)s - " +
                                                  "%(levelname)s - " +
                                                  "%(filename)s - " +
                                                  "line %(lineno)d - " +
                                                  "%(message)s\n")
                else:
                    formatter = logging.Formatter("%(name)s - " +
                                                  "%(levelname)s - " +
                                                  "%(message)s")
                    formatter = logging.Formatter("%(name)s - " +
                                                  "%(levelname)s - " +
                                                  "%(filename)s - " +
                                                  "%(message)s")
                handler.setFormatter(formatter)
                self.logger.addHandler(handler)
                if options.nolog: self.logger.disabled = True
            else:
                self.ready = False
                print('Unable to set_logger')
        else:
            self.ready = False
            print('Unable to set_logger. options={0}, logging={1}'
                .format(options,logging))

    def set_options(self, options=None):
        self.options = None
        if self.ready:
            self.options = options if options else None
            if not self.options: self.logger.error('Unable to set_options.')

    def set_ready(self):
        '''Set error indicator.'''
        self.ready = bool(self.logger and
                          self.options)

    def set_attributes(self):
        '''Set class attributes.'''
        if self.ready:
            self.verbose = self.options.verbose if self.options else None

    def parse_file(self):
        '''
            Parse the HTML of the given URL
            and disseminate it in various formats.
        '''
        if self.ready:
            self.set_file()
            if self.file:
                self.file.parse_file()
                self.ready = self.file.ready
            else:
                self.ready = False
                self.logger.error('Unable to parse_file. self.file: {0}'
                                    .format(self.file))

    def set_file(self):
        ''' Set instance of File class.'''
        self.file = None
        if self.ready:
            self.file = (File(logger=self.logger,options=self.options)
                         if self.logger and self.options else None)
            if not self.file:
                self.ready = False
                self.logger.error('Unable to set_file. self.file: {0}'
                                    .format(self.file))

    def exit(self):
        '''Report the presense/lack of errors.'''
        if self.ready:
            if self.verbose: self.logger.info('Finished!')
            exit(0)
        else:
            if self.verbose: self.logger.info('Fail!')
            exit(1)

