import functools
import shutil
import uuid
import yaml

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from pathlib import Path
from planemo import cli
from planemo.training import Training
from ptdk.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash
from zipfile import ZipFile 


tuto = Blueprint('training', __name__)

with open("config.yaml", "r") as stream:
    config = yaml.load(stream, Loader=yaml.FullLoader)


def check_metadata(tuto):
    '''Check the metadata for a tutorial'''
    error = None
    if not tuto['galaxy_url']:
        error = 'Galaxy URL is required.'
    elif not tuto['workflow_id']:
        error = 'Workflow id is required.'
    elif not tuto['name']:
        error = 'Name for tutorial is required.'
    elif tuto['galaxy_url'] not in config:
        error = 'No API key for this Galaxy instance.'
    return error


def generate(tuto):
    '''Generate skeleton of a tutorial'''
    shutil.rmtree('topics', ignore_errors=True)
    shutil.rmtree('metadata', ignore_errors=True)

    kwds = {
        'topic_name': 'topic',
        'topic_title': "New topic",
        'topic_target': "use",
        'topic_summary': "Topic summary",
        'tutorial_name': tuto['name'],
        'tutorial_title': tuto['title'],
        'hands_on': True,
        'slides': False,
        'workflow_id': tuto['workflow_id'],
        'zenodo_link': tuto['zenodo'],
        'galaxy_url': tuto['galaxy_url'],
        'galaxy_api_key': tuto['api_key'],
        'workflow': None,
        'datatypes': None
    }
    train = Training(kwds)

    ctx = cli.Context()
    ctx.planemo_directory = "/tmp/planemo-test-workspace"
    train.init_training(ctx)

    zip_fn = "%s" % (tuto['uuid'])
    dir_path = Path("topics") / Path("topic") / Path("tutorials") / Path("%s" % tuto['name'])
    shutil.make_archive(Path(zip_fn), 'zip', dir_path)

    zip_fp = Path('static') / Path("%s.zip" % zip_fn)
    shutil.move("%s.zip" % zip_fn, Path('ptdk') / zip_fp)

    shutil.rmtree('topics', ignore_errors=True)
    shutil.rmtree('metadata', ignore_errors=True)

    return zip_fp


@tuto.route('/', methods=('GET','POST'))
def index():
    '''Get tutorial attributes'''
    if request.method == 'POST':
        tuto = {
            'uuid': str(uuid.uuid4())[:8],
            'name': request.form['name'],
            'title': request.form['title'],
            'galaxy_url': request.form['galaxy_url'],
            'workflow_id': request.form['workflow_id'],
            'zenodo': request.form['zenodo']
        }
        error = check_metadata(tuto)

        if error is None:
            db = get_db()
            tuto['api_key'] = config[tuto['galaxy_url']]['api_key']
            tuto['status'] = 'in creation'
            db.execute(
                'INSERT INTO tutorials (uuid, name, title, galaxy_url, workflow_id, zenodo, status) VALUES (?, ?, ?, ?, ?, ?, ?)',
                (tuto['uuid'], tuto['name'], tuto['title'], tuto['galaxy_url'], tuto['workflow_id'], tuto['zenodo'], tuto['status'])
            )
            db.commit()
            zip_fp = generate(tuto)
            return render_template('training/index.html', zip_fp=zip_fp)

        flash(error)

    return render_template('training/index.html')
