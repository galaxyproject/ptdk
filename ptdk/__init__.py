#!/usr/bin/env python

import os

from flask import Flask

from . import training
from . import git

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    try:
        app.config['GIT_COMMIT'] = git.get_commit_id(BASE_DIR)
        app.config['GIT_COMMIT_SHORT'] = git.get_commit_id(BASE_DIR)[0:8]
    except FileNotFoundError:
        app.config['GIT_COMMIT'] = os.environ.get('GIT_REV', 'main')
        app.config['GIT_COMMIT_SHORT'] = app.config['GIT_COMMIT'][0:8]

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    @app.route("/hello")
    def hello():
        return "Hello, World!"

    app.register_blueprint(training.tuto)
    app.add_url_rule("/", endpoint="index")

    return app


app = create_app()
