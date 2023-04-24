import sorunlib as run
from sorunlib._internal import check_response


def move_to(az, el):
    """Move telescope to specified coordinates.

    Args:
        az (float): destination angle for the azimuthal axis
        el (float): destination angle for the elevation axis

    """
    resp = run.CLIENTS['acu'].go_to(az=az, el=el)
    check_response(resp)
