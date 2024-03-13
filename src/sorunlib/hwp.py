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
    hwp = run.CLIENTS['hwp']
    resp = hwp.pid_to_freq(target_freq=freq)
    check_response(hwp, resp)


def stop(active=True, brake_voltage=None):
    """Stop the HWP.

    Args:
        active (bool, optional): If True, actively try to stop the HWP by
            applying the brake. If False, simply turn off the PMX power and let
            it spin down on its own. Defaults to True.
        brake_voltage (float, optional): Voltage used when actively stopping
            the HWP. Only considered when active is True.

    """
    hwp = run.CLIENTS['hwp']

    if active:
        if brake_voltage is None:
            resp = hwp.brake()
        else:
            resp = hwp.brake(brake_voltage=brake_voltage)
        check_response(hwp, resp)
    else:
        resp = hwp.pmx_off()
        check_response(hwp, resp)
