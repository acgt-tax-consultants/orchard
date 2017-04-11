# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources
import unittest

from click.testing import CliRunner

from orchard.cli import orchard

DATA = pkg_resources.resource_filename('orchard', 'tests')


class TestOrchard(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    def test_system(self):
        with self.runner.isolated_filesystem():
            result = self.runner.invoke(orchard)

            self.assertEqual(result.exit_code, 0)
            self.assertIn('build', result.output)
            self.assertIn('template', result.output)

    def test_template(self):
        with self.runner.isolated_filesystem() as fh:
            link_path = os.path.join(DATA, 'data', 'link.yaml')
            result = self.runner.invoke(orchard, ['template', link_path])

            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.exists(os.path.join(fh, 'config.yaml')))

    def test_template_fail_extension(self):
        with self.runner.isolated_filesystem() as fh:
            link_path = os.path.join(DATA, 'data', 'link.txt')
            result = self.runner.invoke(orchard, ['template', link_path])

            self.assertEqual(result.exit_code, 1)
            self.assertTrue(
                not os.path.exists(os.path.join(fh, 'config.yaml')))

    def test_template_fail_yaml(self):
        with self.runner.isolated_filesystem() as fh:
            link_path = os.path.join(DATA, 'data', 'fail.yaml')
            result = self.runner.invoke(orchard, ['template', link_path])

            self.assertEqual(result.exit_code, 1)
            self.assertTrue(
                not os.path.exists(os.path.join(fh, 'config.yaml')))

    def test_build(self):
        with self.runner.isolated_filesystem() as fh:
            link_path = os.path.join(DATA, 'data', 'link.yaml')
            config_path = os.path.join(DATA, 'data', 'config.yaml')

            result = self.runner.invoke(orchard,
                                        ['build', link_path, config_path])

            self.assertEqual(result.exit_code, 0)
            self.assertTrue(os.path.exists(os.path.join(fh, 'test.py')))

    def test_build_fail_extension(self):
        with self.runner.isolated_filesystem() as fh:
            link_path = os.path.join(DATA, 'data', 'link.txt')
            config_path = os.path.join(DATA, 'data', 'link.txt')
            result = self.runner.invoke(orchard,
                                        ['build', link_path, config_path])

            self.assertEqual(result.exit_code, 1)
            self.assertTrue(
                not os.path.exists(os.path.join(fh, 'config.yaml')))

    def test_build_fail_yaml(self):
        with self.runner.isolated_filesystem() as fh:
            link_path = os.path.join(DATA, 'data', 'fail.yaml')
            config_path = os.path.join(DATA, 'data', 'config.yaml')
            result = self.runner.invoke(orchard,
                                        ['build', link_path, config_path])

            self.assertEqual(result.exit_code, 1)
            self.assertTrue(
                not os.path.exists(os.path.join(fh, 'test.py')))


if __name__ == '__main__':
    unittest.main()
