import sorunlib as run
from sorunlib._internal import check_response


def move_to(az, el):
    """Move telescope to specified coordinates.

    Args:
        az (float): destination angle for the azimuthal axis
        el (float): destination angle for the elevation axis

    """
    # Az/El motion
    resp = run.CLIENTS['acu'].go_to(az=az, el=el)
    check_response(resp)


def set_boresight(target):
    """Move the third axis to a specific target angle.

    Args:
        target (float): destination angle for boresight rotation

    Raises:
        RuntimeError: If boresight is passed to a non-satp platform.

    """
    # Check platform type
    resp = run.CLIENTS['acu'].monitor.status()
    platform = resp.session['data']['PlatformType']
    if platform == "satp":
        resp = run.CLIENTS['acu'].set_boresight(target=target)
        check_response(resp)
    else:
        raise RuntimeError(f"Platform type {platform} does not support boresight motion")


def set_scan_params(az_speed, az_accel, reset=False):
    """Update the default scan parameters, used during :func:`sorunlib.seq.scan`.

    Args:
        az_speed (float, optional): The azimuth scan speed.
        az_accel (float, optional): The (average) azimuth acceleration at
            turn-around.
        reset (bool, optional): If True, reset all params to default values
            before applying any updates passed explicitly here.

    """
    resp = run.CLIENTS['acu'].set_scan_params(az_speed=az_speed,
                                              az_accel=az_accel,
                                              reset=reset)
    check_response(resp)
