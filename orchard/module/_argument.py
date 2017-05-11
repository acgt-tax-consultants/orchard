# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------


# TODO: Merge Argument and Exclusive into one class with a single API
# TODO: Save whether we belong to a config or link file and throw errors if you
# request information from one that belongs in the other (i.e., is_flag is only
# defined in the link file, and will always report "False" if called from the
# config file). Alternatively merge the Config and Link file structures into
# a single structure with all of the data
class Argument:
    # self.command - the command string for this argument
    # self.value - the actual value of this argument
    # self.branchable - the true/false state of the branchable flag
    # self.is_flag - whether or not this argument is a flag
    command = None
    value = None
    branchable = True
    is_flag = False
    is_dyn_path = False

    def __init__(self, data):
        self.name = data.get('name')
        self.command = data.get('command')
        self.value = data.get('value')
        # Optional data flags
        tmp = data.get('is_flag')
        if tmp is True:
            self.is_flag = True
        tmp = data.get('is_branch')
        if tmp is False:
            self.branchable = False
        tmp = data.get('is_dyn_path')
        if tmp is True:
            self.is_dyn_path = True

    def add_value(self, value):
        self.value = value

    # Returns itself if the name matches, else throws a ValueError. Used
    # to provide a matching interface with exclusive; replace when they are
    # merged
    def get_argument(self, argument_name):
        if argument_name != self.name:
            raise ValueError(
                'Error, calling mismatched get_argument'
                ' on: %s' % self.name) from None
        return self

    # Used to provide a matching interface with exclusive; replace upon merging
    def has_name(self, inname):
        return self.name == inname

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
            selected, = filter(lambda x: x.value is not None, self.arguments)
        except ValueError:
            raise ValueError(
                'Error in exclusive value: %s' % self.name)
        return selected

    def has_name(self, inname):
        try:
            self.get_argument(inname)
        except ValueError:
            return False
        return True

    def __repr__(self):
        return self.name
