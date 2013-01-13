# -*- coding: utf-8 -*-
"""
garage.cache

Cache helpers.

* created: 2011-03-14 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-01-12 kchan
"""

import hashlib
try:
    import cPickle as pickle
except ImportError:
    import pickle

from django.core.cache import cache

from garage import get_setting, get_site_id, logger
from garage.html_utils import safe_str



# cache helpers
# * simple caching for generic functions and objects
# * uses django caching backend

def s2hex(s):
    """Convert any string to hex digits (for use as cache key)."""
    try:
        return hashlib.md5(s).hexdigest()
    except UnicodeEncodeError:
        return hashlib.md5(safe_str(s)).hexdigest()
    except:
        return hashlib.md5(repr(s)).hexdigest()


# utility function to create cache key
# * accepts prefix string

def create_cache_key(s, prefix=None):
    """Generate cache key based on input data"""
    if prefix is None:
        prefix = ''
    return '%s%s' % (prefix, s2hex(s))


# helper function to calculate cache key with site id prefix

def cache_key(s, *args):
    s = [s]
    s.extend([a for a in args])
    return create_cache_key('_'.join(s), prefix='%s_' % str(get_site_id()))


# see:
# http://djangosnippets.org/snippets/492/

def cache_data(cache_key='', timeout=get_setting('OBJECT_CACHE_TIMEOUT')):
    """
    Decorator to cache objects.
    """
    def decorator(f):
        def _cache_controller(*args, **kwargs):
            if not get_setting('USE_MINI_CACHE'):
                return f(*args, **kwargs)
            if isinstance(cache_key, basestring):
                k = cache_key % locals()
            elif callable(cache_key):
                k = cache_key(*args, **kwargs)
            result = cache.get(k)
            if result is None:
                result = f(*args, **kwargs)
                cache.set(k, result, timeout)
                if get_setting('CACHE_DEBUG'):
                    logger().debug('Cached data: %s' % k)
            else:
                if get_setting('CACHE_DEBUG'):
                    logger().debug('Return cached data: %s' % k)
            return result
        return _cache_controller
    return decorator


def delete_cache(cache_key):
    """
    Delete cached object.
    """
    if not get_setting('USE_MINI_CACHE'):
        return False
    if cache.get(cache_key):
        cache.set(cache_key, None, 0)
        result = True
    else:
        result = False
    if get_setting('CACHE_DEBUG'):
        if result is True:
            logger().debug('delete_cache: Deleting cached data: %s' % cache_key)
        else:
            logger().debug('delete_cache: Unable to get cached data: %s' % cache_key)
    return result


#######################################################################
# cache function
# from: http://djangosnippets.org/snippets/202/

# def cache_function(length):
#   """
#   A variant of the snippet posted by Jeff Wheeler at
#   http://www.djangosnippets.org/snippets/109/
#
#   Caches a function, using the function and its arguments as the key, and the return
#   value as the value saved. It passes all arguments on to the function, as
#   it should.
#
#   The decorator itself takes a length argument, which is the number of
#   seconds the cache will keep the result around.
#
#   It will put in a MethodNotFinishedError in the cache while the function is
#   processing. This should not matter in most cases, but if the app is using
#   threads, you won't be able to get the previous value, and will need to
#   wait until the function finishes. If this is not desired behavior, you can
#   remove the first two lines after the ``else``.
#   """
#   def decorator(func):
#       def inner_func(*args, **kwargs):
#           raw = [func.__name__, func.__module__, args, kwargs]
#           pickled = pickle.dumps(raw, protocol=pickle.HIGHEST_PROTOCOL)
#           key = hashlib.md5.new(pickled).hexdigest()
#           value = cache.get(key)
#           if cache.has_key(key):
#               return value
#           else:
#               # This will set a temporary value while ``func`` is being
#               # processed. When using threads, this is vital, as otherwise
#               # the function can be called several times before it finishes
#               # and is put into the cache.
#               class MethodNotFinishedError(Exception): pass
#               cache.set(key, MethodNotFinishedError(
#                   'The function %s has not finished processing yet. This \
# value will be replaced when it finishes.' % (func.__name__)
#               ), length)
#               result = func(*args, **kwargs)
#               cache.set(key, result, length)
#               return result
#       return inner_func
#   return decorator
