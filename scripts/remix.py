#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import hashlib
import math
import os.path
import random
import sys

from PIL import Image
from StringIO import StringIO


__version__ = '1.0'


class RemixError(Exception):
    pass


class Coder(object):

    def process(self, filename, bytes, **kwargs):
        if 'decode' not in kwargs:
            raise RemixError('Argument "decode" is required.')
        decode = kwargs.pop('decode')
        coder_action = 'DEC' if decode else 'ENC'
        coder_name = self.__class__.__name__
        sys.stdout.write('[%s] %-16s ...... ' % (coder_action, coder_name))
        if decode:
            new_filename, new_bytes = self.decode(filename, bytes, **kwargs)
        else:
            new_filename, new_bytes = self.encode(filename, bytes, **kwargs)
        percentage = (len(new_bytes) * 100.0) / len(bytes)
        sys.stdout.write('%6.2f%% (%d -> %d)\n' % (percentage, len(bytes), len(new_bytes)))
        return new_filename, new_bytes
        

    def encode(self, filename, bytes, **kwargs):
        raise NotImplementedError()

    def decode(self, filename, bytes, **kwargs):
        raise NotImplementedError()


class Verifier(Coder):

    separator = '|'

    def encode(self, filename, bytes, **kwargs):
        basename = os.path.basename(filename)
        size = str(len(bytes))
        md5 = hashlib.md5(bytes).hexdigest().upper()
        bytes = self.separator.join([__version__, basename, size, md5, bytes])
        root, ext = os.path.splitext(filename)
        return '%s.v' % root, bytes

    def decode(self, filename, bytes, **kwargs):
        tokens = bytes.split(self.separator, 4)
        if len(tokens) != 5:
            raise RemixError('Invalid bytes: should contain at least 5 tokens.')
        version, basename, size, md5, bytes = tokens
        actual_size = len(bytes)
        actual_md5 = hashlib.md5(bytes).hexdigest().upper()
        if version != __version__:
            raise RemixError('Incompatible version: %s (current: %s)' % (version, __version__))
        if int(size) != actual_size:
            raise RemixError('Inconsistent size: %s (actual: %s)' % (size, actual_size))
        if md5 != actual_md5:
            raise RemixError('Invalid MD5: %s (actual: %s)' % (md5, actual_md5))
        real_filename = os.path.join(os.path.dirname(filename), basename)
        return real_filename, bytes


class Reverser(Coder):

    def encode(self, filename, bytes, **kwargs):
        return filename, bytes[::-1]

    def decode(self, filename, bytes, **kwargs):
        return filename, bytes[::-1]


class PasswordCoder(Coder):

    def encode(self, filename, bytes, **kwargs):
        return filename, self._apply_password(bytes, **kwargs)

    def decode(self, filename, bytes, **kwargs):
        return filename, self._apply_password(bytes, **kwargs)

    def _apply_password(self, bytes, **kwargs):
        password = kwargs.get('password')
        if not password:
            return bytes
        data_ords = [ord(c) for c in bytes]
        password_ords = [ord(c) for c in password]
        for i in range(0, len(data_ords)):
            masked = data_ords[i] ^ password_ords[i % len(password_ords)]
            data_ords[i] = masked
        return ''.join([chr(o) for o in data_ords])


class ImageCoder(Coder):

    ending_char = chr(255)

    def encode(self, filename, bytes, **kwargs):
        # Append ending char to bytes.
        bytes += self.ending_char
        # Convert bytes into an image.
        width = max(int(math.sqrt(len(bytes) / 4.0) + 1), 16)
        height = max(int(len(bytes) / (4.0 * width) + 1), 16)
        im = Image.new('RGBA', (width, height))
        pixels = im.load()
        for y in range(0, height):
            for x in range(0, width):
                rgba = [0, 0, 0, 0]
                for i in range(0, len(rgba)):
                    # Calculate the byte index corresponding to the current color channel.
                    byte_index = i + x * len(rgba) + y * width * len(rgba)
                    # Embed the byte into the current color channel.
                    if byte_index < len(bytes):
                        rgba[i] = ord(bytes[byte_index])
                    else:
                        rgba[i] = random.randint(0, 250)  # pad with random value.
                pixels[x, y] = tuple(rgba)
        # Get bytes from the image.
        output = StringIO()
        try:
            im.save(output, format='PNG')
            new_bytes = output.getvalue()
        finally:
            output.close()
        # Done: return the image filename and its bytes.
        root, ext = os.path.splitext(filename)
        return '%s.png' % root, new_bytes

    def decode(self, filename, bytes, **kwargs):
        # Restore bytes from image.
        input = StringIO(bytes)
        im = Image.open(input)
        width, height = im.size
        pixels = im.load()
        new_bytes = []
        for y in range(0, height):
            for x in range(0, width):
                r, g, b, a = pixels[x, y]
                new_bytes.extend([chr(r), chr(g), chr(b), chr(a)])
        new_bytes = ''.join(new_bytes)
        # Strip off everything after the ending char.
        new_bytes = new_bytes.rsplit(self.ending_char, 1)[0]
        return filename, new_bytes


PIPE = [Verifier(), Reverser(), PasswordCoder(), ImageCoder()]


def create_argument_parser():
    parser = argparse.ArgumentParser(description='Encode file into an image and vice versa.')
    parser.add_argument('-p', '--password', dest='password', default='',
                        help='specify a password to encode/decode')
    parser.add_argument('-d', '--decode', dest='decode', action='store_true',
                        help='specify whether to decode an image, default to encode')
    parser.add_argument('input', nargs=1,
                        help='specify the input file')
    return parser


def read_bytes(filename):
    if not os.path.isfile(filename):
        raise RemixError('%s is not a file.' % filename)
    f = open(filename, 'rb')
    try:
        return f.read()
    except IOError, exc:
        raise RemixError('Fail to read from file %s: %s' % (filename, exc))
    finally:
        f.close()


def write_bytes(bytes, filename):
    root, ext = os.path.splitext(filename)
    num_tried = 0
    while os.path.exists(root + ext) and num_tried < 10:
        root = '%s_%d' % (root, num_tried)
        num_tried += 1
    filename = root + ext
    if os.path.exists(filename):
        raise RemixError('Fail to find filename for %s: tried %d times.' % (filename, num_tried))
    print 'Saving output to file: %s' % filename
    f = open(filename, 'wb')
    try:
        f.write(bytes)
    except IOError, exc:
        raise RemixError('Fail to write to file %s: %s' % (filename, exc))
    finally:
        f.close()


def main(argv=None):
    # Parse command line arguments.
    argv = argv or sys.argv[1:]
    parser = create_argument_parser()
    args = parser.parse_args(argv)
    # Process file.
    filename = args.input[0]
    bytes = read_bytes(filename)
    kwargs = vars(args)
    pipe = reversed(PIPE) if args.decode else PIPE
    for coder in pipe:
        filename, bytes = coder.process(filename, bytes, **kwargs)
    write_bytes(bytes, filename)


if __name__ == '__main__':
    main()

