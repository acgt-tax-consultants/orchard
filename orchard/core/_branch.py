# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import yaml
from pathlib import Path
import os


# Gets a named module from a link or config file
def get_module(file_data, name):
    return next(
        (item for item in file_data['modules'] if item['name'] == name),
        None)


# Returns the depth level of a given module based on the link file
def depth_level(link_file_data, module):
    current_depth = 0
    # If there are no dependencies then the depth is obviously 1
    if 'dependencies' in module:
        # Else get the highest depth value from the dependencies and add 1
        for mod_name in module['dependencies']:
            current_depth = max(current_depth, depth_level(link_file_data,
                                get_module(link_file_data, mod_name)))
    return current_depth + 1


# Returns true if an argument causes branching in a link module
def is_branching_arg(link_file_mod, argname):
    for arg in link_file_mod['arguments']:
        if arg['name'] == argname:
            if 'is_branch' in arg and not arg['is_branch']:
                return False
            else:
                return True
    return True


# Goes through a list and returns true if the given argument branches,
#  recursively checking in 'exclusive' blocks
def is_branching_in_list(arglist, name):
    for arg in arglist:
        # Special case: dive deeper if we are in an 'exclusive' block
        if 'exclusive' in arg:
            if not is_branching_in_list(arg['exclusive'], name):
                return False
        # Else just check for 'is_branch' appropriately
        if arg.get('name') == name:
            if 'is_branch' in arg and not arg['is_branch']:
                return False
            else:
                return True
    return True


# Returns true if the arguments and their values match for two given modules
def check_args(module_1, module_2, link_module):
    if 'arguments' in module_1:
        # Because all arguments are required we can simply sort both and
        # iterate through them to check both directions at once
        mod1_args = sorted(module_1['arguments'], key=lambda x: list(x))
        mod2_args = sorted(module_2['arguments'], key=lambda x: list(x))
        if len(mod1_args) != len(mod2_args):
            return False
        for arg1, arg2 in zip(mod1_args, mod2_args):
            if list(arg1) != list(arg2):
                # If the arguments themselves don't match then it means the
                # modules don't match no matter what
                return False
            if list(arg1.values()) != list(arg2.values()):
                # Where if a value doesn't match, then it can still be true if
                # the argument doesn't cause branching
                argname, = arg1.keys()
                if not is_branching_arg(link_module, argname):
                    continue
                return False
    return True


# Returns true if the optional values match for module 1 == module 2.
# An optional that does not cause branching that is present in one module but
# not in the other should still return that the modules match, therefore we
# must do the O(2(n^2)) set of checks here instead of the simple O(n) zip
# method that we did before in check_args() above.
# NOTE: This is a one way check, and will not catch if module 2 != module 1!
def check_optionals(module_1, module_2, link_module):
    if 'optionals' in module_1:
        if 'optionals' not in module_2:
            return False
        # Check the normal optionals
        for arg in module_1['optionals']:
            argname, = arg.keys()
            # If it doesn't cause branching there isn't need to check farther
            if not is_branching_in_list(link_module['optionals'], argname):
                continue
            # Get the matching dictionary entry in the second config structure
            match = next((item for item in module_2['optionals'] if
                          argname in item.keys()), None)
            # If we didn't find a match then they obviously don't match
            if match is None or arg[argname] != match[argname]:
                return False
    return True


# Returns False if the modules do not match, else returns True
def modules_align(module_1, module_2, link_file_data):
    # First make sure we are looking at the same module in both places
    if module_1['name'] != module_2['name']:
        return False
    link_module = get_module(link_file_data, module_1['name'])
    if not check_args(module_1, module_2, link_module):
        return False
    # Check optionals only checks in one direction, so we need to call it twice
    if not check_optionals(module_1, module_2, link_module):
        return False
    if not check_optionals(module_2, module_1, link_module):
        return False
    return True


# Returns a path with a branch folder inserted into it, i.e.
# path/to/file.txt -> path/to/branch/file.txt
def insert_branch_into_path(pathstring, branchnum):
    return os.path.join(os.path.dirname(pathstring), str(branchnum),
                        os.path.basename(pathstring))


# Inserts branches into a folder based on the infile/outfile arguments
# and the dependency depth level of the module
def insert_branch_into_module(module, branchnum, top_level):
    for arg in module['arguments']:
        if 'infile' in arg:
            if not top_level:
                arg['infile'] = insert_branch_into_path(arg['infile'],
                                                        branchnum)
        if 'outfile' in arg:
            arg['outfile'] = insert_branch_into_path(arg['outfile'], branchnum)


# Goes through a config file, inserting branching as needed for each module
def insert_branch_into_config(config_file_data, branchnum, dep_struct):
    for module in config_file_data['modules']:
        insert_branch_into_module(module, branchnum,
                                  module_in_top_level(dep_struct,
                                                      module['name']))


# Build a dependency structure for usage in other function calls
# The structure is divided into depth levels for keys, with each value
# being a matching list of modules at that depth level
def build_dep_struct(link_file_data):
    ret = {}
    for module in link_file_data['modules']:
        depth = depth_level(link_file_data, module)
        if depth not in ret:
            ret[depth] = [module]
        else:
            ret[depth].append(module)
    return ret


# Returns true if a module is at the highest depth level (i.e., the module
# has nothing that it depends on)
def module_in_top_level(dep_struct, mod_name):
    for module in dep_struct[1]:
        if module['name'] == mod_name:
            return True
    return False


# Gets the infile or outfile entry of a module as a string
def get_path(config_module, infile):
    if infile:
        return next(item for item in config_module['arguments'] if
                    list(item.keys())[0] == 'infile')['infile']
    else:
        return next(item for item in config_module['arguments'] if
                    list(item.keys())[0] == 'outfile')['outfile']


# Compares branches with a new config file, finding the previous branch that
# matches the most with the new values to branch off of
def branch_compare(config_file_data, branchconfig, dep_struct, link_file_data):
    matching = []
    for level, modules in dep_struct.items():
        for module in modules:
            branch_comp = get_module(branchconfig, module['name'])
            new_comp = get_module(config_file_data, module['name'])
            if not modules_align(new_comp, branch_comp, link_file_data):
                return matching, False
            matching.append(module['name'])
    return matching, True


# The overall branching function, takes in a config and link file as well
# as a workspace path, building the requisite folder structure if one exists
# and updating the passed config_file_data to meet any new branching
# requirements.
def branching(config_file_data, link_file_data, workspace_path):
    # First build the dependency structure for use in later calls
    dep_struct = build_dep_struct(link_file_data)
    # Get the branchlog file
    work_path = Path(workspace_path) / "branchlog.yaml"
    # If no branchlog file exists then this is a brand new workspace, so
    # make a new logdata file and a new branch folder
    if not work_path.is_file():
        with open(work_path, 'w+') as logfile:
            os.makedirs(os.path.join(workspace_path, "1"))
            logdata = {1: config_file_data}
            yaml.safe_dump(logdata, logfile, default_flow_style=False)
            insert_branch_into_config(config_file_data, 1, dep_struct)
            return

    # If we made it here a branchlog file exists, so read it in
    with open(work_path, 'r') as lg:
        logs = yaml.load(lg.read())
    best_branch = 0
    branch_matching = []
    for branch, branchconfig in logs.items():
        # Find how much of each branch matches the new one
        temp_matching, perfect_branch = branch_compare(config_file_data,
                                                       branchconfig,
                                                       dep_struct,
                                                       link_file_data)
        # If we found a perfect branch then just update our config structure
        # and return; no need to mess around with the logfile since this branch
        # already exists in the log
        if perfect_branch:
            insert_branch_into_config(config_file_data, branch, dep_struct)
            return
        # Else see if the branch that we found matches our new one better than
        # our current best fit matches
        if len(temp_matching) > len(branch_matching):
            branch_matching = temp_matching
            best_branch = branch

    # Calculate the number of our newly created branch
    new_branch = 1
    while new_branch in logs:
        new_branch += 1

    # Make a new directory to hold our new branch
    os.makedirs(os.path.join(workspace_path, str(new_branch)))
    # And insert our new branch config data into the logfile
    logs[new_branch] = config_file_data
    with open(work_path, 'w') as logfile:
        yaml.safe_dump(logs, logfile, default_flow_style=False)
    # For each of our modules that match output/input from a previous run we
    # need to generate a symlink to the old outputs/inputs
    for module_name in branch_matching:
        module = get_module(config_file_data, module_name)
        # Inpaths are only symlinked for modules not at the top level, i.e.,
        # non-generated inputs still pull from outside the data structure
        if not module_in_top_level(dep_struct, module_name):
            inpath = os.path.join(workspace_path, get_path(module, True))
            oldinpath = insert_branch_into_path(inpath, best_branch)
            newinpath = insert_branch_into_path(inpath, new_branch)
            if not os.path.exists(newinpath):
                os.symlink(
                    os.path.relpath(oldinpath, os.path.dirname(newinpath)),
                    newinpath)
        # Outpaths generate symlinks regardless of module depth
        outpath = os.path.join(workspace_path, get_path(module, False))
        oldoutpath = insert_branch_into_path(outpath, best_branch)
        newoutpath = insert_branch_into_path(outpath, new_branch)
        if not os.path.exists(newoutpath):
            os.symlink(
                os.path.relpath(oldoutpath, os.path.dirname(newoutpath)),
                newoutpath)

    # Once we've generated all of the requisite symlinks we can just update
    # the paths in our new config data structure and we're done branching
    insert_branch_into_config(config_file_data, new_branch, dep_struct)

# dat = yaml.load(open("data/BranchingExampleConfig.yaml").read())
# linkdat = yaml.load(open("data/link.yaml").read())
# branching(dat, linkdat, "../OrchardTestStruct")
