# -*- coding: utf-8 -*-
"""
tests.utils.tests

Tests for garage.utils

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-23 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import os
import sys
import tempfile
from mock import Mock, patch, call

from garage.test import SimpleTestCase


TestData = """\
This is a test file.
"""

class DummyTestObject(object):
    """
    Object definition to test get_instance.
    """
    name = 'dummy_test_object'


class UtilsTests(SimpleTestCase):

    def test_get_instance(self):
        """
        get_instance should return instance from module class.
        """
        self._msg('test', 'get_instance', first=True)
        from garage.utils import get_instance
        inst = get_instance('garage.tests.utils.tests', 'DummyTestObject')
        self.assertTrue(inst is not None)
        self.assertEqual(inst.name, 'dummy_test_object')
        self._msg('instance', inst)

    def test_encoding_constants(self):
        """
        garage.utils should contain a "default_encoding" constant.
        """
        self._msg('test', 'encoding constants', first=True)
        try:
            from garage.utils import default_text_encoding, default_encoding
        except ImportError:
            self.fail('default_text_encoding and default_encoding not found')
        self.assertEqual(default_encoding, 'utf-8')

    def test_open_file(self):
        """
        open_file should return a stream object if successful.
        """
        self._msg('test', 'open_file', first=True)
        from garage.utils import open_file
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'testfile.txt')
        mode = 'rt'
        with open_file(path, mode=mode) as file_obj:
            data = file_obj.read()
        expected = TestData
        self.assertEqual(data, expected)

    def test_open_file_error(self):
        """
        open_file should raise IOError if file cannot be opened.
        """
        self._msg('test', 'open_file error', first=True)
        from garage.utils import open_file
        mode = 'rt'
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'non-existent-file')
        with self.assertRaises(IOError):
            with open_file(path, mode=mode) as file_obj:
                data = file_obj.read()

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

    def test_get_file_contents_error(self):
        """
        get_file_contents should return None for a non-existent path.
        """
        self._msg('test', 'get_file_contents error', first=True)
        from garage.utils import get_file_contents
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'non-existent-file')
        data = get_file_contents(path)
        self._msg('path', path)
        self._msg('data', data, linebreak=True)
        self.assertEqual(data, None)

        data = get_file_contents(None)
        self._msg('path', path)
        self._msg('data', data, linebreak=True)
        self.assertEqual(data, None)

    def test_write_file(self):
        """
        Ensure write_file function is working properly.
        """
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

    def test_write_file_error(self):
        """
        write_file should return False if there is an IOError.
        """
        from garage.utils import write_file, get_file_contents
        self._msg('test', 'write_file', first=True)

        with patch('garage.utils.open_file') as mock_open_file:
            mock_open_file.side_effect = IOError
            path = 'testfile.txt'
            result = write_file(path, TestData)
            calls = mock_open_file.mock_calls
            self._msg('calls', calls)

        self.assertFalse(result)
        self._msg('result', result)

    def test_delete_file(self):
        """
        Ensure delete_file function is working properly.
        """
        from garage.utils import write_file, get_file_contents, delete_file
        self._msg('test', 'delete_file', first=True)
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
        result = delete_file(path)
        self.assertTrue(result)
        self.assertFalse(os.path.isfile(path))

    def test_delete_nonexistent_file(self):
        """
        delete_file should bypass deletion and return True if file
        does not exist.
        """
        from garage.utils import write_file, get_file_contents, delete_file
        self._msg('test', 'delete non-existent file', first=True)
        path = 'garage-non-existent-testfile'
        result = delete_file(path)
        self.assertTrue(result)
        self.assertFalse(os.path.isfile(path))

    def test_make_dir(self):
        """
        Ensure make_dir function is working properly.
        """
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
        expected = '5fccbb2309b2974d0b3bdf8dcd0791a5c7168b9f'
        self._msg('data', data)
        self._msg('rexpected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

    def test_encode_sdata(self):
        """
        encode_sdata should encode data into a byte string.
        * NOTE: returned data is a byte string (not unicode)
        """
        from garage.utils import encode_sdata
        self._msg('test', 'encode_sdata', first=True)
        data = 'this is a test'
        result = encode_sdata(data)
        expected = b'5674686973206973206120746573740A70310A2E'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self._msg('expected type', type(expected))
        self._msg('result type', type(result))
        self.assertEqual(result, expected)
        self.assertEqual(type(result), type(expected))

        data = 'he said, "q & a" <abc> écriture 寫作'
        result = encode_sdata(data)
        expected = b'56686520736169642C2022712026206122203C6162633E20E963726974757265205C75356265625C75346635630A70310A2E'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self._msg('expected type', type(expected))
        self._msg('result type', type(result))
        self.assertEqual(result, expected)
        self.assertEqual(type(result), type(expected))

        data = [n for n in xrange(5)]
        result = encode_sdata(data)
        expected = b'286C70310A49300A6149310A6149320A6149330A6149340A612E'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self._msg('expected type', type(expected))
        self._msg('result type', type(result))
        self.assertEqual(result, expected)
        self.assertEqual(type(result), type(expected))

    def test_decode_sdata(self):
        """
        Ensure decode_sdata function is working properly.
        """
        from garage.utils import decode_sdata
        self._msg('test', 'decode_sdata', first=True)

        data = b'5674686973206973206120746573740A70310A2E'
        result = decode_sdata(data)
        expected = 'this is a test'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self._msg('expected type', type(expected))
        self._msg('result type', type(result))
        self.assertEqual(result, expected)
        self.assertEqual(type(result), type(expected))

        data = b'56686520736169642C2022712026206122203C6162633E20E963726974757265205C75356265625C75346635630A70310A2E'
        result = decode_sdata(data)
        expected = 'he said, "q & a" <abc> écriture 寫作'
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self._msg('expected type', type(expected))
        self._msg('result type', type(result))
        self.assertEqual(result, expected)
        self.assertEqual(type(result), type(expected))

        data = b'286C70310A49300A6149310A6149320A6149330A6149340A612E'
        result = decode_sdata(data)
        expected = [n for n in range(5)]
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self._msg('expected type', type(expected))
        self._msg('result type', type(result))
        self.assertEqual(result, expected)
        self.assertEqual(type(result), type(expected))

    def test_decode_sdata_error(self):
        """
        decode_sdata should raise exception if input data is not
        base16 byte string.
        """
        from garage.utils import decode_sdata
        self._msg('test', 'decode_sdata', first=True)

        data = ['<abc>', 'écriture', '寫作']
        result = decode_sdata(data)
        expected = None
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

        data = 'écriture 寫作'
        result = decode_sdata(data)
        expected = None
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

        data = b'286C70300A4930'
        result = decode_sdata(data)
        expected = None
        self._msg('data', data)
        self._msg('expected', expected)
        self._msg('result', result)
        self.assertEqual(result, expected)

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

        data = {
            'a': 1,
            'b': 2,
            'c': 'three'
        }
        obj = DataObject()
        obj.add(**data)
        self._msg('data', data)
        self._msg('obj', obj)
        self._msg('len', len(obj))
        self.assertEqual(len(data), len(obj))
        for k, v in data.items():
            self.assertEqual(getattr(obj, k), v)

        data = ['a', 'b', 'c']
        obj = DataObject()
        obj.add(data)
        self._msg('data', data)
        self._msg('obj', obj)
        self._msg('len', len(obj))
        self.assertEqual(len(data), len(obj))
        for k in data:
            self.assertEqual(getattr(obj, k), True)

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

        # test ``reverse_mapping`` dict
        self.assertTrue(hasattr(obj, 'reverse_mapping'))
        val = obj.c
        self.assertEqual(obj.reverse_mapping[val], 'c')

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

    def test_cvt2list(self):
        """
        cvt2list should return an object as a list.
        * This is a legacy function.
        """
        self._msg('test', 'cvt2list', first=True)
        from garage.utils import cvt2list
        data = 'abc'
        result = cvt2list(data)
        self.assertTrue(hasattr(result, '__iter__'))
        self.assertTrue(len(result), 1)
        self.assertTrue(isinstance(result, list))
