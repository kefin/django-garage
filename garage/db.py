# -*- coding: utf-8 -*-
"""
garage.db

Django database and queryset helper functions

* created: 2011-02-15 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import copy


# batch queryset iterator
#
# from:
# http://djangosnippets.org/snippets/1170/
#
# Most of the time when I need to iterate over Whatever.objects.all()
# in a shell script, my machine promptly reminds me that sometimes even
# 4GB isn't enough memory to prevent swapping like a mad man, and
# bringing my laptop to a crawl. I've written 10 bazillion versions of
# this code. Never again.
#
# Caveats
#
# Note that you'll want to order the queryset, as ordering is not
# guaranteed by the database and you might end up iterating over some
# items twice, and some not at all. Also, if your database is being
# written to in between the time you start and finish your script,
# you might miss some items or process them twice.
#

# batch size for queryset iterator
# * number of entries to retrieve and iterate in batches
DEFAULT_QS_BATCH_SIZE = 50

def batch_qs(qs, batch_size=DEFAULT_QS_BATCH_SIZE):
    """
    Returns a (start, end, total, queryset) tuple for each batch in the given
    queryset.

    Usage:

    # Make sure to order your querset
    article_qs = Article.objects.order_by('id')
    for start, end, total, qs in batch_qs(article_qs):
        print "Now processing %s - %s of %s" % (start + 1, end, total)
        for article in qs:
            print article.body

    """
    total = qs.count()
    for start in range(0, total, batch_size):
        end = min(start + batch_size, total)
        yield (start, end, total, qs[start:end])


class ClonableMixin(object):
    """
    Model mixin with method to clone objects.
    * from:
      http://djangosnippets.org/snippets/1271/
    """

    def clone(self):
        """Return an identical copy of the instance with a new ID."""
        if not self.pk:
            raise ValueError('Instance must be saved before it can be cloned.')
        duplicate = copy.copy(self)
        # Setting pk to None tricks Django into thinking this is a new object.
        duplicate.pk = None
        duplicate.save()
        # ... but the trick loses all ManyToMany relations.
        for field in self._meta.many_to_many:
            source = getattr(self, field.attname)
            destination = getattr(duplicate, field.attname)
            for item in source.all():
                destination.add(item)
        return duplicate


def clone_objects(objects):
    """
    Generic model object cloner function.
    * see:
      http://www.bromer.eu/2009/05/23/a-generic-copyclone-action-for-django-11/
      http://djangosnippets.org/snippets/1271/
    * The function below combines code from the above reference articles.
    """
    def clone(obj):
        """Return an identical copy of the instance with a new ID."""
        if not obj.pk:
            raise ValueError('Instance must be saved before it can be cloned.')
        duplicate = copy.copy(obj)
        # Setting pk to None tricks Django into thinking this is a new object.
        duplicate.pk = None
        duplicate.save()
        # ... but the trick loses all ManyToMany relations.
        for field in obj._meta.many_to_many:
            source = getattr(obj, field.attname)
            destination = getattr(duplicate, field.attname)
            for item in source.all():
                destination.add(item)
        return duplicate

    if not hasattr(objects,'__iter__'):
        objects = [objects]

    objs = []
    for obj in objects:
        new_obj = clone(obj)
        new_obj.save()
        objs.append(new_obj)

    return objs
