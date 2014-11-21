# -*- coding: utf-8 -*-
"""
tests.utils.tests

Tests for garage.utils

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import os
import sys

from garage.test import SimpleTestCase


TestData = """\
This is a test file.
"""

class UtilsTests(SimpleTestCase):

    def test_get_file_contents(self):
        """
        Ensure get_file_contents function is working properly.
        """
        self._msg('test', 'get_file_contents', first=True)
        from garage.utils import get_file_contents
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'testfile.txt')
        data = get_file_contents(path)
        self._msg('path', path)
        self._msg('data', data, linebreak=True)
        self.assertEqual(data, TestData)

    def test_write_file(self):
        """
        Ensure write_file function is working properly.
        """
        import tempfile
        from garage.utils import write_file, get_file_contents
        self._msg('test', 'write_file', first=True)
        filename = 'garage-testfile'
        tmpfile_dir = tempfile.gettempdir()
        path = os.path.join(tmpfile_dir, filename)
        result = write_file(path, TestData)
        self.assertTrue(result)
        # chect contents
        data = get_file_contents(path)
        self._msg('path', path)
        self._msg('data', data, linebreak=True)
        self.assertEqual(data, TestData)
        os.unlink(path)

    def test_make_dir(self):
        """
        Ensure make_dir function is working properly.
        """
        import tempfile
        from garage.utils import make_dir
        self._msg('test', 'make_dir', first=True)
        tmpfile_dir = tempfile.gettempdir()
        test_dir = 'garage-test-dir'
        path = os.path.join(tmpfile_dir, test_dir)
        result = make_dir(path)
        self.assertTrue(os.path.isdir(path))
        os.rmdir(path)
        self.assertFalse(os.path.isdir(path))
        self._msg('path', path)

    def test_load_yaml(self):
        """
        Ensure load_yaml function is working properly.
        """
        from garage.utils import load_yaml, get_file_contents
        self._msg('test', 'load_yaml', first=True)
        data = {
            'a': 1,
            'b': 2,
            'c': 'three'
        }
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'example_data.yaml')
        result = load_yaml(get_file_contents(path))
        self.assertEqual(result, data)
        self._msg('path', path)
        self._msg('expected', data)
        self._msg('result', result)


    def test_load_yaml_docs(self):
        """
        Ensure load_yaml_docs function is working properly.
        """
        from garage.utils import load_yaml_docs, get_file_contents
        self._msg('test', 'load_yaml_docs', first=True)
        data = [
            {
                'a': 1,
                'b': 2,
                'c': 'three'
            },
            {
                'x': 0,
                'y': 1,
                'z': 2
            }
        ]
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'example_yaml_docs.yaml')
        result = load_yaml_docs(get_file_contents(path))
        self._msg('path', path)
        self._msg('expected', data)
        self._msg('result', result)
        for i, y in enumerate(result):
            self.assertEqual(y, data[i])
            self._msg('yaml doc', y)

    def test_dump_yaml(self):
        """
        Ensure dump_yaml function is working properly.
        """
        from garage.utils import dump_yaml
        self._msg('test', 'dump_yaml', first=True)
        data = {
            'a': 1,
            'b': 2,
            'c': 'three'
        }
        y = dump_yaml(data, explicit_start=True, default_flow_style=False)
        self._msg('data', data)
        self._msg('yaml', y, linebreak=True)
        
    def test_sha1hash(self):
        """
        Ensure sha1hash function is working properly.
        """
        from garage.utils import sha1hash
        self._msg('test', 'sha1hash', first=True)

        data = 'this is a test'
        result = sha1hash(data)
        expected = 'fa26be19de6bff93f70bc2308434e4a440bbad02'
        self._msg('data', data)
        self._msg('rexpected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

        data = 'he said, "q & a" <abc> écriture 寫作'
        result = sha1hash(data)
        expected = '4c6e57246a9b857867d842534a618a1bdcf873be'
        self._msg('data', data)
        self._msg('rexpected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

    def test_encode_sdata(self):
        """
        Ensure encode_sdata function is working properly.
        """
        from garage.utils import encode_sdata
        self._msg('test', 'encode_sdata', first=True)
        data = 'this is a test'
        result = encode_sdata(data)
        expected = '5674686973206973206120746573740A70300A2E'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

        data = 'this is a test'
        result = encode_sdata(data)
        expected = '567468697320697'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self.assertNotEqual(result, expected)

    def test_decode_sdata(self):
        """
        Ensure decode_sdata function is working properly.
        """
        from garage.utils import decode_sdata
        self._msg('test', 'decode_sdata', first=True)
        data = '5674686973206973206120746573740A70300A2E'
        result = decode_sdata(data)
        expected = 'this is a test'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

        data = 'aaa5674686973206973206120746573740A70300A2E'
        result = decode_sdata(data)
        expected = 'this is a test'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self.assertEqual(result, None)

    def test_data_object(self):
        """
        Ensure DataObject class is working properly.
        """
        from garage.utils import DataObject
        self._msg('test', 'DataObject', first=True)
        data = {
            'a': 1,
            'b': 2,
            'c': 'three'
        }
        obj = DataObject(data)
        self._msg('data', data)
        self._msg('obj', obj)
        self._msg('len', len(obj))
        self.assertEqual(len(data), len(obj))
        for k, v in data.items():
            self.assertEqual(getattr(obj, k), v)

        data = {
            'a': 1,
            'b': 2,
            'c': 'three'
        }
        obj = DataObject(data)
        del data['c']
        del obj.c
        self._msg('data', data)
        self._msg('obj', obj)
        self._msg('len', len(obj))
        self.assertEqual(len(data), len(obj))
        for k, v in data.items():
            self.assertEqual(getattr(obj, k), v)

    def test_enum(self):
        """
        Ensure enum type is working properly.
        """
        from garage.utils import enum
        self._msg('test', 'enum', first=True)
        data = {
            'a': 1,
            'b': 2,
            'c': 'three'
        }
        obj = enum(a=1, b=2, c='three')
        for k, v in data.items():
            self.assertEqual(getattr(obj, k), v)
            self._msg(k, v)
        obj = enum('x', 'y', 'z')
        self.assertEqual(obj.x, 0)
        self.assertEqual(obj.y, 1)
        self.assertEqual(obj.z, 2)
        self._msg('x', obj.x)
        self._msg('y', obj.y)
        self._msg('z', obj.z)
        
    def test_get_file_ext(self):
        """
        Ensure get_file_ext function is working properly.
        """
        self._msg('test', 'get_file_ext', first=True)
        from garage.utils import get_file_ext
        path = '/home/user/test.txt'
        fbase, fext = get_file_ext(path)
        self.assertEqual(fext, '.txt')
        self._msg('path', path)
        self._msg('ext', fext)

        path = '/home/user/test'
        fbase, fext = get_file_ext(path)
        self.assertEqual(fext, '')
        self._msg('path', path)
        self._msg('ext', fext)
