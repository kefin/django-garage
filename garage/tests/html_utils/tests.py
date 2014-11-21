# -*- coding: utf-8 -*-
"""
tests.html_utils.tests

Tests for garage.html_utils

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from garage.test import SimpleTestCase


ExampleText = """
## Fruits

* apples
* oranges
* bananas

### Subtitle

lorem ipsum...
"""

ConvertedHtmlText = """\
<h2>Fruits</h2>
<ul>
<li>apples</li>
<li>oranges</li>
<li>bananas</li>
</ul>
<h3>Subtitle</h3>
<p>lorem ipsum...</p>\
"""

PlainText = """\
Fruits

apples

oranges

bananas

Subtitle

lorem ipsum...
"""


class HtmlUtilsTests(SimpleTestCase):

    def test_html_escape(self):
        """
        Ensure html_utils function is working properly.
        """
        from garage.html_utils import html_escape
        self._msg('test', 'html_escape', first=True)
        txt = 'he said, "q & a" <abc> écriture 寫作'
        escaped = html_escape(txt)
        expected = 'he said, &quot;q &amp; a&quot; &lt;abc&gt; écriture 寫作'
        self._msg('text', txt)
        self._msg('escaped', escaped)
        self._msg('expected', expected)
        self.assertEqual(escaped, expected)

    def test_html_entities(self):
        """
        Ensure html_entities function is working properly.
        """
        from garage.html_utils import html_entities
        self._msg('test', 'html_entities', first=True)
        txt = 'he said, "q & a" <abc> écriture 寫作'
        escaped = html_entities(txt)
        expected = 'he said, "q & a" <abc> &eacute;criture &#23531;&#20316;'
        self._msg('text', txt)
        self._msg('escaped', escaped)
        self._msg('expected', expected)
        self.assertEqual(escaped, expected)

    def test_escape(self):
        """
        Ensure escape function is working properly.
        """
        from garage.html_utils import escape
        self._msg('test', 'escape', first=True)

        txt = 'he said, "q & a" <abc> écriture 寫作'
        escaped = escape(txt)
        expected = 'he said, &quot;q &amp; a&quot; &lt;abc&gt; &amp;eacute;criture &amp;#23531;&amp;#20316;'
        self._msg('text', txt)
        self._msg('escaped', escaped)
        self._msg('expected', expected)
        self.assertEqual(escaped, expected)

    def test_strip_tags(self):
        """
        Ensure strip_tags function is working properly.
        """
        from garage.html_utils import strip_tags
        self._msg('test', 'strip_tags', first=True)
        txt = '<em>Holy Cow!</em> <span style="font-size: 10em">a b c</span>'
        result = strip_tags(txt)
        expected = 'Holy Cow! a b c'
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

        txt = 'he said, &quot;q &amp; a&quot; &lt;abc&gt; &eacute;criture &#23531;&#20316;'
        expected = 'he said, "q & a" <abc> écriture 寫作'
        result = strip_tags(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

    def test_unescape(self):
        """
        Ensure unescape function is working properly.
        """
        from garage.html_utils import unescape
        self._msg('test', 'unescape', first=True)

        txt = '<em>he said, &quot;q &amp; a&quot;</em> &lt;abc&gt; &eacute;criture &#23531;&#20316;'
        expected = '<em>he said, "q & a"</em> <abc> écriture 寫作'
        result = unescape(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

    def test_txt2html(self):
        """
        Ensure txt2html function is working properly.
        """
        from garage.html_utils import (
            txt2html,
            NO_CONVERSION,
            MARKDOWN_CONVERSION,
            TEXTILE_CONVERSION,
            SIMPLE_CONVERSION,
            VISUAL_EDITOR,
        )
        self._msg('test', 'txt2html', first=True)
        result = txt2html(ExampleText, MARKDOWN_CONVERSION)
        self._msg('text', ExampleText, linebreak=True)
        self._msg('result', result, linebreak=True)
        self.assertEqual(result, ConvertedHtmlText)

    def test_to_html(self):
        """
        Ensure to_html function is working properly.
        """
        from garage.html_utils import (
            to_html,
            NO_CONVERSION,
            MARKDOWN_CONVERSION,
            TEXTILE_CONVERSION,
            SIMPLE_CONVERSION,
            VISUAL_EDITOR,
        )
        self._msg('test', 'to_html', first=True)
        result = to_html(ExampleText, 'markdown')
        self._msg('text', ExampleText, linebreak=True)
        self._msg('result', result, linebreak=True)
        self.assertEqual(result, ConvertedHtmlText)

    def test_get_cvt_method(self):
        """
        Ensure get_cvt_method function is working properly.
        """
        from garage.html_utils import (
            get_cvt_method,
            NO_CONVERSION,
            MARKDOWN_CONVERSION,
            TEXTILE_CONVERSION,
            SIMPLE_CONVERSION,
            VISUAL_EDITOR,
        )
        self._msg('test', 'get_cvt_method', first=True)

        method = 'markdown'
        result = get_cvt_method(method)
        self.assertEqual(result, MARKDOWN_CONVERSION)
        self._msg('method', method)
        self._msg('conversion', result)

        method = 'textile'
        result = get_cvt_method(method)
        self.assertEqual(result, TEXTILE_CONVERSION)
        self._msg('method', method)
        self._msg('conversion', result)

        method = 'none'
        result = get_cvt_method(method)
        self.assertEqual(result, NO_CONVERSION)
        self._msg('method', method)
        self._msg('conversion', result)

        method = 'abc'
        result = get_cvt_method(method)
        self.assertEqual(result, NO_CONVERSION)
        self._msg('method', method)
        self._msg('conversion', result)

    def test_get_cvt_method_name(self):
        """
        Ensure get_cvt_method_name function is working properly.
        """
        from garage.html_utils import (
            get_cvt_method_name,
            NO_CONVERSION,
            MARKDOWN_CONVERSION,
            TEXTILE_CONVERSION,
            SIMPLE_CONVERSION,
            VISUAL_EDITOR,
        )
        self._msg('test', 'get_cvt_method', first=True)

        method = NO_CONVERSION
        result = get_cvt_method_name(method)
        self.assertEqual(result, 'none')
        self._msg('method', method)
        self._msg('conversion', result)

        method = MARKDOWN_CONVERSION
        result = get_cvt_method_name(method)
        self.assertEqual(result, 'markdown')
        self._msg('method', method)
        self._msg('conversion', result)

        method = TEXTILE_CONVERSION
        result = get_cvt_method_name(method)
        self.assertEqual(result, 'textile')
        self._msg('method', method)
        self._msg('conversion', result)

        method = SIMPLE_CONVERSION
        result = get_cvt_method_name(method)
        self.assertEqual(result, 'markdown')
        self._msg('method', method)
        self._msg('conversion', result)

        method = VISUAL_EDITOR
        result = get_cvt_method_name(method)
        self.assertEqual(result, 'visual')
        self._msg('method', method)
        self._msg('conversion', result)

    def test_html_to_text(self):
        """
        Ensure html_to_text function is working properly.
        """
        from garage.html_utils import html_to_text
        self._msg('test', 'html_to_text', first=True)
        txt = html_to_text(ConvertedHtmlText)
        self._msg('txt', txt, linebreak=True)
        self.assertEqual(txt, PlainText)
