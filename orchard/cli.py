# ----------------------------------------------------------------------------
# Copyright (c) 2016--, AGCT development team.
#
# Distributed under the terms of the GPLv3 License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import pkg_resources
import subprocess
import shutil

import click
import yaml
import jinja2

TEMPLATES = pkg_resources.resource_filename('orchard', 'data')


@click.group()
def orchard():
    pass


@orchard.command()
@click.argument('filename')
def init(filename):
    if not (filename.endswith('.yml') or filename.endswith('.yaml')):
        filename += '.yml'

    shutil.copy(os.path.join(TEMPLATES, 'config.yml'), filename)

    click.secho('Successfully wrote configuration file to %s' % filename,
                fg='green')


@orchard.command()
@click.argument('filename')
@click.argument('task')
def launch(filename, task):
    subprocess.run(['python', filename, task])


@orchard.command()
@click.argument('config_file')
@click.option('-o', '--output', default='out.py')
def build(config_file, output):
    # Load example config yaml
    with open(config_file) as fh:
        context = yaml.load(fh.read())

    # Prepare and render against luigi template
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES))
    template = env.get_template('luigi.py.j2')
    rendered_content = template.render(**context)

    if not output.endswith('.py'):
        output += '.py'
    # Write out luigi code
    with open(output, 'w') as fh:
        fh.write(rendered_content)

    # Alert user of completion
    click.secho('Successfully wrote luigi file to %s' % output, fg='green')
