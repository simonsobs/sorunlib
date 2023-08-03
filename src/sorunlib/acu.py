import sorunlib as run
from sorunlib._internal import check_response


def move_to(az, el, boresight=None):
    """Move telescope to specified coordinates.

    Args:
        az (float): destination angle for the azimuthal axis
        el (float): destination angle for the elevation axis
        boresight (float, optional): destination angle for boresight rotation
            on SAT platforms

    Raises:
        RuntimeError: If boresight is passed to a non-satp platform.

    """
    # Az/El motion
    resp = run.CLIENTS['acu'].go_to(az=az, el=el)
    check_response(resp)

    # Boresight motion (satp only)
    if boresight is None:
        return

    # Check platform type
    resp = run.CLIENTS['acu'].monitor.status()
    platform = resp.session['data']['PlatformType']
    if platform == "satp":
        resp = run.CLIENTS['acu'].set_boresight(target=boresight)
        check_response(resp)
    else:
        raise RuntimeError(f"Platform type {platform} does not support boresight motion")
