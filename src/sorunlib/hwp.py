import sorunlib as run
from sorunlib._internal import check_response


# Public API
def set_freq(freq):
    """Set the rotational frequency of the HWP.

    Args:
        freq (float): Target frequency to rotate the HWP in Hz. This is a
            *signed float*, the meaning of which depends on the OCS site
            configuration. For details see the `documentation for the HWP
            Supervisor Agent <docs_>`_.

    .. _docs: https://socs.readthedocs.io/en/main/agents/hwp_supervisor_agent.html

    """
    pass


def stop(active=True):
    """Stop the HWP.

    Args:
        active (bool, optional): If True, actively try to stop the HWP by
            applying the brake. If False, simply turn off the PMX power and let
            it spin down on its own. Defaults to True.

    """
    hwp = run.CLIENTS['hwp']

    if active:
        resp = hwp.brake()
        check_response(hwp, resp)
    else:
        resp = hwp.pmx_off()
        check_response(hwp, resp)
