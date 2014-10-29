# -*- coding: utf-8 -*-

from __future__ import with_statement

import os
from logging import getLogger, StreamHandler, Formatter, getLoggerClass, DEBUG
from threading import Lock
import urllib2

from lxml.builder import E


_logger_lock = Lock()

# Hide Debug Logs if Travis is providing secure env variables
HIDE_DEBUG_LOGS = os.environ.get('TRAVIS_SECURE_ENV_VARS') == 'true'


class PyUPSException(Exception):
    pass


def not_implemented_yet(func):
    """A decorator function which raises the `NotImplementedYet` error
    for the given function.
    """
    def wrapper(*args, **kwargs):
        raise Exception('%s is not Implemented yet' % func.__name__)
    return wrapper


class BaseAPIClient(object):
    """Base client class to be sublassed by all API methods. It implemented the
    most common minimum functionality required across all APIs.

    :param license_no: Access License No/Key
    :param user_id: API user ID, Usually your UPS accoutn login
    :param password: API Password,Usually UPS account Password
    :param sandbox: True if supposed to work in test mode
    """

    #: UPS uses different URLs to differenciate between a production request
    #: and a sandbox request.
    base_url = {
        'sandbox': "https://wwwcie.ups.com/ups.app/xml",
        'production': "https://onlinetools.ups.com/ups.app/xml"
    }

    #: The logging format used for the debug logger.  This is only used when
    #: the application is in debug mode, otherwise the attached logging
    #: handler does the formatting.
    #:
    #: :copyright: (c) 2010 by Armin Ronacher.
    debug_log_format = (
        '-' * 80 + '\n' +
        '%(levelname)s in %(module)s [%(pathname)s:%(lineno)d]:\n' +
        '%(message)s\n' +
        '-' * 80
    )

    #: UPS API allows test requests to be made to its servers. The `sandbox`
    #: flag, is used by the API to determine if calls must be made to the
    #: production servers or the sandbox servers provided by UPS
    sandbox = True

    def __init__(self, license_no, user_id, password, sandbox,
                 return_xml=False):
        """ """
        self.license_no = license_no
        self.user_id = user_id
        self.password = password
        self.sandbox = sandbox
        self.return_xml = return_xml

        #: Prepare the lazy setup of the logger.
        self._logger = None
        self.logger_name = 'PyUPS'

    def create_logger(self):
        """Creates a logger.  This logger works similar to a regular Python
        logger but changes the effective logging level based on the API's
        sandbox flag.
        Furthermore this function also removes all attached handlers in case
        there was a logger with the log name before.

        :copyright: (c) 2010 by Armin Ronacher.
        """
        Logger = getLoggerClass()

        class DebugLogger(Logger):
            def getEffectiveLevel(x):
                return DEBUG if self.sandbox and not HIDE_DEBUG_LOGS \
                    else Logger.getEffectiveLevel(x)

        class DebugHandler(StreamHandler):
            def emit(x, record):
                StreamHandler.emit(x, record) if self.sandbox else None

        handler = DebugHandler()
        handler.setLevel(DEBUG)
        handler.setFormatter(Formatter(self.debug_log_format))
        logger = getLogger(self.logger_name)
        # just in case that was not a new logger, get rid of all the handlers
        # already attached to it.
        del logger.handlers[:]
        logger.__class__ = DebugLogger
        logger.addHandler(handler)
        return logger

    @property
    def logger(self):
        """A :class:`~logging.Logger` object

        This logger can be used to (surprise) log messages.

        Here are some examples::

            self.logger.debug('Something to debug ')
            self.logger.warning('Final Warning : %s', 'I dont know')

        The :attr:`sandbox` flag automatically sets the logger in
        :attr:`~logging.DEBUG` mode.

        >>> import sys; sys.stderr = sys.stdout
        >>> c = BaseAPIClient('a', 'b', 'c', True)
        >>> c.logger
        <....DebugLogger instance at 0x...>
        >>> c.logger.debug('Test')
        -...
        DEBUG in ...:
        Test
        -...
        >>> c.sandbox = False
        >>> c._logger = None
        >>> c.logger.debug('Test')

        """
        if self._logger and self._logger.name == self.logger_name:
            return self._logger

        with _logger_lock:
            if self._logger and self._logger.name == self.logger_name:
                return self._logger
            self._logger = rv = self.create_logger()
            return rv

    def send_request(self, url, data):
        """Sends data to the server on a request
        """
        request = urllib2.Request(url=url, data=data.encode("utf-8"))
        return urllib2.urlopen(request).read()

    @classmethod
    def look_for_error(cls, response, request=None):
        """Looks for an element error and raises an :exception:`PyUPSException`
        out of it, which could be handled by applications using this API.
        """
        try:
            error = response.Response.Error
        except AttributeError:
            return None
        else:
            if error.ErrorSeverity.pyval != 'Warning':
                raise PyUPSException("%s-%s:%s" % (
                    error.ErrorSeverity.pyval,
                    error.ErrorCode.pyval,
                    error.ErrorDescription.pyval,
                ), request, response)

    @property
    def access_request(self):
        """
        Returns the XML container for first part of any request

        >>> client = BaseAPIClient('license_no', 'user_id',
        ...     'password', True
        ... )
        >>> client.access_request
        <Element AccessRequest at 0x...>
        >>> from lxml import etree
        >>> print etree.tostring(client.access_request, pretty_print=True)
        <AccessRequest>
          <Password>password</Password>
          <UserId>user_id</UserId>
          <AccessLicenseNumber>license_no</AccessLicenseNumber>
        </AccessRequest>
        <BLANKLINE>
        >>>
        """
        return \
            E.AccessRequest(
                E.Password(self.password),
                E.UserId(self.user_id),
                E.AccessLicenseNumber(self.license_no)
            )

    @classmethod
    def make_elements(cls, required_keys, args, kwargs):
        """Ensures that the given keys exist in either the elements list given
        by args or exist as keys in the kwargs (with their values). The kwargs
        are converted into elements with tags as their keys and the text as the
        value provided in the dict. Then the elements in args and kwargs are
        combined into a list and returned

        :param required_keys: An iterable of the required Keys
        :param kwargs: A dictionary of the key:value pairs to make elements
        :param args: A list of elements as positional args. Their tag attribute
            will be evaluated to check for existance
        :return: a list of lxml Elements made out of key value pairs and args

        >>> BaseAPIClient.make_elements(['a', 'b'], [], {'a': '1', 'b': '2'})
        [<Element a at 0x...>, <Element b at 0x...>]
        >>> BaseAPIClient.make_elements(['a', 'b'], [E.b('2')], {'a': '1'})
        [<Element a at 0x...>, <Element b at 0x...>]
        >>> BaseAPIClient.make_elements(['a', 'b'], [], {'a': '1',})
        Traceback (most recent call last):
            ...
        ValueError: Attributes b is/are required.
        >>> BaseAPIClient.make_elements(['a', 'b', 'c'], [], {'a': '1',})
        Traceback (most recent call last):
            ...
        ValueError: Attributes c,b is/are required.

        """
        keys_set = frozenset(required_keys)
        args_keys = frozenset([e.tag for e in args])
        dict_keys_set = frozenset(kwargs.keys())

        # Diff = required_keys - elements in args - elements in the kwargs
        difference = keys_set.difference(args_keys).difference(dict_keys_set)

        if difference:
            raise ValueError(
                'Attributes %s is/are required.' % ','.join(difference)
            )

        return [E(k, v) for k, v in kwargs.iteritems()] + list(args)


if __name__ == '__main__':
    import doctest
    doctest.testmod(optionflags=doctest.ELLIPSIS)
