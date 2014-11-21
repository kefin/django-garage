# -*- coding: utf-8 -*-
"""
tests.db.tests

Tests for garage.db

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from garage.test import SimpleTestCase

from mock import MagicMock


class DbTests(SimpleTestCase):

    def test_batch_qs(self):
        """
        Ensure batch_qs function is working properly.
        """
        from garage.db import batch_qs, DEFAULT_QS_BATCH_SIZE
        self._msg('test', 'batch_qs', first=True)
        num_entries = 1000
        entries = MagicMock()
        entries.count.return_value = num_entries

        n = 0
        for start, end, total, qs in batch_qs(entries):
            self._msg('processing', '%s - %s of %s' % (start + 1, end, total))
            n += 1

        self._msg('total batches', n)
        total = int(num_entries/DEFAULT_QS_BATCH_SIZE)
        if num_entries % DEFAULT_QS_BATCH_SIZE:
            total += 1
        self.assertEqual(total, n)

    def test_clonable_mixin(self):
        """
        Ensure ClonableMixon class is working properly.

        TODO
        """
        from garage.db import ClonableMixin
        self._msg('test', 'ClonableMixin', first=True)

    def test_clone_objects(self):
        """
        Ensure clone_objects function is working properly.

        TODO
        """
        from garage.db import clone_objects
        self._msg('test', 'clone_objects', first=True)
