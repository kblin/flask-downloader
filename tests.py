 # -*- coding: utf-8 -*-
from __future__ import with_statement

import unittest
import tempfile
import shutil
import os
from os import path

from flask import Flask
from flaskext.downloader import Downloader, DownloaderError

def assert_first_line(filename, expected):
    """Assert the first line of a file is as expected
    """
    if not path.exists(filename):
        raise AssertionError("File %r does not exist" % filename)

    try:
        handle = open(filename)
    except IOError, e:
        raise AssertionError("Opening %r failed: %s" % (filename, e))

    line = handle.readline()
    handle.close()

    if line != expected:
        raise AssertionError("line %r, expected %r" % (line, expected))

class DownloaderTest(unittest.TestCase):

    TESTING = True

    def setUp(self):
        self.DEFAULT_DOWNLOAD_DIR = tempfile.mkdtemp()
        self.BAD_CONTENT = ('Error reading from remote server',
                            'Test bad content')
        (fd, name) = tempfile.mkstemp(dir=self.DEFAULT_DOWNLOAD_DIR)
        os.write(fd, 'Test file\n')
        os.close(fd)
        self.tmp_name = name

        (fd, name) = tempfile.mkstemp(dir=self.DEFAULT_DOWNLOAD_DIR)
        os.write(fd, 'Test bad content\n')
        os.close(fd)
        self.bad_file = name

        self.app = Flask(__name__)
        self.app.config.from_object(self)

        assert self.app.testing

        self.dl = Downloader(self.app)

    def tearDown(self):
        shutil.rmtree(self.DEFAULT_DOWNLOAD_DIR)

    def test_download(self):
        """Test download function downloads file from URL
        """
        res = self.dl.download(self.tmp_name)
        assert res is not None
        assert hasattr(res, 'save')

    def test_download_returns_none_on_failure(self):
        """Test download function returns None on failure
        """
        res = self.dl.download(path.join(
                        self.DEFAULT_DOWNLOAD_DIR,'invalid.txt'))
        assert res is None

    def test_download_raises_download_error_on_bad_content(self):
        """Test download function checks file for bad content
        """
        self.assertRaises(DownloaderError, self.dl.download, self.bad_file)
        try:
            self.dl.download(self.bad_file)
            raise AssertionError('download() failed to raise an exception on bad content')
        except DownloaderError, e:
            self.assertEqual(str(e), "File contains bad content: 'Test bad content'")

        self.app.config.pop('BAD_CONTENT')
        res = self.dl.download(self.bad_file)
        assert res is not None

    def test_save(self):
        """Test save function downloads and saves a file
        """
        test_file = path.join(self.DEFAULT_DOWNLOAD_DIR, 'test.txt')
        assert not path.exists(test_file)
        self.dl.save(self.tmp_name, 'test.txt')
        assert_first_line(test_file, 'Test file\n')

    def test_save_specified_dir(self):
        """Test save function downloads file and saves it in a given directory
        """
        tmp_dir = tempfile.mkdtemp(dir=self.DEFAULT_DOWNLOAD_DIR)
        test_file = path.join(tmp_dir, 'test.txt')
        assert not path.exists(test_file)
        self.dl.save(self.tmp_name, 'test.txt', tmp_dir)
        assert_first_line(test_file, 'Test file\n')

    def test_save_raises_downloader_error(self):
        """Test save function raises a DownloaderError on error
        """
        invalid = path.join(self.DEFAULT_DOWNLOAD_DIR,'invalid.txt')
        assert not os.path.exists(invalid)
        self.assertRaises(DownloaderError, self.dl.save, invalid, 'test.txt')
