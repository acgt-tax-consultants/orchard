# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from setuptools import find_packages, setup

with open("README.md") as fh:
    long_description = fh.read()

setup(
    name='orchard',
    version='0.0.1',
    long_description=long_description,
    packages=find_packages(),
    install_requires=['luigi', 'sciluigi', 'jinja2']
)
