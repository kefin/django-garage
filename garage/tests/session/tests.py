# -*- coding: utf-8 -*-
"""
tests.session.tests

Tests for garage.session

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-23 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from mock import Mock, MagicMock, patch, call

from garage.test import SimpleTestCase


class SessionTests(SimpleTestCase):

    def test_set_session_var(self):
        """
        Ensure set_session_var function is working properly.
        """
        from garage.session import set_session_var
        self._msg('test', 'set_session_var', first=True)
        key = 'abc'
        val = '123'
        request = MagicMock()
        my_dict = {}
        def getitem(name):
            return my_dict[name]
        def setitem(name, val):
            my_dict[name] = val
        request.session = MagicMock(spec_set=dict)
        request.session.__getitem__.side_effect = getitem
        request.session.__setitem__.side_effect = setitem
        set_session_var(request, key, val)
        result = my_dict[key]
        self._msg('key', key)
        self._msg('val', val)
        self._msg('result', result)
        self.assertEqual(result, val)

    def test_set_session_var_error(self):
        """
        set_session_var should bypass setting request.session raises
        exception.
        """
        from garage.session import set_session_var
        self._msg('test', 'set_session_var error', first=True)

        request = MagicMock()
        my_dict = {}
        def getitem(name):
            return my_dict[name]
        def setitem(name, val):
            my_dict[name] = 'AttributeError'
            raise AttributeError
        request.session = MagicMock(spec_set=dict)
        request.session.__getitem__.side_effect = getitem
        request.session.__setitem__.side_effect = setitem
        set_session_var(request, 'key', 'val')
        result = my_dict.get('key')
        self.assertEqual(result, 'AttributeError')
        self._msg('result', result)

        request = MagicMock()
        my_dict = {}
        def getitem(name):
            return my_dict[name]
        def setitem(name, val):
            my_dict[name] = 'TypeError'
            raise TypeError
        request.session = MagicMock(spec_set=dict)
        request.session.__getitem__.side_effect = getitem
        request.session.__setitem__.side_effect = setitem
        set_session_var(request, 'key', 'val')
        result = my_dict.get('key')
        self.assertEqual(result, 'TypeError')
        self._msg('result', result)

    def test_get_session_var(self):
        """
        Ensure get_session_var function is working properly.
        """
        from garage.session import get_session_var
        self._msg('test', 'get_session_var', first=True)
        key = 'abc'
        val = '123'
        request = MagicMock()
        my_dict = {key: val}
        def getitem(name):
            return my_dict[name]
        def setitem(name, val):
            my_dict[name] = val
        request.session = MagicMock(spec_set=dict)
        request.session.__getitem__.side_effect = getitem
        request.session.__setitem__.side_effect = setitem

        result = get_session_var(request, key)
        self.assertEqual(result, val)
        self._msg('key', key)
        self._msg('val', val)
        self._msg('result', result)

        val = 'foo'
        my_dict[key] = val
        result = get_session_var(request, key)
        self.assertEqual(result, val)
        self._msg('key', key)
        self._msg('val', val)
        self._msg('result', result)

    def test_get_session_var_error(self):
        """
        get_session_var should return default value if getting key
        raises exception.
        """
        from garage.session import get_session_var
        self._msg('test', 'get_session_var error', first=True)
        request = MagicMock()
        my_dict = {}
        def getitem(name):
            raise AttributeError
        def setitem(name, val):
            my_dict[name] = val
        request.session = MagicMock(spec_set=dict)
        request.session.__getitem__.side_effect = getitem
        request.session.__setitem__.side_effect = setitem
        result = get_session_var(request, 'key', default='AttributeError')
        calls = request.session.mock_calls
        self._msg('calls', calls)
        self.assertEqual(result, 'AttributeError')
        self._msg('result', result)

        request = MagicMock()
        my_dict = {}
        def getitem(name):
            raise TypeError
        def setitem(name, val):
            my_dict[name] = val
        request.session = MagicMock(spec_set=dict)
        request.session.__getitem__.side_effect = getitem
        request.session.__setitem__.side_effect = setitem
        result = get_session_var(request, 'key', default='TypeError')
        calls = request.session.mock_calls
        self._msg('calls', calls)
        self.assertEqual(result, 'TypeError')
        self._msg('result', result)
        
