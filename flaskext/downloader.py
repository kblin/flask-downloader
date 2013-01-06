# -*- coding: utf-8 -*-
"""
    flaskext.downloader
    ~~~~~~~~~~~~~~~~~~~

    Allow a Flask web app to download files on behalf of the user.

    :copyright: (c) 2011 by Kai Blin.
    :license: BSD, see LICENSE for more details.
"""
import urllib
import os.path
from werkzeug import FileStorage
try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class DownloaderError(Exception):
    """Error raised by :class:`Downloader` if download failed.
    """
    pass

class Downloader(object):
    """Download manager class for handling downloads in Flask
    """

    def __init__(self, app=None):
        self.app = app

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Set up this instance for use with *app*
        """
        self.app = app

        app.extensions = getattr(app, 'extensions', {})
        app.extensions['downloader'] = self

        app.config.setdefault('DEFAULT_DOWNLOAD_DIR', os.path.dirname(__file__))

    def download(self, url):
        """Download the URL's contents, returning a :class:`FileStorage` instance

        If the URL cannot be opened, returns `None`
        """
        try:
            handle = urllib.urlopen(url)
            content_type = handle.headers.get('content-type',
                                'application/octet-stream')
            content_length = handle.headers.get('content-length', -1)
            headers = handle.headers
            if 'BAD_CONTENT' in self.app.config:
                handle = StringIO(handle.read())
                for line in handle:
                    for bad in self.app.config['BAD_CONTENT']:
                        if bad in line:
                            raise DownloaderError('File contains bad content: %r' % bad)
                handle.seek(0)
            store = FileStorage(stream=handle, content_type=content_type,
                                content_length=content_length,
                                headers=headers)
            return store
        except IOError:
            return None

    def save(self, url, filename, dirname=None):
        """Download the URL's contents, saving to a file.
           Raises a :class:`DownloaderError` when download fails.
        """
        try:
            if dirname is None:
                dirname = self.app.config['DEFAULT_DOWNLOAD_DIR']
            full_name = os.path.join(dirname, filename)
            urllib.urlretrieve(url, full_name)
        except IOError, e:
            raise DownloaderError(unicode(e))
        except urllib.ContentTooShortError, e:
            raise DownloaderError(e.msg)

