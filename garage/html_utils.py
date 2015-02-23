# -*- coding: utf-8 -*-
"""
garage.html_utils

Utility functions to handle html-text conversions.

* FIXME: need to reorganize, refactor and delete unnecessary code.

* created: 2008-06-22 kevin chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import six
import re
from htmlentitydefs import codepoint2name, name2codepoint
from markdown import markdown
from textile import textile


# functions to escape html special characters

def html_escape(text):
    """
    Escape reserved html characters within text.
    """
    htmlchars = {
        "&": "&amp;",
        '"': "&quot;",
        "'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
    }
    if isinstance(text, six.text_type):
        text = ''.join([htmlchars.get(c, c) for c in text])
    return text


def html_entities(u):
    """
    Convert non-ascii characters to old-school html entities.
    """
    result = []
    for c in u:
        if ord(c) < 128:
            result.append(c)
        else:
            try:
                result.append('&%s;' % codepoint2name[ord(c)])
            except KeyError:
                result.append("&#%s;" % ord(c))
    return ''.join(result)


def escape(txt):
    """
    Escapes html reserved characters (<>'"&) and convert non-ascii
    text to html entities.
    * To escape only html reserved characters (<>'"&), use
      `html_escape`.
    """
    return html_escape(html_entities(txt))


def unescape(text):
    """
    Removes HTML or XML character references and entities from a text string.
    * Note: does not strip html tags (use `strip_tags` instead for that).

    :Info: http://effbot.org/zone/re-sub.htm#unescape-html

    :param text: The HTML (or XML) source text.
    :return: The plain text, as a Unicode string, if necessary.
    """
    def fixup(m):
        text = m.group(0)
        if text[:2] == "&#":
            # character reference
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        else:
            # named entity
            try:
                text = unichr(name2codepoint[text[1:-1]])
            except KeyError:
                pass
        return text # leave as is
    return re.sub("&#?\w+;", fixup, text)


def strip_tags(html_txt):
    """
    Strip tags from html text (uses strip_tags from django.utils.html).
    * also unescapes html entities
    * fall back on using `re.sub` if django's `strip_tags` is not
      importable for some reason.
    """
    try:
        from django.utils.html import strip_tags as _strip_tags
    except ImportError:
        stripped = re.sub(r'<[^>]*?>', '', html_txt)
    else:
        stripped = _strip_tags(html_txt)
    return unescape(stripped)



# functions for converting plain text content to html
# * available conversion methods:
#   * no conversion
#   * markdown
#   * textile
#   * simple conversion of line breaks
#   * visual editor (using wysiwyg editor like TinyMCE)

NO_CONVERSION = 1
MARKDOWN_CONVERSION = 2
TEXTILE_CONVERSION = 3
SIMPLE_CONVERSION = 4
VISUAL_EDITOR = 5

CONVERSION_CHOICES = (
    (NO_CONVERSION, 'None'),
    (MARKDOWN_CONVERSION, 'Markdown'),
    (TEXTILE_CONVERSION, 'Textile'),
    (SIMPLE_CONVERSION, 'Simple (Convert Line Breaks)'),
    (VISUAL_EDITOR, 'Visual (WYSIWYG) Editor'),
)

CONVERSION_METHODS = (
    (NO_CONVERSION, 'none'),
    (MARKDOWN_CONVERSION, 'markdown'),
    (TEXTILE_CONVERSION, 'textile'),
    (SIMPLE_CONVERSION, 'markdown'),
    (VISUAL_EDITOR, 'visual')
)

def txt2html(txt, method):
    try:
        assert txt is not None and len(txt) > 0
        if method == MARKDOWN_CONVERSION:
            txt = markdown(txt)
        elif method == TEXTILE_CONVERSION:
            txt = textile(txt)
        elif method == SIMPLE_CONVERSION:
            txt = markdown(txt)
        else:
            # NO_CONVERSION
            pass
    except (TypeError, AssertionError):
        pass
    return txt


def get_cvt_method(name):
    """
    Get conversion method "code" corresponding to name
    """
    c = {
        'none': NO_CONVERSION,
        'markdown': MARKDOWN_CONVERSION,
        'textile': TEXTILE_CONVERSION
    }
    try:
        method = c.get(name.lower(), NO_CONVERSION)
    except (TypeError, AttributeError):
        method = NO_CONVERSION
    return method


def get_cvt_method_name(code):
    """
    Get conversion method name corresponding to "code"
    """
    if code > 0:
        code -= 1
    try:
        codenum, name = CONVERSION_METHODS[code]
    except:
        codenum, name = CONVERSION_METHODS[NO_CONVERSION]
    return name


def to_html(txt, cvt_method='markdown'):
    """
    Convert text block to html
    * cvt_method is name of method (markdown, textile, or none)
    * cf. txt2html where method is the conversion "code" (number)
    """
    return txt2html(txt, get_cvt_method(cvt_method))


# html-to-text utility function

def html_to_text(html):
    """
    Utility function to convert html content to plain text.
    * uses Django `strip_tags` function to convert html to text;
    * multiple blank lines are reduced to 2;
    * strips beginning and ending white space.
    * does not perform any kind of formatting or structuring to the
      plain text result.

    :param html: html content
    :returns: plain text content after conversion
    """
    from garage.text_utils import tidy_txt
    txt = tidy_txt(strip_tags(html))
    lines = []
    for line in txt.splitlines():
        s = line.strip()
        if len(s) > 0:
            lines.append(s)
    txt = '\n\n'.join(lines)
    txt = '%s\n' % txt
    return txt
