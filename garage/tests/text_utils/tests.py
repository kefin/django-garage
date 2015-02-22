# -*- coding: utf-8 -*-
"""
tests.text_utils.tests

Tests for garage.text_utils

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-21 kchan
"""

from __future__ import (absolute_import, unicode_literals, print_function)

import sys

from garage.test import SimpleTestCase

# dummy text for testing formatting functions
DUMMY_TEXT = """\
one


two


three


"""

FORMATTED = """\
one

two

three
"""

class TextUtilsTests(SimpleTestCase):

    def test_uprint(self):
        """
        Ensure uprint function is working properly.
        * All text fed to uprint should be unicode (byte strings will
          raise UnicodeDecodeError).
        * If input is bytes (and UTF-8 encoded), decode before printing.
        """
        self._msg('test', 'uprint', first=True)
        from StringIO import StringIO
        from garage.text_utils import uprint

        old_stdout = sys.stdout

        def _print(s):
            # StringIO will accept unicode (cStringIO does not)
            sys.stdout = mystdout = StringIO()
            uprint(s)
            sys.stdout = old_stdout
            output = mystdout.getvalue()
            return output.strip('\n')

        def out(*args, **kwargs):
            if self.verbosity > 2:
                print(*args, **kwargs)

        out('')

        txt = 'foo'
        result = _print(txt)
        out('original: %s' % txt)
        out('result: %s' % result)
        out('type: %s' % type(result))
        self.assertEqual(result, txt)

        txt = 'écriture 寫作'
        result = _print(txt)
        out('original: %s' % txt)
        out('result: %s' % result)
        out('type: %s' % type(result))
        self.assertEqual(result, txt)

        # byte string should raise UnicodeDecodeError
        txt = b'Schei\xc3\x9f_Encoding'
        out('original: %s' % txt.decode('utf-8'))
        with self.assertRaises(UnicodeDecodeError):
            result = _print(txt)
        out('type: %s' % type(txt))
        out('* raises UnicodeDecodeError')

        # decode UTF-8 bytes before calling uprint
        txt = b'Schei\xc3\x9f_Encoding'.decode('utf-8')
        result = _print(txt)
        out('original: %s' % txt)
        out('result: %s' % result)
        out('type: %s' % type(result))
        self.assertEqual(result, txt)

        txt = 'Klüft skräms inför på fédéral électoral große'
        result = _print(txt)
        out('original: %s' % txt)
        out('result: %s' % result)
        out('type: %s' % type(result))
        self.assertEqual(result, txt)

        txt = u'caf\xe9'
        out('original: %s' % txt)
        result = _print(txt)
        out('result: %s' % result)
        out('type: %s' % type(txt))

        txt = u'caf\xe9'.encode('utf-8')
        with self.assertRaises(UnicodeDecodeError):
            result = _print(txt)
        out('original: %s' % txt.decode('utf-8'))
        out('type: %s' % type(txt))
        out('* raises UnicodeDecodeError')

    def test_trim(self):
        """
        trim should strip whitespace from beginning and end of text.
        """
        self._msg('test', 'trim', first=True)
        from garage.text_utils import trim
        txt = ' foo bar '
        expected = 'foo bar'
        result = trim(txt)
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('result', result)

    def test_check_eos(self):
        """
        check_eos should add an ending '\n' to string if it's missing.
        """
        self._msg('test', 'check_eos', first=True)
        from garage.text_utils import check_eos
        txt = 'foo'
        expected = 'foo\n'
        result = check_eos(txt)
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('result', result)

    def test_has_digits(self):
        """
        has_digits should return True if string contains any digits.
        """
        self._msg('test', 'has_digits', first=True)
        from garage.text_utils import has_digits
        txt = 'foo'
        result = has_digits(txt)
        self.assertFalse(result)
        self._msg('txt', txt)
        self._msg('result', result)

        txt = 'f0o'
        result = has_digits(txt)
        self.assertTrue(result)
        self._msg('txt', txt)
        self._msg('result', result)

    def test_has_alpha(self):
        """
        has_alpha should return True if string contains any
        alphabetical characters.
        """
        self._msg('test', 'has_alpha', first=True)
        from garage.text_utils import has_alpha
        txt = '123'
        result = has_alpha(txt)
        self.assertFalse(result)
        self._msg('txt', txt)
        self._msg('result', result)

        txt = '123a'
        result = has_alpha(txt)
        self.assertTrue(result)
        self._msg('txt', txt)
        self._msg('result', result)


    def test_has_alphanum(self):
        """
        has_alphanum should return True if string contains any
        alphabetical characters or digits.
        """
        self._msg('test', 'has_alphanum', first=True)
        from garage.text_utils import has_alphanum
        txt = '-=-'
        result = has_alphanum(txt)
        self.assertFalse(result)
        self._msg('txt', txt)
        self._msg('result', result)

        txt = '-=-1'
        result = has_alphanum(txt)
        self.assertTrue(result)
        self._msg('txt', txt)
        self._msg('result', result)

        txt = 'a-=-'
        result = has_alphanum(txt)
        self.assertTrue(result)
        self._msg('txt', txt)
        self._msg('result', result)

    def test_tidy_txt(self):
        """
        tidy_txt should compress runs of blank lines to 2 ('\n\n') (so
        paragraphs will have a blank line between each).
        """
        self._msg('test', 'tidy_txt', first=True)
        from garage.text_utils import tidy_txt
        txt = DUMMY_TEXT
        expected = FORMATTED
        result = tidy_txt(txt)
        self.assertEqual(result, expected)
        self._msg('raw text', repr(txt), linebreak=True)
        self._msg('result', repr(result), linebreak=True)

    def test_to_camel_case(self):
        """
        to_camel_case should convert a string to CamelCase.
        """
        self._msg('test', 'to_camel_case', first=True)
        from garage.text_utils import to_camel_case
        txt = 'ABC__*foo bar baz qux norf 321*__'
        expected = 'AbcFooBarBazQuxNorf321'
        result = to_camel_case(txt)
        self.assertEqual(result, expected)
        self._msg('raw text', repr(txt))
        self._msg('result', repr(result))

    def test_substitute(self):
        """
        substitute should do text placement if given a context dict.
        * default substution var pattern is ${VAR}
        """
        self._msg('test', 'substitute', first=True)
        from garage.text_utils import substitute

        txt = 'foo ${VAR1} baz${VAR1} ${VAR2}'
        context = {'VAR1': 'bar', 'VAR2': 'NORF'}
        result = substitute(txt, context)
        expected = 'foo bar bazbar NORF'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('context', repr(context))
        self._msg('expected', expected)
        self._msg('result', result)

        # with no context
        txt = 'foo ${VAR1} baz${VAR1} ${VAR2}'
        context = None
        result = substitute(txt, context)
        expected = 'foo  baz '
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('context', repr(context))
        self._msg('expected', repr(expected))
        self._msg('result', repr(result))

        # with callable context
        def ctx(kw):
            c = {'VAR1': 'bar', 'VAR2': 'NORF'}
            return c.get(kw, '???')

        txt = 'foo ${VAR1} baz${VAR1} ${VAR2}'
        context = ctx
        result = substitute(txt, ctx)
        expected = 'foo bar bazbar NORF'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('context', repr(context))
        self._msg('expected', repr(expected))
        self._msg('result', repr(result))

        # with custom keyword pattern
        pattern = r'\{\{ *([a-z_][a-z0-9_]*) *\}\}'
        txt = 'foo {{ VAR1 }} baz{{VAR1}} {{ VAR2 }}'
        context = {'VAR1': 'bar', 'VAR2': 'NORF'}
        result = substitute(txt, context, pattern=pattern)
        expected = 'foo bar bazbar NORF'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('pattern', pattern)
        self._msg('context', repr(context))
        self._msg('expected', expected)
        self._msg('result', result)

    def test_subs(self):
        """
        subs should perform simple substitution using Python's named
        argument string formatting.
        """
        self._msg('test', 'subs', first=True)
        from garage.text_utils import subs
        txt = 'foo %(VAR1)s baz%(VAR1)s %(VAR2)s'
        context = {'VAR1': 'bar', 'VAR2': 'NORF'}
        result = subs(txt, context)
        expected = 'foo bar bazbar NORF'
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('context', repr(context))
        self._msg('expected', expected)
        self._msg('result', result)

    def test_safe_unicode(self):
        """
        safe_unicode should return an unicode string or an escaped
        byte string (as unicode string).
        * this function is mostly for debugging use.
        """
        self._msg('test', 'safe_unicode', first=True)
        from garage.text_utils import safe_unicode

        # input is unicode
        txt = '你好'
        expected = unicode(txt)
        result = safe_unicode(txt)
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        # input is bytes
        txt = b'\xe4\xbd\xa0\xe5\xa5\xbd'
        expected = txt.encode('string_escape')
        result = safe_unicode(txt)
        self.assertEqual(result, expected)
        txt = txt.decode('utf-8')
        expected = expected.decode('utf-8')
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

    def test_safe_str(self):
        """
        safe_str returns a byte string of the object/unicode input.
        """
        self._msg('test', 'safe_str', first=True)
        from garage.text_utils import safe_str

        # input is bytes
        txt = b'\xe4\xbd\xa0\xe5\xa5\xbd'
        expected = txt
        result = safe_str(txt)
        self.assertEqual(result, expected)
        txt = txt.decode('utf-8')
        expected = expected.decode('utf-8')
        result = result.decode('utf-8')
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

        # input is unicode
        # unicode escaped string: '\u4f60\u597d'
        txt = '你好'
        expected = txt.encode('unicode_escape')
        result = safe_str(txt)
        self.assertEqual(result, expected)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)

    def test_truncate_chars(self):
        """
        truncate_chars should truncate string to 'maxlen' characters.
        """
        self._msg('test', 'truncate_chars', first=True)
        from garage.text_utils import truncate_chars
        txt = 'foo bar baz qux norf'
        maxlen = 12
        result = truncate_chars(txt, maxlen)
        expected = 'foo bar b...'
        self.assertEqual(result, expected)
        self.assertEqual(len(result), maxlen)
        self._msg('txt', txt)
        self._msg('expected', expected)
        self._msg('result', result)
