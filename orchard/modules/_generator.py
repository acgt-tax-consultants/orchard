# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
#
# usage: from _generator import generate_luigi
# usage cont: generate_luigi("configfilepath", "linkfilepath")
#
# will generate a luigi file named test.py
# ----------------------------------------------------------------------------

import yaml
import sys


def generate_luigi(inConfig, inLink):

    fh = open('test.py', 'w')

    newconfig = open(inConfig)
    data = yaml.load(newconfig.read())

    link = open(inLink)
    linkData = yaml.load(link.read())
    linkModules = linkData['modules']

    fh.write('import luigi\n')
    fh.write('from luigi.contrib.external_program'
             ' import ExternalProgramTask\n')
    fh.write('\n\n')

    modules = data['modules']

    for module in modules:
        arguments = module['arguments']
        currentModuleName = str(module['name'])

        fh.write('class ' + currentModuleName + '(ExternalProgramTask):\n')
        for linkModule in linkModules:
            if linkModule['name'] == currentModuleName:
                if 'dependencies' in linkModule:
                    currentDependancy = str(linkModule['dependencies'][0])
                    fh.write("    def requires(self):\n")
                    fh.write("        return " + currentDependancy + "()\n\n")

        fh.write('    def program_args(self):\n')
        fh.write('        return [')
        fh.write('\'./' + currentModuleName + '\'')

        # firstArg = True
        for argument in arguments:
            for key in argument:
                # if firstArg:
                #     fh.write('\'' + str(argument[str(key)]) + '\'')
                #     firstArg = False
                # else:
                fh.write(', \'' + str(argument[str(key)]) + '\'')

        fh.write("]\n")
        fh.write("\n")
        fh.write("    def output(self):\n")
        fh.write("        return luigi.LocalTarget(")
        for argument in arguments:
            for key in argument:
                if str(key) == 'outfile':
                    fh.write('\'' + str(argument[str(key)]) + '\')\n')
        fh.write("\n\n")

    fh.write("if __name__ == '__main__':\n")
    fh.write("    luigi.run()\n")
    fh.close()


def main(argv):
    generate_luigi(argv[0], argv[1])


if __name__ == "__main__":
    main(sys.argv[1:3])
