# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

from orchard.module import Argument, Exclusive


class TestArguments(unittest.TestCase):
    def setUp(self):
        self.arg_data = [{'name': 'infile'}, {'name': 'outfile'}]
        self.values = ['test1.txt', 'test2.txt']

    def test_creation(self):
        for data in self.arg_data:
            arg = Argument(data)

            self.assertIsInstance(arg, Argument)

    def test_value_addition(self):
        for data, value in zip(self.arg_data, self.values):
            arg = Argument(data)
            arg.add_value(value)

            self.assertEqual(arg.value, value)

    def test_repr(self):
        for data, value in zip(self.arg_data, self.values):
            arg = Argument(data)

            self.assertEqual(str(arg), data.get('name'))


class TestExclusives(unittest.TestCase):

    def test_exclusives(self):
        arg_data = [{'name': 'infile', 'value': None},
                    {'name': 'outfile', 'value': True}]
        exc = Exclusive(arg_data)
        result = exc.get_selected()

        self.assertEqual(str(exc), '(infile, outfile)')
        self.assertEqual(result.name, 'outfile')

    def test_exclusives_fail(self):
        arg_data = [{'name': 'infile', 'value': True},
                    {'name': 'outfile', 'value': True}]
        exc = Exclusive(arg_data)

        with self.assertRaisesRegex(ValueError, 'exclusive'):
            exc.get_selected()

    def test_exclusive_get_argument(self):
        arg_data = [{'name': 'infile', 'value': True},
                    {'name': 'outfile', 'value': True}]
        exc = Exclusive(arg_data)

        with self.assertRaisesRegex(ValueError, 'argument'):
            exc.get_argument('zipfile')


if __name__ == '__main__':
    unittest.main()
