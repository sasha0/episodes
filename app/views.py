from flask import render_template, send_from_directory
from flask.ext.security import current_user
from . import app


@app.route('/')
def main():
    return render_template('index.html', user=current_user)


@app.route('/partials/<template_name>')
def output_partial(template_name):
    return send_from_directory('templates/partials', template_name)
