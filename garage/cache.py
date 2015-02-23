# -*- coding: utf-8 -*-
"""
garage.cache

Cache helpers
* The cache functions/decorators use the Django's caching backend.

* created: 2011-03-14 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-22 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import six
import functools
import hashlib
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.core.cache import cache


def s2hex(s):
    """
    Convert any string to a hex-digit hash for use as cache key.
    * uses MD5 hash from hashlib

    :param s: string to hash
    :returns: hash of string as hex digits
    """
    try:
        hashed = hashlib.md5(s).hexdigest()
    except UnicodeEncodeError:
        hashed = hashlib.md5(s.encode('utf-8')).hexdigest()
    except TypeError:
        hashed = hashlib.md5(pickle.dumps(s)).hexdigest()
    return hashed


CACHE_KEY_SEPARATOR = '/'

def cache_key(keystr, *args, **kwargs):
    """
    A helper function to calculate a hashed cache key.
    * accepts the following keyword parameters:
      key_separator -- separator string to use when concatenating args
      prefix -- prefix to prepend to key (after hashing)

    :param keystr: text to create key hash
    :param args: list of strings to join to "keystr"
    :param kwargs: keyword arguments (see code below for keywords)
    :returns: hashed key
    """
    key_separator = kwargs.get('key_separator', CACHE_KEY_SEPARATOR)
    prefix = kwargs.get('prefix')

    if not hasattr(keystr, '__iter__'):
        key_data = [keystr]
    else:
        key_data = keystr
    if len(args) > 0:
        key_data.extend(args)

    elems = []
    for s in key_data:
        if not isinstance(s, six.string_types):
            s = pickle.dumps(s)
        elems.append(s)

    key_string = key_separator.join(elems)
    key = s2hex(key_string)
    if prefix is not None:
        key = '{0}{1}'.format(prefix, key)
    return key

def create_cache_key(name, *args, **kwargs):
    """
    Same as cache_key (for compatibility with legacy function).
    """
    return cache_key(name, *args, **kwargs)


DEFAULT_TIMEOUT = 1800

def cache_data(key=None, timeout=DEFAULT_TIMEOUT):
    """
    A decorator to cache objects.
    * see: http://djangosnippets.org/snippets/492/

    How to use:

    # cache output of ``myfunc`` for 5 min.
    @cache_data(key='mymodule.myfunc', timeout=300)
    def myfunc(arg):
        ...

    # to delete/invalidate cached data, use the ``delete_cache``
    # function:
    delete_cache('mymodule.myfunc')

    """
    def decorator(f):
        @functools.wraps(f)
        def _cache_controller(*args, **kwargs):
            if key is None:
                k = f.__name__
            elif isinstance(key, six.string_types):
                k = key
            elif hasattr(key, '__call__'):
                k = key(*args, **kwargs)
            result = cache.get(k)
            if result is None:
                result = f(*args, **kwargs)
                cache.set(k, result, timeout)
            return result
        return _cache_controller
    return decorator


def delete_cache(key):
    """
    Delete cached object.

    :param key: key to retrieve data from cache
    :returns: True if cached data is found and deleted else False
    """
    if key in cache:
        cache.set(key, None, 0)
        return True
    else:
        return False
