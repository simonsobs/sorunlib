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
            applying the brake. If False, simply turn off the PMX power and wait
            for it to spin down on its own. Defaults to True.
        brake_voltage (float, optional): Voltage used when actively stopping
            the HWP. Only considered when active is True.

    """
    hwp = run.CLIENTS['hwp']

    print('Stopping HWP and waiting for it to spin down.')
    if active:
        if brake_voltage is None:
            resp = hwp.brake()
        else:
            resp = hwp.brake(brake_voltage=brake_voltage)
        check_response(hwp, resp)
    else:
        resp = hwp.pmx_off(wait_stop=True)
        check_response(hwp, resp)


def get_direction():
    """Return the rotational direction of the HWP.
    If True, it is counter-clockwise (CCW) seen from the sky to window.
    If False, it is clockwise (CW).

    Args:
        None

    .. _docs: https://socs.readthedocs.io/en/main/agents/hwp_supervisor_agent.html

    """
    hwp = run.CLIENTS['hwp']

    resp = hwp.monitor.status()
    pid_direction = resp.session['data']['hwp_state']['pid_direction']
    if pid_direction == 0:
        is_forward = True
    elif pid_direction == 1:
        is_forward = False
    else:
        raise RuntimeError("The HWP direction is unknown. Aborting...")

    forward_is_cw = hwp.forward_is_cw  # TODO: Need to check if this is possible

    if is_forward ^ forward_is_cw:
        return True
    else:
        return False
