# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import tempfile
import unittest

from orchard.core import generate_luigi
from orchard.file import LinkFile, ConfigFile
from . import DATA

FILES = os.path.join(DATA, 'tests', 'data', 'generator')


class TestGenerator(unittest.TestCase):
    def test_pass_full(self):
        # Tests working full config and link file.
        link_path = os.path.join(FILES, 'link.yaml')
        config_path = os.path.join(FILES, 'config.yaml')

        link_file = LinkFile(link_path)
        config_file = ConfigFile(config_path, True)

        with tempfile.NamedTemporaryFile('w+') as fh:
            generate_luigi(config_file, link_file, fh.name)

            self.assertTrue(os.path.exists(fh.name))
            self.assertIn('ExternalProgramTask', fh.read())
