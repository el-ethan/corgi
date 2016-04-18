#!/usr/bin/python
"""corgi is a simple utility for quick capture to an org-mode file (or any
text file really), and sync between an org file and mobile devices.

Command line options:
- taskpapersync
All tasks scheduled for today or tomorrow get written to `today.taskpaper` and
`tomorrow.taskpaper` respectively, and all tasks with tags will be written to a
file named based on the pattern `@TAG.taskpaper`
- orgsync
Sync all tasks that have accumulated in the sync_file to the org_file

When tasks are saved with corgi, if Emacs is open it will not save to the org
file so as not to risk modifying a file that might already have an open buffer
that is being worked on.

image credit: http://cyodee.deviantart.com/art/Pixel-Frida-421834726
"""
import os
import sys
import psutil

from kivy.app import App
from kivy.config import Config
from kivy.logger import Logger
from kivy.properties import ObjectProperty
from kivy.uix.behaviors import CodeNavigationBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

from parse import get_org_tasks, org_to_taskpaper
from config import corgi_home, sync_file, org_file, default_prefix

# Installed version of Kivy may not yet have EmacsBehavior. Prepare for worst.
try:
    from kivy.uix.behaviors import EmacsBehavior
    _emacs = True
except ImportError:
    _emacs = False


class CorgiCapture(object):

    @property
    def running_emacs_count(self):
        """Count how many instances of Emacs are currently open"""
        return [psutil.Process(p).name() for p in psutil.pids()].count('emacs')

    @property
    def tasks_to_send(self):
        """Return list of tasks to send to the org file"""
        with open(sync_file) as sf:
            tasks = sf.readlines()
        return [t.strip() for t in tasks if t.strip() != '']

    @property
    def confirm_sent(self):
        """Confirm that all tasks from sync_file are also in org_file"""
        with open(org_file) as org_f:
            _org_f = org_f.read()
            synced_tasks = [t for t in self.tasks_to_send if t in _org_f]
        if sorted(synced_tasks) == sorted(self.tasks_to_send):
            return True
        return False

    def sync_to_org(self, sync_only=False):
        """If conditions are right, copy tasks from sync_file to org_file
        and remove contents of sync_file afterwards.
        """

        if self.tasks_to_send and self.running_emacs_count <= 1:
            how_many_tasks = len(self.tasks_to_send)
            with open(org_file, 'a') as org_f:
                for task in self.tasks_to_send:
                    org_f.write(default_prefix + task + '\n')
            assert self.confirm_sent
            with open(sync_file, 'w+') as f:
                f.write('')
                f.seek(0)
                assert not f.read()
                Logger.info('CorgiCapture: sync file emptied')

            Logger.info('CorgiCapture: tasks synced: %s' % how_many_tasks)
            Logger.info('CorgiCapture: sync completed')
            return

        reason = ('nothing to sync' if not self.tasks_to_send
                  else 'Multiple instances of Emacs are running')

        Logger.warning('CorgiCapture: not synced because %s' % reason)
        return


class CaptureBox(BoxLayout):
    """Layout for app"""
    corgi = CorgiCapture()
    task_input = ObjectProperty()

    def on_submit(self):
        """Write contents of TextInput to sync_file"""
        inp = self.task_input.text
        if not inp:
            return
        with open(sync_file, 'a') as sf:
            sf.write('\n' + inp)
        self.corgi.sync_to_org()


class InputBase(EmacsBehavior, CodeNavigationBehavior):
    pass


class CaptureInput(InputBase if _emacs else CodeNavigationBehavior, TextInput):
    """Modified TextInput. Text is submitted on enter and app is stopped.
    If enter modified by shift key, text is submitted, and widget is cleared
    for the next entry.
    """
    def keyboard_on_key_down(self, window, keycode, text, modifiers):
        """Override behaviour to control effect of enter key"""
        key, key_str = keycode
        Logger.info('modifier -- key: %s -- %s' % (modifiers, key))
        Logger.info('cursor index: %s' % (self.cursor_index()))
        # check if enter (13) and shift are pressed together
        if key == 13 and 'shift' in modifiers:
            self.parent.on_submit()
            self.text = ''

        # Check if just enter was pressed (since it is a multiline)
        elif key == 13 and not modifiers:
            self.parent.on_submit()
            app.stop()
        else:
            super(CaptureInput, self).keyboard_on_key_down(
                window, keycode, text, modifiers
            )


class CorgiApp(App):

    def build(self):
        Config.set('graphics', 'width', '700')
        Config.set('graphics', 'height', '50')
        return CaptureBox()


if __name__ == '__main__':
    from glob import glob

    if len(glob(corgi_home + 'to_sync*')) > 1:
        Logger.warning('CorgiCapture: ***MORE THAN ONE SYNC FILE EXISTS, '
                       'RESOLVE MANUALLY***')

    if not os.path.exists(corgi_home):
        os.makedirs(corgi_home)

    if not os.path.isfile(sync_file):
        with open(sync_file, 'w+') as f:
            f.write('')

    c = CorgiCapture()

    command_arg = sys.argv[1] if len(sys.argv) > 1 else None

    if command_arg == 'orgsync':
        c.sync_to_org(sync_only=True)
    elif command_arg == 'taskpapersync':
        tasks = get_org_tasks(org_file)
        org_to_taskpaper(tasks)

    elif not command_arg:
        app = CorgiApp()
        app.run()

    else:
        Logger.warning('Command arg %s not recognized', command_arg)
