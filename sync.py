"""
Methods related to syncing of tasks

"""

from datetime import datetime, timedelta
from collections import defaultdict

from kivy.logger import Logger
from config import *


def sync_to_taskpaper(tasks):
    """Add all tasks with deadline today or tomorrow to taskpaper file"""

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
                with open(tag + '.taskpaper', 'w') as f:
                    f.write(task.taskpaper_task)

    for day, dt in (('today', today), ('tomorrow', tomorrow)):
        with open('%s.taskpaper' % day, 'w') as f:
            f.write(dt.strftime(time_fmt + ', %a') + ':' + '\n\n')
            for task in tasks_dict[day]:
                f.write(task.taskpaper_task)

    # with open('u')
    # for task in unsched_tasks:
    #     f.write(task.task + '\t' + ' '.join(task.tags) + '\n')

    Logger.info('CorgiCapture: tasks synced to taskpaper file: %s' % how_many)
    Logger.info('CorgiCapture: taskpaper sync complete')
