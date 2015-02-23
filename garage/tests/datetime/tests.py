# -*- coding: utf-8 -*-
"""
tests.datetime.tests

Tests for garage.datetime

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-23 kchan
"""

from __future__ import (absolute_import, unicode_literals)

try:
    from django.test import override_settings
except ImportError:
    from django.test.utils import override_settings

from garage.test import SimpleTestCase


class DatetimeTests(SimpleTestCase):

    @override_settings(TIME_ZONE='America/New_York')
    def test_get_local_tz(self):
        """
        Ensure get_local_tz function returns proper value.
        """
        import pytz
        from garage.datetime import get_local_tz
        local_tz = get_local_tz()
        self._msg('test', 'local_tz', first=True)
        self._msg('local_tz', local_tz)
        self.assertEqual(local_tz, pytz.timezone('America/New_York'))

    def test_convert_datetime(self):
        """
        Ensure convert_datetime function returns proper value.
        """
        import pytz
        from datetime import datetime
        from garage.datetime import convert_datetime

        loc_dt = datetime(2014, 8, 24, 0, 0, 0)
        from_tz = pytz.timezone('UTC')
        to_tz = pytz.utc
        utc_dt = convert_datetime(loc_dt, from_tz, to_tz)

        result_dt = convert_datetime(utc_dt, to_tz, from_tz)
        local_dt_aware = loc_dt.replace(tzinfo=from_tz)

        self._msg('test', 'convert_datetime', first=True)
        self._msg('local', loc_dt)
        self._msg('converted', utc_dt)
        self._msg('reconverted', result_dt)
        self.assertEqual(result_dt, local_dt_aware)

    def test_local_to_utc(self):
        """
        Ensure local_to_utc function returns proper value.
        """
        import pytz
        from datetime import datetime
        from garage.datetime import local_to_utc

        local_tz = pytz.timezone('America/Los_Angeles')
        dt = datetime(2014, 8, 24, 0, 0, 0)
        utc_dt = local_to_utc(dt, local_tz=local_tz)

        local_dt_aware = local_tz.localize(dt)
        to_tz = pytz.timezone('UTC')
        expected = local_dt_aware.astimezone(to_tz)

        self._msg('test', 'local_to_utc', first=True)
        self._msg('dt', dt)
        self._msg('utc_dt', utc_dt)
        self._msg('expected', expected)
        self.assertEqual(utc_dt, expected)

    def test_utc_to_local(self):
        """
        Ensure local_to_utc function returns proper value.
        """
        import pytz
        from datetime import datetime
        from garage.datetime import utc_to_local

        utc_tz = pytz.timezone('UTC')
        local_tz = pytz.timezone('America/Los_Angeles')

        dt = datetime(2014, 8, 24, 0, 0, 0)
        local_dt = utc_to_local(dt, local_tz=local_tz)

        dt_aware = utc_tz.localize(dt)
        expected = dt_aware.astimezone(local_tz)

        self._msg('test', 'utc_to_local', first=True)
        self._msg('dt', dt)
        self._msg('local_dt', local_dt)
        self._msg('expected', expected)
        self.assertEqual(local_dt, expected)
