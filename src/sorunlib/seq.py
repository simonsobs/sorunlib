import sorunlib as run
from sorunlib._internal import check_response


OP_TIMEOUT = 60


def scan(description, stop_time, width, az_drift=0, tag=None, subtype=None):
    """Run a constant elevation scan, collecting detector data.

    Args:
        description (str): Description of the field/object being scanned.
        stop_time (str): Time in ISO format to scan until, i.e.
            "2022-06-21T15:58:00"
        width (float): Scan width in azimuth. The scan will start at the
            current position and move in the positive azimuth direction.
        az_drift (float): Drift velocity in deg/s, causing scan extrema to move
            accordingly.
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation. Passed through to the smurf stream command.
        subtype (str, optional): Operation subtype used to tag the stream.

    """
    # Enable SMuRF streams
    run.smurf.stream('on', subtype=subtype, tag=tag)

    try:
        # Grab current telescope position
        resp = run.CLIENTS['acu'].monitor.status()
        az = resp.session['data']['StatusDetailed']['Azimuth current position']
        el = resp.session['data']['StatusDetailed']['Elevation current position']

        # Start telescope motion
        # az_speed and az_accel assumed from ACU defaults
        # Can be modified by acu.set_scan_params()
        resp = run.CLIENTS['acu'].generate_scan.start(az_endpoint1=az,
                                                      az_endpoint2=az + width,
                                                      el_endpoint1=el,
                                                      el_endpoint2=el,
                                                      el_speed=0,
                                                      az_drift=az_drift)

        if not resp.session:
            raise Exception(f"Generate Scan failed to start:\n  {resp}")

        # Wait until stop time
        run.commands.wait_until(stop_time)
    finally:
        # Stop motion
        run.CLIENTS['acu'].generate_scan.stop()
        resp = run.CLIENTS['acu'].generate_scan.wait(timeout=OP_TIMEOUT)
        check_response(resp)

        # Stop SMuRF streams
        run.smurf.stream('off')
