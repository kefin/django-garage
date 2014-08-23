# -*- coding: utf-8 -*-
"""
garage

Utilities and helpers functions.

* created: 2011-02-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-23 kchan
"""

# package version
VERSION = (0, 1, 8, 'alpha', 0)

def get_version(version=None):
    """
    Copied from django.utils.version.

    Returns a PEP 386-compliant version number from VERSION.
    """
    if version is None:
        version = VERSION
    else:
        assert len(version) == 5
        assert version[3] in ('alpha', 'beta', 'rc', 'final')

    # Now build the two parts of the version number:
    # main = X.Y[.Z]
    # sub = .devN - for pre-alpha releases
    #     | {a|b|c}N - for alpha, beta and rc releases

    parts = 2 if version[2] == 0 else 3
    main = '.'.join(str(x) for x in version[:parts])

    sub = ''

    # * Not used for this package.
    # if version[3] == 'alpha' and version[4] == 0:
    #     git_changeset = get_git_changeset()
    #     if git_changeset:
    #         sub = '.dev%s' % git_changeset
    # elif version[3] != 'final':

    if version[3] != 'final':
        mapping = {'alpha': 'a', 'beta': 'b', 'rc': 'c'}
        sub = mapping[version[3]] + str(version[4])

    return main + sub


# helper functions and shortcuts

# get setting

def get_setting(name, default=None):
    """Retrieve attribute from settings."""
    from django.conf import settings
    return getattr(settings, name, default)


# shortcuts

def resp(request, template, context):
    """Shortcut for render_to_response()."""
    from django.shortcuts import render_to_response
    from django.template import RequestContext
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
