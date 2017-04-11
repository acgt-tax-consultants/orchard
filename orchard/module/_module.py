# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._argument import Argument, Exclusive


class Module:
    data = None
    optionals = None
    dependencies = []

    def __init__(self, module_data, from_link=False):
        self.name = module_data.get('name')
        self.executable_path = module_data.get('executable_path')

        arguments = module_data.get('arguments')
        if arguments:
            self.arguments = []
            if from_link:
                self._add_link_values(arguments, self.arguments)
            else:
                self._add_config_values(arguments, self.arguments)

        optionals = module_data.get('optionals')
        if optionals:
            self.optionals = []
            if from_link:
                self._add_link_values(optionals, self.optionals)
            else:
                self._add_config_values(optionals, self.optionals)

    def get_command_line_args(self, link_file):
        commands = []
        module_link_data = link_file.get_module_data(self.name)

        for argument in self.arguments:
            argument_link_data = \
                module_link_data.get_argument_data(argument.name)
            if isinstance(argument, Argument):
                if argument_link_data.command:
                    commands.append(argument_link_data.command)
                if not argument.is_flag:
                    commands.append(argument.value)
            elif isinstance(argument, Exclusive):
                selected = argument.get_selected()
                exc_arg_data = argument_link_data.get_argument(selected.name)
                if exc_arg_data.command:
                    commands.append(exc_arg_data.command)
                if exc_arg_data.is_flag is False:
                    commands.append(selected.value)
        return [module_link_data.executable_path, *commands]

    def get_argument_data(self, argument_name):
        try:
            argument, = filter(lambda x: x.name == argument_name,
                               self.arguments)
        except ValueError:
            raise ValueError('Unable to retreive linkage data from link file '
                             'for module: %s.' % argument_name) from None
        return argument

    def add_dependency(self, dependency):
        self.dependencies = self.dependencies or []
        self.dependencies.append(dependency)

    def _add_link_values(self, values, dest):
        for value in values:
            if value.get('exclusive'):
                data = value['exclusive']
                dest.append(Exclusive(data))
            else:
                dest.append(Argument(value))

    def _add_config_values(self, values, dest):
        for value in values:
            (name, val), = value.items()
            if name == 'exclusive':
                vals = []
                for arg in val:
                    (key, value), = arg.items()
                    vals.append({'name': key, 'value': value})
                arg = Exclusive(vals)
            else:
                arg = Argument({'name': name, 'value': val})
            dest.append(arg)

    def __repr__(self):
        return '%s: %s' % (self.name, self.arguments)
