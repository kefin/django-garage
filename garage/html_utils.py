# -*- coding: utf-8 -*-
"""
garage.html_utils

HTML utility functions.

* created: 2008-06-22 kevin chan <kefin@makedostudio.com>
* updated: 2012-07-14 kchan
"""

import re
import string
from unicodedata import normalize
from htmlentitydefs import codepoint2name, name2codepoint
from markdown import markdown
from textile import textile

from garage.utils import trim, safe_unicode, safe_str



### functions to escape html special characters

# escape basic html special characters (quotes, brackets, ampersands, etc.)

def html_escape(text):
    """
    Escape html entities within text.
    """
    htmlchars = {
        "&": "&amp;",
        '"': "&quot;",
        #"'": "&apos;",
        ">": "&gt;",
        "<": "&lt;",
        }
    if not isinstance(text, basestring):
        text = str(text)
    return ''.join([htmlchars.get(c, c) for c in text])


# convert non-ascii characters to html entities

def html_entities(u):
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


# convert string into "safe" html

def safe_html(data):
    """
    Convert string into "safe" html

    * escapes entities
    * converts unicode
    """
    return html_entities(safe_unicode(html_escape(data)))


def escape(txt):
    """Same as html_escape but accepts all kinds of input."""
    if isinstance(txt, basestring):
        return html_escape(txt)
    if isinstance(txt, (list, tuple)):
        return [html_escape(s) for s in txt]
    try:
        return dict([html_escape(k), html_escape(v)] for k, v in txt.items())
    except (AttributeError, TypeError, KeyError):
        return html_escape(txt)


def strip_tags(html_txt):
    """*Very simple* strip html tags function"""
    return re.sub(r'<[^>]*?>', '', html_txt)


def strip_html(text):
    """
    Removes HTML markup from a text string.

    :Info: http://effbot.org/zone/re-sub.htm#unescape-html

    :param text: The HTML source.
    :return: The plain text.  If the HTML source contains non-ASCII
    entities or character references, this is a Unicode string.
    """
    def fixup(m):
        text = m.group(0)
        if text[:1] == "<":
            return "" # ignore tags
        if text[:2] == "&#":
            try:
                if text[:3] == "&#x":
                    return unichr(int(text[3:-1], 16))
                else:
                    return unichr(int(text[2:-1]))
            except ValueError:
                pass
        elif text[:1] == "&":
            import htmlentitydefs
            entity = htmlentitydefs.entitydefs.get(text[1:-1])
            if entity:
                if entity[:2] == "&#":
                    try:
                        return unichr(int(entity[2:-1]))
                    except ValueError:
                        pass
                else:
                    return unicode(entity, "iso-8859-1")
        return text # leave as is
    return re.sub("(?s)<[^>]*>|&#?\w+;", fixup, text)


def unescape(text):
    """
    Removes HTML or XML character references and entities from a text string.

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


# ents.pty
# Convert SGML character entities into Unicode
#
# Function taken from:
# http://stackoverflow.com/questions/1197981/convert-html-entities-to-ascii-in-python/1582036#1582036
#
# Thanks agazso!

# def html2unicode(s):
#     """
#     Take an input string s, find all things that look like SGML character
#     entities, and replace them with the Unicode equivalent.
#
#     :Info:
#
#     http://stackoverflow.com/questions/1197981/convert-html-entities-to-ascii-in-python/1582036#1582036
#
#     """
#     matches = re.findall("&#\d+;", s)
#     if len(matches) > 0:
#         hits = set(matches)
#         for hit in hits:
#             name = hit[2:-1]
#             try:
#                 entnum = int(name)
#                 s = s.replace(hit, unichr(entnum))
#             except ValueError:
#                 pass
#     matches = re.findall("&\w+;", s)
#     hits = set(matches)
#     amp = "&"
#     if amp in hits:
#         hits.remove(amp)
#     for hit in hits:
#         name = hit[1:-1]
#         if name in name2codepoint:
#             s = s.replace(hit, unichr(name2codepoint[name]))
#     s = s.replace(amp, "&")
#     return s


### slugify functions

SlugDeleteChars = """'"‘’“”:;,~!@#$%^*()_+`=<>./?\\|—–"""

def strip_accents(s):
    """Strip accents from string and return ascii version."""
    return normalize('NFKD', unicode(s)).encode('ASCII', 'ignore')

def slugify(s, delete_chars=SlugDeleteChars):
    """Slugify string."""
    s = s.strip("\r\n")
    s = s.replace("\n", " ")
    s = trim(s)
    s = strip_html(strip_accents(unescape(s)))
    s = s.replace("–", "-")
    s = s.replace("—", "-")
    s = s.replace("&amp;", " and ")
    s = s.replace("&", " and ")
    s = re.sub(r'([0-9]+)%', '\\1-percent', s)
    s = s.translate(string.maketrans(' _','--'), delete_chars).lower()
    s = re.sub(r'--+', '-', s)
    s = s.strip('-')
    return s



########################################################################
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
        method = c.get(name.lower(), 'none')
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
