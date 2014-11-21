# -*- coding: utf-8 -*-
"""
helpers.text_utils

Utility text and string processing functions

* created: 2013-10-27 kevin chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals, print_function)

import six
import re
import string


default_encoding = "utf-8"

def uprint(data, encoding=default_encoding):
    """
    Print unicode output to stdout.

    :param data: data to print.
    :param encoding: data encoding (default is `utf-8`).
    """
    try:
        print(data.encode(encoding))
    except AttributeError:
        print(data)


# utility string functions

def trim(s):
    """Trim white space from beginning and end of string."""
    return s.lstrip().rstrip()


CR = '\n'

def check_eos(s, cr=CR):
    """
    Check end of string and make sure there's a return.

    :param s: text
    :param cr: EOL character or string
    :returns: text wth EOL appended
    """
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


def tidy_txt(txt):
    """
    Utility function to tidy up text block by compressing multiple
    blank lines.
    * multiple (>2) blank lines are reduced to 2.

    :param txt: text block
    :returns: tidied up text block with multiple blank lines removed.
    """
    if isinstance(txt, six.text_type):
        lines = unicode(txt).split('\n')
        s = []
        run = 0
        for line in lines:
            txt = line.strip()
            if len(txt) == 0:
                if run < 1:
                    s.append(u'')
                run += 1
            else:
                run = 0
                s.append(txt)
        txt = '\n'.join(s)
    return txt


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

    caption_template = '<div class="%(caption_css_class)s">%(caption)s</div>'
    caption = subs(caption_template,
                  {
                      'caption_css_class': 'image-caption',
                      'caption': 'test'
                  })

    """
    result = u''
    try:
        assert template is not None
        result = template % context
    except (AssertionError, TypeError):
        pass
    return result


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


# utility function to truncate text

def truncate_chars(data, maxlen):
    """
    Truncate string to at most ``maxlen``, including elipsis.
    * uses django.utils.text Truncator class.

    :param data: string to truncate
    :param maxlen: length to truncate to
    :returns: string (truncated if necessary)
    """
    from django.utils.text import Truncator
    if isinstance(data, six.text_type) and len(data) > maxlen:
        truncator = Truncator(data)
        data = truncator.chars(maxlen)
    return data
