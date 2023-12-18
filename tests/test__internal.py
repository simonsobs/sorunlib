import os
import ocs
import pytest

from ocs.ocs_client import OCSReply

from sorunlib._internal import check_response, check_running

from util import create_session as create_unencoded_session

os.environ["OCS_CONFIG_DIR"] = "./test_util/"


def create_session(*args, **kwargs):
    session = create_unencoded_session(*args, **kwargs)
    return session.encoded()


# Very partial mock as we only need the instance_id to exist.
class MockClient:
    def __init__(self):
        self.instance_id = 'test-id'


invalid_responses = [(MockClient(), OCSReply(ocs.TIMEOUT,
                                             'msg',
                                             create_session('test', success=True))),
                     (MockClient(), OCSReply(ocs.ERROR,
                                             'msg',
                                             create_session('test', success=False)))]

valid_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', success=True)))]

invalid_running_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test')))]

running_responses = [
    (MockClient(), OCSReply(ocs.OK, 'msg', create_session('test', status='running')))]


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
