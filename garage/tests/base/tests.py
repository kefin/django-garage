# -*- coding: utf-8 -*-
"""
tests.base.tests

Base tests for garage

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-24 kchan
"""

from __future__ import unicode_literals

from garage.test import SimpleTestCase, module_exists


class BaseTests(SimpleTestCase):

    def test_module_imports(self):
        """
        Ensure modules are importable.
        """
        apps = (
            'garage',
            'garage.cache',
            'garage.datetime',
            'garage.db',
            'garage.exceptions',
            'garage.html_utils',
            'garage.image_utils',
            'garage.logger',
            'garage.session',
            'garage.slugify',
            'garage.test',
            'garage.test.base',
            'garage.test.settings',
            'garage.test.utils',
            'garage.text_utils',
            'garage.urlgen',
            'garage.utils',
        )
        self._msg('test', 'module imports', first=True)
        for a in apps:
            exists = module_exists(a)
            self._msg('exists', '%s: %s' % (a, exists))
            self.assertTrue(module_exists(a),
                            msg='Cannot import module: %s' % a)
