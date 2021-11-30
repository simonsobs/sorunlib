import os

from unittest.mock import MagicMock, patch

from sorunlib import util

os.environ["OCS_CONFIG_DIR"] = "./test_util/"


def test_load_site_config():
    cfg = util._load_site_config()
    assert 'localhost' in cfg.hosts
    assert 'ocs-docker' in cfg.hosts


def test_find_instances():
    instances = util._find_instances('PysmurfController')
    assert instances == ['pysmurf-controller']


def test_find_instances_host():
    instances = util._find_instances('PysmurfController', host='localhost')
    assert instances == []


@patch('sorunlib.util.OCSClient', MagicMock())
def test_create_clients():
    clients = util.create_clients()
    assert 'acu' in clients
    assert 'smurf' in clients
    assert len(clients['smurf']) == 1
