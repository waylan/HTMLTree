#!/usr/bin/env python

from setuptools import setup

with  open('README.rst', mode='r') as fd:
    long_description = fd.read()

from htree import __version__

setup(
    name='HTMLTree',
    version=__version__,
    url='https://github.com/waylan/HTMLTree',
    description='An HTML Node Tree toolkit.',
    long_description=long_description,
    author='Waylan Limberg',
    author_email='waylan.limberg@icloud.com',
    license='BSD License',
    py_modules=['htree'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: HTML',
        'Topic :: Utilities'
    ]
)