# -*- coding: utf-8 -*-
"""
tests.db.tests

Tests for garage.db

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-21 kchan
"""

from __future__ import (absolute_import, unicode_literals)

from mock import Mock, MagicMock, patch, call

from garage.test import SimpleTestCase


# dummy object to test cloning
class DummyObject(object):
    label = 'foo'
    pk = 999
    saved = False
    m2m_fields = ['bar', 'baz', 'qux', 'norf']

    def __init__(self):
        self.update_slug()
        self.generate_meta_data()

    def __unicode__(self):
        return self.slug

    def __str__(self):
        return self.slug

    def update_pk(self, pk):
        self.pk = pk
        self.update_slug()

    def update_slug(self):
        self.slug = '{0}-{1}'.format(self.label, self.pk)

    def save(self):
        if self.pk:
            self.pk += 1
        self.update_slug()
        self.saved = True

    def generate_meta_data(self):
        """Generate some dummy data for _meta.many_to_many fields"""
        meta = MagicMock()
        meta.many_to_many = []

        class Field(object):
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

        for name in self.m2m_fields:
            f = Field(attname=name)
            meta.many_to_many.append(f)
            data_obj = MagicMock()
            data_obj.all.return_value = ['{0} data'.format(name)]
            setattr(self, name, data_obj)

        self._meta = meta


class DbTests(SimpleTestCase):

    def test_batch_qs(self):
        """
        Ensure batch_qs function is working properly.
        """
        from garage.db import batch_qs, DEFAULT_QS_BATCH_SIZE
        self._msg('test', 'batch_qs', first=True)
        num_entries = 1000
        entries = MagicMock()
        entries.count.return_value = num_entries

        n = 0
        for start, end, total, qs in batch_qs(entries):
            self._msg('processing', '%s - %s of %s' % (start + 1, end, total))
            n += 1

        self._msg('total batches', n)
        total = int(num_entries/DEFAULT_QS_BATCH_SIZE)
        if num_entries % DEFAULT_QS_BATCH_SIZE:
            total += 1
        self.assertEqual(total, n)

    def test_clonable_mixin(self):
        """
        ClonableMixin should duplicate the object with the ``clone``
        method.
        """
        from garage.db import ClonableMixin
        self._msg('test', 'ClonableMixin', first=True)

        class TestObject(DummyObject, ClonableMixin):
            pass

        obj = TestObject()
        self.assertEqual(obj.pk, 999)
        self.assertEqual(obj.slug, 'foo-999')
        self.assertEqual(str(obj), obj.slug)
        self.assertTrue(hasattr(obj, 'clone'))

        cloned = obj.clone()
        cloned.update_pk(1001)
        self.assertEqual(cloned.pk, 1001)
        self.assertEqual(cloned.slug, 'foo-1001')
        self.assertEqual(str(cloned), cloned.slug)
        self.assertTrue(hasattr(cloned, 'clone'))

        self._msg('obj', obj)
        self._msg('obj.slug', obj.slug)
        self._msg('cloned', cloned)
        self._msg('cloned.slug', cloned.slug)

        # check dummy m2m_fields and verify they are present
        self.assertEqual(len(obj._meta.many_to_many), len(obj.m2m_fields))

        for field in obj._meta.many_to_many:
            orig_data = getattr(obj, field.attname)
            self._msg(field.attname, orig_data.all())
            self.assertTrue(field.attname in obj.m2m_fields)

            cloned_data = getattr(cloned, field.attname)
            self.assertEqual(orig_data, cloned_data)
            self.assertTrue(field.attname in cloned.m2m_fields)

            self.assertEqual(orig_data.all(), cloned_data.all())

    def test_clonable_mixin_error(self):
        """
        ClonableMixin should raise ValueError if object pk is None.
        """
        from garage.db import ClonableMixin
        self._msg('test', 'ClonableMixin error', first=True)

        class TestObject(DummyObject, ClonableMixin):
            pass

        obj = TestObject()
        obj.update_pk(None)
        self.assertEqual(obj.pk, None)
        self.assertEqual(obj.slug, 'foo-None')
        self.assertEqual(str(obj), obj.slug)
        self.assertTrue(hasattr(obj, 'clone'))

        with self.assertRaises(ValueError):
            self._msg('clone method error', 'ValueError')
            cloned = obj.clone()


    def test_clone_objects(self):
        """
        clone_objects should duplicate an object using the same function (method)
        as ClonableMixin.
        """
        from garage.db import clone_objects
        self._msg('test', 'clone_objects', first=True)

        class TestObject(DummyObject):
            pass

        obj = TestObject()
        self.assertEqual(obj.pk, 999)
        self.assertEqual(obj.slug, 'foo-999')
        self.assertEqual(str(obj), obj.slug)
        self.assertFalse(hasattr(obj, 'clone'))

        new_objs = clone_objects(obj)
        cloned = new_objs[0]

        cloned.update_pk(1001)
        self.assertEqual(cloned.pk, 1001)
        self.assertEqual(cloned.slug, 'foo-1001')
        self.assertEqual(str(cloned), cloned.slug)
        self.assertFalse(hasattr(cloned, 'clone'))

        self._msg('obj', obj)
        self._msg('obj.slug', obj.slug)
        self._msg('cloned', cloned)
        self._msg('cloned.slug', cloned.slug)

        # check dummy m2m_fields and verify they are present
        self.assertEqual(len(obj._meta.many_to_many), len(obj.m2m_fields))

        for field in obj._meta.many_to_many:
            orig_data = getattr(obj, field.attname)
            self._msg(field.attname, orig_data.all())
            self.assertTrue(field.attname in obj.m2m_fields)

            cloned_data = getattr(cloned, field.attname)
            self.assertEqual(orig_data, cloned_data)
            self.assertTrue(field.attname in cloned.m2m_fields)

            self.assertEqual(orig_data.all(), cloned_data.all())

    def test_clone_objects_error(self):
        """
        clone_objects should raise ValueError if object pk is None.
        """
        from garage.db import clone_objects
        self._msg('test', 'clone_objects error', first=True)

        class TestObject(DummyObject):
            pass

        obj = TestObject()
        obj.update_pk(None)
        self.assertEqual(obj.pk, None)
        self.assertEqual(obj.slug, 'foo-None')
        self.assertEqual(str(obj), obj.slug)
        self.assertFalse(hasattr(obj, 'clone'))

        with self.assertRaises(ValueError):
            self._msg('clone method error', 'ValueError')
            new_objs = clone_objects(obj)
