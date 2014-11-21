# -*- coding: utf-8 -*-
"""
garage.test.utils

Utility functions for tests (using Django test runner).

* created: 2013-07-20 kevin chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import importlib
import inspect

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
        importlib.import_module(module_name)
    except ImportError:
        return False
    else:
        return True


def function_exists(mod, func):
    """
    Test if function exists in module.
    * see: http://stackoverflow.com/questions/20926909/

    :param mod: module name (e.g. garage.utils)
    :param func: function name
    :returns: True if exists, else False
    """
    try:
        m = importlib.import_module(mod)
        f = getattr(m, func)
        return inspect.isfunction(f)
    except ImportError:
        pass
    return False


def var_exists(mod, var_name):
    """
    Test if variable exists in module.
    * see: http://stackoverflow.com/questions/20926909/

    :param mod: module name (e.g. garage.utils)
    :param var_name: variable name
    :returns: True if exists, else False
    """
    try:
        m = importlib.import_module(mod)
        return var_name in dir(m)
    except (ImportError, AttributeError):
        pass
    return False


class DummyObject(object):
    """
    Generic object for testing.
    """
    def __init__(self, *args, **kwargs):
        for k, v in kwargs.items():
            if not k.startswith('_'):
                setattr(self, k, v)
