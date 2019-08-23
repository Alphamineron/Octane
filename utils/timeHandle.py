import datetime

def timestamp_from_webkit(webkit_timestamp):
    """
        Helper function to convert a webkit_timestamp into a UNIX_timestamp
        `TimeZone = UTC`

        # Parameters
        `webkit_timestamp` :  ->  _(int)_

        # Returns
        `UNIX_timestamp` :  -> _(int)_
    """
    epoch_start = datetime.datetime(1601,1,1)
    delta = datetime.timedelta(microseconds=int(webkit_timestamp))
    date = epoch_start + delta
    return int(date.replace(microsecond=0).timestamp())

def timestamp_from_MediumDate(date_string):
    """
        Helper function to convert Medium's Date format into a UNIX_timestamp
        `TimeZone = UTC`

        # Parameters
        `date_string` : "2019-08-23 4:50 pm"  ->  _(str)_

        # Returns
        `UNIX_timestamp` :  -> _(int)_
    """
    medium_Time_Format = "%Y-%m-%d %H:%M %p"
    date = datetime.datetime.strptime(date_string, medium_Time_Format)
    return int(date.timestamp())
