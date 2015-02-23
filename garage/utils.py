# -*- coding: utf-8 -*-
"""
garage.utils

General utility functions.

* created: 2008-08-11 kevin chan <kefin@makedostudio.com>
* updated: 2015-02-22 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import six
import os
import sys
import re
import hashlib
import base64
import codecs

try:
    import cPickle as pickle
except ImportError:
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


# file read/write/delete helper functions

default_text_encoding = "utf-8"
default_encoding = default_text_encoding

def open_file(path, mode=None, encoding=None, **kwargs):
    """
    Helper function to open a file for reading/writing.

    :param path: path of file to read.
    :param mode: "b" for bytes or "t" for text (default is "t")
    :param encoding: file encoding for text (default is `utf-8`).
    :returns: stream object for reading/writing
    """
    try:
        from io import open as _open
    except ImportError:
        def _open(path, mode=None, encoding=None, **kwargs):
            return codecs.open(path, mode, encoding=encoding, **kwargs)
    return _open(path, mode=mode, encoding=encoding, **kwargs)


def get_file_contents(path, mode=None, encoding=None, **kwargs):
    """
    Load text file from file system and return content as text.

    :param path: path of file to read.
    :param mode: "b" for bytes or "t" for text (default is "t")
    :param encoding: file encoding for text (default is `utf-8`).
    :returns: file content as string or `None` if file cannot be read.

    This function reads the entire content of the file before
    returning the data as a string or as bytes.
    """
    try:
        assert path is not None and os.path.isfile(path)
    except AssertionError:
        data = None
    else:
        if not mode:
            mode = ''
        mode = 'r%s' % mode
        if 'b' in mode:
            encoding = None
        else:
            # read file as text
            if not encoding:
                encoding = default_text_encoding
        with open_file(path, mode=mode, encoding=encoding, **kwargs) as file_obj:
            data = file_obj.read()
    return data


def write_file(path, data, mode=None, encoding=None, **kwargs):
    """
    Write text file to file system.

    :param path: path of file to write to.
    :param data: data to write.
    :param mode: "b" for bytes or "t" for text (default is "t")
    :param encoding: file encoding for text (default is `utf-8`).
    :returns: `True` if no error or `False` if ``IOError``.
    """
    if not mode:
        mode = ''
    mode = 'w%s' % mode
    if 'b' in mode:
        encoding = None
    else:
        if not encoding:
            encoding = default_text_encoding
    try:
        with open_file(path, mode=mode, encoding=encoding, **kwargs) as file_obj:
            file_obj.write(data)
        return True
    except IOError:
        return False


def delete_file(path):
    """
    Truncates file to zero size and unlinks file.

    :param path: file system path for file
    :returns: True if file is unlinked (no longer found) else False
    """
    with open_file(path, mode='wb') as file_obj:
        file_obj.truncate(0)
    try:
        os.unlink(path)
    except OSError:
        pass
    return os.path.isfile(path) is False


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

def load_yaml(data):
    """
    Parse yaml data.

    # yaml usage:
    # data = load(stream, Loader=Loader)
    # output = dump(data, Dumper=Dumper)

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
    print(dump_yaml(y, explicit_start=True, default_flow_style=False))

    :param data: data structure
    :param opts: optional parameters for yaml engine
    :returns: YAML-formatted `basestring` for output
    """
    return yaml.dump(data, Dumper=Dumper, **opts)


def sha1hash(s):
    """
    Calculate sha1 hash in hex for string.
    """
    try:
        return hashlib.sha1(s).hexdigest()
    except UnicodeEncodeError:
        return hashlib.sha1(s.encode('utf-8')).hexdigest()


# encode/decode functions
# * note: encode_sdata and decode_sdata do not perform any sort of
#   encryption

def encode_sdata(data):
    """
    Encode data (dict) using pickle, b16encode and base64
    * Use ``decode_sdata`` to convert base16-encoded string back into
      Python data.

    :param data: any Python data object
    :returns: pickled byte string of data
    """
    return base64.b16encode(pickle.dumps(data))

def decode_sdata(encoded_string):
    """
    Decode data pickled and encoded using encode_sdata
    * Input must be base16-encoded string produced by the
      ``encode_sdata`` function.

    :param encoded_string: pickled string of data
    :returns: unpickled data or None if error
    """
    try:
        return pickle.loads(base64.b16decode(encoded_string))
    except (TypeError, EOFError, pickle.UnpicklingError):
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
    Enum type with ``reverse_mapping`` dict to retrieve key from value.

    from:
    http://stackoverflow.com/a/1695250/220783

    >>> Numbers = enum(ONE=1, TWO=2, THREE='three')
    >>> Numbers.ONE
    1
    >>> Numbers.TWO
    2
    >>> Numbers.THREE
    'three'
    >>> Numbers.reverse_mapping['three']
    'THREE'

    """
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
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


from garage.text_utils import (
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
