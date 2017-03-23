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


def check_lfp(link_file_path):

    # Check that link file path has the correct extension
    if (not link_file_path.split('.')[1] == 'yaml'):
        print('The link file path has the wrong extension.')
        print('\tExpected: \t.yaml')
        print('\tFound: \t\t.' + link_file_path.split('.')[1])
        sys.exit()

    # Check that the link file exists
    elif (not os.path.isfile(link_file_path)):
        print('The link file: ', link_file_path,
              'does not exist.')
        sys.exit()

    # If the file path is exists and is yml/yaml
    # config file generation begins
    else:
        generate_config_file(link_file_path)


def generate_config_file(link_file_path):
    with open(link_file_path) as fileHandle:
        try:
            dictionary = yaml.load(fileHandle, Loader=yaml.Loader)
        except Exception as e:
            print("The link file is not in the correct format.")
            sys.exit()
        dict_list = dictionary['modules']
        for modules in dict_list:
            try:
                del modules['dependencies']
            except KeyError:
                pass
            try:
                del modules['exclusive']
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
                    try:
                        del arguments['optional']
                    except KeyError:
                        pass
                    try:
                        del arguments['isFlag']
                    except KeyError:
                        pass
            if ('optionals' in modules):
                for optionals in modules['optionals']:
                    optionals[optionals['name']] = None
                    optionals.pop('name')
                    try:
                        del optionals['isFlag']
                    except KeyError:
                        pass
                    try:
                        del optionals['command']
                    except KeyError:
                        pass
        yaml.SafeDumper.add_representer(
          type(None), lambda dumper,
          value: dumper.represent_scalar(
            u'tag:yaml.org,2002:null', ''))
        with open("ConfigFileTest.yaml", 'w') as fh:
            yaml.safe_dump(dictionary, fh, default_flow_style=False)


def main(argv):
    check_lfp(argv)


if __name__ == '__main__':
    main(sys.argv[1])
