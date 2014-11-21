# -*- coding: utf-8 -*-
"""
garage.tests.imports

Test garage to ensure legacy imports are not broken.

* created: 2014-11-21 kevin chan <kefin@makedostudio.com>
* updated: 2014-11-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import importlib
import inspect
import unittest

from garage.test.base import SimpleTestCase
from garage.test.utils import msg, module_exists, function_exists, var_exists


class ImportTests(SimpleTestCase):

    def test_imports(self):
        """
        Verify garage modules, function, classes and vars are importable.
        * the following is a list of functions, classes and variables
          in various projects that have used garage and what they
          import (expect to import).
        """
        funcs = (

            ("", "get_session_var"),
            ("", "get_setting"),
            ("", "resp"),
            ("", "set_session_var"),
            ("cache", "cache_data"),
            ("cache", "cache_key"),
            ("cache", "create_cache_key"),
            ("cache", "delete_cache"),
            ("db", "clone_objects"),
            ("help_text", "get_help_text"),
            ("html_utils", "escape"),
            ("html_utils", "get_cvt_method_name"),
            ("html_utils", "html_escape"),
            ("html_utils", "strip_tags"),
            ("html_utils", "to_html"),
            ("html_utils", "txt2html"),
            ("image_utils", "generate_thumb"),
            ("image_utils", "get_file_basename"),
            ("image_utils", "get_image_size"),
            ("image_utils", "get_img_ext"),
            ("image_utils", "resize_image"),
            ("logger", "logger"),
            ("session", "get_session_var"),
            ("session", "set_session_var"),
            ("slugify", "create_unique_slug"),
            ("slugify", "get_slug_base"),
            ("slugify", "get_unique_slug"),
            ("test.utils", "module_exists"),
            ("test.utils", "msg"),
            ("test", "module_exists"),
            ("text_utils", "check_eos"),
            ("text_utils", "safe_str"),
            ("text_utils", "safe_unicode"),
            ("text_utils", "substitute"),
            ("text_utils", "trim"),
            ("text_utils", "uprint"),
            ("utils", "enum"),
            ("utils", "get_file_contents"),
            ("utils", "get_file_ext"),
            ("utils", "load_yaml"),
            ("utils", "sha1hash"),

        )

        vars = (

            ("html_utils", "MARKDOWN_CONVERSION"),
            ("html_utils", "NO_CONVERSION"),
            ("html_utils", "VISUAL_EDITOR"),
            ("html_utils", "CONVERSION_CHOICES"),
            ("test.settings", "DIVIDER"),

            ("urlgen", "urlGen"),
            ("utils", "DataObject"),
            ("test.utils", "DummyObject"),
            ("test.base", "SimpleTestCase"),
            ("test", "SimpleTestCase"),

        )

        for m, f in funcs:
            if m != "":
                mod = '%s.%s' % ('garage', m)
            else:
                mod = 'garage'

            mod_exists = module_exists(mod)
            self._msg(mod, 'module exists: %s' % mod_exists)

            func_exists = function_exists(mod, f)
            self._msg('* %s' % f, 'function exists: %s' % func_exists)

            self.assertTrue(mod_exists and func_exists,
                            msg="not found: %s.%s" % (mod, f))

        for m, v in vars:
            if m != "":
                mod = '%s.%s' % ('garage', m)
            else:
                mod = 'garage'

            mod_exists = module_exists(mod)
            self._msg(mod, 'module exists: %s' % mod_exists)

            var_name_exists = var_exists(mod, v)
            self._msg('* %s' % v, 'var exists: %s' % var_name_exists)

            self.assertTrue(mod_exists and var_exists,
                            msg="not found: %s.%s" % (mod, v))
