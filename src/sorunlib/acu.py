import sorunlib as run
from sorunlib._internal import check_response


def move_to(az, el):
    """Move telescope to specified coordinates.

    Args:
        az (float): destination angle for the azimuthal axis
        el (float): destination angle for the elevation axis

    """
    acu = run.CLIENTS['acu']
    resp = acu.go_to(az=az, el=el)
    check_response(acu, resp)


def set_boresight(target):
    """Move the third axis to a specific target angle.

    Args:
        target (float): destination angle for boresight rotation

    Raises:
        RuntimeError: If boresight is passed to a non-satp platform.

    """
    acu = run.CLIENTS['acu']

    # Check platform type
    resp = acu.monitor.status()
    platform = resp.session['data']['PlatformType']
    if platform == "satp":
        resp = acu.set_boresight(target=target)
        check_response(acu, resp)
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
    acu = run.CLIENTS['acu']
    resp = acu.set_scan_params(az_speed=az_speed,
                               az_accel=az_accel,
                               reset=reset)
    check_response(acu, resp)
