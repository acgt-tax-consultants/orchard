# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import click
from orchard import commands


@click.group()
def orchard():
    pass


@orchard.command()
@click.argument('filename')
def init(filename):
    commands.init(filename)


@orchard.command()
@click.argument('filename')
@click.argument('task')
def launch(filename, task):
    commands.launch(filename, task)
