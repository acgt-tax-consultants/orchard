# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


import os
import tempfile
import filecmp

import yaml
from ..file import LinkFile


# Configuration File Reader compares two files: the config template file,
# and the config file the user filled out.
# It checks to make sure that the user correctly filled out the variable
# values and didn't add/remove any other parts to/from the file.
def validate(link_file_path, config_file_path):
    # Simplify both the link and the config files then compare

    with tempfile.TemporaryDirectory() as tmp:
        link_path = os.path.join(tmp, 'link_test.yaml')
        config_path = os.path.join(tmp, 'config_test.yaml')

        # Create a config template file
        LinkFile(link_file_path).template_config_file(link_path)
        # Simplify the users filled out config file.
        # Simplify is described below.
        error_checking = simplify(config_file_path, config_path)
        if (error_checking == 1):
            print("User failed to provide required input arguments")
            return 1
        elif (error_checking == 2):
            print("User provided too many exclusive arguments")
            return 1
        elif (error_checking == 3):
            print("User failed to provide a single exclusive argument")
            return 1
        else:
            print("Configuration arguments were entered properly")

        print("Comparing files")
        sameFile = filecmp.cmp(link_path, config_path)

    if (sameFile):
        print("Files have passed validation")
        return 0
    else:
        print("Files have failed validation")
        return 1


# simplify() takes the config file and 'simplifies' it down to a version that
# doesn't have it's argument values filled out.
# Basically, it creates a new, empty config file. This file is temporary and is
# destoyed at the end of this validation.
# This file is compared against the config template file that is generated
# for this pipeline. If the two files are identical, then the user has not
# broken the config file. It has the correct modules, variables, etc.
# All they have done is fill in the values.
# If, for example, the user accidently removes a variable or module,
# this function will find the discrepancy.
# If the user does not fill out a required variable or too many exclusives,
# or not enough exclusives it will return an error value.
def simplify(config_file_path, output_file_name):
    # These "to-ignore" key words are those that are not
    # variables. We have currently have:
    # Exclusive: Those groups of variables that
    # should only have one variable filled.
    # Optional: Those variables that don't need to be filled out for the
    # pipeline to run.
    # If you come up with a different 'type' of argument like those,
    # then you should add it to the to_ignore list.
    to_ignore = ['exclusive', 'optionals']

    with open(config_file_path) as fh:
        dictionary = yaml.load(fh, Loader=yaml.Loader)

    # Loops through data in config file.
    for modules in dictionary['modules']:
        for arguments in modules.get('arguments', []):
            # Check that all required arguments have values
            # If they do, delete the value from the file.
            for key in arguments:
                if key not in to_ignore:
                    if (arguments[key] is None):
                        return 1
                    else:
                        arguments[key] = None
            # Check that only one exclusive argument has a value.
            # If it does, delete the value from the file.
            if 'exclusive' in arguments:
                exclusivity_test = False
                for exclusives in arguments.get('exclusive', []):
                    for key in exclusives:
                        # This exclusivity test makes sure that:
                        # One, and only one argument is filled in.
                        if (exclusives[key] is None):
                            pass
                        elif (exclusivity_test):
                            return 2
                        else:
                            exclusivity_test = True
                            exclusives[key] = None
                if (not exclusivity_test):
                    return 3
        # If an optional argument has a value, delete the value from the file.
        for optionals in modules.get('optionals', []):
            for key in optionals:
                if key not in to_ignore:
                    optionals[key] = None
            # If optional exclusive, check that either no value was given
            # or only one value is given. Delete the value from the file.
            if 'exclusive' in optionals:
                exclusivity_test = False
                for exclusives in optionals.get('exclusive', []):
                    for key in exclusives:
                        # This exclusivity test makes sure that either:
                        # A - There are no responses or
                        # B - There is only one response.
                        if (exclusives[key] is None):
                            pass
                        elif (exclusivity_test):
                            return 2
                        else:
                            exclusivity_test = True
                            exclusives[key] = None

    def _add_repr(dumper, value):
        return dumper.represent_scalar(u'tag:yaml.org,2002:null', '')

    # Output the temporary file for testing.
    yaml.SafeDumper.add_representer(type(None), _add_repr)
    with open(output_file_name, 'w') as fh:
        yaml.safe_dump(dictionary, fh, default_flow_style=False)
