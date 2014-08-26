# -*- coding: utf-8 -*-
"""
garage.help_text

Helper function to retrieve help text for backend admin form views.

* created: 2011-03-18 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-26 kchan
"""

from __future__ import unicode_literals


# maintain a help text registry for django models

HELP_TEXT_REGISTRY = {}

def register_help_text_dictionary(module, dictionary):
    HELP_TEXT_REGISTRY[module] = dictionary


def unregister_help_text_dictionary(module):
    try:
        d = HELP_TEXT_REGISTRY.get(module)
        del HELP_TEXT_REGISTRY[module]
        return d
    except (AttributeError, KeyError):
        return None


def get_help_text_registry(module=None):
    if module:
        return HELP_TEXT_REGISTRY.get(module)
    return HELP_TEXT_REGISTRY


def get_help_text(module, model, field, default_dict={}):
    """
    Legacy function for compatiblity with old projects using the
    `help_text` module.

    Get help text for model and field in module help registry.

    """
    for d in [get_help_text_registry(module), default_dict]:
        try:
            txt = d[model].get(field)
            if txt:
                return txt
        except (TypeError, KeyError):
            pass
    return ''
