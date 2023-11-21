import os
os.environ["OCS_CONFIG_DIR"] = "./test_util/"
os.environ["SORUNLIB_CONFIG"] = "./data/example_config.yaml"

from sorunlib.config import load_config


def test_load_config():
    cfg = load_config("./data/example_config.yaml")
    assert cfg == {'registry': 'registry'}


def test_load_config_from_env():
    cfg = load_config()
    assert cfg == {'registry': 'registry'}
