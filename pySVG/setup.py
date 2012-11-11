#!/usr/bin/env python

#from distutils.core import setup
from setuptools import setup

setup(name="pysvg",
      version="0.2.2",
      description="Python SVG Library",
      author="Kerim Mansour",
      author_email="kmansour@web.de",
      url="http://codeboje.de/pysvg/",
      packages=['pysvg'],
      package_dir={"pysvg":"src/pysvg"},
      classifiers = [
          'Development Status :: 4 - Beta',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: MacOS :: MacOS X',
          'Operating System :: Microsoft :: Windows',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Topic :: Multimedia :: Graphics',
          ],
     )
