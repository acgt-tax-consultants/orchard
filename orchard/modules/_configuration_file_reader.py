import sys
import os
import yaml
import filecmp


def validate(link_file_path, config_file_path):
    # Check that the link file exists
    if (not os.path.isfile(link_file_path)):
        print('The link file: ' + link_file_path +
              ' ,does not exist.')
        sys.exit()

    # Check that the configuration file exists
    if (not os.path.isfile(config_file_path)):
        print('The configuration file: ' +
              config_file_path + ', does not exist.')
        sys.exit()

    # Check that link file path has the correct extension
    if (not link_file_path.split('.')[1] == 'yaml'):
        print('The link file path has the wrong extension.')
        print('\tExpected: \t.yaml')
        print('\tFound: \t\t.' + link_file_path.split('.')[1])
        sys.exit()

    # Check that config file path has the correct extension
    if (not config_file_path.split('.')[1] == 'yaml'):
        print('The configuration file path has',
              'the wrong extension.')
        print('\tExpected: \t.yaml')
        print('\tFound: \t\t.',
              config_file_path.split('.')[1])
        sys.exit()

    print("The files exist and have proper extensions.")

    # Simplify both the link and the config files then compare
    simplify(link_file_path, "linkTest.yaml")
    simplify(config_file_path, "configTest.yaml")

    print("Comparing files")
    sameFile = filecmp.cmp('linkTest.yaml', 'configTest.yaml')
    os.remove("linkTest.yaml")
    os.remove("configTest.yaml")
    if (sameFile):
        print("Files have passed validation")
        return 0
    else:
        print("Files have failed validation")
        return 1


def simplify(link_file_path, output_file_name):
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
                    try:
                        if (arguments['infile']):
                            arguments['infile'] = None
                    except KeyError:
                        pass
                    try:
                        if (arguments['outfile']):
                            arguments['outfile'] = None
                    except KeyError:
                        pass
                    try:
                        if (arguments['digit']):
                            arguments['digit'] = None
                    except KeyError:
                        pass
                    try:
                        arguments[arguments['name']] = None
                        arguments.pop('name')
                    except KeyError:
                        pass
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
    yaml.SafeDumper.add_representer(
         type(None), lambda dumper,
         value: dumper.represent_scalar(
            u'tag:yaml.org,2002:null', ''))
    with open(output_file_name, 'w') as fh:
        yaml.safe_dump(dictionary, fh, default_flow_style=False)


def main(argv):
    validate(argv[0], argv[1])


if __name__ == "__main__":
    # Pass in arguments 1 and 2 from the commandline
    main(sys.argv[1:3])
