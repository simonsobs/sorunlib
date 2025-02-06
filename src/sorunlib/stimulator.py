import time
import sorunlib as run

ID_SHUTTER = 1


def _open_shutter():
    """Open the shutter of the stimulator"""
    ds = run.CLIENTS['stimulator']['ds378']
    ds.set_relay(relay_number=ID_SHUTTER, on_off=1)
    time.sleep(1)


def _close_shutter():
    """Close the shutter of the stimulator"""
    ds = run.CLIENTS['stimulator']['ds378']
    ds.set_relay(relay_number=ID_SHUTTER, on_off=0)
    time.sleep(1)


def _setup():
    # Open shutter
    _open_shutter()
    time.sleep(1)

    # Acceleration / Decceleration configuration
    blh = run.CLIENTS['stimulator']['blh']
    blh.set_value(accl_time=10)
    blh.set_value(decl_time=10)


def _stop():
    blh = run.CLIENTS['stimulator']['blh']

    # Stop rotation
    blh.stop_rotation()
    time.sleep(10)

    # Close shutter
    _close_shutter()


def calibrate_tau(duration_step=10,
                  speeds_rpm=[225, 495, 945, 1395, 1845, 2205],
                  forward=True, do_setup=True, stop=True):
    """Time constant calibration using the stimulator.

    Parameters
    ----------
    duration_step : float, optional
        Duration of each step of time constant measurement in sec, default to 10 sec.
    speeds_rpm : list of float, default [225, 495, 945, 1395, 1845, 2205].
        List of chopper rotation speed in RPM for each step.
    forward : bool, default True
        Chopper rotation direction. True for clockwise rotation.
    do_setup : bool, default True
        Do initial setup (i.e. open shutter, set acceleration, start rotation) if True.
    stop : bool, default True
        Stop the rotation and close the shutter if True.
    """

    blh = run.CLIENTS['stimulator']['blh']

    # Replace to the following after the implementation of `downsample_factor` parameter
    # run.smurf.stream('on', tag=f'stimulator, tau, {speeds_rpm}', subtype='cal',
    #                  downsample_factor=1, filter_disable=True)
    run.smurf.stream('on', tag=f'stimulator, tau, {speeds_rpm}', subtype='cal')

    if do_setup:
        _setup()
        # Rotation setting
        blh.set_value(speed=speeds_rpm[0])
        blh.start_rotation(forward)
        speeds_rpm = speeds_rpm[1:]

        # First data point
        time.sleep(duration_step)

    for speed_rpm in speeds_rpm:
        blh.set_value(speed=speed_rpm)
        time.sleep(duration_step)

    if stop:
        _stop()

    run.smurf.stream('off')


def calibrate_gain(duration=60, speed_rpm=90,
                   forward=True, do_setup=True, stop=True):
    """Gain calibration with the stimulator

    Parameters
    ----------
    duration : float, optional
        Duration of the gain calibration in sec, default to 60 sec.
    speed_rpm : float, optional
        Rotation speed of the chopper wheel in RPM, default to 90 RPM.
    forward : bool, default True
        Chopper rotation direction. True for clockwise rotation.
    do_setup : bool, default True
        Do initial setup (i.e. open shutter, set acceleration, start rotation) if True.
    stop : bool, default True
        Stop the rotation and close the shutter if True.
    """
    blh = run.CLIENTS['stimulator']['blh']

    run.smurf.stream('on', tag=f'stimulator, gain, {speed_rpm}', subtype='cal')

    blh.set_value(speed=speed_rpm)

    if do_setup:
        _setup()
        # Rotation setting
        blh.start_rotation(forward)

    # Sleep for rotation stabilization
    time.sleep(10)

    # Data taking
    time.sleep(duration)

    if stop:
        _stop()

    run.smurf.stream('off')
