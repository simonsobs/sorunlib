import os
import ocs
import pytest

from unittest.mock import MagicMock, patch
from ocs.ocs_client import OCSReply

from sorunlib._internal import check_response, check_running, check_started

from util import create_session as create_unencoded_session

os.environ["OCS_CONFIG_DIR"] = "./test_util/"


def create_session(*args, **kwargs):
    session = create_unencoded_session(*args, **kwargs)
    return session.encoded()


# Very partial mock as we only need the instance_id to exist.
class MockClient:
    def __init__(self):
        self.instance_id = 'test-id'
        self.test_op = MagicMock()


invalid_responses = [(MockClient(), OCSReply(ocs.TIMEOUT,
                                             'msg',
                                             create_session('test', success=True))),
                     (MockClient(), OCSReply(ocs.ERROR,
                                             'msg',
                                             create_session('test', success=False)))]

valid_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', success=True)))]

invalid_running_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', status='done')))]

running_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', status='running')))]

invalid_starting_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', status='starting')))]


@pytest.mark.parametrize("client,response", invalid_responses)
def test_check_response_raises(client, response):
    with pytest.raises(RuntimeError):
        check_response(client, response)


@pytest.mark.parametrize("client,response", valid_responses)
def test_check_response(client, response):
    check_response(client, response)


@pytest.mark.parametrize("client,response", invalid_running_responses)
def test_check_running_raises(client, response):
    with pytest.raises(RuntimeError):
        check_running(client, response)


@pytest.mark.parametrize("client,response", running_responses)
def test_check_running(client, response):
    check_running(client, response)


@patch('sorunlib._internal.time.sleep', MagicMock())
@pytest.mark.parametrize("client,response", invalid_starting_responses)
def test_check_started_raises_timeout(client, response):
    with pytest.raises(RuntimeError):
        check_started(client, response)


@pytest.mark.parametrize("client,response", invalid_running_responses)
def test_check_started_raises(client, response):
    with pytest.raises(RuntimeError):
        check_started(client, response, timeout=1)


@pytest.mark.parametrize("client,response", running_responses)
def test_check_started(client, response):
    check_started(client, response)
