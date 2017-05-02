# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import collections

import yaml


class YAMLFile:
    # self.modules - a list of Module Class objects for each module
    # self.data - a collection that contains the raw yaml dictionary

    # Contains number of Module Class objects
    modules = None

    def __init__(self, filepath):
        data = collections.defaultdict(list)
        with open(filepath) as fh:
            try:
                data.update(yaml.load(fh))
            except Exception as e:
                raise RuntimeError('The link file is not a valid yaml format.')

        modules = data.get('modules')
        if modules:
            self.modules = []
            self._add_modules(modules)

    # Gets the module object with the matching module name
    def get_module_data(self, module_name):
        try:
            module, = filter(lambda x: x.name == module_name, self.modules)
        except ValueError:
            raise ValueError('Unable to retreive linkage data from link file '
                             'for module: %s.' % module_name) from None
        return module

    # Writes the yaml-file data out to the given filepath
    def write(self, data, filepath):
        def _add_repr(dumper, value):
            return dumper.represent_scalar(u'tag:yaml.org,2002:null', '')
        yaml.SafeDumper.add_representer(type(None), _add_repr)

        with open(filepath, 'w') as fh:
            yaml.safe_dump(data, fh, default_flow_style=False)
