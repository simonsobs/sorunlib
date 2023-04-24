import time
import datetime as dt


def wait(target_time):
    """Wait until a specified time.

    Args:
        target_time (str): Time in ISO format and in UTC timezone to wait
            until, i.e. "2015-10-21T07:28:00", "2023-01-01T0:00:00+00:00"

    """
    target = dt.datetime.fromisoformat(target_time)
    TZ = target.tzinfo

    if TZ not in [None, dt.timezone.utc]:
        offset = target.tzinfo.tzname(None)
        raise ValueError(f'Unsupported timezone ({offset}) detected. '
                         + 'Timezone must be UTC.')

    now = dt.datetime.now(TZ)

    assert target > now, f"time {target} is in the past"

    diff = target - now
    print(f"Waiting for {diff.total_seconds()} seconds")
    time.sleep(diff.total_seconds())
