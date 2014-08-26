# -*- coding: utf-8 -*-
"""
garage.test.base

Test classes based on Django TestCase

* created: 2013-07-21 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-23 kchan
"""

from __future__ import unicode_literals

from django.utils import unittest

from garage import get_setting as _s
from garage.test.utils import msg


# set verbosity to > 2 to output diagnostics and messages in tests
VERBOSITY = _s('TEST_VERBOSITY', 0)


class SimpleTestCase(unittest.TestCase):
    """
    Test case based on Python unittest TestCase.
    """
    # verbose output
    verbosity = VERBOSITY

    def _msg(self, *args, **kwargs):
        """
        Utility method to print out verbose test and debug messages.
        * print output only if verbosity level is above 2.
        """
        if self.verbosity > 2:
            msg(*args, **kwargs)
