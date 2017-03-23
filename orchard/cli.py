# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import pkg_resources
import subprocess

import click

from .modules import generate_config_file, validate, generate_luigi

TEMPLATES = pkg_resources.resource_filename('orchard', 'data')


@click.group()
def orchard():
    pass


@orchard.command()
@click.argument('filepath', type=click.Path(exists=True))
def template(filepath):
    if not filepath.endswith('.yaml'):
        click.secho('Invalid filetype, please provide a .yml or .yaml link '
                    'file', fg='red', err=True)
        click.get_current_context().exit(1)

    try:
        generate_config_file(filepath)
    except RuntimeError as e:
        click.secho(str(e), fg='red', err=True)
        click.get_current_context().exit(1)

    click.secho('Successfully wrote config.yaml', fg='green')


@orchard.command()
@click.argument('filename')
@click.argument('task')
def launch(filename, task):
    subprocess.run(['python', filename, task])


@orchard.command()
@click.argument('link_file_path', type=click.Path(exists=True))
@click.argument('config_file_path', type=click.Path(exists=True))
@click.option('-o', '--output', default='out.py')
def build(link_file_path, config_file_path, output):
    if not (link_file_path.endswith('.yaml') or
            config_file_path.endswith('.yaml')):
        click.secho('Invalid filetype, please provide a .yml or .yaml link '
                    'file', fg='red', err=True)
        click.get_current_context().exit(1)
    try:
        validate(link_file_path, config_file_path)
    except RuntimeError as e:
        click.secho(str(e), fg='red', err=True)
        click.get_current_context().exit(1)

    generate_luigi(config_file_path, link_file_path)
