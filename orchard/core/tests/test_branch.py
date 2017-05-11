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

from orchard.core import branching
from orchard.file import LinkFile, ConfigFile
from . import DATA

FILES = os.path.join(DATA, 'tests', 'data', 'branch')


class TestGenerator(unittest.TestCase):
    def test_pass_first(self):
        config_path = os.path.join(FILES, 'config.yaml')
        link_path = os.path.join(FILES, 'link.yaml')

        config_file = ConfigFile(config_path, True)
        link_file = LinkFile(link_path)

        with tempfile.TemporaryDirectory() as tmp:
            branching(config_file, link_file, tmp)

            self.assertTrue(
                os.path.exists(os.path.join(tmp, '.branchlog.yaml')))
            self.assertTrue(os.path.exists(os.path.join(tmp, '1')))

    def test_pass_perfect(self):
        config_path = os.path.join(FILES, 'config.yaml')
        link_path = os.path.join(FILES, 'link.yaml')

        config_file = ConfigFile(config_path, True)
        config_file_dup = ConfigFile(config_path, True)
        link_file = LinkFile(link_path)

        with tempfile.TemporaryDirectory() as tmp:
            branching(config_file, link_file, tmp)
            branching(config_file_dup, link_file, tmp)

            self.assertFalse(os.path.exists(os.path.join(tmp, '2')))

    def test_pass_second(self):
        config_path = os.path.join(FILES, 'config.yaml')
        config_path2 = os.path.join(FILES, 'config2.yaml')
        link_path = os.path.join(FILES, 'link.yaml')

        config_file = ConfigFile(config_path, True)
        config_file2 = ConfigFile(config_path2, True)
        link_file = LinkFile(link_path)

        with tempfile.TemporaryDirectory() as tmp:
            branching(config_file, link_file, tmp)
            branching(config_file2, link_file, tmp)

            self.assertTrue(os.path.exists(os.path.join(tmp, '2')))
            self.assertTrue(os.path.lexists(os.path.join(tmp, '2', 'b.txt')))
            self.assertFalse(os.path.lexists(os.path.join(tmp, '2', 'c.txt')))
            self.assertFalse(os.path.lexists(os.path.join(tmp, '2', 'd.txt')))

    # TODO: Figure out why this test breaks when run with test_pass_second()
    # def test_pass_third(self):
    #     config_path = os.path.join(FILES, 'config.yaml')
    #     config_path2 = os.path.join(FILES, 'config2.yaml')
    #     config_path3 = os.path.join(FILES, 'config3.yaml')
    #     link_path = os.path.join(FILES, 'link.yaml')
    #
    #     config_file = ConfigFile(config_path, True)
    #     config_file2 = ConfigFile(config_path2, True)
    #     config_file3 = ConfigFile(config_path3, True)
    #     link_file = LinkFile(link_path)
    #
    #     with tempfile.TemporaryDirectory() as tmp:
    #         branching(config_file, link_file, tmp)
    #         branching(config_file2, link_file, tmp)
    #         branching(config_file3, link_file, tmp)
    #
    #         self.assertTrue(os.path.exists(os.path.join(tmp, '3')))
    #         self.assertTrue(os.path.lexists(os.path.join(tmp, '3', 'b.txt')))
    #         self.assertTrue(os.path.lexists(os.path.join(tmp, '3', 'c.txt')))
    #        self.assertFalse(os.path.lexists(os.path.join(tmp, '3', 'd.txt')))
