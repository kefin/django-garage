# -*- coding: utf-8 -*-
"""
garage.test.utils

Utility functions for tests (using Django test runner).

* created: 2013-07-20 kevin chan <kefin@makedostudio.com>
* updated: 2014-08-24 kchan
"""

from __future__ import unicode_literals

from garage.test.settings import DIVIDER


# helper functions

def msg(label, txt, first=False, linebreak=False, divider=DIVIDER):
    """
    Print out debug message.
    """
    from garage.text_utils import uprint, safe_unicode
    if first:
        uprint(u'\n%s' % safe_unicode(divider))
    label = safe_unicode(label)
    txt = safe_unicode(txt)
    if not linebreak:
        uprint(u'# %-16s : %s' % (label, txt))
    else:
        uprint(u'# %-16s :\n%s' % (label, txt))


def module_exists(module_name):
    """
    Check if module is importable.

    :param module_name: name of module to import (basestring)
    :returns: True if importable else False
    """
    try:
        __import__(module_name)
    except ImportError:
        return False
    else:
        return True


class DummyObject(object):
    """
    Generic object for testing.
    """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if not k.startswith('_'):
                setattr(self, k, v)
