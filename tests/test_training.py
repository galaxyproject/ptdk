import pytest
from ptdk import g, session
from ptdk.db import get_db



@pytest.mark.parametrize(('galaxy_url', 'workflow_id', 'name', 'message'), (
    ('', '', '', b'Galaxy URL is required.'),
    ('usegalaxy.eu', '', '', b'Workflow id is required.'),
    ('usegalaxy.eu', '20db0889', '', b'Name for tutorial is required.'),
    ('usegalaxy.au', '20db0889', 'name', b'No API key for this Galaxy instance.'),
))
def test_login_validate_input(client, galaxy_url, workflow_id, name, message):
    tuto = {
        'uuid': str(uuid.uuid4())[:8],
        'name': name,
        'title': '',
        'galaxy_url': galaxy_url,
        'workflow_id': workflow_id,
        'zenodo': ''
    }
    response = client.check_metadata(tuto)
    assert message in response.data



def test_index(client):
    response = client.get('/')
    assert b"Generate skeleton for a new Galaxy tutorial" in response.data
    assert b"Tutorial name" in response.data
    assert b"Tutorial title" in response.data
    assert b"Galaxy instance with the public workflow" in response.data
    assert b"Id of the workflow" in response.data
    assert b"Zenodo URL with the input data" in response.data

    response = client.post(
        '/', 
        data={'name': 'metatranscriptomics', 'title': '', 'galaxy_url': 'usegalaxy.eu', 'workflow_id': 'usegalaxy.eu', 'zenodo': ''})
    assert b"The skeleton of the tutorial has been generated" in response.data


