import datetime
from dateutil import tz

def timestamp_from_webkit(webkit_timestamp):
    epoch_start = datetime.datetime(1601,1,1)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    date = epoch_start + delta
    return int(date.replace(microsecond=0).timestamp())

def date_to_webkit(date_string):
    epoch_start = datetime.datetime(1601, 1, 1)
    date_ = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S')
    diff = date_ - epoch_start
    seconds_in_day = 60 * 60 * 24
    return '{:<017d}'.format(
        diff.days * seconds_in_day + diff.seconds + diff.microseconds)

def timestamp_to_webkit(UNIX_timestamp):
    epoch_start = datetime.datetime(1601, 1, 1)
    date_ = datetime.datetime.fromtimestamp(UNIX_timestamp)
    diff = date_ - epoch_start
    seconds_in_day = 60 * 60 * 24
    return '{:<017d}'.format(
        diff.days * seconds_in_day + diff.seconds + diff.microseconds)


def timestamp_from_MediumDate(date_string = "2019-08-23 4:50 pm"):
    medium_Time_Format = "%Y-%m-%d %H:%M %p"
    date = datetime.datetime.strptime(date_string, medium_Time_Format)
    return int(date.timestamp())

    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    utc = date.replace(tzinfo=from_zone)
    local = utc.astimezone(to_zone)   # Convert to local Time
    print("Naive: ", date, "|", date.timestamp(), "|", datetime.datetime.fromtimestamp(date.timestamp()))
    print("UTC__: ", utc, "|", utc.timestamp(), "|", datetime.datetime.fromtimestamp(utc.timestamp()))
    print("Local: ", local, "|", local.timestamp(), "|", datetime.datetime.fromtimestamp(local.timestamp()))
    # return utc.timestamp()


# inTime = int(input("Enter a Webkit timestamp to convert: "))
# timestamp_from_webkit(13211019643868699)
# timestamp_from_MediumDate()
