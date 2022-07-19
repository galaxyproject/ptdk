import uuid

from ptdk.training import check_metadata, config, generate

import pytest


@pytest.mark.parametrize(('galaxy_url', 'workflow_id', 'name', 'message'), (
    ('', '', '', 'Galaxy URL is required.'),
    ('usegalaxy.eu', '', '', 'Workflow id is required.'),
    ('usegalaxy.eu', '20db0889', '', 'Name for tutorial is required.'),
    (
        'usegalaxy.au',
        '20db0889',
        'name',
        'No API key for this Galaxy instance.'),
))
def test_check_metadata(client, galaxy_url, workflow_id, name, message):
    tuto = {
        'uuid': str(uuid.uuid4())[:8],
        'name': name,
        'title': '',
        'galaxy_url': galaxy_url,
        'workflow_id': workflow_id,
        'zenodo': ''
    }
    response = check_metadata(tuto)
    assert message in response


@pytest.mark.parametrize(('workflow_id', 'message'), (
    ('7ab70660e6235cf', 'specified, unable to decode'),
    ('58660160ca820fcb', 'The workflow is not shared publicly'),
))
def test_generate(client, workflow_id, message):
    tuto = {
        'uuid': str(uuid.uuid4())[:8],
        'name': 'name',
        'title': '',
        'galaxy_url': 'usegalaxy.eu',
        'workflow_id': workflow_id,
        'zenodo': '',
        'api_key': config['usegalaxy.eu']['api_key']
    }
    with pytest.raises(Exception) as e_info:
        response = generate(tuto)
        assert message in e_info


def test_index(client):
    response = client.get('/')
    assert b"Generate skeleton for a new Galaxy tutorial" in response.data
    assert b"Folder name" in response.data
    assert b"Tutorial title" in response.data
    assert b"Galaxy instance with the public workflow" in response.data
    assert b"ID of the workflow" in response.data
    assert b"Zenodo URL with the input data" in response.data

    response = client.post(
        '/',
        data={
            'name': 'metatranscriptomics',
            'title': '',
            'galaxy_url': 'usegalaxy.eu',
            'workflow_id': '7ab70660e6235cf0',
            'zenodo': ''})

    assert b"The skeleton of the tutorial has been generated" in response.data
