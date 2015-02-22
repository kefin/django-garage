# -*- coding: utf-8 -*-
"""
tests.base.tests

Base tests for garage

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from mock import Mock, patch,call

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


    def test_get_version(self):
        """
        get_version should return app version (in PEP 440 format) if
        parameter is None.
        * app version is in the form: (major, minor, revision)
        """
        self._msg('test', 'get_version', first=True)
        from garage import get_version
        version = get_version()
        self.assertTrue(len(version), 3)
        self._msg('version', version)

    def test_get_setting(self):
        """
        get_setting should return VARS defined in settings.
        """
        self._msg('test', 'get_setting', first=True)
        from garage import get_setting
        apps = get_setting('INSTALLED_APPS')
        self.assertTrue(apps is not None)
        secret_key = get_setting('SECRET_KEY')
        self.assertTrue(secret_key is not None)
        self._msg('INSTALLED_APPS', apps)

    def test_resp(self):
        """
        resp is a legacy function that works as a shorcut to
        ``render_to_response``.
        * tests that ``render_to_response`` is being called.
        """
        self._msg('test', 'resp', first=True)
        from django.template import RequestContext
        from garage import resp
        with patch('django.shortcuts.render_to_response') as mock_render_to_response:
            expected = 'FOO'
            mock_render_to_response.return_value = expected
            request = Mock()
            template = Mock()
            context = {}
            result = resp(request, template, context)
            self.assertEqual(result, expected)
            self.assertTrue(mock_render_to_response.called)
            args, kwargs = mock_render_to_response.call_args
            self.assertEqual(args, (template, context))
            self.assertTrue('context_instance' in kwargs)
            self._msg('args', args)
            self._msg('kwargs', kwargs)
            self._msg('result', result)
