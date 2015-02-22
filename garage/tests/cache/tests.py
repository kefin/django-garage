# -*- coding: utf-8 -*-
"""
tests.cache.tests

Tests for garage.cache

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-22 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import pickle
import six

from garage.test import SimpleTestCase


class CacheTests(SimpleTestCase):

    def test_s2hex(self):
        """
        Ensure s2hex function returns proper values.
        """
        from garage.cache import s2hex

        some_string = 'abcd1234'
        md5hash = 'e19d5cd5af0378da05f63f891c7467af'
        result = s2hex(some_string)
        self._msg('test', 's2hex', first=True)
        self._msg('some_string', some_string)
        self._msg('result', result)
        self.assertEqual(result, md5hash)

        some_string = 'abcd1234 l’écriture 寫作'
        md5hash = 'c249c03ab4ee9b4045e653394fd60932'
        result = s2hex(some_string)
        self._msg('test', 's2hex', first=True)
        self._msg('some_string', some_string)
        self._msg('result', result)
        self.assertEqual(result, md5hash)

        data = ['foo', 'bar', 'baz']
        md5hash = 'ae0f56e9c34a13072ddf950d4d0e32d3'
        result = s2hex(data)
        self._msg('test', 's2hex', first=True)
        self._msg('data', data)
        self._msg('result', result)
        self.assertEqual(result, md5hash)

    def test_cache_key_with_simple_key_string(self):
        """
        cache_key should return an MD5 hash of the input key string.
        """
        from garage.cache import s2hex, cache_key
        some_string = 'abcd1234 l’écriture 寫作'
        md5hash = 'c249c03ab4ee9b4045e653394fd60932'
        prefix = 'CACHE:'
        key = '%s%s' % (prefix, s2hex(some_string))
        result = cache_key(some_string, prefix=prefix)
        self._msg('test', 'create_cache_key', first=True)
        self._msg('prefix', prefix)
        self._msg('some_string', some_string)
        self._msg('expected', key)
        self._msg('result', result)
        self.assertEqual(result, key)

        result = cache_key([some_string], prefix=prefix)
        self._msg('test', 'create_cache_key', first=True)
        self._msg('prefix', prefix)
        self._msg('some_string', some_string)
        self._msg('expected', key)
        self._msg('result', result)
        self.assertEqual(result, key)

    def test_cache_key_with_mixed_key_data(self):
        """
        cache_key should concatenate and convert all key data to base
        string to create the cache key.
        """
        from garage.cache import s2hex, cache_key, CACHE_KEY_SEPARATOR

        prefix = 'CACHE:'
        some_string = 'abcd1234 l’écriture 寫作'
        key_data = [
            some_string, 'a', 1, 'b', 2, 'c', 3, '寫作',
            {
                'key1': 'foo',
                'key2': 'bar',
            }
        ]

        elems = []
        for s in key_data:
            if not isinstance(s, six.string_types):
                s = pickle.dumps(s)
            elems.append(s)

        key_string = CACHE_KEY_SEPARATOR.join(elems)
        key = '{0}{1}'.format(prefix, s2hex(key_string))

        result = cache_key(*key_data, prefix=prefix)
        self._msg('test', 'create_cache_key', first=True)
        self._msg('prefix', prefix)
        self._msg('key data', key_data)
        self._msg('expected', key)
        self._msg('result', result)
        self.assertEqual(result, key)

    def test_create_cache_key(self):
        """
        Ensure create_cache_key function is working.
        """
        from garage.cache import create_cache_key, cache_key
        some_string = 'abcd1234 l’écriture 寫作'
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

        key = 'abcd1234'

        @cache_data(key)
        def dummy_func(*args):
            return '_'.join(args)

        # make sure data is not in cache
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)

        # cache data
        some_data = ['abcd1234', 'l’écriture', '寫作']
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
            return '_'.join([a for a in args])

        key = dummy_func.__name__

        # make sure data is not in cache
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)

        # cache data
        some_data = ['abcd1234', 'l’écriture', '寫作']
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

        # test cache_data with callable key

        def make_key(*args, **kwargs):
            k = '{0}#{1}'.format(repr(args), repr(kwargs))
            return k

        @cache_data(make_key)
        def dummy_func(*args):
            return '_'.join([a for a in args])

        # cache data
        some_data = ['abcd1234', 'l’écriture', '寫作']
        key = make_key(*some_data)

        # make sure data is not in cache
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)
        result = dummy_func(*some_data)

        # test if data is in cache
        cached_data = django_cache.get(key)

        self._msg('test', 'cache_data (without key)', first=True)
        self._msg('key (from callable)', key)
        self._msg('some_data', repr(some_data))
        self._msg('result', result)
        self._msg('cached_data', cached_data)
        self.assertEqual(result, cached_data)
        delete_cache(key)
        cached_data = django_cache.get(key)
        self.assertFalse(cached_data)

    def test_delete_cache_no_op(self):
        """
        delete_cache should return False and do nothing if key is not
        in cache.
        """
        from django.conf import settings
        from django.core.cache import cache as django_cache
        from garage.cache import delete_cache
        key = 'abcd1234'
        # test if data is in cache
        cached_data = django_cache.get(key)
        # delete cache and check result
        result = delete_cache(key)
        self._msg('test', 'delete_cache', first=True)
        self._msg('CACHES', repr(settings.CACHES))
        self._msg('key', key)
        self._msg('result', result)
        self._msg('cached_data', cached_data)
        self.assertFalse(cached_data)
        self.assertFalse(result)

    def test_delete_cache(self):
        """
        Ensure delete_cache function is working.
        """
        from django.conf import settings
        from django.core.cache import cache as django_cache
        from garage.cache import cache_key, cache_data, delete_cache

        key = 'abcd1234'

        @cache_data(key)
        def dummy_func(*args):
            return '_'.join([a for a in args])

        some_data = ['abcd1234', 'l’écriture', '寫作']
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
