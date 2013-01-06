"""
Flask-Downloader
----------------

Allow a Flask web app to download files on behalf of the user.

Links
`````

* `documentation <http://packages.python.org/Flask-Downloader>`_
* `development version
  <http://github.com/kblin/flask-downloader/zipball/master#egg=Flask-Downloader-dev>`_

"""
from setuptools import setup


setup(
    name='Flask-Downloader',
    version='0.2',
    url='https://github.com/kblin/flask-downloader',
    license='BSD',
    author='Kai Blin',
    author_email='kai@samba.org',
    description='Allow a Flask web app to download files on behalf of the user.',
    long_description=__doc__,
    packages=['flaskext'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
