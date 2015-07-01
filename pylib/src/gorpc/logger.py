#!/usr/bin/python


'''protobuf/logger.py - Module for configuring the package level logging.

This module contains a convenience function for creating and retrieving a
logger with a given name. In addition a Null handler is added to the logger
to prevent client software not implementing the logging package from
receiving "No handler" error messages.

'''

# Standard library imports
import logging


class _NullHandler(logging.Handler):
    ''' NULL logging handler.

    A null logging handler to prevent clients that don't require the
    logging package from reporting no handlers found.
    '''

    def emit(self, record):
        ''' Override the emit function to do nothing. '''
        pass


def getLogger(name):
    ''' Create and return a logger with the specified name. '''

    # Create logger and add a default NULL handler
    log = logging.getLogger(name)
    log.addHandler(_NullHandler())

    return log
