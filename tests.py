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
        self.app = Flask(__name__)
        self.app.config.from_object(self)

        assert self.app.testing

        self.dl = Downloader(self.app)

    def tearDown(self):
        shutil.rmtree(self.DEFAULT_DOWNLOAD_DIR)

    def test_download(self):
        """Test download function"""
        res = self.dl.download(path.join(
                        self.DEFAULT_DOWNLOAD_DIR,'invalid.txt'))
        assert res is None
