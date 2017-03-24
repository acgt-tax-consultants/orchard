# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import sys
import os
import yaml
import filecmp
from .CFT import generate_config_file


def validate(link_file_path, config_file_path):
    # Simplify both the link and the config files then compare
    generate_config_file(link_file_path, "linkTest.yaml")
    error_checking = simplify(config_file_path, "configTest.yaml")
    if (error_checking):
        if (error_checking == 1):
            print("User failed to provide required input arguments")
        elif (error_checking == 2):
            print("User provided too many exclusive arguments")
        elif (error_checking == 3):
            print("User failed to provide a single exclusive argument")
        sys.exit()
    else:
        print("Configuration arguments were entered properly")

    print("Comparing files")
    sameFile = filecmp.cmp('linkTest.yaml', 'configTest.yaml')
    # Delete files after comparison
    os.remove("linkTest.yaml")
    os.remove("configTest.yaml")
    if (sameFile):
        print("Files have passed validation")
        return 0
    else:
        print("Files have failed validation")
        return 1


def simplify(config_file_path, output_file_name):
    to_ignore = ['exclusive', 'optionals']

    with open(config_file_path) as fh:
        try:
            dictionary = yaml.load(fh, Loader=yaml.Loader)
        except Exception as e:
            raise RuntimeError("The config file is not in the correct format.")

    for modules in dictionary['modules']:
        for arguments in modules.get('arguments', []):
            for key in arguments:
                if key not in to_ignore:
                    if (arguments[key] is None):
                        return 1
                    else:
                        arguments[key] = None

            if 'exclusive' in arguments:
                exclusivity_test = False
                for exclusives in arguments.get('exclusive', []):
                    for key in exclusives:
                        if (exclusives[key] is None):
                            pass
                        elif (exclusivity_test):
                            return 2
                        else:
                            exclusivity_test = True
                            exclusives[key] = None
                if (not exclusivity_test):
                    return 3

        for optionals in modules.get('optionals', []):
            for key in optionals:
                if key not in to_ignore:
                    optionals[key] = None

            if 'exclusive' in optionals:
                exclusivity_test = False
                for exclusives in optionals.get('exclusive', []):
                    for key in exclusives:
                        if (exclusives[key] is None):
                            pass
                        elif (exclusivity_test):
                            return 2
                        else:
                            exclusivity_test = True
                            exclusives[key] = None

    def _add_repr(dumper, value):
        return dumper.represent_scalar(u'tag:yaml.org,2002:null', '')

    yaml.SafeDumper.add_representer(type(None), _add_repr)
    with open(output_file_name, 'w') as fh:
        yaml.safe_dump(dictionary, fh, default_flow_style=False)
