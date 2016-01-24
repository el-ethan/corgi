"""
Methods related to syncing of tasks

"""


class CorgiTask(object):
    """A task with a deadline, scheduled date, and a taskpaper-style @tag"""
    def __init__(self, task, deadline=None, sched=None):
        self.deadline = deadline
        self.sched = sched
        # Replace default org-mode tags with taskpaper ones
        tags_and_task = task.split(':')[::-1]
        self.task = tags_and_task.pop()

        self.tags = ['@' + t.strip() for t in tags_and_task if t.strip() != '']


def get_org_tasks():
    """Return a list of tasks in an org file"""
    tasks = []
    with open(org_file) as f:
        lines = f.readlines()

    for i, line in enumerate(lines):

        if "* TODO " in line:
            clean_task = re.sub(r'\**\sTODO\s', '- ', line)
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

def sync_to_taskpaper(tasks):
    """Add all tasks with deadline today or tomorrow to taskpaper file"""
    tomorrow_tasks = []
    today_tasks = []
    unsched_tasks = []
    habits = []

    today = datetime.now()
    tomorrow = datetime.now() + timedelta(1)

    for task in tasks:
        if set(task.tags) & set(filter_tags):
            continue
        if task.sched:
            habits.append(task)
        elif task.deadline == 'unscheduled':
            unsched_tasks.append(task)
        elif task.deadline.date() == today.date():
            today_tasks.append(task)
        elif task.deadline.date() == tomorrow.date():
            tomorrow_tasks.append(task)

    how_many = len(tomorrow_tasks + today_tasks + unsched_tasks)

    f = open(taskpaper_file, 'w')

    f.write(today.strftime(time_fmt + ', %a') + ':' + '\n\n')
    for task in today_tasks:
        f.write(task.task + '\t' + ' '.join(task.tags) + '\n')

    f.write(tomorrow.strftime(time_fmt + ', %a') + ':' + '\n\n')
    for task in tomorrow_tasks:
        f.write(task.task + '\t' + ' '.join(task.tags) + '\n')

    f.write('Unscheduled tasks:\n\n')
    for task in unsched_tasks:
        f.write(task.task + '\t' + ' '.join(task.tags) + '\n')

    Logger.info('CorgiCapture: tasks synced to taskpaper file: %s' % how_many)
    Logger.info('CorgiCapture: taskpaper sync complete')

    f.close()
