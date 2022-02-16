import sorunlib as run


def move_to(az, el, wait=None):
    """Move telescope to specified coordinates.

    Args:
        az (float): destination angle for the azimuthal axis
        el (float): destination angle for the elevation axis
        wait (float): amount of time to wait for motion to end

    """
    run.CLIENTS['acu'].go_to(az, el, wait)
