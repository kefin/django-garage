# -*- coding: utf-8 -*-
"""
tests.slugify.tests

Tests for garage.slugify

* created: 2014-08-24 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-23 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from mock import Mock, patch, call

try:
    from django.test import override_settings
except ImportError:
    from django.test.utils import override_settings

from garage.test import SimpleTestCase


class SlugifyTests(SimpleTestCase):

    def test_strip_accents(self):
        """
        Ensure strip_accents function is working properly.
        """
        from garage.slugify import strip_accents
        self._msg('test', 'strip_accents', first=True)

        txt = 'écriture 寫作'
        expected = 'ecriture '
        result = strip_accents(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

    def test_slugify(self):
        """
        Ensure slugify function is working properly.
        """
        from garage.slugify import slugify
        self._msg('test', 'slugify', first=True)

        txt = 'The Renaissance of Giselle “G” Töngi'
        expected = 'the-renaissance-of-giselle-g-tongi'
        result = slugify(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

        txt = 'Apoyan resolución a favor de niños migrantes en LA'
        expected = 'apoyan-resolucion-a-favor-de-ninos-migrantes-en-la'
        result = slugify(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

        txt = '“foo! écriture 寫作 #bar???”'
        expected = 'foo-ecriture-bar'
        result = slugify(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

        txt =  txt = 'Nín hǎo. Wǒ shì zhōng guó rén'
        expected = 'nin-hao-wo-shi-zhong-guo-ren'
        result = slugify(txt)
        self._msg('text', txt)
        self._msg('result', result)
        self._msg('expected', expected)
        self.assertEqual(result, expected)

    @override_settings(SLUG_SEPARATOR='.')
    def test_get_slug_separator(self):
        """
        Ensure get_slug_separator function is working properly.
        """
        self._msg('test', 'get_slug_separator', first=True)
        from garage.slugify import get_slug_separator
        separator = get_slug_separator()
        self.assertEqual(separator, '.')
        self._msg('separator', separator)

    @override_settings(SLUG_ITERATION_SEPARATOR='.')
    def test_get_slug_iteration_separator(self):
        """
        Ensure get_slug_iteration_separator function is working properly.
        """
        self._msg('test', 'get_slug_iteration_separator', first=True)
        from garage.slugify import get_slug_iteration_separator
        separator = get_slug_iteration_separator()
        self.assertEqual(separator, '.')
        self._msg('separator', separator)

    @override_settings(SLUG_ITERATION_SEPARATOR='.')
    def test_get_slug_base(self):
        """
        Ensure get_slug_base function is working properly.
        """
        self._msg('test', 'get_slug_base', first=True)
        from garage.slugify import get_slug_base
        separator = '.'
        slug = 'example.999'
        slug_base = get_slug_base(slug, slug_iteration_separator=separator)
        self.assertEqual(slug_base, 'example')
        self._msg('slug', slug)
        self._msg('separator', separator)
        self._msg('slug_base', slug_base)

        separator = '--'
        slug = 'example-2015--2'
        slug_base = get_slug_base(slug, slug_iteration_separator=separator)
        self.assertEqual(slug_base, 'example-2015')
        self._msg('slug', slug)
        self._msg('separator', separator)
        self._msg('slug_base', slug_base)

        separator = '~'
        slug = 'example-999~9876'
        slug_base = get_slug_base(slug, slug_iteration_separator=separator)
        self.assertEqual(slug_base, 'example-999')
        self._msg('slug', slug)
        self._msg('separator', separator)
        self._msg('slug_base', slug_base)

        separator = '~'
        slug = 'example-123-4567'
        slug_base = get_slug_base(slug, slug_iteration_separator=separator)
        self.assertEqual(slug_base, 'example-123-4567')
        self._msg('slug', slug)
        self._msg('separator', separator)
        self._msg('slug_base', slug_base)

        separator = '-copy'
        slug = 'example-copy4'
        slug_base = get_slug_base(slug, slug_iteration_separator=separator)
        self.assertEqual(slug_base, 'example')
        self._msg('slug', slug)
        self._msg('separator', separator)
        self._msg('slug_base', slug_base)

    def test_slug_creation_error(self):
        """
        slug_creation_error raises a ValidationError (obsolete function).
        """
        self._msg('test', 'slug_creation_error', first=True)
        from django.core.exceptions import ValidationError
        from garage.slugify import slug_creation_error
        with self.assertRaises(ValidationError):
            slug_creation_error()

    def test_create_unique_slug(self):
        """
        create_unique_slug will create a unique slug for a model
        instance.
        """
        self._msg('test', 'create_unique_slug', first=True)
        from garage.slugify import create_unique_slug, SLUG_ITERATION_SEPARATOR
        separator = SLUG_ITERATION_SEPARATOR

        obj = Mock()
        obj.slug = 'example'
        queryset = Mock()
        queryset.exclude.return_value = queryset
        queryset.filter.return_value = None
        dummy_model = Mock()
        dummy_model._default_manager.all.return_value = queryset
        obj.__class__ = dummy_model
        result = create_unique_slug(obj)
        expected = 'example'
        self.assertEqual(result, expected)
        self._msg('slug', result)

        # create a unique slug that ends with '3'
        ncopy = '3'

        def side_effect(**kwargs):
            slug = kwargs.get('slug')
            if slug and slug.endswith(ncopy):
                return None
            return True

        obj = Mock()
        obj.slug = 'example{0}1'.format(separator)
        queryset = Mock()
        queryset.exclude.return_value = queryset
        queryset.filter.side_effect = side_effect
        dummy_model = Mock()
        dummy_model._default_manager.all.return_value = queryset
        obj.__class__ = dummy_model
        result = create_unique_slug(obj)
        expected = 'example{0}{1}'.format(separator, ncopy)
        self.assertEqual(result, expected)
        self._msg('slug', result)

    def test_get_unique_slug(self):
        """
        get_unique_slug will create a unique slug for a model
        instance.
        """
        self._msg('test', 'get_unique_slug', first=True)
        from garage.slugify import get_unique_slug, SLUG_ITERATION_SEPARATOR
        separator = SLUG_ITERATION_SEPARATOR
        slug_field = 'slug'
        slug_base = 'example'

        obj = Mock()
        obj.slug = slug_base
        queryset = Mock()
        queryset.exclude.return_value = queryset
        queryset.filter.return_value = None
        dummy_model = Mock()
        dummy_model._default_manager.all.return_value = queryset
        obj.__class__ = dummy_model
        result, _ = get_unique_slug(obj,
                                 slug_field=slug_field,
                                 slug_base=slug_base,
                                 slug_separator=separator)
        expected = slug_base
        self.assertEqual(result, expected)
        self._msg('slug', result)

        # create a unique slug that ends with '3'
        ncopy = '3'

        def side_effect(**kwargs):
            slug = kwargs.get(slug_field)
            if slug and slug.endswith(ncopy):
                return None
            return True

        obj = Mock()
        obj.slug = '{0}{1}1'.format(slug_base, separator)
        queryset = Mock()
        queryset.exclude.return_value = queryset
        queryset.filter.side_effect = side_effect
        dummy_model = Mock()
        dummy_model._default_manager.all.return_value = queryset
        obj.__class__ = dummy_model
        result, _ = get_unique_slug(obj,
                                 slug_field=slug_field,
                                 slug_base=slug_base,
                                 slug_separator=separator)
        expected = '{0}{1}{2}'.format(slug_base, separator, ncopy)
        self.assertEqual(result, expected)
        self._msg('slug', result)
