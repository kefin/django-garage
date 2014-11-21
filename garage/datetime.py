# -*- coding: utf-8 -*-
"""
garage.datetime

Datetime and timezone utility functions.

* created: 2013-04-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import pytz


def get_local_tz():
    """
    Get local timezone.

    :returns: local timezone object
    """
    from django.utils.timezone import get_current_timezone_name
    from garage import get_setting
    local_timezone = get_setting('TIME_ZONE')
    if not local_timezone:
        local_timezone = get_current_timezone_name()
    local_tz = pytz.timezone(local_timezone)
    return local_tz


def convert_datetime(dt, from_tz, to_tz):
    """
    Convert datetime object from one timezone to another.

    How to use:
    loc_dt = datetime(2013, 4, 15, 22, 30, 30)
    from_tz = pytz.timezone('America/Los_Angeles')
    to_tz = pytz.utc
    utc_dt = convert_datetime(loc_dt, from_tz, to_tz)

    :param dt: datetime object
    :param from_tz: local timezone object
    :param to_tz: timezone object to convert datetime to
    :returns: converted datetime object (in target timezone)
    """
    try:
        t = from_tz.localize(dt)
        src_dt = from_tz.normalize(t)
    except (AttributeError, ValueError):
        src_dt = dt
    try:
        dst_dt = src_dt.astimezone(to_tz)
    except AttributeError:
        dst_dt = dt
    return dst_dt


def local_to_utc(dt, local_tz=None):
    """
    Convert datetime object from local time to UTC.
    * if local_tz is not specified, get timezone from django settings.

    How to use:
    local_dt = datetime(2013, 4, 15, 22, 30, 30)
    utc_dt = local_to_utc(local_dt)

    Reference link:
    * pytz utc conversion
    * http://stackoverflow.com/questions/1357711/pytz-utc-conversion

    :param dt: datetime object
    :param local_tz: use this local timezone object
    :returns: datetime object converted to UTC time
    """
    if local_tz is None:
        local_tz = get_local_tz()
    return convert_datetime(dt, local_tz, pytz.utc)


def utc_to_local(dt, local_tz=None):
    """
    Convert datetime object from UTC to local time.
    * if local_tz is not specified, get timezone from django settings.
    
    How to use:
    dt = datetime(2013, 4, 15, 22, 30, 30)
    utc_dt = dt.replace(tzinfo=pytz.utc)
    loc_dt = utc_to_local(utc_dt)

    :param dt: datetime object
    :param local_tz: use this local timezone object as target
    :returns: datetime object converted to target local timezone
    """
    if local_tz is None:
        local_tz = get_local_tz()
    return convert_datetime(dt, pytz.utc, local_tz)
