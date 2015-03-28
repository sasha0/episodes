# -*- coding: utf-8 -*-
"""Generic Flask controllers."""

from flask import render_template, send_from_directory
from flask.ext.security import current_user
from . import app


@app.route('/')
def main():
    """Primitive controller to render main page of single-page application."""

    return render_template('index.html', user=current_user)


@app.route('/partials/<template_name>')
def output_partial(template_name):
    """Raw output of templates for single-page application."""

    return send_from_directory('templates/partials', template_name)
