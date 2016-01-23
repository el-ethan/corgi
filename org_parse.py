"""Various helper functions for parsing org files"""

from datetime import datetime


def org_timestamp_to_dt(tstamp):
    """Return a datetime object from a org-mode timestamp string"""

    org_date_fmt = ('%Y-%m-%d')
    _date, _, _time = tstamp.strip('<>').split(' ')
    _time = _time.split(':')

    dt = datetime.strptime(_date, org_date_fmt)
    dt = dt.replace(hour=int(_time[0]), minute=int(_time[1]))

    return dt
