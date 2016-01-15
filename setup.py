#!/usr/bin/env python
# -*- coding: utf-8 -*-

from distutils.core import setup
from setuptools import find_packages

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='xvecc',
    version='2.0', # __import__('xvecc').__version__,
    author='Mathieu Agopian and more',
    author_email='mathieu.agopian@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    url='https://github.com/topchretien/xvecc',
    license='BSD',
    description='Video Embed Code Cleaner',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
    zip_safe=False,
    install_requires=['argparse', 'requests'],
    entry_points="""
        [console_scripts]
            xvecc = xvecc.xvecc:main"""
)
