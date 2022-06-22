"""Internal module for shared utilities within sorunlib.

The usual caveats apply, these interfaces might change without notice.

"""


def check_response(response):
    """Check that a response from OCS indicates successful task/process
    completion.

    Args:
        response (ocs.ocs_client.OCSReply): Response from an OCS operation
            call.

    Raises:
        RuntimeError: When task/process has not completed successfully.

    """
    if not response.session['success']:
        error = 'Task failed to complete successfully.\n' + str(response)
        raise RuntimeError(error)
