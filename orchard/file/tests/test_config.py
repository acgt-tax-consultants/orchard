# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import tempfile
import unittest

from orchard.file import ConfigFile


class TestConfigFile(unittest.TestCase):

    def setUp(self):
        yaml_text = \
            'modules:\n' \
            '- name: ModuleOne\n' \
            '  arguments:\n' \
            '  - infile: in.txt\n' \
            '  - outfile: out.txt\n' \
            '  - digit: 5\n' \
            '- name: ModuleTwo\n' \
            '  arguments:\n' \
            '  - infile: c://temp/out.txt\n' \
            '  - outfile: out2.txt\n' \
            '  - digit: 5\n' \
            '  optionals:\n' \
            '  - forward:\n' \
            '  - reverse:\n' \
            '- name: ModuleThree\n' \
            '  arguments:\n' \
            '  - infile: out2.txt\n' \
            '  - outfile: out3.txt\n' \
            '  - digit: 5\n'

        self.yaml_file = tempfile.NamedTemporaryFile('w+')
        self.yaml_file.write(yaml_text)
        self.yaml_file.flush()

    def test_creation(self):
        config_file = ConfigFile(self.yaml_file.name)

        self.assertIsInstance(config_file, ConfigFile)
        self.assertEqual(len(config_file.modules), 3)


if __name__ == '__main__':
    unittest.main()
