import bioblend
import os
import shutil
import uuid

from flask import (
    Blueprint, flash, render_template, request
)
from pathlib import Path
from planemo import cli
from planemo.training import Training
from ptdk.db import get_db


tuto = Blueprint('training', __name__)
topic_dp = Path("topics") / "topic" / "tutorials"

config = {
    'usegalaxy.eu': {
        'url': 'https://usegalaxy.eu/',
        'api_key': os.getenv('USEGALAXY_EU_APIKEY') 
    },
    'usegalaxy.org.au': {
        'url': 'https://usegalaxy.org.au/',
        'api_key': os.getenv('USEGALAXY_ORG_AU_APIKEY') 
    },
    'usegalaxy.org': {
        'url': 'https://usegalaxy.org/',
        'api_key': os.getenv('USEGALAXY_ORG_APIKEY') 
    }
}


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

    error = None
    try:
        train.init_training(ctx)
    except bioblend.ConnectionError as connect_error:
        print(connect_error)
        if "Malformed id" in connect_error.body:
            error = (
                "The id of the workflow is malformed "
                "for the given Galaxy instance. "
                "Please check it before trying again.")
        elif "not owned by or shared with current user" in connect_error.body:
            error = (
                "The workflow is not shared publicly "
                "on the given Galaxy instance. "
                "Please share it before trying again.")
        else:
            error = connect_error.body

    tuto_dp = topic_dp / Path("%s" % tuto['name'])
    tuto_fp = tuto_dp / Path('tutorial.md')

    if error is None and not tuto_fp.is_file():
        error = (
            "The tutorial file was not generated. "
            "The workflow may have some errors. "
            "Please check it before trying again.")

    if error is None:
        zip_fn = "%s" % (tuto['uuid'])
        shutil.make_archive(Path(zip_fn), 'zip', tuto_dp)

        zip_fp = Path('static') / Path("%s.zip" % zip_fn)
        shutil.move("%s.zip" % zip_fn, Path('ptdk') / zip_fp)

        shutil.rmtree('topics', ignore_errors=True)
        shutil.rmtree('metadata', ignore_errors=True)

        return zip_fp

    return error


@tuto.route('/', methods=('GET', 'POST'))
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
            db.execute(
                ("INSERT INTO tutorials (uuid, name, galaxy_url, workflow_id) "
                    "VALUES (?, ?, ?, ?)"),
                (
                    tuto['uuid'],
                    tuto['name'],
                    tuto['galaxy_url'],
                    tuto['workflow_id'])
            )
            db.commit()
            zip_fp = generate(tuto)
            if ".zip" in str(zip_fp):
                return render_template('training/index.html', zip_fp=zip_fp)
            else:
                error = zip_fp

        flash(error)

    return render_template('training/index.html')
