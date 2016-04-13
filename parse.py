"""Various helper functions for parsing org files"""

import os
import re
from datetime import datetime, timedelta
from collections import defaultdict

from kivy.logger import Logger

from task import CorgiTask
from config import time_fmt, filter_tags, corgi_home

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


def org_to_taskpaper(tasks, taskpaper_dir=None):
    """Add all tasks with deadline today or tomorrow to taskpaper file"""

    if not taskpaper_dir:
        taskpaper_dir = corgi_home

    if not os.path.exists(taskpaper_dir):
        os.mkdir(taskpaper_dir)

    tasks_dict = defaultdict(list)
    today = datetime.now()
    tomorrow = datetime.now() + timedelta(1)

    how_many = 0

    for task in tasks:

        how_many += 1

        if set(task.tags) & set(filter_tags):
            continue

        if task.deadline == 'unscheduled':
            tasks_dict['unscheduled'].append(task)
        elif task.deadline.date() == today.date():
            tasks_dict['today'].append(task)
        elif task.deadline.date() == tomorrow.date():
            tasks_dict['tomorrow'].append(task)

        if task.tags:
            for tag in task.tags:
                with open(taskpaper_dir + tag + '.taskpaper', 'a+') as f:
                    if task.taskpaper_task not in f.readlines():
                        f.write(task.taskpaper_task)

    for day, dt in (('today', today), ('tomorrow', tomorrow)):
        with open(taskpaper_dir + '%s.taskpaper' % day, 'w') as f:
            f.write(dt.strftime(time_fmt + ', %a') + ':' + '\n\n')
            for task in tasks_dict[day]:
                f.write(task.taskpaper_task)

    Logger.info('CorgiCapture: tasks synced to taskpaper file: %s' % how_many)
    Logger.info('CorgiCapture: taskpaper sync complete')
