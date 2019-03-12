import datetime


def eos_timestamp_to_datetime(timestamp):
    if '.' in timestamp:
        timestamp, timedelta_ms = timestamp.split('.')
    else:
        timedelta_ms = 0

    timestamp = datetime.datetime.strptime(timestamp, '%Y-%m-%dT%H:%M:%S')
    timedelta_ms = datetime.timedelta(milliseconds=int(timedelta_ms))

    return timestamp + timedelta_ms


def datetime_to_eos_timestamp(dt):
    timestamp = dt.strftime('%Y-%m-%dT%H:%M:%S')
    if dt.microsecond:
        timedelta_ms = '{}'.format(int(dt.microsecond / 1000))
        timedelta_ms = timedelta_ms.zfill(3)
        return '{}.{}'.format(timestamp, timedelta_ms)
    return timestamp
