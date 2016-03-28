"""Various helper functions for parsing org files"""

import re
from datetime import datetime

from corgi import CorgiTask, time_fmt

org_date_fmt = '%Y-%m-%d'

def get_org_tasks(filepath):
    """Return a list of tasks in an org file"""
    tasks = []
    with open(filepath) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):

        if "* TODO " in line:
            clean_task = re.sub(r'\**\sTODO\s', '', line)
            task = CorgiTask(clean_task)
            task.deadline = 'unscheduled'
            tasks.append(task)

        if 'DEADLINE: ' in line and "* TODO " in lines[i - 1]:
            deadline_m = re.search(r'\d{4}-\d{2}-\d{2}', line)
            # Set deadline for previous task (which deadline belongs to)
            tasks[-1].deadline = datetime.strptime(deadline_m.group(), time_fmt)

        if 'SCHEDULED: ' in line and "* TODO " in lines[i - 1]:
            sched_m = re.search(r'\d{4}-\d{2}-\d{2}', line)
            # Set scheduled date for previous task (which deadline belongs to)
            tasks[-1].sched = datetime.strptime(sched_m.group(), time_fmt)

    return tasks


def org_timestamp_to_dt(tstamp):
    """Accepts an org-mode timestamp and returns a datetime object"""

    _date, _, _time = tstamp.strip('<>').split(' ')
    _time = _time.split(':')

    dt = datetime.strptime(_date, org_date_fmt)
    dt = dt.replace(hour=int(_time[0]), minute=int(_time[1]))

    return dt

def dt_to_org_timestamp(dt, show_time=False, zero_padded=False):
    """Accepts a datetime object and returns a string org-mode timestamp"""

    _hour = '%-H' if not zero_padded else '%H'

    fmt = org_date_fmt + ' %a'
    if show_time:
        fmt += ' {}:%M'.format(_hour)

    date = dt.strftime(fmt)
    return '<' + date + '>'
