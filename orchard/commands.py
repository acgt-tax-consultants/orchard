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

import click
import yaml
import jinja2

TEMPLATES = pkg_resources.resource_filename('orchard', 'data')


def launch(filename, task):
    subprocess.run(['luigi', '--module', filename, task])


def init(filename):
    # Load example config yaml
    with open(os.path.join(TEMPLATES, 'config.template')) as fh:
        context = yaml.load(fh.read())

    # Prepare and render against luigi template
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATES))
    template = env.get_template('luigi.template')
    rendered_content = template.render(**context)

    # Write out luigi code
    with open(filename, 'w') as fh:
        fh.write(rendered_content)

    # Alert user of completion
    click.secho('Successfully wrote luigi file to %s' % filename, fg='green')
