# -*- coding: utf-8 -*-
"""
garage.slugify

Functions to create slugs.

* created: 2011-02-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import re
import string
from unicodedata import normalize

from django.core.exceptions import ValidationError


# general slugify function

SlugDeleteChars = """'"‘’“”:;,~!@#$%^*()_+`=<>./?\\|—–"""
SubstChar = "-"

def strip_accents(s):
    """Strip accents from string and return ascii version."""
    return unicode(normalize('NFKD', unicode(s)).encode('ASCII', 'ignore'))


def slugify(s, delete_chars=SlugDeleteChars, subst_char=SubstChar):
    """
    Convert (unicode) string to slug.
    * This only handles Western-language strings with very basic
      accents.
    """
    from garage.html_utils import strip_tags, unescape

    def convert_unwanted_chars(txt):
        converted = []
        for ch in txt:
            if ch in delete_chars:
                ch = subst_char
            converted.append(ch)
        return ''.join(converted)

    s = s.strip("\r\n")
    s = s.replace("\n", " ")
    s = strip_accents(s)
    s = strip_tags(unescape(s))
    s = re.sub(r"['’]s", 's', s)
    s = re.sub(r'([0-9\.]+)%', '\\1-percent', s)
    s = s.replace("&amp;", " and ")
    s = s.replace("&", " and ")
    s = s.replace("/", " ")
    s = s.replace(" ", "-")
    s = s.replace("_", "-")
    s = convert_unwanted_chars(s)
    s = re.sub(r'\.\.+', '.', s)
    s = re.sub(r'--+', '-', s)
    s = s.strip('.')
    s = s.strip('-')
    s = s.lower()
    return s


# function to generate unique slugs for django model entries

# default slug spearators
SLUG_SEPARATOR = '-'
SLUG_ITERATION_SEPARATOR = '--'

def get_slug_separator():
    from garage import get_setting
    return get_setting('SLUG_SEPARATOR', SLUG_SEPARATOR)

def get_slug_iteration_separator():
    """
    The slug iteration separator is used to mark entries with the same slug base.

    e.g. article (first entry)
         article--2 (second entry)
    """
    from garage import get_setting
    return get_setting('SLUG_ITERATION_SEPARATOR', SLUG_ITERATION_SEPARATOR)


slug_pat = r'^(.+){0}(\d+)$'

def get_slug_base(slug, slug_iteration_separator=None):
    """
    Return slug minus the slug_iteration_separator + 'n' sufix.

    * Example: 'article--2' will return 'article' if
      slug_iteration_separator is '--'.
    """
    if not slug_iteration_separator:
        slug_iteration_separator = get_slug_iteration_separator()
    sep = re.escape(slug_iteration_separator)
    slug_regex = re.compile(slug_pat.format(sep), re.I)
    matched = slug_regex.match(slug)
    if matched:
        return matched.group(1)
    else:
        return slug


def slug_creation_error(msg=None):
    """
    This function is UNUSED and is here for compatibility purposes.
    """
    if msg is None:
        msg = 'Unable to create slug.'
    raise ValidationError(msg)


def get_unique_slug(instance, slug_field, queryset=None, slug_base=None,
                    prefix=None, suffix=None, slug_separator=None):
    """
    Helper function to generate unique slug for model entries.

    * object instance must already exist.
    * unqiue slug has the format: prefix-slug-n
    * examples:

    if prefix is '20110311-', generated unique slugs for identically
    slugged articles will produce:

    article -> 20110311-article
    article -> 20110211-article--2
    article -> 20110211-article--3
    etc.

    :param instance: object instance
    :param slug_base: slug to use as base for unique slug
    :param slug_field: unique slug field name for queries to test uniqueness
    :param queryset: queryset to use for db access (optional)
    :param prefix: prefix to prepend to unique slug before doing query
    :param suffix: suffix to prepend to unique slug before doing query
    :param slug_separator: string to separate last part of the slug
           from the base (default: SLUG_ITERATION_SEPARATOR)
    :returns: (unque_slug, unique_slug_without_prefix)
    """
    if not prefix:
        prefix = ''
    if not suffix:
        suffix = ''
    if not slug_separator:
        slug_separator = get_slug_iteration_separator()
    try:
        if queryset is None:
            queryset = instance.__class__._default_manager.all()
        if instance.pk:
            queryset = queryset.exclude(pk=instance.pk)
        if slug_base is None:
            try:
                slug_base = getattr(instance, slug_field)
            except AttributeError:
                slug_base = 'entry'
        slug = None
        num = ''
        next = 1
        while 1:
            slug = '%s%s%s' % (slug_base, num, suffix)
            unique_slug = '%s%s' % (prefix, slug)
            if not queryset.filter(**{slug_field: unique_slug}):
                return (unique_slug, slug)
            next += 1
            num = '%s%d' % (slug_separator, next)
    except (AttributeError, TypeError):
        msg = 'Unable to create slug.'
        raise ValidationError(msg)


def create_unique_slug(obj, slug_field=None, slug_separator=None):
    """
    Create simple unique slug for object instance.

    * if slug_field is not supplied, assume it's called 'slug'.

    :param instance: model object instance
    :returns: unique slug
    """
    if not slug_field:
        slug_field = 'slug'
    try:
        sbase = get_slug_base(getattr(obj, slug_field))
    except (AttributeError, TypeError):
        sbase = None
    slugs = get_unique_slug(obj,
                            slug_field=slug_field,
                            slug_base=sbase,
                            slug_separator=slug_separator)
    return slugs[0]



# unique slug function
# from: http://djangosnippets.org/snippets/690/
#
# def unique_slugify(instance, value, slug_field_name='slug', queryset=None,
#                  slug_separator='-'):
#   """
#   Calculates and stores a unique slug of ``value`` for an instance.
#
#   ``slug_field_name`` should be a string matching the name of the field to
#   store the slug in (and the field to check against for uniqueness).
#
#   ``queryset`` usually doesn't need to be explicitly provided - it'll default
#   to using the ``.all()`` queryset from the model's default manager.
#   """
#   slug_field = instance._meta.get_field(slug_field_name)
#
#   slug = getattr(instance, slug_field.attname)
#   slug_len = slug_field.max_length
#
#   # Sort out the initial slug, limiting its length if necessary.
#   slug = slugify(value)
#   if slug_len:
#       slug = slug[:slug_len]
#   slug = _slug_strip(slug, slug_separator)
#   original_slug = slug
#
#   # Create the queryset if one wasn't explicitly provided and exclude the
#   # current instance from the queryset.
#   if queryset is None:
#       queryset = instance.__class__._default_manager.all()
#   if instance.pk:
#       queryset = queryset.exclude(pk=instance.pk)
#
#   # Find a unique slug. If one matches, at '-2' to the end and try again
#   # (then '-3', etc).
#   next = 2
#   while not slug or queryset.filter(**{slug_field_name: slug}):
#       slug = original_slug
#       end = '%s%s' % (slug_separator, next)
#       if slug_len and len(slug) + len(end) > slug_len:
#           slug = slug[:slug_len-len(end)]
#           slug = _slug_strip(slug, slug_separator)
#       slug = '%s%s' % (slug, end)
#       next += 1
#
#   setattr(instance, slug_field.attname, slug)
#
#
# def _slug_strip(value, separator='-'):
#   """
#   Cleans up a slug by removing slug separator characters that occur at the
#   beginning or end of a slug.
#
#   If an alternate separator is used, it will also replace any instances of
#   the default '-' separator with the new separator.
#   """
#   separator = separator or ''
#   if separator == '-' or not separator:
#       re_sep = '-'
#   else:
#       re_sep = '(?:-|%s)' % re.escape(separator)
#   # Remove multiple instances and if an alternate separator is provided,
#   # replace the default '-' separator.
#   if separator != re_sep:
#       value = re.sub('%s+' % re_sep, separator, value)
#   # Remove separator from the beginning and end of the slug.
#   if separator:
#       if separator != '-':
#           re_sep = re.escape(separator)
#       value = re.sub(r'^%s+|%s+$' % (re_sep, re_sep), '', value)
#   return value

#######################################################################
