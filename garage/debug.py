# -*- coding: utf-8 -*-
"""
garage.debug

Debugging utilities.

* created: 2011-02-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2011-10-24 kchan
"""

from garage.logger import logger



# decorator to time execution and dump to log file
# * see: http://stackoverflow.com/questions/4170992/

def print_latency(f):
    def wrapped(*args, **kwargs):
        try:
            start = time.time()
            r = f(*args, **kwargs)
        finally:
            logger().debug('Latency (%s): %.4fs' \
                               % (f.__name__, time.time() - start))
        return r
    wrapped.__name__ = f.__name__
    return wrapped
