# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._yaml_file import YAMLFile

from ..module import Module


class ConfigFile(YAMLFile):

    def _add_modules(self, modules):
        for module in modules:
            self.modules.append(Module(module))
