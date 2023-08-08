"""Internal module for shared utilities within sorunlib.

The usual caveats apply, these interfaces might change without notice.

"""

import ocs


def check_response(response):
    """Check that a response from OCS indicates successful task/process
    completion.

    Args:
        response (ocs.ocs_client.OCSReply): Response from an OCS operation
            call.

    Raises:
        RuntimeError: When Operation has not completed successfully (either on
            initial request or after completion) or the response has timed out.

    """
    op = response.session['op_name']

    if response.status == ocs.ERROR:
        error = f"Request for Operation {op} failed.\n" + str(response)
        raise RuntimeError(error)
    elif response.status == ocs.TIMEOUT:
        error = f"Timeout reached waiting for {op} to complete." + str(
            response)
        raise RuntimeError(error)

    if not response.session['success']:
        error = 'Task failed to complete successfully.\n' + str(response)
        raise RuntimeError(error)


def check_start(response):
    """Check that a response from OCS indicates successful task/process
    startup.

    Args:
        response (ocs.ocs_client.OCSReply): Response from an OCS operation
            call.

    Raises:
        RuntimeError: When Operation has not started successfully or the
            response has timed out.

    """
    op = response.session['op_name']

    # Do we ever get these from a .start() call?
    if response.status == ocs.ERROR:
        error = f"Request for Operation {op} failed.\n" + str(response)
        raise RuntimeError(error)
    elif response.status == ocs.TIMEOUT:
        error = f"Timeout reached waiting for {op} to complete." + str(
            response)
        raise RuntimeError(error)

    # STARTING, RUNNNING, SUCCEEDED
    if response.session['op_code'] not in [2, 3, 5]:
        error = 'Task failed to start successfully.\n' + str(response)
        raise RuntimeError(error)

    print(response.session['op_code'])
