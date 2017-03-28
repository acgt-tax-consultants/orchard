# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest

from click.testing import CliRunner

from ..cli import orchard


class TestOrchard(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_system(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(orchard)

            self.assertEqual(result.exit_code, 0)
            self.assertIn('build', result.output)
            self.assertIn('template', result.output)


if __name__ == '__main__':
    unittest.main()
