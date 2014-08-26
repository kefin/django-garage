# -*- coding: utf-8 -*-
"""
tests.slugify.tests

Tests for garage.slugify

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-24 kchan
"""

from __future__ import unicode_literals

from garage.test import SimpleTestCase


class SlugifyTests(SimpleTestCase):

    def test_strip_accents(self):
        """
        Ensure strip_accents function is working properly.
        """
        from garage.slugify import strip_accents
        self._msg('test', 'strip_accents', first=True)

        txt = u'écriture 寫作'
        expected = u'ecriture '
        result = strip_accents(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

    def test_slugify(self):
        """
        Ensure slugify function is working properly.
        """
        from garage.slugify import slugify
        self._msg('test', 'slugify', first=True)

        txt = u'The Renaissance of Giselle “G” Töngi'
        expected = u'the-renaissance-of-giselle-g-tongi'
        result = slugify(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

        txt = u'Apoyan resolución a favor de niños migrantes en LA'
        expected = u'apoyan-resolucion-a-favor-de-ninos-migrantes-en-la'
        result = slugify(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)


    def test_get_slug_separator(self):
        """
        Ensure get_slug_separator function is working properly.
        """
        self._msg('test', 'get_slug_separator', first=True)
        self._msg('TODO', '')


    def test_get_slug_iteration_separator(self):
        """
        Ensure get_slug_iteration_separator function is working properly.
        """
        self._msg('test', 'get_slug_iteration_separator', first=True)
        self._msg('TODO', '')


    def test_get_slug_base(self):
        """
        Ensure get_slug_base function is working properly.
        """
        self._msg('test', 'get_slug_base', first=True)
        self._msg('TODO', '')


    def test_slug_creation_error(self):
        """
        Ensure slug_creation_error function is working properly.
        """
        self._msg('test', 'slug_creation_error', first=True)
        self._msg('TODO', '')


    def test_create_unique_slug(self):
        """
        Ensure create_unique_slug function is working properly.
        """
        self._msg('test', 'create_unique_slug', first=True)
        self._msg('TODO', '')

