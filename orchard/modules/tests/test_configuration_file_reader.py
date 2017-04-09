import unittest
from orchard.modules._configuration_file_reader import validate


class Test_CFR(unittest.TestCase):
    def test_pass_full(self):
        # Test's a passing scenario with optionals
        # exlcusives, and optional exclusives all
        # filled correctly.
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_pass_1.yaml"), 0)

    def test_pass_optional(self):
        # Tests a passing scenario with optional
        # filled correctly
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_pass_2.yaml"), 0)

    def test_pass_optional_exlcusive(self):
        # Tests a passing scenario with
        # optional exclusive filled correctly
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_pass_3.yaml"), 0)

    def test_error_everything(self):
        # Test that error value is received empty.
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_1.yaml"), 1)

    def test_error_required(self):
        # Test that error value is received when missing
        # required arguments
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_2_1.yaml"), 1)
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_2_2.yaml"), 1)
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_2_3.yaml"), 1)

    def test_error_required_exlusive(self):
        # Test that error value is received when
        # when too many exlcusives are filled
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_3.yaml"), 1)

    def test_error_optional_exclusive(self):
        # Test that error value is received when
        # too many optional exclusives are filled in.
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_4.yaml"), 1)

    def test_error_exclusive(self):
        # Test that error value is received when
        # no required exclusive is entered
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_5.yaml"), 1)

    def test_error_missing_element(self):
        # Test that error value is received when
        # config file is fundamentally changed.
        # ex: entire argument is removed.
        self.assertEqual(validate(
          "orchard/modules/tests/Test_Data/CFR_Data/link.yaml",
          "orchard/modules/tests/Test_Data/CFR_Data/config_fail_6.yaml"), 1)
