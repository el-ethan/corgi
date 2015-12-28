from datetime import datetime


def org_timestamp_to_dt(tstamp):
    date_fmt = ('%Y-%m-%d')
    tstamp = tstamp.strip('<>').split(' ')
    _date = tstamp[0]
    _time = tstamp[2].split(':')
    dt = datetime.strptime(_date, date_fmt)
    dt.replace(hour=_time[0], minute=[1])
    return dt
