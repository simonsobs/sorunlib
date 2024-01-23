import sorunlib as run
from sorunlib._internal import check_response, check_started, monitor_process


OP_TIMEOUT = 60


def scan(description, stop_time, width, start_location='edge', az_drift=0, tag=None, subtype=None):
    """Run a constant elevation scan, collecting detector data.

    Args:
        description (str): Description of the field/object being scanned.
        stop_time (str): Time in ISO format to scan until, i.e.
            "2022-06-21T15:58:00"
        width (float): Scan width in azimuth. This is always the full width of
            the scan.
        start_location (str): Either 'edge' or 'center'. In either case, the
            scan starts from the current position. If 'edge' the starting
            position is taken to be the far left edge of the scan. If 'center'
            the starting position is taken to be the center of the scan, with
            the first leg being a half-width motion to the right.
        az_drift (float): Drift velocity in deg/s, causing scan extrema to move
            accordingly.
        tag (str, optional): Tag or comma-separated listed of tags to attach to
            the operation. Passed through to the smurf stream command.
        subtype (str, optional): Operation subtype used to tag the stream.

    """
    acu = run.CLIENTS['acu']

    # Enable SMuRF streams
    run.smurf.stream('on', subtype=subtype, tag=tag)

    try:
        # Grab current telescope position
        resp = acu.monitor.status()
        az = resp.session['data']['StatusDetailed']['Azimuth current position']
        el = resp.session['data']['StatusDetailed']['Elevation current position']

        # Start telescope motion
        # az_speed and az_accel assumed from ACU defaults
        # Can be modified by acu.set_scan_params()
        if start_location.lower() == 'edge':
            az1 = az
            az2 = az + width
        elif start_location.lower() == 'center':
            az1 = az + width / 2
            az2 = az - width / 2
        else:
            print(f"Unsupported start_location: {start_location}")

        resp = acu.generate_scan.start(az_endpoint1=az1,
                                       az_endpoint2=az2,
                                       el_endpoint1=el,
                                       el_endpoint2=el,
                                       el_speed=0,
                                       az_drift=az_drift)
        check_started(acu, resp)

        # Wait until stop time
        monitor_process(acu, 'generate_scan', stop_time)
    finally:
        print("Stopping scan.")
        # Stop SMuRF streams
        run.smurf.stream('off')

        # Stop motion
        acu.generate_scan.stop()
        resp = acu.generate_scan.wait(timeout=OP_TIMEOUT)
        check_response(acu, resp)
        print("Scan finished.")
