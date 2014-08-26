# -*- coding: utf-8 -*-
"""
tests.session.tests

Tests for garage.session

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-08-24 kchan
"""

from __future__ import unicode_literals

from garage.test import SimpleTestCase

from mock import MagicMock


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

        request.session.get.return_value = val
        result = get_session_var(request, key)
        self.assertEqual(result, val)
        self._msg('key', key)
        self._msg('val', val)
        self._msg('result', result)

        val = 'Yes!'
        request.session.get.return_value = val
        result = get_session_var(request, key)
        self.assertEqual(result, val)
        self._msg('key', key)
        self._msg('val', val)
        self._msg('result', result)
