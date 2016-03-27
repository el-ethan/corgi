"""
Methods related to syncing of tasks

"""

import re
from datetime import datetime


def sync_to_taskpaper(tasks):
    """Add all tasks with deadline today or tomorrow to taskpaper file"""
    tagged_tasks = {}

    for task in tasks:
        if task.tags:
            for tag in task.tags:
                with open(tag + '.taskpaper', 'w') as f:
                    f.write(task.taskpaper_task)

    # tomorrow_tasks = []
    # today_tasks = []
    # unsched_tasks = []
    # habits = []

    # today = datetime.now()
    # tomorrow = datetime.now() + timedelta(1)

    # for task in tasks:
    #     if set(task.tags) & set(filter_tags):
    #         continue
    #     if task.sched:
    #         habits.append(task)
    #     elif task.deadline == 'unscheduled':
    #         unsched_tasks.append(task)
    #     elif task.deadline.date() == today.date():
    #         today_tasks.append(task)
    #     elif task.deadline.date() == tomorrow.date():
    #         tomorrow_tasks.append(task)

    # how_many = len(tomorrow_tasks + today_tasks + unsched_tasks)

    # # f = open(taskpaper_file, 'w')

    # f.write(today.strftime(time_fmt + ', %a') + ':' + '\n\n')
    # for task in today_tasks:
    #     f.write(task.task + '\t' + ' '.join(task.tags) + '\n')

    # f.write(tomorrow.strftime(time_fmt + ', %a') + ':' + '\n\n')
    # for task in tomorrow_tasks:
    #     f.write(task.task + '\t' + ' '.join(task.tags) + '\n')

    # f.write('Unscheduled tasks:\n\n')
    # for task in unsched_tasks:
    #     f.write(task.task + '\t' + ' '.join(task.tags) + '\n')

    # Logger.info('CorgiCapture: tasks synced to taskpaper file: %s' % how_many)
    # Logger.info('CorgiCapture: taskpaper sync complete')

    # f.close()
