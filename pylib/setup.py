#!/usr/bin/python

from setuptools import setup, find_packages

DESCRIPTION = """ Greenlet based Google's protocol buffer RPC implementation
"""

setup(
    name="gorpc",
    version="0.0.1",
    description="a Python implementation of protobuf RPC over sockets/greenlet",
    long_description=DESCRIPTION,
    author='Jyotiswarup Raiturkar',
    author_email='jyotiswarip.raiturkar@goibibo.com',
    packages=find_packages('src', exclude=[
            '*.*.tests', '*.*.examples', '*.*.examples.*']),
    package_dir={'': 'src'},
    #install_requires=['protobuf>=2.6'],
)
