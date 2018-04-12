#!/usr/bin/env python
# -*-python-*-

import os
import sys
from shutil import rmtree

cwd = os.path.dirname(os.path.realpath(sys.argv[0]))
egg_info = cwd + "/whosonfirst.schema.egg-info"
if os.path.exists(egg_info):
    rmtree(egg_info)

from setuptools import setup, find_packages

packages = find_packages()
print(packages)
desc = open("README.md").read()
version = open("VERSION").read()

setup(
    name='whosonfirst.schema',
    namespace_packages=['whosonfirst'],
    version=version,
    description='Python tools for doing JSON Schema related things with Who\'s On First property definitions.',
    author='Gary Gale',
    author_email='gary@vicchi.org',
    url='https://github.com/whosonfirst/py-whosonfirst-json-schema',
    packages=packages,
    scripts=[
        'scripts/wof-build-schema',
        ],
    download_url='https://github.com/whosonfirst/py-whosonfirst-json-schema/releases/tag/' + version,
    license='BSD'
)
