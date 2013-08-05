try:
    import time
    import calendar

    def to_struct_time_local(s):
        return time.localtime(s)

    def to_struct_time_utc(s):
        return time.gmtime(s)

    def from_struct_time_local(s):
        return int(time.mktime(s))

    def from_struct_time_utc(s):
        return int(calendar.timegm(s))

except ImportError:
    pass

try:
    import datetime

    def to_datetime_naive(t):
        return datetime.datetime.fromtimestamp(t)


    def from_datetime_naive(dt):
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0)
        delta = dt - unix_epoch
        return int(delta.total_seconds())

except ImportError:
    pass

try:
    import dateutil.tz
    
    def to_datetime_local(t):
        naive = datetime.datetime.fromtimestamp(t)
        result = naive.replace(tzinfo=dateutil.tz.tzlocal())
        return result

    def to_datetime_utc(t):
        naive = datetime.datetime.utcfromtimestamp(t)
        result = naive.replace(tzinfo=dateutil.tz.tzutc())
        return result

    def from_datetime_local(dt):
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        delta = dt - unix_epoch
        return int(delta.total_seconds())

    def from_datetime_utc(dt):
        unix_epoch = datetime.datetime(1970, 1, 1, 0, 0, 0, tzinfo=dateutil.tz.tzutc())
        delta = dt - unix_epoch
        return int(delta.total_seconds())

        

except ImportError:
    pass

# rfc822  : Tue, 08 Jun 1982 23:11:00 GMT
# iso8601 : 1982-08-06T23:11:00Z
#           1982-09-06T01:11:00+0200
# ctime
# jdn
