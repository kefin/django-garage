# -*- coding: utf-8 -*-
"""
garage

Utilities and helpers functions.

* created: 2011-02-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2013-01-12 kchan
"""

from django.conf import settings
from django.template import RequestContext


# helper functions and shortcuts

# get setting

def get_setting(name, default=None):
    """Retrieve attribute from settings."""
    return getattr(settings, name, default)


# shortcuts

def resp(request, template, context):
    """Shortcut for render_to_response()."""
    return render_to_response(template, context,
                              context_instance=RequestContext(request))


# get/set session vars

def set_session_var(request, skey, sval):
    """Set key-value in session cookie."""
    try:
        request.session[skey] = sval
    except (TypeError, AttributeError):
        pass


def get_session_var(request, skey, default=None):
    """Get value from session cookie."""
    try:
        return request.session.get(skey)
    except (TypeError, AttributeError):
        return None
