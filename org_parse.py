"""Various helper functions for parsing org files"""

import re
from datetime import datetime

from corgi import CorgiTask, time_fmt


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
    """Return a datetime object from a org-mode timestamp string"""

    org_date_fmt = ('%Y-%m-%d')
    _date, _, _time = tstamp.strip('<>').split(' ')
    _time = _time.split(':')

    dt = datetime.strptime(_date, org_date_fmt)
    dt = dt.replace(hour=int(_time[0]), minute=int(_time[1]))

    return dt
