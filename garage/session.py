# -*- coding: utf-8 -*-
"""
garage.session

Helper functions to set/get session data.
* The ``session`` object must be in the ``request`` passed to the functions.

* created: 2011-02-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)


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
        return request.session.get(skey, default)
    except (TypeError, AttributeError):
        return default
