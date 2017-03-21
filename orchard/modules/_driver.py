# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import sys
import os.path
import yaml


class Driver:
    def __init__(self):
        # Check that there are only two input arguments
        if (len(sys.argv) == 3 or len(sys.argv) == 2):
            # Check that link file path has the correct extension
            self.link_file_path = str(sys.argv[1])
            if (not self.link_file_path.split('.')[1] == 'yaml' and
                    not self.link_file_path.split('.')[1] == 'yml'):
                print('The link file path has the wrong extension.')
                print('\tExpected: \t.yaml')
                print('\tFound: \t\t.' + self.link_file_path.split('.')[1])
                sys.exit()

            # Check that the link file exists
            if (not os.path.isfile(self.link_file_path)):
                print('The link file: ', self.link_file_path,
                      'does not exist.')
                sys.exit()
            # Check that a config file was given as argument 3
            if (len(sys.argv) == 3):
                # Check that config file path has the correct extension
                self.config_file_path = str(sys.argv[2])
                if (not self.config_file_path.split('.')[1] == 'yaml' and
                        not self.config_file_path.split('.')[1] == 'yml'):
                    print('The configuration file path has',
                          'the wrong extension.')
                    print('\tExpected: \t.yaml')
                    print('\tFound: \t\t.',
                          self.config_file_path.split('.')[1])
                    sys.exit()

                # Check that the configuration file exists
                if (not os.path.isfile(self.config_file_path)):
                    print('The configuration file: ' +
                          self.config_file_path + ' does not exist.')
                    sys.exit()
            else:
                self.generate_config_file()
        else:
            print('Orchard requires a Link File path' +
                  ' and/or a Config File path')
            sys.exit()
        print("Nothing Went Wrong")

    def generate_config_file(self):
        with open(self.link_file_path) as fileHandle:
            try:
                dictionary = yaml.load(fileHandle, Loader=yaml.Loader)
            except Exception as e:
                print("The link file is not in the correct format.")
                sys.exit()
            dict_list = dictionary['modules']
            for modules in dict_list:
                try:
                    del modules['dependencies']
                    del modules['exlusive']
                except KeyError:
                    pass
                if ('arguments' in modules):
                    for arguments in modules['arguments']:
                        arguments[arguments['name']] = None
                        arguments.pop('name')
                        try:
                            del arguments['isBranch']
                        except KeyError:
                            pass
                        try:
                            del arguments['command']
                        except KeyError:
                            pass
                if ('optionals' in modules):
                    for arguments in modules['optionals']:
                        arguments[arguments['name']] = None
                        arguments.pop('name')
                        try:
                            del arguments['isBranch']
                        except KeyError:
                            pass
                        try:
                            del arguments['command']
                        except KeyError:
                            pass
                        try:
                            del arguments['isFlag']
                        except KeyError:
                            pass
            yaml.SafeDumper.add_representer(
              type(None), lambda dumper,
              value: dumper.represent_scalar(
                u'tag:yaml.org,2002:null', ''))
            with open("ConfigFile.yaml", 'w') as fh:
                yaml.safe_dump(dictionary, fh, default_flow_style=False)
