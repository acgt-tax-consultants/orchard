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


def generate_luigi(config_file, link_file, dest="test.py"):

    fh = open(dest, 'w')

    fh.write('import luigi\n')
    fh.write('from luigi.contrib.external_program'
             ' import ExternalProgramTask\n')
    fh.write('\n\n')

    for module in config_file.modules:
        module_link_data = link_file.get_module_data(module.name)
        fh.write('class ' + module.name + '(ExternalProgramTask):\n')

        if module_link_data.dependencies:
            dependencies = []
            for dependency in module_link_data.dependencies:
                dependencies.append('%s()' % dependency.name)
            fh.write("    def requires(self):\n")
            fh.write("        return %s\n\n" % ', '.join(dependencies))

        fh.write('    def program_args(self):\n')
        fh.write('        return %s\n' %
                 module.get_command_line_args(link_file))

        fh.write("\n")
        fh.write("    def output(self):\n")
        fh.write("        return luigi.LocalTarget(")
        for argument in module.arguments:
            if argument.name == 'outfile':
                fh.write('\'' + argument.value + '\')\n')
        fh.write("\n\n")

    fh.write("if __name__ == '__main__':\n")
    fh.write("    luigi.run()\n")
    fh.close()
