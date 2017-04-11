# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import unittest

from orchard.core import validate
from . import DATA

FILES = os.path.join(DATA, 'tests', 'data', 'configuration_file_reader')


class TestCFR(unittest.TestCase):
    def test_pass_full(self):
        # Test's a passing scenario with optionals
        # exlcusives, and optional exclusives all
        # filled correctly.
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_pass_1.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 0)

    def test_pass_optional(self):
        # Tests a passing scenario with optional
        # filled correctly
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_pass_2.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 0)

    def test_pass_optional_exlcusive(self):
        # Tests a passing scenario with
        # optional exclusive filled correctly
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_pass_3.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 0)

    def test_error_everything(self):
        # Test that error value is received empty.
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_fail_1.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 1)

    def test_error_required(self):
        # Test that error value is received when missing
        # required arguments
        link_path = os.path.join(FILES, 'link.yaml')
        config_path_1 = os.path.join(FILES, 'config_fail_2_1.yaml')
        config_path_2 = os.path.join(FILES, 'config_fail_2_2.yaml')
        config_path_3 = os.path.join(FILES, 'config_fail_2_3.yaml')

        result_1 = validate(link_path, config_path_1)
        result_2 = validate(link_path, config_path_2)
        result_3 = validate(link_path, config_path_3)

        self.assertEqual(result_1, 1)
        self.assertEqual(result_2, 1)
        self.assertEqual(result_3, 1)

    def test_error_required_exlusive(self):
        # Test that error value is received when
        # when too many exlcusives are filled
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_fail_3.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 1)

    def test_error_optional_exclusive(self):
        # Test that error value is received when
        # too many optional exclusives are filled in.
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_fail_4.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 1)

    def test_error_exclusive(self):
        # Test that error value is received when
        # no required exclusive is entered
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_fail_5.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 1)

    def test_error_missing_element(self):
        # Test that error value is received when
        # config file is fundamentally changed.
        # ex: entire argument is removed.
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config_fail_6.yaml')

        result = validate(link_path, config_path)

        self.assertEqual(result, 1)
