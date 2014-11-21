# -*- coding: utf-8 -*-
"""
garage.utils

Utility functions

* created: 2008-08-11 kevin chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import six
import os
import sys
import re
import hashlib
import base64
import codecs
import pickle
import yaml

try:
    from yaml import (
        CLoader as Loader,
        CDumper as Dumper
    )
except ImportError:
    from yaml import Loader, Dumper


def get_instance(module, class_name, *args, **kwargs):
    """
    Return an instance of the object based on
    module name and class name.

    :param module: module name (e.g. garage.utils)
    :param class_name: name of class defined in module (e.g. DataObject)
    :param args, kwargs: args and kwargs to supply to class when
        creating instance
    :returns: object instance of class
    """
    if not module in sys.modules:
        __import__(module)
    f = getattr(sys.modules[module], class_name)
    obj = f(*args, **kwargs)
    return obj


default_encoding = "utf-8"

def get_file_contents(path, encoding=default_encoding):
    """
    Load text file from file system and return content as string.
    * default encoding is utf-8

    :param path: path to file on local file system
    :param encoding: encoding for file date (default: utf-8)
    :returns: file data or None is file cannot be read
    """
    try:
        assert path is not None and os.path.isfile(path)
        file_obj = codecs.open(path, "r", encoding)
        data = file_obj.read()
        file_obj.close()
    except (TypeError, AssertionError, IOError):
        data = None
    return data


def write_file(path, data, encoding=default_encoding):
    """
    Write text to local file system.

    :param path: path to file to write to on local file system
    :param encoding: encoding for file date (default: utf-8)
    :returns: True if successful else False
    """
    try:
        the_file = open(path, 'wb')
        the_file.write(data.encode(encoding))
        the_file.close()
        return True
    except IOError:
        return False


def make_dir(path):
    """
    Make sure path exists by create directories
    * path should be directory path
      (example: /home/veryloopy/www/app/content/articles/archives/)

    :param path: path to directory
    :returns: True if directory exists else False
    """
    if not os.path.exists(path):
        try:
            os.makedirs(path)
        except OSError:
            pass
    if os.path.exists(path):
        return True
    else:
        return False


# YAML utilities

# yaml usage:
# data = load(stream, Loader=Loader)
# output = dump(data, Dumper=Dumper)

def load_yaml(data):
    """
    Parse yaml data.

    :param data: YAML-formatted data
    :returns: loaded data structure
    """
    return yaml.load(data, Loader=Loader)


def load_yaml_docs(data):
    """
    Parse a series of documents embedded in a YAML file.

    * documents are delimited by '---' in the file

    :param data: YAML-formatted data
    :returns: generator object with loaded data
    """
    return yaml.load_all(data, Loader=Loader)


def dump_yaml(data, **opts):
    """
    Dump data structure in yaml format.

    example usage:
    print dump_yaml(y, explicit_start=True, default_flow_style=False)

    :param data: data structure
    :param opts: optional parameters for yaml engine
    :returns: YAML-formatted `basestring` for output
    """
    return yaml.dump(data, Dumper=Dumper, **opts)


def sha1hash(s):
    """
    Calculate sha1 hash in hex for string.
    """
    from garage.text_utils import safe_str
    try:
        return hashlib.sha1(s).hexdigest()
    except UnicodeEncodeError:
        return hashlib.sha1(safe_str(s)).hexdigest()
    except:
        return hashlib.sha1(repr(s)).hexdigest()


# encode/decode functions
# * note: encode_sdata and decode_sdata do not perform any sort of
#   encryption

def encode_sdata(data):
    """
    Encode data (dict) using pickle, b16encode and base64

    :param data: any Python data object
    :returns: pickled string of data
    """
    try:
        return base64.b16encode(pickle.dumps(data))
    except:
        return ''

def decode_sdata(encoded_string):
    """
    Decode data pickled and encoded using encode_sdata

    :param encoded_string: pickled string of data
    :returns: unpickled data
    """
    try:
        return pickle.loads(base64.b16decode(encoded_string))
    except:
        return None


class DataObject(dict):
    """
    Data object class
    * based on webpy dict-like Storage object

    # DataObject class for storing generic dict key/value pairs
    # * object is a dict that behaves like a class object (key/value
    #   can be accessed like object attributes).
    #
    # borrowed from web.py
    #
    # class Storage(dict):
    #   '''
    #   A Storage object is like a dictionary except `obj.foo` can be used
    #   in addition to `obj['foo']`.
    #
    #       >>> o = storage(a=1)
    #       >>> o.a
    #       1
    #       >>> o['a']
    #       1
    #       >>> o.a = 2
    #       >>> o['a']
    #       2
    #       >>> del o.a
    #       >>> o.a
    #       Traceback (most recent call last):
    #           ...
    #       AttributeError: 'a'
    #
    #   '''
    #   def __getattr__(self, key):
    #       try:
    #           return self[key]
    #       except KeyError, k:
    #           raise AttributeError, k
    #
    #   def __setattr__(self, key, value):
    #       self[key] = value
    #
    #   def __delattr__(self, key):
    #       try:
    #           del self[key]
    #       except KeyError, k:
    #           raise AttributeError, k
    #
    #   def __repr__(self):
    #       return '<Storage ' + dict.__repr__(self) + '>'
    #
    """

    def __init__(self, *args, **kwargs):
        self.add(*args, **kwargs)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k

    def __repr__(self):
        return '<DataObject ' + dict.__repr__(self) + '>'

    def add(self, *args, **kwargs):
        """
        add({
            'a': 1,
            'b': 3.14
            'c': 'foo'
        })
        """
        for d in args:
            if isinstance(d, six.string_types):
                self[d] = True
            elif isinstance(d, dict):
                for name, value in d.items():
                    self[name] = value
            else:
                try:
                    for name in d:
                        self[name] = True
                except TypeError:
                    pass
        for name, value in kwargs.items():
            try:
                self[name] = value
            except TypeError:
                pass


def enum(*sequential, **named):
    """
    Definition for an `enum` type.

    # enum type
    #
    # from:
    # http://stackoverflow.com/questions/36932/whats-the-best-way-to-implement-an-enum-in-python
    #
    # def enum(**enums):
    #     return type('Enum', (), enums)
    # Used like so:
    #
    # >>> Numbers = enum(ONE=1, TWO=2, THREE='three')
    # >>> Numbers.ONE
    # 1
    # >>> Numbers.TWO
    # 2
    # >>> Numbers.THREE
    # 'three'
    # You can also easily support automatic enumeration with something like this:
    #
    # def enum(*sequential, **named):
    #     enums = dict(zip(sequential, range(len(sequential))), **named)
    #     return type('Enum', (), enums)
    # Used like so:
    #
    # >>> Numbers = enum('ZERO', 'ONE', 'TWO')
    # >>> Numbers.ZERO
    # 0
    # >>> Numbers.ONE
    # 1

    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type(str('Enum'), (), enums)


# get file extension

def get_file_ext(filename):
    """
    Extract extension for file.
    * This simple function is here for legacy reasons. Some projects
      import this function from this module so it's here to keep those
      from breaking.

    :param filename: filename or path
    :returns: tuple of file base name and extension (extension is '' if none)
    """
    return os.path.splitext(filename)


# for compatibiity with old versions

def cvt2list(s):
    """Convert object to list"""
    if not hasattr(s, '__iter__'):
        s = [s]
    return s


from text_utils import (
    trim,
    check_eos,
    has_digits,
    has_alpha,
    has_alphanum,
    to_camel_case,
    substitute,
    subs,
    safe_unicode,
    safe_str
)
