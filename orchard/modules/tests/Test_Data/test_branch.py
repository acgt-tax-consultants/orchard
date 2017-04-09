import unittest
import yaml
from orchard.modules._branch import branching


class Test_Generator(unittest.TestCase):
    def test_pass_full(self):
        # Several tests for incorrect yaml format of input link file
        branching(
            yaml.load(open(
             "orchard/modules/tests/Test_Data/Branch_Data/config.yaml")),
            yaml.load(open(
             "orchard/modules/tests/Test_Data/Branch_Data/link.yaml")),
            "./")
