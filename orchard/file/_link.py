# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._yaml_file import YAMLFile
from ..module import Module, Argument, Exclusive


class LinkFile(YAMLFile):
    # self.config - used to store configuration data from the link file

    def __init__(self, filepath):
        super().__init__(filepath)
        self._resolve_dependencies()

    # Adds a module to the class's self.modules; generates a temporary
    # self.dependency_map for use in resolve_dependencies() below
    def _add_modules(self, modules):
        self.dependency_map = {}
        for module in modules:
            self.modules.append(Module(module, from_link=True))
            if 'dependencies' in module:
                self.dependency_map[module['name']] = module['dependencies']

    # Adds dependencies to the individual Module class objects in self.modules
    # as defined by self.dependency_map which was generated in add_modules()
    def _resolve_dependencies(self):
        for module in self.modules:
            deps = self.dependency_map.get(module.name)
            if deps:
                for dep in deps:
                    dep_module, = filter(lambda x: x.name == dep, self.modules)
                    module.add_dependency(dep_module)

    def get_module_depth(self, module_name):
        # If it isn't in the map then it is at a level of 1
        if module_name not in self.dependency_map:
            return 1
        else:
            # Else find the depth of the deepest dependency and add 1 to
            # the answer
            depth = 0
            for mod_name in self.dependency_map[module_name]:
                depth = max(depth, self.get_module_depth(mod_name))
            return depth + 1

    # Used by template_config_file() during config file generation
    def _build_dictionary(self, module, key):
        result = []
        for value in getattr(module, key):
            if isinstance(value, Argument):
                result.append({value.name: None})
            elif isinstance(value, Exclusive):
                exc_data = {'exclusive': []}
                for exc_arg in value.arguments:
                    exc_data['exclusive'].append({exc_arg.name: None})
                result.append(exc_data)
        return result

    # Generates a template config file from the class's data
    def template_config_file(self, output_path="config.yaml"):
        data = {'modules': []}
        for module in self.modules:
            module_data = {}

            module_data['name'] = module.name
            module_data['arguments'] = self._build_dictionary(module,
                                                              'arguments')
            if module.optionals:
                module_data['optionals'] = self._build_dictionary(module,
                                                                  'optionals')

            data['modules'].append(module_data)

        self.write(data, output_path)
