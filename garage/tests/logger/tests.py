# -*- coding: utf-8 -*-
"""
tests.logger.tests

Tests for garage.logger

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import os
import tempfile
import re
from mock import Mock, patch, call

from django.test import override_settings
from garage.test import SimpleTestCase


class LoggerTests(SimpleTestCase):

    def setUp(self):
        super(LoggerTests, self).setUp()
        from garage.logger import DebugLogger
        DebugLogger = None

    def test_create_log(self):
        """
        Ensure create_log function is working properly.
        * create new log file and log a message, then confirm the file
        and message exist.
        """
        from garage.logger import create_log
        from garage.utils import get_file_contents, delete_file
        self._msg('test', 'create_log', first=True)

        tmpfile_dir = tempfile.gettempdir()
        logname = 'garage-test'
        filename = '{0}.log'.format(logname)
        path = os.path.join(tmpfile_dir, filename)
        delete_file(path)

        self._msg('logfile', path)
        logger = create_log(logname, logfile=path)
        msg = 'this is a test log message'
        logger.debug(msg)

        regexp = re.compile(r'^.*{0} - DEBUG - {1}$'.format(logname, msg), re.I)
        data = get_file_contents(path)
        for lineno, line in enumerate(data.splitlines()):
            matched = regexp.match(line)
            if matched:
                self._msg('match: {0}'.format(lineno), matched.group(0))
            self.assertTrue(matched)

        delete_file(path)

    def test_existing_logger(self):
        """
        logger should return existing loggng object if DebugLogger is
        not None.
        """
        from garage.logger import logger
        from garage.logger import logger, DebugLogger
        self._msg('test', 'logger', first=True)
        with patch('garage.logger.DebugLogger') as mock_logger:
            expected = 'foobar'
            mock_logger.debug.return_value = expected
            result = logger().debug('this is a test message')
            self.assertEqual(result, expected)
            self._msg('result', result)

    @override_settings(
        LOG_DIR='/tmp/',
        LOG_FILE='garage-test.log',
        LOG_FORMAT="%(asctime)s - %(levelname)s - %(message)s",
        LOG_PROJECT_CODE='garage-test'
    )
    def _test_new_logger(self):
        """
        logger should create new logging object if DebugLogger is None.
        * verify function is calling ``create_log`` with the correct
          parameters to create a new logger.
        """
        from garage.logger import logger, DebugLogger
        self._msg('test', 'logger', first=True)
        DebugLogger = None
        with patch('garage.logger.create_log') as mock_create_log:
            expected = 'foo'
            mock_create_log.return_value = expected
            result = logger()
            args, kwargs = mock_create_log.call_args
            self.assertEqual(result, expected)
            self.assertTrue('logname' in kwargs)
            self.assertTrue('logfile' in kwargs)
            self.assertTrue('format' in kwargs)
            self.assertEqual(kwargs['logname'], 'garage-test')
            self.assertEqual(kwargs['logfile'], 'garage-test.log')
            self.assertEqual(kwargs['format'],
                             "%(asctime)s - %(levelname)s - %(message)s")
            self._msg('result', result)
            self._msg('args', args)
            self._msg('kwargs', kwargs)
