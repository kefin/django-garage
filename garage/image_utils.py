# -*- coding: utf-8 -*-
"""
garage.image_utils

Image-processing utility functions.

* created: 2012-08-10 Kevin Chan <kefin@makedostudio.com>
* updated: 2012-09-08 kchan
"""

import os.path
import re
import imghdr
import Image



# image utilities

DEFAULT_IMG_QUALITY = 75
RE_PATS = [
	r'^(.*)([_\-][0-9]+x[0-9]+)(\.[^\.]+)$',
	r'^(.*)(\.[^\.]+)$'
    ]
Regexp = None
DEFAULT_FNAME = 'image'


def resize_image(img, box, fit):
    """
    Downsample image and resize to 'box' dimensions.
    @param img: Image - an Image-object
    @param box: tuple(x, y) - the bounding box of the result image
    @param fit: boolean - crop the image to fill the box
    """
    w, h = box

    def f2i(n):
        return int(round(n))

    if fit:
        x, y = img.size
        src_ratio = 1.0 * x/y
        dst_ratio = 1.0 * w/h
        if src_ratio > dst_ratio:
            dy = 0.0
            dx = dst_ratio * y - x
        else:
            dx = 0.0
            dy = x / dst_ratio - y
        x += dx
        y += dy
        a0 = 1.0 * abs(dx/2)
        a1 = a0 + x
        b0 = 1.0 * abs(dy/2)
        b1 = b0 + y
        a0 = f2i(a0)
        a1 = f2i(a1)
        b0 = f2i(b0)
        b1 = f2i(b1)
        crop_coordinates = (a0, b0, a1, b1)
        img = img.crop(crop_coordinates)

    img = img.resize(box, Image.ANTIALIAS)
    return img


def get_image_size(image_file):
    img = Image.open(image_file)
    imgw, imgh = img.size
    return imgw, imgh


def create_thumb(image_file, w, h, quality, dst, fbase, fext):
    """
    Uses resize function above.
    """
    quality = int(quality)

    img = Image.open(image_file)

    imgw, imgh = img.size
    r = (1.0 * imgw) / imgh
    if not w:
        w = round(r * float(h))
    if not h:
        h = round(float(w) / r)

    w = int(w)
    h = int(h)

    img = resize_image(img, (w, h,), True)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    filename = '%s-%dx%d.%s' % (fbase, w, h, fext)
    output = os.path.join(dst, filename)
    img.save(output, quality=quality)
    return output


def get_file_basename(f, default=DEFAULT_FNAME):
    global Regexp
    if Regexp is None:
        Regexp = [re.compile(r, re.I) for r in RE_PATS]
    fname = os.path.basename(f)
    for r in Regexp:
        m = r.match(fname)
        if m:
            return m.group(1)
    return default


def get_img_ext(path, default_ext='unknown'):
    """
    Detect image type from file path and return file extension.
    """
    imgtype = imghdr.what(path)
    suffix = {
        'rgb': 'rgb',
        'gif': 'gif',
        'pbm': 'pbm',
        'pgm': 'pgm',
        'ppm': 'ppm',
        'tiff': 'tif',
        'rast': 'rast',
        'xbm': 'xbm',
        'jpeg': 'jpg',
        'bmp': 'bmp',
        'png': 'png'
        }
    return suffix.get(imgtype, default_ext)


def generate_thumb(img_file, width, height, quality, dest_dir):
    """
    Process image file and create thumbnail according to parameters.
    """
    fbase = get_file_basename(img_file)
    fext = get_img_ext(img_file)
    return create_thumb(img_file, width, height, quality, dest_dir, fbase, fext)
