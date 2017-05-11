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

import hashlib

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
        fh.write('        return %s\n\n' %
                 module.get_command_line_args(link_file))
        hash_ = hashlib.md5(module.__repr__().encode('utf-8')).hexdigest()

        fh.write('    def on_success(self):\n')
        fh.write('        with self.output().open() as fh:\n')
        fh.write('            fh.write("Done")\n\n')
        fh.write("    def output(self):\n")
        fh.write("        return luigi.LocalTarget('.%s')" % hash_)
        fh.write("\n\n")

    fh.write('class wrapper(luigi.WrapperTask):\n')
    fh.write('    def requires(self):\n')
    fh.write('        return (%s)\n\n' % ', '.join(['%s()' % i.name for i in config_file.modules]))


    fh.write("if __name__ == '__main__':\n")
    fh.write("    luigi.run()\n")
    fh.close()
