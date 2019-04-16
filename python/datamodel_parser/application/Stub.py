# This file is not executable.
# -*- coding: utf-8 -*-
# $Id: generate.py 70958 2016-07-11 18:45:59Z joelbrownstein $
'''
Created by Brian Cherinka on 2016-03-07 17:35:14
Licensed under a 3-clause BSD license.

Revision History:
    Initial Version: 2016-03-07 17:35:14 by Brian Cherinka
    Last Modified On: 2016-03-07 17:35:14 by Brian

'''
from __future__ import division, print_function
import jinja2
import os
import re
import sys
from argparse import ArgumentParser
from astropy.io import fits
# from bs4 import BeautifulSoup as bs


__author__ = 'Brian Cherinka'


class Stub(object):
    """Class to create a datamodel stub.

    Parameters
    ----------
    files : str or list of str, optional
        Operate on these files.
    console : bool, optional
        If ``True``, assume this code is being run from a command-line script.
    outpath : str, optional
        Write HTML files to this directory.
    """
    def __init__(self, files=None, console=False, outpath=None):
        if isinstance(files, str):
            files = [files]
        self.files = files
        self.outpath = outpath
        self.tempDict = {}
        self.hdulist = None
        if console:
            self._parseArgs()
        if self.files is not None and len(self.files) == 1:
            self.filename = self.files[0]
        else:
            self.filename = None
        self.fmap = {'A': 'char', 'I': 'int16', 'J': 'int32', 'K': 'int64',
                     'E': 'float32', 'D': 'float64', 'B': 'bool', 'L': 'bool'}

    def _parseArgs(self):
        """Parse the command line arguments.
        """
        parser = ArgumentParser(prog=os.path.basename(sys.argv[0]),
                                description="Generate Datamodel stubs.")
        parser.add_argument('-o', '--outpath', metavar='DIR',
                            help='Path to the output HTML stub.', default='.')
        parser.add_argument('files', help='filename of a FITS file',
                            metavar='FILE', nargs='+')
        options = parser.parse_args()
        if self.files is None:
            self.files = options.files
        if self.outpath is None:
            self.outpath = options.outpath
        return

    def getModelName(self):
        """Build the output model name.

        Returns
        -------
        str
            The name for the model file.
        """
        self.basename = os.path.basename(self.filename)
        namesplit = re.split('[-.]', self.basename)
        if len(namesplit) > 1:
            self.modelname = namesplit[0]
        else:
            # if split failed, then default to generic name
            self.modelname = 'my_datamodel_template'
        return self.modelname

    def formatBytes(self, value):
        """Convert an integer to human-readable format.

        Parameters
        ----------
        value : int
            An integer representing number of bytes.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """
        for unit in ('bytes', 'KB', 'MB', 'GB'):
            if value < 1024:
                return "{0:d} {1}".format(int(value), unit)
            else:
                value /= 1024.0
        return "{0:3.1f} {1}".format(value, 'TB')

    def getFileSize(self):
        """Get the size of the input file.

        Returns
        -------
        str
            Size of the file in human-readable format.
        """
        return self.formatBytes(os.path.getsize(self.filename))

    def getHDUSize(self, value):
        """Jinja2 filter - Get the size of an HDU.

        Parameters
        ----------
        value : int
            An integer representing number of bytes.

        Returns
        -------
        str
            Size of the HDU in human-readable format.
        """
        return self.formatBytes(value)

    def getFileExtension(self):
        """Get the extension of the input file.

        Returns
        -------
        str
            File type in upper case.
        """
        filename, file_extension = os.path.splitext(self.filename)
        if 'gz' in file_extension:
            filename, file_extension = os.path.splitext(filename)
        return file_extension[1:].upper()

    def readFile(self):
        """Read the file and hdus.
        """
        self.hdulist = fits.open(self.filename)

    def getHeaders(self):
        """Return a list of headers.

        Returns
        -------
        list
            The headers stripped from the file.
        """
        if self.hdulist is None:
            self.readFile()
        headers = []
        for hdu in self.hdulist:
            headers.append(hdu.header)
        return headers

    def getType(self, value):
        """Jinja2 Filter to map the format type to a data type.

        Parameters
        ----------
        value : str?
            Not sure what type this is supposed to have.

        Returns
        -------
        str
            The data type.
        """
        out = [val if value.isalpha() else '{0}[{1}]'.format(val, value[:-1])
               for key, val in self.fmap.items() if key in value]
        return out[0]

    def isKeyAColumn(self, value):
        """Jinja2 Filter to filter out a header keyword
        that specifies a column in a binary table hdu.

        Parameters
        ----------
        value : str
            Not sure what the type of value is supposed to be.

        Returns
        -------
        bool
            ``True`` if `value` does *not* contain 'TFORM' or 'TTYPE'.
        """
        return tuple([value.find(f) for f in ('TFORM', 'TTYPE')]) == (-1, -1)

    def makeStubs(self):
        """Loop over the files.
        """
        for f in self.files:
            self.filename = f
            self.generateStub()

    def generateStub(self):
        """Build the html stub for a single file.
        """
        # generate the template
        template = self.createJinjaTemplate()
        # build the dictionary
        self.getModelName()
        self.readFile()
        self.buildDict()
        # render the HTML
        output = self.renderJinjaTemplate(template)
        # write the file
        self.writeFile(output)
        # actually close the file we opened!
        self.hdulist.close()

    def createJinjaTemplate(self):
        """Create the Jinja2 environment.

        Returns
        -------
        jinja2.Template
            The template object.
        """
        # searchpath = os.path.join(os.getenv('DATAMODEL_DIR'), 'datamodel')
        # templateLoader = jinja2.FileSystemLoader(searchpath=searchpath)
        templateLoader = jinja2.PackageLoader('datamodel', 'templates')
        env = jinja2.Environment(loader=templateLoader, trim_blocks=True,
                                 lstrip_blocks=True)
        env.filters['getType'] = self.getType
        env.filters['getHDUSize'] = self.getHDUSize
        env.filters['isKeyAColumn'] = self.isKeyAColumn
        return env.get_template('template_jinja2.html')

    def buildDict(self):
        """Set up input dictionary to the HTML template files.
        """
        self.tempDict['name'] = self.modelname
        self.tempDict['filesize'] = self.getFileSize()
        self.tempDict['filetype'] = self.getFileExtension()
        self.tempDict['filename'] = self.basename.replace('.', '\.')
        self.tempDict['hdus'] = self.hdulist
        return

    def renderJinjaTemplate(self, template):
        """Render the html output.

        Parameters
        ----------
        template : jinja2.Template
            The template to render.

        Returns
        -------
        str
            The rendered output.
        """
        output = template.render(self.tempDict)
        return output

    def writeFile(self, output):
        """Write out the HTML file.

        Parameters
        ----------
        output : str
            The data to write.
        """
        outfile = '{0}.html'.format(self.modelname)
        htmlpath = os.path.join(self.outpath, outfile)
        with open(htmlpath, 'w') as f:
            f.write(output)
        return


def main():
    """Entry point for command-line scripts.
    """
    stub = Stub(console=True)
    stub.makeStubs()
    return 0

