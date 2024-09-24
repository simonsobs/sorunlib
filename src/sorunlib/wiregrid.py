import time

import sorunlib as run
from sorunlib._internal import check_response, check_running

EL_DIFF_THRESHOLD = 0.5  # deg diff from target that its ok to run calibration
BORESIGHT_DIFF_THRESHOLD = 0.5  # deg
AGENT_TIMEDIFF_THRESHOLD = 5  # sec
OP_TIMEOUT = 60


# Internal Helper Functions
def _check_process_data(process, last_timestamp):
    """Check the latest timestamp from a process' session.data is recent enough.

    Args:
        process (str): Descriptive name, used in the error message.
        last_timestamp (float): Latest timestamp from the session.data.

    Raises:
        RuntimeError: When the last timestamp was more than
            AGENT_TIMEDIFF_THRESHOLD old.

    """
    try:
        assert ((time.time() - last_timestamp) < AGENT_TIMEDIFF_THRESHOLD)
    except AssertionError:
        error = f"{process} has no updated data. Cannot proceed with " + \
            "wiregrid calibration. Aborting."
        raise RuntimeError(error)


def _verify_temp_response(response, sensor, min_temp):
    """Check temperature above minimum temperation for safe operation of wiregrid.

    Args:
        response (ocs.ocs_client.OCSReply): Client response from the labjack
            acq process.
        sensor (str): Sensor name in the labjack session data, i.e. 'AIN0'.
        min_temp (int, float): Minimum temperature for safe operation in C.

    Raises:
        RuntimeError: When the temperature of sensor below ``min_temp``.

    """
    temp = response.session['data']['data'][sensor]
    try:
        assert (temp > min_temp)
    except AssertionError:
        error = f"Sensor {sensor} reads {temp} C, which is below minimum " + \
            f"temperature of {min_temp} C. Cannot proceed with wiregrid " + \
            "calibration. Aborting"
        raise RuntimeError(error)


def _check_zenith():
    """Checks to see if the telescope is currently pointing at zenith.

    Returns:
        bool: True if the telescope is at zenith, otherwise returns False.

    """
    acu = run.CLIENTS['acu']
    resp = acu.monitor.status()
    el = resp.session['data']['StatusDetailed']['Elevation current position']

    zenith = False
    if (abs(el - 90) < EL_DIFF_THRESHOLD):
        zenith = True

    return zenith


# Calibration Functions
def _check_telescope_position(elevation_check=True, boresight_check=True):
    # Get current telescope position
    acu = run.CLIENTS['acu']
    resp = acu.monitor.status()
    az = resp.session['data']['StatusDetailed']['Azimuth current position']
    el = resp.session['data']['StatusDetailed']['Elevation current position']
    boresight = resp.session['data']['StatusDetailed']['Boresight current position']

    # Check appropriate elevation
    if elevation_check:
        try:
            assert (el > 50 - EL_DIFF_THRESHOLD)
        except AssertionError:
            error = "Telescope not at > 50 deg elevation. Cannot proceed with " + \
                    f"wiregrid calibration in current position ({az}, {el}). " + \
                    "Aborting."
            raise RuntimeError(error)

    # Check boresight angle
    if boresight_check:
        try:
            assert (abs(boresight - 0) < BORESIGHT_DIFF_THRESHOLD)
        except AssertionError:
            error = "Telescope not at 0 deg boresight. Cannot proceed with " + \
                    f"wiregrid calibration in current position ({boresight}). " + \
                    "Aborting."
            raise RuntimeError(error)


def _configure_power(continuous):
    """Configure the KIKUSUI power supply for rotation based on rotation type.

    Args:
        continuous (bool): Configure for continuous rotation or not.

    """
    kikusui = run.CLIENTS['wiregrid']['kikusui']

    resp = kikusui.set_v(volt=12)
    check_response(kikusui, resp)

    cfg = run.config.load_config()
    current = cfg.get('wiregrid_motor_current', 3.0)

    resp = kikusui.set_c(current=current)
    check_response(kikusui, resp)


def _rotate_continuously(duration):
    kikusui = run.CLIENTS['wiregrid']['kikusui']

    # Start rotation
    resp = kikusui.set_on()
    check_response(kikusui, resp)

    # Wait
    time.sleep(duration)

    # Stop rotation
    resp = kikusui.set_off()
    check_response(kikusui, resp)


def _check_motor_on():
    actuator = run.CLIENTS['wiregrid']['actuator']

    # Check motor is on
    resp = actuator.acq.status()
    if resp.session['data']['fields']['motor'] == 1:
        print("Wiregrid motor already on.")
    # Turn on motor if needed
    elif resp.session['data']['fields']['motor'] == 0:
        resp = actuator.motor_on()
        check_response(actuator, resp)
    else:
        raise RuntimeError("Motor state unknown. Aborting...")


def _check_agents_online():
    """Check OCS agents related to the wiregrid are running."""
    actuator = run.CLIENTS['wiregrid']['actuator']
    kikusui = run.CLIENTS['wiregrid']['kikusui']
    encoder = run.CLIENTS['wiregrid']['encoder']
    labjack = run.CLIENTS['wiregrid']['labjack']

    # wiregrid_actuator
    resp = actuator.acq.status()
    last_timestamp = resp.session['data']['timestamp']
    check_running(actuator, resp)
    _check_process_data("Actuator agent", last_timestamp)

    # wiregrid_kikusui
    resp = kikusui.IV_acq.status()
    last_timestamp = resp.session['data']['timestamp']
    check_running(kikusui, resp)
    _check_process_data("Kikusui agent", last_timestamp)

    # wiregrid_encoder
    resp = encoder.acq.status()
    last_timestamp = resp.session['data']['timestamp']
    check_running(encoder, resp)
    _check_process_data("Encoder agent", last_timestamp)

    # labjack
    resp = labjack.acq.status()
    last_timestamp = resp.session['data']['timestamp']
    check_running(labjack, resp)
    _check_process_data("Labjack agent", last_timestamp)

    # encoder data stream
    resp = encoder.acq.status()
    last_timestamp = resp.session['data']['fields']['encoder_data']['last_updated']
    _check_process_data("Encoder BBB", last_timestamp)


def _check_temperature_sensors():
    """Check temperatures within safe range."""
    labjack = run.CLIENTS['wiregrid']['labjack']
    resp = labjack.acq.status()
    # AIN0 > -10 C && AIN1 > -10 C (On the wiregrid)
    _verify_temp_response(resp, 'AIN0C', -10)
    _verify_temp_response(resp, 'AIN1C', -10)
    # AIN2 > 0 C (Inside the electronics enclosure for the gridloader)
    _verify_temp_response(resp, 'AIN2C', 0)


# Public API
def insert():
    """Insert the wiregrid."""
    actuator = run.CLIENTS['wiregrid']['actuator']
    resp = actuator.insert()
    try:
        check_response(actuator, resp)
    except RuntimeError as e:
        error = "Wiregrid insertion failed. Please inspect wiregrid before " + \
                "continuing observations.\n" + str(e)
        raise RuntimeError(error)


def eject():
    """Eject the wiregrid."""
    actuator = run.CLIENTS['wiregrid']['actuator']
    resp = actuator.eject()
    try:
        check_response(actuator, resp)
    except RuntimeError as e:
        error = "Wiregrid eject failed. Please inspect wiregrid before " + \
                "continuing observations.\n" + str(e)
        raise RuntimeError(error)


def rotate(continuous, duration=30, num_laps=1, stopped_time=10.):
    """Rotate the wiregrid.

    Rotation is either continuously for ``duration`` seconds or stepwise for
    ``num_laps``, stopping every 22.5 degrees for ``stopped_time`` seconds.

    This function sets the Kikusui power settings appropriately based on the
    rotation type.

    Args:
        continuous (bool): Rotate the grid continuously if True or not if
            False.
        duration (int, float): Amount of time in seconds to rotate if rotating
            continuously. Defaults to 30 seconds.
        num_laps (int): Number of revolutions if rotating stepwise (i.e.
            ``continuous = False``). Defaults to 1.
        stopped_time (float): Duration of each 22.5 deg step in seconds if
            rotating stepwise. Defaults to 10 seconds.

    """
    kikusui = run.CLIENTS['wiregrid']['kikusui']

    # Configure power settings based on rotation type
    _configure_power(continuous)

    if continuous:
        _rotate_continuously(duration)
    else:
        resp = kikusui.stepwise_rotation(num_laps=num_laps,
                                         stopped_time=stopped_time)
        check_response(kikusui, resp)


def calibrate(continuous=False, elevation_check=True, boresight_check=True,
              temperature_check=True):
    """Run a wiregrid calibration.

    Args:
        continuous (bool): Calibration by continuous rotation or not.
            Default is False, in which the wiregrid rotates step-wisely.
        elevation_check (bool): Check the elevation angle is in an appropriate
            range before the calibration or not. Default is True.
        boresight_check (bool): Check the boresight angle is in an appropriate
            range before the calibration or not. Default is True.
        temperature_check (bool): Check the temperature of various components
            are within operational limits before the calibration or not.
            Default is True.

    """
    try:
        _check_telescope_position(elevation_check=elevation_check,
                                  boresight_check=boresight_check)
        _check_agents_online()
        if temperature_check:
            _check_temperature_sensors()
        _check_motor_on()

        # Rotate for reference before insertion
        rotate(continuous=True, duration=10)

        # Enable SMuRF streams
        if continuous:
            rotation = 'wg_continuous'
        else:
            rotation = 'wg_stepwise'
        if _check_zenith():
            el_tag = ', wg_el90'
        else:
            el_tag = ''
        run.smurf.stream('on', tag=f'wiregrid, {rotation}{el_tag}', subtype='cal')

        # Insert the wiregrid
        insert()

        # Rotate the wiregrid
        rotate(continuous)

        # Eject the wiregrid
        eject()
    finally:
        # Stop SMuRF streams
        run.smurf.stream('off')
