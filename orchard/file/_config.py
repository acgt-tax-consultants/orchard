# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._yaml_file import YAMLFile

from ..module import Module, Argument, Exclusive


class ConfigFile(YAMLFile):
    # If fromfile is true then filedata is a filepath that we open. Else
    # filedata is a dictionary that contains the new ConfigFile's data and
    # we just use it directly
    def __init__(self, filedata, fromfile):
        if fromfile:
            super().__init__(filedata)
        else:
            self.data = filedata
            modules = self.data.get('modules')
            if modules:
                self.modules = []
                self._add_modules(modules)

    # Nothing fancy here, just add our module to self.modules
    def _add_modules(self, modules):
        for module in modules:
            self.modules.append(Module(module))

    def _build_config_dict(self, module, key):
        result = []
        for value in getattr(module, key):
            if isinstance(value, Argument):
                result.append({value.name: value.value})
            elif isinstance(value, Exclusive):
                exc_data = {'exclusive': []}
                for exc_arg in value.arguments:
                    exc_data['exclusive'].append({exc_arg.name: exc_arg.value})
                result.append(exc_data)
        return result

    # Gets the ConfigFile's data structure. This needs to be rebuilt every time
    # in case any of the values contained within their modules/arguments have
    # been updated
    def get_yaml(self):
        data = {'modules': []}
        for module in self.modules:
            module_data = {}

            module_data['name'] = module.name
            module_data['arguments'] = self._build_config_dict(module,
                                                               'arguments')
            if module.optionals:
                module_data['modules'] = self._build_config_dict(module,
                                                                 'optionals')
            data['modules'].append(module_data)

        return data

    def compare(self, config_file, link_file):
        ret = []
        dep_order = {}
        for module in self.modules:
            depth = link_file.get_module_depth(module.name)
            if depth in dep_order:
                dep_order[depth].append(module.name)
            else:
                dep_order[depth] = [module.name]

        # For each module name in ascending depth order
        for depth, mod_names in sorted(dep_order.items()):
            for name in mod_names:
                # Get the matching modules
                try:
                    my_module = self.get_module_data(name)
                    other_module = config_file.get_module_data(name)
                    link_module = link_file.get_module_data(name)
                # Modules didn't match, return our current list of matches
                except ValueError:
                    return ret, False

                # Iterate through each of the arguments in the link file
                for link_arg in link_module.arguments:
                    if isinstance(link_arg, Argument):
                        # Get the matching arguments
                        try:
                            my_arg = my_module.get_argument_data(link_arg.name)
                            other_arg = other_module.get_argument_data(
                                link_arg.name)
                        # One of the args didn't match, so the module didn't
                        # match; return our list of current matches
                        except ValueError:
                            return ret, False

                        # If the arguments don't match return our list of
                        # current matches
                        if not self._compare_arguments(my_arg, other_arg,
                                                       link_arg):
                            return ret, False
                    elif isinstance(link_arg, Exclusive):
                        # Get matching exclusives
                        try:
                            my_exc = my_module.get_argument_or_exclusive(
                                link_arg.name)
                            other_exc = other_module.get_argument_or_exclusive(
                                link_arg.name)
                        except ValueError:
                            return ret, False

                        for link_exc_arg in link_arg.arguments:
                            # Get the matching arguments
                            try:
                                my_exc_arg = my_exc.get_argument(
                                    link_exc_arg.name)
                                other_exc_arg = other_exc.get_argument(
                                    link_exc_arg.name)
                            except ValueError:
                                return ret, False

                            if not self._compare_arguments(my_exc_arg,
                                                           other_exc_arg,
                                                           link_exc_arg):
                                return ret, False

                # This module completely matched, append it to our list of
                # matching modules to return
                ret.append(my_module)

        return ret, True

    def _compare_arguments(self, arg, other_arg, link_arg):
        if not link_arg.branchable:
            return True
        if arg.name != other_arg.name:
            return False
        if arg.value != other_arg.value:
            return False
        return True
