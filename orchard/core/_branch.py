# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------
import os
from pathlib import Path
from ..file import LogFile


# Returns a path with a branch folder inserted into it, i.e.
# path/to/file.txt -> path/to/branch/file.txt
def insert_branch_into_path(pathstring, branchnum):
    return os.path.join(os.path.dirname(pathstring), str(branchnum),
                        os.path.basename(pathstring))


def branching(config_file, link_file, workspace_path):
    # Get the branchlog file
    work_path = Path(workspace_path) / "branchlog.yaml"
    # If no branchlog file exists then this is a brand new workspace, so
    # make a new logdata file and a new branch folder
    if not work_path.is_file():
        os.makedirs(os.path.join(workspace_path, "1"))
        logdata = LogFile(config_file, True)
        logdata.write(work_path)
        branch_config_struct(config_file, link_file, "1")
        return config_file

    # If we made it this far then a branchlog file already exists, so read it
    logs = LogFile(work_path, False)
    best_branchnum = 0
    branch_matching = []
    for branchnum, branchconfig in LogFile.configs.items():
        # Compare our ConfigFile with each subsequent branch ConfigFile,
        # storing the matching modules and if it is a perfect match
        matching_modules, perfect_branch = config_file.compare(branchconfig,
                                                               link_file)

        # If we found a perfect branch then just update config_file and return;
        # no need to mess around with the logfile since this branch already
        # exists in the logfile
        if perfect_branch:
            branch_config_struct(config_file, link_file, branchnum)
            return config_file

        # Else see if the branch that we found is a better match then our
        # current best match
        if len(matching_modules) > len(branch_matching):
            branch_matching = matching_modules
            best_branchnum = branchnum

    # At this point we have our best branch figured out
    # Add the new branch to our logfile
    new_branchnum = logs.add_branch(config_file)
    # and make a new directory to hold it
    os.makedirs(os.path.join(workspace_path, str(new_branchnum)))
    # Then write out our updated logfile
    logs.write(work_path)

    # For each dynamic path in our modules that match from a previous run
    # we need to generate a symlink to the old dynamic path
    for module in branch_matching:
        for arg in module.get_dynamic_paths(
                link_file.get_module_data(module.name)):
            path = arg.value
            working_path = os.path.join(workspace_path, path)
            oldpath = insert_branch_into_path(working_path, best_branchnum)
            newpath = insert_branch_into_path(working_path, new_branchnum)
            if not os.path.lexists(newpath):
                os.symlink(
                    os.path.relpath(oldpath, os.path.dirname(newpath)),
                    newpath)

    # Once we've generated all of the requisite symlinks we can just update
    # the paths in our ConfigFile and we're done branching
    branch_config_struct(config_file, link_file, new_branchnum)
    return config_file


def branch_config_struct(config_file, link_file, branchnum):
    # Insert our branchnum into all of the dynamic paths of each module
    for module in config_file.modules:
        dyn_paths = module.get_dynamic_paths(
            link_file.get_module_data(module.name))
        for arg in dyn_paths:
            if arg.value is not None:
                arg.value = insert_branch_into_path(arg.value, branchnum)
