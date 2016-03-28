

class CorgiTask(object):
    """A task with a deadline, scheduled date, and a taskpaper-style @tag"""
    def __init__(self, task, deadline=None, sched=None):
        self.deadline = deadline
        self.sched = sched
        # Replace default org-mode tags with taskpaper ones
        tags_and_task = task.split(':')[::-1]
        self.task = tags_and_task.pop().strip()

        self.tags = ['@' + t.strip() for t in tags_and_task if t.strip() != '' and '//' not in t]

    @property
    def taskpaper_task(self):
        task = '- %s' % self.task
        tags = (' ' + ' '.join(self.tags)) if self.tags else ''

        return task + tags + '\n'
