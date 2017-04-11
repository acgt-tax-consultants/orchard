# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


class Argument:
    command = None
    value = None
    branchable = False
    is_flag = False

    def __init__(self, data):
        self.name = data.get('name')
        self.command = data.get('command')
        self.value = data.get('value')
        self.is_flag = data.get('is_flag')
        self.branchable = data.get('is_branch')

    def add_value(self, value):
        self.value = value

    def __repr__(self):
        return self.name


class Exclusive:
    def __init__(self, arguments):
        self._add_arguments(arguments)
        self.name = '(%s)' % ', '.join([arg.name for arg in self.arguments])

    def _add_arguments(self, arguments):
        self.arguments = []
        for argument in arguments:
            arg = Argument(argument)
            if argument.get('value'):
                arg.add_value(argument['value'])
            self.arguments.append(arg)

    def get_argument(self, argument_name):
        try:
            argument, = filter(lambda x: x.name == argument_name,
                               self.arguments)
        except ValueError:
            raise ValueError('No argument %s found in exclusive: %s' %
                             (argument_name, self.name)) from None
        return argument

    def get_selected(self):
        try:
            selected, = filter(lambda x: x.value is True, self.arguments)
        except ValueError:
            raise ValueError(
                'Error in exclusive value: %s' % self.name)
        return selected

    def __repr__(self):
        return self.name
