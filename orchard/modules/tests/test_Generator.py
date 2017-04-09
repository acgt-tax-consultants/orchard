import unittest
from orchard.modules._generator import generate_luigi


class Test_Generator(unittest.TestCase):
    def test_pass_full(self):
        # Tests working full config and link file.
        generate_luigi(
         "orchard/modules/tests/Test_Data/Generator_Data/link.yaml",
         "orchard/modules/tests/Test_Data/Generator_Data/config.yaml")
