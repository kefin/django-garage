# -*- coding: utf-8 -*-
"""
tests.logger.tests

Tests for garage.logger

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from garage.test import SimpleTestCase


class LoggerTests(SimpleTestCase):

    def test_create_log(self):
        """
        Ensure create_log function is working properly.
        """
        self._msg('test', 'create_log', first=True)
        self._msg('TODO', '')


    def test_logger(self):
        """
        Ensure logger function is working properly.
        """
        self._msg('test', 'logger', first=True)
        self._msg('TODO', '')

