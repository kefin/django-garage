# -*- coding: utf-8 -*-
"""
garage.cache

Cache helpers.

* created: 2011-03-14 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-28 kchan
"""

from __future__ import unicode_literals

import six
import functools
import hashlib

from django.core.cache import cache


# cache helpers
# * uses django caching backend

def s2hex(s):
    """
    Convert any string to a hex-digit hash for use as cache key.
    * uses MD5 hash from hashlib

    :param s: string to hash
    :returns: hash of string as hex digits
    """
    from garage.text_utils import safe_str
    try:
        h = hashlib.md5(s).hexdigest()
    except UnicodeEncodeError:
        h = hashlib.md5(safe_str(s)).hexdigest()
    except:
        h = hashlib.md5(repr(s)).hexdigest()
    return h


CACHE_KEY_SEPARATOR = '/'

def cache_key(name, *args, **kwargs):
    """
    helper function to calculate cache key.
    * accepts the following keyword parameters:
      key_separator -- separator string to use when concatenating args
      prefix -- prefix to prepend to key (after hashing)

    :param name: text to create key hash
    :param args: list of strings to join to "name"
    :param kwargs: keyword arguments (see code below for keywords)
    :returns: hashed key
    """
    key_separator = kwargs.get('key_separator', CACHE_KEY_SEPARATOR)
    prefix = kwargs.get('prefix')
    if not hasattr(name, '__iter__'):
        name = [name]
    if len(args) > 0:
        name.extend(args)
    key = s2hex(key_separator.join(name))
    if prefix is not None:
        key = '%s%s' % (prefix, key)
    return key

def create_cache_key(name, *args, **kwargs):
    """
    Same as cache_key (for compatibility with legacy function).
    """
    return cache_key(name, *args, **kwargs)


DEFAULT_TIMEOUT = 1800

def cache_data(key=None, timeout=DEFAULT_TIMEOUT)):
    """
    Decorator to cache objects.
    * see: http://djangosnippets.org/snippets/492/
    """
    def decorator(f):
        @functools.wraps(f)
        def _cache_controller(*args, **kwargs):
            if key is None:
                k = f.__name__
            elif isinstance(key, six.string_types):
                k = key
            elif callable(key):
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
    if cache.get(key):
        cache.set(key, None, 0)
        result = True
    else:
        result = False
    return result
