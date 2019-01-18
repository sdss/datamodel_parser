# !usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed under a 3-clause BSD license.
#
# @Author: Brian Cherinka
# @Date:   2017-12-05 12:01:21
# @Last modified by:   Brian Cherinka
# @Last Modified time: 2017-12-05 12:19:32

from __future__ import print_function, division, absolute_import


class Datamodel_parserError(Exception):
    """A custom core Datamodel_parser exception"""

    def __init__(self, message=None):

        message = 'There has been an error' \
            if not message else message

        super(Datamodel_parserError, self).__init__(message)


class Datamodel_parserNotImplemented(Datamodel_parserError):
    """A custom exception for not yet implemented features."""

    def __init__(self, message=None):

        message = 'This feature is not implemented yet.' \
            if not message else message

        super(Datamodel_parserNotImplemented, self).__init__(message)


class Datamodel_parserAPIError(Datamodel_parserError):
    """A custom exception for API errors"""

    def __init__(self, message=None):
        if not message:
            message = 'Error with Http Response from Datamodel_parser API'
        else:
            message = 'Http response error from Datamodel_parser API. {0}'.format(message)

        super(Datamodel_parserAPIError, self).__init__(message)


class Datamodel_parserApiAuthError(Datamodel_parserAPIError):
    """A custom exception for API authentication errors"""
    pass


class Datamodel_parserMissingDependency(Datamodel_parserError):
    """A custom exception for missing dependencies."""
    pass


class Datamodel_parserWarning(Warning):
    """Base warning for Datamodel_parser."""


class Datamodel_parserUserWarning(UserWarning, Datamodel_parserWarning):
    """The primary warning class."""
    pass


class Datamodel_parserSkippedTestWarning(Datamodel_parserUserWarning):
    """A warning for when a test is skipped."""
    pass


class Datamodel_parserDeprecationWarning(Datamodel_parserUserWarning):
    """A warning for deprecated features."""
    pass
