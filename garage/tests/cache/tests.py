# -*- coding: utf-8 -*-
"""
tests.cache.tests

Tests for garage.cache

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from garage.test import SimpleTestCase


class CacheTests(SimpleTestCase):

    def test_s2hex(self):
        """
        Ensure s2hex function returns proper values.
        """
        from garage.cache import s2hex
        some_string = u'abcd1234 l’écriture 寫作'
        md5hash = u'3dc75e194bf9b951120746625998bc70'
        result = s2hex(some_string)
        self._msg('test', 's2hex', first=True)
        self._msg('some_string', some_string)
        self._msg('result', result)
        self.assertEqual(result, md5hash)

    def test_cache_key(self):
        """
        Ensure cache_key function is working.
        """
        from garage.cache import s2hex, cache_key
        some_string = u'abcd1234 l’écriture 寫作'
        md5hash = u'3dc75e194bf9b951120746625998bc70'
        prefix = u'CACHE:'
        key = '%s%s' % (prefix, s2hex(some_string))
        result = cache_key(some_string, prefix=prefix)
        self._msg('test', 'create_cache_key', first=True)
        self._msg('prefix', prefix)
        self._msg('some_string', some_string)
        self._msg('expected', key)
        self._msg('result', result)
        self.assertEqual(result, key)

    def test_create_cache_key(self):
        """
        Ensure create_cache_key function is working.
        """
        from garage.cache import create_cache_key, cache_key
        some_string = u'abcd1234 l’écriture 寫作'
        key = create_cache_key(some_string)
        result = cache_key(some_string)
        self._msg('test', 'cache_key', first=True)
        self._msg('some_string', some_string)
        self._msg('cache_key', key)
        self._msg('result', result)
        self.assertEqual(result, key)

    def test_cache_data(self):
        """
        Ensure cache_data decorator is working.
        * assumes CACHES is defined as a real cache (not dummy cache)

        """
        from django.conf import settings
        from django.core.cache import cache as django_cache
        from garage.cache import cache_key, cache_data, delete_cache
        from garage.text_utils import safe_str

        key = u'abcd1234'

        @cache_data(key)
        def dummy_func(*args):
            return u'_'.join([safe_str(a) for a in args])

        # make sure data is not in cache
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)

        # cache data
        some_data = [u'abcd1234', u'l’écriture', u'寫作']
        result = dummy_func(*some_data)

        # test if data is in cache
        cached_data = django_cache.get(key)

        self._msg('test', 'cache_data', first=True)
        self._msg('CACHES', repr(settings.CACHES))
        self._msg('key', key)
        self._msg('some_data', repr(some_data))
        self._msg('result', result)
        self._msg('cached_data', cached_data)
        self.assertEqual(result, cached_data)
        delete_cache(key)
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)

        # test cache_data without providing key

        @cache_data()
        def dummy_func(*args):
            return u'_'.join([safe_str(a) for a in args])

        key = dummy_func.__name__

        # make sure data is not in cache
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)

        # cache data
        some_data = [u'abcd1234', u'l’écriture', u'寫作']
        result = dummy_func(*some_data)

        # test if data is in cache
        cached_data = django_cache.get(key)

        self._msg('test', 'cache_data (without key)', first=True)
        self._msg('key', key)
        self._msg('some_data', repr(some_data))
        self._msg('result', result)
        self._msg('cached_data', cached_data)
        self.assertEqual(result, cached_data)
        delete_cache(key)
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)


    def test_delete_cache(self):
        """
        Ensure delete_cache function is working.
        """
        from django.conf import settings
        from django.core.cache import cache as django_cache
        from garage.cache import cache_key, cache_data, delete_cache
        from garage.text_utils import safe_str

        key = u'abcd1234'

        @cache_data(key)
        def dummy_func(*args):
            return u'_'.join([safe_str(a) for a in args])

        some_data = [u'abcd1234', u'l’écriture', u'寫作']
        result = dummy_func(*some_data)

        # test if data is in cache
        cached_data = django_cache.get(key)

        self._msg('test', 'delete_cache', first=True)
        self._msg('CACHES', repr(settings.CACHES))
        self._msg('key', key)
        self._msg('some_data', repr(some_data))
        self._msg('result', result)
        self._msg('cached_data', cached_data)
        self.assertEqual(result, cached_data)
        delete_cache(key)
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)
        self._msg('data after delete', cached_data)
