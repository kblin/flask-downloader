 # -*- coding: utf-8 -*-
from __future__ import with_statement

import unittest
import tempfile
import shutil
from os import path

from flask import Flask
from flaskext.downloader import Downloader

class DownloaderTest(unittest.TestCase):

    TESTING = True

    def setUp(self):
        self.DEFAULT_DOWNLOAD_DIR = tempfile.mkdtemp()
        (fd, name) = tempfile.mkstemp(dir=self.DEFAULT_DOWNLOAD_DIR)
        os.write(fd, 'Test file\n')
        os.close(fd)
        self.tmp_name = name
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
