# -*- coding: utf-8 -*-
"""
tests.urlgen.tests

Tests for garage.urlgen

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from garage.test import SimpleTestCase


class UrlgenTests(SimpleTestCase):

    def test_url_gen(self):
        """
        urlGen object should generate valid percent-encoded uri's.
        """
        self._msg('test', 'url_gen', first=True)
        from garage.urlgen import urlGen
        uri_obj = urlGen()
        params = {
            'sort': 1,
            'reverse': 0,
        }
        uri = uri_obj.generate('q', params)
        expected = '?sort=1&reverse=0&q='
        self.assertEqual(uri, expected)
        self._msg('uri', uri)
        self._msg('expected', expected)
