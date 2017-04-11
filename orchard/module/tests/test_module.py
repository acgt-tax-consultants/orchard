# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

from orchard.module import Module


class TestModules(unittest.TestCase):
    def setUp(self):
        self.link_data = [
            {'name': 'Module1',
             'arguments': [{'name': 'infile'}, {'name': 'outfile'}]},
            {'name': 'Module2',
             'arguments': [{'name': 'infile'}, {'name': 'outfile'}]},
        ]

        self.config_data = [
            {'name': 'Module1',
             'arguments': [{'infile': 'test.txt'}]}
        ]

    def test_from_link_file_creation(self):
        for module_data in self.link_data:
            module = Module(module_data, from_link=True)

            self.assertEqual(module.name, module_data.get('name'))
            self.assertIsInstance(module, Module)

            for i, argument in enumerate(module.arguments):
                self.assertEqual(argument.name,
                                 module_data['arguments'][i].get('name'))

    def test_from_config_file_creation(self):
        for module_data in self.config_data:
            module = Module(module_data)

            self.assertEqual(module.name, module_data.get('name'))
            self.assertIsInstance(module, Module)

            for i, argument in enumerate(module.arguments):
                self.assertIn(argument.name,
                              module_data['arguments'][i].keys())

    def test_add_dependency(self):
        parent = Module(self.link_data[0], from_link=True)
        child = Module(self.link_data[1], from_link=True)

        child.add_dependency(parent)

        self.assertIn(parent, child.dependencies)

    def test_repr(self):
        module = Module(self.config_data[0])

        self.assertEqual(str(module), "%s: [infile]" % module.name)


if __name__ == '__main__':
    unittest.main()
