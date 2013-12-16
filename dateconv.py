import re

#
# time.struct_time
#

import time
import calendar

def to_struct_time_local(t):
    return time.localtime(t)

def to_struct_time_utc(t):
    return time.gmtime(t)

def from_struct_time_local(st):
    return int(time.mktime(st))

def from_struct_time_utc(st):
    return int(calendar.timegm(st))

#
# datetime.datetime
#

import datetime

def to_datetime_naive(t):
    return datetime.datetime.fromtimestamp(t)


def from_datetime_naive(dt):
    unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
    delta = dt - unix_epoch
    return int(delta.total_seconds())

#
# datetime.datetime with dateutil.tz
#

try:
    import dateutil.tz
    
    def _du_to_datetime_local(t):
        naive = datetime.datetime.fromtimestamp(t)
        result = naive.replace(tzinfo=dateutil.tz.tzlocal())
        return result

    def _du_to_datetime_utc(t):
        naive = datetime.datetime.utcfromtimestamp(t)
        result = naive.replace(tzinfo=dateutil.tz.tzutc())
        return result

    def _du_from_datetime_local(dt):
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        delta = dt - unix_epoch
        return int(delta.total_seconds())

    def _du_from_datetime_utc(dt):
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        delta = dt - unix_epoch
        return int(delta.total_seconds())

    to_datetime_local   = _du_to_datetime_local
    to_datetime_utc     = _du_to_datetime_utc
    from_datetime_local = _du_from_datetime_local
    from_datetime_utc   = _du_from_datetime_utc

except ImportError:
    pass

#
# datetime.datetime with pytz
#

try:
    import pytz

    def _get_local_timezone():
        with open('/etc/timezone') as f:
            return f.read().strip()
    _local = pytz.timezone(_get_local_timezone())

    def _tz_to_datetime_local(t, tzname=None, tzinfo=None):
        if tzname:
            tzinfo = pytz.timezone(tzname)
        if not tzinfo:
            tzinfo = _local
        return datetime.datetime.utcfromtimestamp(t).replace(tzinfo=pytz.utc).astimezone(tzinfo)

    def _tz_to_datetime_utc(t):
        return datetime.datetime.utcfromtimestamp(t).replace(tzinfo=pytz.utc)

    def _tz_from_datetime_local(dt):
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        delta = dt - unix_epoch
        return int(delta.total_seconds())

    def _tz_from_datetime_utc(dt):
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=pytz.utc)
        delta = dt - unix_epoch
        return int(delta.total_seconds())

    to_datetime_local   = _tz_to_datetime_local
    to_datetime_utc     = _tz_to_datetime_utc
    from_datetime_local = _tz_from_datetime_local
    from_datetime_utc   = _tz_from_datetime_utc

except ImportError:
    pass

#
# ISO-8601
#

def to_iso8601(t):
    st = to_struct_time_utc(t)
    return time.strftime('%Y-%m-%dT%H:%M:%SZ', st)

def from_iso8601(s):
    st = time.strptime(s, '%Y-%m-%dT%H:%M:%SZ')
    return from_struct_time_utc(st)

#
# RFC 822
#

def to_rfc822(t):
    days = 'Mon Tue Wed Thu Fri Sat Sun'.split()
    months = 'Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    dt = to_datetime_utc(t)
    return '{}, {:02} {} {:04} {:02}:{:02}:{:02} GMT'.format(
        days[dt.weekday()], dt.day, months[dt.month - 1], dt.year,
        dt.hour, dt.minute, dt.second)   

def from_rfc822(s):
    months = '_ Jan Feb Mar Apr May Jun Jul Aug Sep Oct Nov Dec'.split()
    match = re.match(r'^[A-Z][a-z][a-z], (\d\d) ([A-Z][a-z][a-z]) (\d\d\d\d) (\d\d):(\d\d):(\d\d) GMT$', s)
    match = match and list(match.groups())
    if match:
        match[1] = months.index(match[1])
        match[0], match[2] = match[2], match[0]
        match = map(int, match)
        iso8601 = '{:04}-{:02}-{:02}T{:02}:{:02}:{:02}Z'.format(*match)
        return from_iso8601(iso8601)
    else:
        raise ValueError('Could not parse date {!r}'.format(s))

#
# pyephem
#

try:
    import ephem

    def to_pyephem(t):
        return ephem.Date((t / 86400.0) + 25567.5)

    def from_pyephem(d):
        return int((d - 25567.5) * 86400)

except ImportError:
    pass

# rfc822  : Tue, 08 Jun 1982 23:11:00 GMT
# iso8601 : 1982-08-06T23:11:00Z
#           1982-09-06T01:11:00+0200
# ctime
# jdn
