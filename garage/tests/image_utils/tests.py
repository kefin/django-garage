# -*- coding: utf-8 -*-
"""
tests.image_utils.tests

Tests for garage.image_utils

* created: 2014-08-23 Kevin Chan <kefin@makedostudio.com>
* updated: 2015-02-22 kchan
"""

from __future__ import (absolute_import, unicode_literals)

import os
import tempfile
try:
    from PIL import Image
except ImportError:
    import Image

from garage.test import SimpleTestCase


DEFAULT_TEST_IMAGES = {
    'rodents': ('rodents-600x338.jpg', 600, 338, 'jpg'),
    'monkeys1': ('monkeys-600x338.png', 600, 338, 'png'),
    'monkeys2': ('monkeys-600x338.gif', 600, 338, 'gif'),
}
DEFAULT_IMAGE = 'rodents'


class ImageUtilsTests(SimpleTestCase):

    def _get_test_image(self, image_label=None):
        """
        Utility method to return the local path of a test image to use
        for testing.
        * test images are located in ./img/tests/
        """
        if not image_label:
            image_label = DEFAULT_IMAGE
        fname, width, height, ext = DEFAULT_TEST_IMAGES.get(
            image_label, DEFAULT_IMAGE)
        module_dir = os.path.dirname(os.path.realpath(__file__))
        path = os.path.join(module_dir, 'img', 'tests', fname)
        return (path, fname, width, height, ext)

    def test_resize_image(self):
        """
        resize_image should downsample an image and resize according
        to input dimensions.
        """
        from garage.image_utils import (
            resize_image,
            get_img_ext,
            get_file_basename,
            get_image_size,
        )
        from garage.utils import delete_file
        self._msg('test', 'resize_image', first=True)

        tempdir = tempfile.gettempdir()
        path, fname, w, h, ext = self._get_test_image('rodents')
        fbase = 'rodents'
        w, h = 500, 280
        dst = '%s-%dx%d.%s' % (os.path.join(tempdir, fbase), w, h, ext)
        img = Image.open(path)
        result = resize_image(img, (w, h), True)
        result.save(dst, quality=75)
        self.assertTrue(os.path.isfile(dst))
        width, height = get_image_size(dst)
        fext = get_img_ext(dst)
        self.assertEqual((width, height), (w, h))
        self.assertEqual(fext, ext)
        self._msg('original', dst)
        self._msg('resized', result)
        self._msg('width', width)
        self._msg('height', height)
        self._msg('ext', fext)
        self.assertTrue(delete_file(dst))

    def test_get_image_size(self):
        """
        get_image_size should return images's width x height as tuple.
        """
        from garage.image_utils import get_image_size
        self._msg('test', 'get_image_size', first=True)
        path, fname, w, h, ext = self._get_test_image()
        width, height = get_image_size(path)
        self.assertEqual(width, w)
        self.assertEqual(height, h)
        self._msg('img', fname)
        self._msg('width', width)
        self._msg('height', height)

    def test_create_thumb(self):
        """
        create_thumb should generate a thumbnail of specified size and
        quality.
        * result should be, e.g., /path/to/thumb/thumb-245x136.jpg
        """
        from garage.image_utils import (
            create_thumb,
            get_image_size,
            get_img_ext,
        )
        from garage.utils import delete_file
        self._msg('test', 'create_thumb', first=True)

        tempdir = tempfile.gettempdir()
        path, fname, w, h, ext = self._get_test_image('rodents')
        w, h = 245, 138
        quality = 75
        dst = tempdir
        fbase = 'rodents'
        thumb = create_thumb(path, w, h, quality, dst, fbase, ext)
        width, height = get_image_size(thumb)
        fext = get_img_ext(thumb)
        self.assertTrue(os.path.isfile(thumb))
        self.assertEqual((width, height), (w, h))
        self.assertEqual(fext, ext)
        self._msg('original', fname)
        self._msg('thumb', thumb)
        self._msg('width', width)
        self._msg('height', height)
        self._msg('ext', fext)
        self.assertTrue(delete_file(thumb))

    def test_get_file_basename(self):
        """
        get_file_basename should return base name of image file minus
        the image extension and -WWWxHHH dimensions.
        """
        from garage.image_utils import get_file_basename
        self._msg('test', 'get_file_basename', first=True)

        img_file = 'example-image.jpg'
        img_base = get_file_basename(img_file)
        self.assertEqual(img_base, 'example-image')
        self._msg('file', img_file)
        self._msg('base', img_base)

        img_file = 'img/tests/rodents-600x338.jpg'
        img_base = get_file_basename(img_file)
        self.assertEqual(img_base, 'rodents')
        self._msg('file', img_file)
        self._msg('base', img_base)

        img_file = 'img/tests/rodents_600x338.jpg'
        img_base = get_file_basename(img_file)
        self.assertEqual(img_base, 'rodents')
        self._msg('file', img_file)
        self._msg('base', img_base)

    def test_get_img_ext(self):
        """
        get_img_ext should return the appropriate image type extension
        for file or a default ('unknown') if file cannot be
        deciphered.
        """
        from garage.image_utils import get_img_ext
        self._msg('test', 'get_img_ext', first=True)

        path, fname, w, h, ext = self._get_test_image('rodents')
        result = get_img_ext(path)
        self.assertEqual(result, ext)
        self._msg('image', fname)
        self._msg('ext', ext)
        self._msg('result', result)

        path, fname, w, h, ext = self._get_test_image('monkeys1')
        result = get_img_ext(path)
        self.assertEqual(result, ext)
        self._msg('image', fname)
        self._msg('ext', ext)
        self._msg('result', result)

        path, fname, w, h, ext = self._get_test_image('monkeys2')
        result = get_img_ext(path)
        self.assertEqual(result, ext)
        self._msg('image', fname)
        self._msg('ext', ext)
        self._msg('result', result)

    def test_generate_thumb(self):
        """
        generate_thumb is a wrapper function for create_thumb, so
        should bahave identically with the same parameters.
        * result should be, e.g., /path/to/thumb/thumb-245x136.jpg
        """
        from garage.image_utils import (
            generate_thumb,
            get_image_size,
            get_img_ext,
        )
        from garage.utils import delete_file
        self._msg('test', 'generate_thumb', first=True)

        tempdir = tempfile.gettempdir()
        path, fname, w, h, ext = self._get_test_image('rodents')
        w, h = 245, 138
        quality = 75
        dst = tempdir
        thumb = generate_thumb(path, w, h, quality, dst)
        width, height = get_image_size(thumb)
        fext = get_img_ext(thumb)
        self.assertTrue(os.path.isfile(thumb))
        self.assertEqual((width, height), (w, h))
        self.assertEqual(fext, ext)
        self._msg('original', fname)
        self._msg('thumb', thumb)
        self._msg('width', width)
        self._msg('height', height)
        self._msg('ext', fext)
        self.assertTrue(delete_file(thumb))
