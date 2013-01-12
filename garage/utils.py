# -*- coding: utf-8 -*-
"""
garage.utils

Utility functions

* created: 2008-08-11 kevin chan <kefin@makedostudio.com>
* updated: 2013-01-12 kchan
"""

import os
import sys
import re
import hashlib
import string
import codecs
import yaml

try:
    from yaml import CLoader as Loader
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

from django.conf import settings



# add directory to module search path (sys.path)

def add_to_sys_path(app_dir):
    """
    Add directory to sys.path
    """
    if os.path.isdir(app_dir):
        sys.path.append(app_dir)


# import module given path

def import_module(path):
    """
    Dynamically import module from path and return a module object
    """
    try:
        assert path is not None and os.path.isfile(path)
        src = open(path, 'rb')
        m = hashlib.md5()
        m.update(path)
        module = imp.load_source(m.hexdigest(), path, src)
        src.close()
    except (TypeError, AssertionError, IOError):
        module = None
    return module


# import vars from module

def import_module_vars(module, *args):
    """
    Import vars from module
    * module is module name
    * args are variables to import
    * returns None on error, otherwise dict of name/values
    * if no args, return module __dict__

    Example:
    data = import_module_vars('webapp.urls', 'URLS')

    * see: http://stackoverflow.com/questions/2259427/load-python-code-at-runtime

    """
    try:
        m = __import__(module, globals(), locals(), args, -1)
    except ImportError:
        return None

    if module.find('.') != -1:
        # submodule
        m = sys.modules[module]

    if len(args) == 0:
        result = m.__dict__
    else:
        result = {}
        for name in args:
            try:
                result[name] = getattr(m, name)
            except AttributeError:
                result[name] = None
    return result


def import_module_settings(module):
    """
    Import settings from module
    * only global vars in ALL CAPS are imported
    * return None on error
    """
    data = import_module_vars(module)
    try:
        return dict([(k, v) for k, v in data.items() if k == k.upper()])
    except AttributeError:
        pass
    return None


# create class instance based on module and class name

def get_instance(module, class_name, *args, **kwargs):
    """
    Return an instance of the object based on
    module name and class name
    """
    __import__(module)
    f = getattr(sys.modules[module], class_name)
    obj = f(*args, **kwargs)
    return obj


# get text file content

default_encoding = "utf-8"

def get_file_contents(path, encoding=default_encoding):
    """
    Load text file from file system and return content as string.
    * default encoding is utf-8
    * return None is file cannot be read
    """
    try:
        assert path is not None and os.path.isfile(path)
        file_obj = codecs.open(path, "r", encoding)
        data = file_obj.read()
        file_obj.close()
    except (TypeError, AssertionError, IOError):
        data = None
    return data


# write data to file

def write_file(path, data, encoding=default_encoding):
    """
    Write text file to file system.
    """
    try:
        the_file = open(path, 'wb')
        the_file.write(data.encode(encoding))
        the_file.close()
        return True
    except IOError:
        return False


# make directories

def make_dir(path):
    """
    Make sure path exists by create directories
    * path should be directory path
      (example: /home/veryloopy/www/app/content/articles/archives/)
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
    :returns: loaded data structure
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


# encryption/decryption, encode/decode functions

def sha1hash(s):
    """
    Calculate sha1 hash in hex for string.
    """
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


# data object class for storing generic dict key/value pairs
#
# from web.py
#
# class Storage(dict):
#   """
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
#   """
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

class DataObject(dict):
    """
    Data object class

    * based on webpy dict-like Storage object
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
            if isinstance(d, basestring):
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

def enum(**enums):
    return type('Enum', (), enums)


# utility string functions

def trim(s):
    """Trim white space from beginning and end of string."""
    return s.lstrip().rstrip()


def cvt2list(s):
    """Convert object to list"""
    if isinstance(s, (list, tuple)):
        return s
    return [s]


def check_eos(s):
    """
    Check end of string and make sure there's a return.
    """
    cr = '\n'
    try:
        if not s.endswith(cr):
            s += cr
    except (TypeError, AttributeError):
        pass
    return s


# string test functions

def has_digits(s):
    """
    Test if string has digits.

    :param s: string
    :returns: number of digits in string
    """
    return len(set(s) & set(string.digits))

def has_alpha(s):
    """
    Test if string has alphabets.

    :param s: string
    :returns: number of letters in string
    """
    return len(set(s) & set(string.letters))

def has_alphanum(s):
    """
    Test if string has alphabets and digits.

    :param s: string
    :returns: number of letters and digits in string
    """
    alphanum = set(string.letters + string.digits)
    return len(set(s) & alphanum)


# convert uri request string to list

def uri_to_list(path):
    """
    Parse request path and split uri into list
    * /action/param1/param2 will be parsed as:
      ['action', 'param1', 'param2']
    """
    if path[0] == '/':
        path = path[1:]
    if path[-1:] == '/':
        path = path[:-1]
    return path.split('/')


# utility functions to convert names to/from CamelCase

def to_camel_case(name):
    """
    Convert name to CamelCase.
    * does not do any sanity checking (assumes name
      is somewhat already alphanumeric).
    """
    delete_chars = """'":;,~!@#$%^&*()_+-`=<>./?\\|"""
    result = []
    prev = ' '
    for c in name:
        if not prev.isalnum():
            c = c.upper()
        else:
            c = c.lower()
        result.append(c)
        prev = c
    return "".join(result).translate(string.maketrans(' -','__'), delete_chars)


# perform substitution on a chunk of text

# default id pattern: ${VARIABLE}
IdPattern = r'\$\{([a-z_][a-z0-9_]*)\}'
IdRegexp = re.compile(IdPattern, re.I)

def substitute(txt, context, pattern=None):
    """
    Perform variable substitution on a chunk of text.
    * returns None if input text is None.
    * default var pattern is ${var}

    Parameters:
    * txt is text or template to perform substitution on
    * context is dict of key/value pairs or callable to retrieve values
    * pattern is regexp pattern or compiled regexp object to perform match
    """
    if txt is None:
        return None
    if pattern is None:
        regexp = IdRegexp
    elif isinstance(pattern, basestring):
        regexp = re.compile(pattern, re.I)
    else:
        regexp = pattern
    if callable(context):
        getval = context
    else:
        if context is None:
            context = {}
        getval = lambda kw: context.get(kw, '')
    done = False
    while not done:
        matches = regexp.findall(txt)
        if len(matches) > 0:
            txt = regexp.sub(lambda m: getval(m.group(1)), txt)
        else:
            done = True
    return txt


# simple string substitution function

def subs(template, context):
    """
    Perform simple string substitutions using string template

    Example:
    Caption = '<div class="%(caption_css_class)s">%(caption)s</div>'
    output = subs(Caption, {
                    'caption_css_class': 'image_caption',
                    'caption': 'test'})

    """
    result = ''
    try:
        assert template is not None
        result = template % context
    except (AssertionError, TypeError):
        pass
    return result


# format timestamp/date string

def fmt_date(date_string, fmt='%Y-%m-%dT%H:%M:%S'):
    """
    Return formatted timestamp from iso 8601 date/time string
    * input should be YYYY-MM-DDTHH:MM:SS
    * default output is same (iso 8601)
    * bad input will return '1900-01-01T00:00:00'
    * TODO: timezone
    """
    def chkval(t):
        if t is None or len(t) == 0: return '0'
        else: return t
    default_timestamp = (1900, 1, 1, 0, 0, 0)
    pat = re.compile(r'^(\d+)-(\d+)-(\d+)(T(\d+):(\d+):?(\d+)?(\.\d+)?)?$')
    m = pat.match(date_string)
    if m:
        timestamp = m.group(1, 2, 3, 5, 6, 7)
    else:
        timestamp = default_timestamp
    dt = [int(chkval(t)) for t in timestamp]
    try:
        return datetime(*dt).strftime(fmt)
    except ValueError:
        return datetime(*default_timestamp).strftime(fmt)



# from: http://code.activestate.com/recipes/466341-guaranteed-conversion-to-unicode-or-byte-string/
# Recipe 466341 (r1): Guaranteed conversion to unicode or byte string

def safe_unicode(obj, *args):
    """ return the unicode representation of obj """
    try:
        return unicode(obj, *args)
    except UnicodeDecodeError:
        # obj is byte string
        ascii_text = str(obj).encode('string_escape')
        return unicode(ascii_text)

def safe_str(obj):
    """ return the byte string representation of obj """
    try:
        return str(obj)
    except UnicodeEncodeError:
        # obj is unicode
        return unicode(obj).encode('unicode_escape')


### get file basename and extensions

PATH_REGEXP_PAT = r'^(.*)(\.[^\.]+)$'
PathRegexp = None

def get_file_ext(filename):
    """
    Extract extension for file.
    """
    global PathRegexp
    if PathRegexp is None:
        PathRegexp = re.compile(PATH_REGEXP_PAT, re.I)
    m = PathRegexp.match(filename)
    if m:
        fbase, fext = m.groups()
    else:
        fbase, fext = (filename, '')
    return fbase, fext
