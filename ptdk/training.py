import os
import tempfile
import re
import shutil
import uuid
from pathlib import Path

import bioblend

from flask import Blueprint, flash, render_template, request

from planemo import cli
from planemo.training import Training

PTDK_DIRECTORY = os.getcwd()


class PtdkException(Exception):
    pass


tuto = Blueprint("training", __name__)
topic_dp = Path("topics") / "topic" / "tutorials"

config = {
    "usegalaxy.eu": {
        "url": "https://usegalaxy.eu/",
        "api_key": os.getenv("USEGALAXY_EU_APIKEY"),
    },
    "usegalaxy.org.au": {
        "url": "https://usegalaxy.org.au/",
        "api_key": os.getenv("USEGALAXY_ORG_AU_APIKEY"),
    },
    "usegalaxy.org": {
        "url": "https://usegalaxy.org/",
        "api_key": os.getenv("USEGALAXY_ORG_APIKEY"),
    },
    "usegalaxy.fr": {
        "url": "https://usegalaxy.fr/",
        "api_key": os.getenv("USEGALAXY_FR_APIKEY"),
    },
}


def check_metadata(tuto):
    """Check the metadata for a tutorial"""
    error = None
    if not tuto["galaxy_url"]:
        error = "Galaxy URL is required."
    elif not tuto["workflow_id"]:
        error = "Workflow id is required."
    elif not tuto["name"]:
        error = "Name for tutorial is required."
    elif tuto["galaxy_url"] not in config:
        error = "No API key for this Galaxy instance."
    return error


def generate(tuto):
    """Generate skeleton of a tutorial"""
    # Start by setting up a temporary workspace just for this request.
    safe_tutorial_title = re.sub(
        "[^a-z0-9-]*", "", re.sub(" ", "-", tuto["title"].lower())
    )
    kwds = {
        "topic_name": "topic",
        "topic_title": "New topic",
        "topic_target": "use",
        "topic_summary": "Topic summary",
        "tutorial_name": tuto["name"],
        "tutorial_title": tuto["title"],
        "hands_on": True,
        "slides": False,
        "workflow_id": tuto["workflow_id"],
        "zenodo_link": tuto["zenodo"],
        "galaxy_url": tuto["galaxy_url"],
        "galaxy_api_key": tuto["api_key"],
        "workflow": None,
        "datatypes": None,
    }
    train = Training(kwds)

    ctx = cli.PlanemoCliContext()
    ctx.planemo_directory = "/tmp/planemo-test-workspace"

    try:
        train.init_training(ctx)
    except bioblend.ConnectionError as connect_error:
        print(connect_error)
        if "Malformed id" in connect_error.body:
            raise PtdkException(
                "The id of the workflow is malformed "
                "for the given Galaxy instance. "
                "Please check it before trying again."
            ) from connect_error
        if "not owned by or shared with current user" in connect_error.body:
            raise PtdkException(
                "The workflow is not shared publicly "
                "on the given Galaxy instance. "
                "Please share it before trying again."
            ) from connect_error

        raise connect_error

    tuto_dp = topic_dp / Path("%s" % tuto["name"])
    tuto_fp = tuto_dp / Path("tutorial.md")

    if not tuto_fp.is_file():
        raise PtdkException(
            "The tutorial file was not generated. "
            "The workflow may have some errors. "
            "Please check it before trying again."
        )

    zip_fn = f"ptdk-{safe_tutorial_title}-{tuto['workflow_id']}-{tuto['uuid']}"
    shutil.make_archive(Path(zip_fn), "zip", tuto_dp)
    return zip_fn + ".zip"


@tuto.route("/", methods=("GET", "POST"))
def index():
    """Get tutorial attributes"""
    if request.method == "POST":
        tuto_metadata = {
            "uuid": str(uuid.uuid4())[:8],
            "name": request.form["name"],
            "title": request.form["title"],
            "galaxy_url": request.form["galaxy_url"],
            "workflow_id": request.form["workflow_id"],
            "zenodo": request.form["zenodo"],
        }
        print(tuto_metadata)
        error = check_metadata(tuto_metadata)

        if error is not None:
            flash(error)
            return render_template("training/index.html", servers=config.keys())

        tuto_metadata["api_key"] = config[tuto_metadata["galaxy_url"]]["api_key"]
        with tempfile.TemporaryDirectory() as twd:
            output_path = None
            try:
                # Move into the temp directory for maximum safety
                os.chdir(twd)
                # All of the subsequent file generation is done in there.
                # We get back a filename (relative to twd)
                zip_fn = generate(tuto_metadata)

                # Here's where we want the final output to go.
                output_name = Path("static") / Path(zip_fn)
                output_path = Path(PTDK_DIRECTORY) / Path("ptdk") / output_name
                print(zip_fn, output_path)
                shutil.move(Path(twd) / Path(zip_fn), output_path)
            except (PtdkException, bioblend.ConnectionError) as err:
                flash(err)
                return render_template("training/index.html", servers=config.keys())
            finally:
                os.chdir(PTDK_DIRECTORY)

            return render_template("training/index.html", zip_fp=output_name, servers=config.keys())

    return render_template("training/index.html", servers=config.keys())
