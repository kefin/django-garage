# -*- coding: utf-8 -*-
"""
tests.help_text.tests

Tests for garage.help_text

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from garage.test import SimpleTestCase


Module = 'DummyModule'
HelpText = {
    'article': {
        'title': 'Article Title',
        'slug': 'article-slug',
        'content': 'Article Content',
        'author': 'Article Author',
    },
    'author': {
        'first_name': 'First Name',
        'last_name': 'Last Name',
        'email': 'Email',
        'username': 'Username',
    }
}

class HelpTextTests(SimpleTestCase):

    def test_register_help_text_dictionary(self):
        """
        Ensure register_help_text_dictionary function is working properly.
        """
        from garage.help_text import (
            register_help_text_dictionary,
            HELP_TEXT_REGISTRY
        )
        self._msg('test', 'register_help_text_dictionary', first=True)

        register_help_text_dictionary(Module, HelpText)
        self.assertTrue(Module in HELP_TEXT_REGISTRY)
        h = HELP_TEXT_REGISTRY[Module]
        self.assertEqual(HelpText, h)
        self._msg('module', Module)
        self._msg('help text', h)

    def test_unregister_help_text_dictionary(self):
        """
        Ensure unregister_help_text_dictionary function is working properly.
        """
        from garage.help_text import (
            register_help_text_dictionary,
            unregister_help_text_dictionary,
            HELP_TEXT_REGISTRY
        )
        self._msg('test', 'unregister_help_text_dictionary', first=True)

        register_help_text_dictionary(Module, HelpText)
        self.assertTrue(Module in HELP_TEXT_REGISTRY)
        h = HELP_TEXT_REGISTRY[Module]
        self.assertTrue(h, HelpText)
        result = unregister_help_text_dictionary(Module)
        self.assertFalse(Module in HELP_TEXT_REGISTRY)
        self.assertEqual(result, HelpText)
        self._msg('module', Module)
        self._msg('deleted help text', h)

        result = unregister_help_text_dictionary('ABC')
        self.assertTrue(result is None)

    def test_get_help_text_registry(self):
        """
        Ensure get_help_text_registry function is working properly.
        """
        from garage.help_text import (
            register_help_text_dictionary,
            get_help_text_registry,
            HELP_TEXT_REGISTRY
        )
        self._msg('test', 'get_help_text_registry', first=True)

        register_help_text_dictionary(Module, HelpText)
        self.assertTrue(Module in HELP_TEXT_REGISTRY)
        expected = HELP_TEXT_REGISTRY[Module]
        self.assertEqual(expected, HelpText)

        h = get_help_text_registry(Module)
        self.assertEqual(h, HelpText)
        self._msg('module', Module)
        self._msg('help text', h)

        h = get_help_text_registry('ABC')
        self.assertFalse(h)
        self._msg('module', 'ABC')
        self._msg('help text', h)

        h = get_help_text_registry()
        self.assertEqual(h, HELP_TEXT_REGISTRY)
        self._msg('module', None)
        self._msg('help text', h)

    def test_get_help_text(self):
        """
        Ensure get_help_text function is working properly.
        """
        from garage.help_text import (
            register_help_text_dictionary,
            get_help_text,
            HELP_TEXT_REGISTRY
        )
        self._msg('test', 'get_help_text', first=True)

        register_help_text_dictionary(Module, HelpText)
        self.assertTrue(Module in HELP_TEXT_REGISTRY)
        expected = HELP_TEXT_REGISTRY[Module]
        self.assertEqual(expected, HelpText)

        model = 'article'
        field = 'slug'
        data = get_help_text(Module, model, field)
        expected = HelpText[model][field]
        self.assertEqual(data, expected)
        self._msg('module', Module)
        self._msg('model', model)
        self._msg('field', field)
        self._msg('expected', expected)
        self._msg('data', data)

        model = 'no-such-model'
        field = 'no-such-field'
        data = get_help_text(Module, model, field)
        expected = ''
        self.assertEqual(data, expected)
        self._msg('module', Module)
        self._msg('model', model)
        self._msg('field', field)
        self._msg('expected', expected)
        self._msg('data', data)
