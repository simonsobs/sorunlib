import time
import datetime as dt


def wait_until(timestamp, tolerance=None):
    """Wait until a specified time.

    Args:
        timestamp (str): Time in ISO format and in UTC timezone to wait
            until, i.e. "2015-10-21T07:28:00", "2023-01-01T0:00:00+00:00"
        tolerance (int or str): Tolerance on the difference between the time
            when the function is evaluated and `timestamp`. Can be specified as
            a ISO formatted timestamp (str) or in number of seconds (int).

            When evaluated, if `tolerance` (str) is in the past or if the
            difference between the current time and `timestamp` is greater than
            this `tolerance` (int), then an error is raised. If `None`, an
            error will not be raised. Default is `None`.

    Raises:
        ValueError: If `timestamp` has an unsupported timezone, `tolerance`
            is an unsupported type, or if the current time at evaluation is past
            the threshold set by the `tolerance`.

    """
    target = dt.datetime.fromisoformat(timestamp)

    # Determine timezone
    TZ = target.tzinfo
    if TZ not in [None, dt.timezone.utc]:
        offset = target.tzinfo.tzname(None)
        raise ValueError(f'Unsupported timezone ({offset}) detected. '
                         + 'Timezone must be UTC.')

    # Grab current TZ aware timestamp
    now = dt.datetime.now(TZ)

    # Determine "deadline" from tolerance
    if tolerance is None:
        deadline = None
    elif isinstance(tolerance, int):
        deadline = target + dt.timedelta(seconds=tolerance)
    elif isinstance(tolerance, str):
        deadline = dt.datetime.fromisoformat(tolerance)
    else:
        raise ValueError(f"Unsupported type {type(tolerance)} provide for tolerance {tolerance}")

    # Raise error if currently past the "deadline"
    if deadline is None:
        pass
    elif now > deadline:
        raise ValueError(f"Current time ({timestamp}) is past deadline "
                         + f"({deadline.isoformat()}) set by tolerance ({tolerance})")

    # Wait until timestamp
    if target > now:
        duration = (target - now).total_seconds()
    else:
        duration = 0
    print(f"Waiting for {duration} seconds")
    time.sleep(duration)
