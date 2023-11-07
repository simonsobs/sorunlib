"""Internal module for shared utilities within sorunlib.

The usual caveats apply, these interfaces might change without notice.

"""

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
