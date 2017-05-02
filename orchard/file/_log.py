# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._config import ConfigFile
import collections
import yaml


class LogFile():
    # self.configs - a list of Config_File Class objects for each branch
    # self.data - a collection that contains the raw yaml dictionary
    configs = {}

    # If new is not true then open filedata as a path and read it in, else
    # make a new branch 1 in our structure that matches the ConfigFile passed
    # in as filedata
    def __init__(self, filedata, new):
        if not new:
            data = collections.defaultdict(list)
            with open(str(filedata)) as fh:
                try:
                    data.update(yaml.load(fh))
                except Exception as e:
                    raise RuntimeError(
                        'The log file is not a valid yaml format.')

            # Push each branch's ConfigFile Structure to the matching branchnum
            # entry in self.configs
            for branchnum, config_dat in data.items():
                self.configs[branchnum] = ConfigFile(config_dat, False)
        else:
            self.configs[1] = filedata

    # Returns a yaml representation of the Logfile
    def _get_yaml(self):
        data = {}
        for branchnum, config_file in self.configs.items():
            data[branchnum] = config_file.get_yaml()
        return data

    # Adds a new branch to the logfile structure, returning the branchnum of
    # the new branch
    def add_branch(self, config_file):
        new_branch_num = 1
        while new_branch_num in self.configs:
            new_branch_num += 1

        self.configs[new_branch_num] = config_file
        return new_branch_num

    # Writes the log data out to the given filepath
    def write(self, filepath):
        def _add_repr(dumper, value):
            return dumper.represent_scalar(u'tag:yaml.org,2002:null', '')

        yaml.SafeDumper.add_representer(type(None), _add_repr)

        with open(str(filepath), 'w') as fh:
            yaml.safe_dump(self._get_yaml(), fh, default_flow_style=False)
