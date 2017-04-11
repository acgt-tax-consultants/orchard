# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import tempfile
import unittest

import yaml
from orchard.core import branching
from . import DATA

FILES = os.path.join(DATA, 'tests', 'data', 'branch')


class TestGenerator(unittest.TestCase):
    def test_pass_full(self):
        # Several tests for incorrect yaml format of input link file
        config_path = os.path.join(FILES, 'config.yaml')
        link_path = os.path.join(FILES, 'link.yaml')

        with open(config_path) as fh1, open(link_path) as fh2:
            config_yaml = yaml.load(fh1.read())
            link_yaml = yaml.load(fh2.read())

        with tempfile.TemporaryDirectory() as tmp:
            branching(config_yaml, link_yaml, tmp)

            self.assertTrue(
                os.path.exists(os.path.join(tmp, 'branchlog.yaml')))
            self.assertTrue(os.path.exists(os.path.join(tmp, '1')))
