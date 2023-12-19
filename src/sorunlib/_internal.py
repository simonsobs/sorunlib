"""Internal module for shared utilities within sorunlib.

The usual caveats apply, these interfaces might change without notice.

"""

import time

import ocs


def _check_error(client, response):
    """Check if a response is an error or timeout."""
    op = response.session['op_name']
    instance = client.instance_id

    if response.status == ocs.ERROR:
        error = f"Request for Operation {op} in Agent {instance} failed.\n" + \
            str(response)
        raise RuntimeError(error)
    elif response.status == ocs.TIMEOUT:
        error = f"Timeout reached waiting for {op} in Agent {instance} to " + \
            "complete.\n" + str(response)
        raise RuntimeError(error)


def check_response(client, response):
    """Check that a response from OCS indicates successful task/process
    completion.

    Args:
        client (ocs.ocs_client.OCSClient): OCS Client which returned the
            response.
        response (ocs.ocs_client.OCSReply): Response from an OCS operation
            call.

    Raises:
        RuntimeError: When Operation has not completed successfully (either on
            initial request or after completion) or the response has timed out.

    """
    op = response.session['op_name']
    instance = client.instance_id

    _check_error(client, response)

    if not response.session['success']:
        error = f'Task {op} in Agent {instance} failed to complete " + \
            "successfully.\n' + str(response)
        raise RuntimeError(error)


def check_running(client, response):
    """Check that a response from OCS indicates a task/process is still
    running.

    Args:
        client (ocs.ocs_client.OCSClient): OCS Client which returned the
            response.
        response (ocs.ocs_client.OCSReply): Response from an OCS operation
            call.

    Raises:
        RuntimeError: When Operation is not running.

    """
    op = response.session['op_name']
    instance = client.instance_id

    _check_error(client, response)
    if response.session['status'] != 'running':
        error = f"Operation {op} in Agent {instance} is not in the 'running' " + \
                "state.\n" + str(response)
        raise RuntimeError(error)


def check_started(client, response, timeout=60):
    """Check that a process has started and is in the 'running' state. If it
    has not finished starting, wait for timeout seconds for it to start. If
    it is not running by then, raise exception.

    This is meant to be called right after a process' start call is made, to
    ensure that process starts successfully. Use ``check_running()`` if you
    want to check that an already running process is still running.

    Args:
        client (ocs.ocs_client.OCSClient): OCS Client which returned the
            response.
        response (ocs.ocs_client.OCSReply): Response from an OCS operation
            call.
        timeout (float): How long to wait, in seconds, for the operation to go
            from 'starting' to 'running' before raising an exception.

    Raises:
        RuntimeError: When Operation does not properly transition from
            'starting' to 'running' or is not 'running'.

    """
    op = response.session['op_name']
    instance = client.instance_id

    _check_error(client, response)

    op_code = response.session.get('op_code')

    if op_code == 2:  # STARTING
        _operation = client.__getattribute__(op)

        # Wait at most ~timeout seconds while checking the status
        for i in range(timeout):
            response = _operation.status()
            op_code = response.session.get('op_code')
            if op_code == 3:
                # Tricky to change state during testing w/little reward
                return  # pragma: no cover
            time.sleep(1)

        error = f"Check timed out. Operation {op} in Agent {instance} stuck in " + \
                "'starting' state.\n" + str(response)
        raise RuntimeError(error)

    if op_code != 3:  # RUNNING
        error = f"Operation {op} in Agent {instance} is not 'running'.\n" + \
                f"Current OpCode: {op_code}\n" + str(response)
        raise RuntimeError(error)
