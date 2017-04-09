import unittest
from orchard.modules.CFT import generate_config_file


class Test_CFR(unittest.TestCase):
    def test_error_yaml_format(self):
        # Several tests for incorrect yaml format of input link file
        with self.assertRaises(RuntimeError):
            generate_config_file(
             "orchard/modules/tests/Test_Data/CFT_Data/link_fail_1.yaml")
        with self.assertRaises(RuntimeError):
            generate_config_file(
             "orchard/modules/tests/Test_Data/CFT_Data/link_fail_3.yaml")

    def test_pass_missing_name_argument(self):
        # Tests 'name' not being in exclusives
        generate_config_file(
         "orchard/modules/tests/Test_Data/CFT_Data/link_fail_2.yaml")
