#!/usr/bin/python
"""corgi (capture org instantly): a utility for quick capture of notes and 
reminders for org mode. 

If passed the commandline argument 'sync' the ui will not open and tasks will 
be synced. You can bind this action to an emacs hook to have your tasks sync 
when before you open your task file in emacs.
"""
import os
import sys
import psutil
from datetime import datetime, timedelta
from kivy.logger import Logger
from kivy.uix.textinput import TextInput
from ConfigParser import RawConfigParser
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty
import re

config = RawConfigParser()
config.read('/home/ethan/Dropbox/development/corgi/corgi.cfg')

sync_file = config.get('files', 'sync')
org_file = config.get('files', 'org')
taskpaper_file = config.get('files', 'taskpaper')
prefix = '** TODO '
time_fmt = config.get('formats', 'time')

class OrgTask:
	
	def __init__(self, task, deadline=None, sched=None):
		self.deadline = deadline
		self.sched = sched
		self.task = re.sub(r':(?P<tag>.*):', '@\g<tag>', task)


class Corgi(object):
	
	@property
	def running_emacs(self):
		if 'emacs' in [psutil.Process(p).name() for p in psutil.pids()]:
			return True
		return False
	
	@property
	def tasks_to_sync(self):
		with open(sync_file) as sf:
			tasks = sf.readlines()
		return [t.strip() for t in tasks if t.strip() != '']
	
	@property
	def org_tasks(self):
		"""Gather all tasks in an org file"""
		tasks = []
		with open(org_file) as f:
			lines = f.readlines()
	
		for i, line in enumerate(lines):
	
			if "* TODO " in line:
				clean_task = re.sub(r'\**\sTODO\s', '- ', line)
				task = OrgTask(clean_task)
				task.deadline = 'unscheduled'
				tasks.append(task)
			
			if 'DEADLINE: ' in line and "* TODO " in lines[i-1]:
				deadline_m = re.search(r'\d{4}-\d{2}-\d{2}', line)
				# Set deadline for previous task (which deadline bleongs to)
				tasks[-1].deadline = datetime.strptime(deadline_m.group(), time_fmt)
	
			if 'SCHEDULED: ' in line and "* TODO " in lines[i-1]:
				sched_m = re.search(r'\d{4}-\d{2}-\d{2}', line)
				# Set scheduled date for previous task (which deadline bleongs to)
				tasks[-1].sched = datetime.strptime(sched_m.group(), time_fmt)
	
		return tasks
		
	@property
	def confirm_synced(self):
		with open(org_file) as org_f:
			_org_f = org_f.read()
			synced_tasks = [t for t in self.tasks_to_sync if t in _org_f]
		if sorted(synced_tasks) == sorted(self.tasks_to_sync):
			return True
		return False

	def sync_to_org(self, sync_only=False):
		should_sync = True if sync_only or not self.running_emacs else False
		if should_sync and self.tasks_to_sync:
			how_many_tasks = len(self.tasks_to_sync)
			with open(org_file, 'a') as org_f:
				for task in self.tasks_to_sync:
					org_f.write(prefix + task + '\n')
			assert self.confirm_synced
			with open(sync_file, 'w+') as f:
				f.write('')
				f.seek(0)
				assert not f.read()
				Logger.info('Corgi: sync file emptied')
			
			Logger.info('Corgi: tasks synced: %s' % how_many_tasks)				
			Logger.info('Corgi: sync completed')
			return 
		
		reason = 'nothing to sync' if not self.tasks_to_sync else 'Emacs is running'
		Logger.warning('Corgi: not synced because %s' % reason)		
		return

	def sync_to_taskpaper(self):
		"""Add all tasks with deadline today or tomorrow to taskpaper file"""
		
		tomorrow_tasks = []
		today_tasks = []
		unsched_tasks = []
		habits = []
		today = datetime.now()
		tomorrow = datetime.now() + timedelta(1)
		
		tasks = self.org_tasks
			
		for task in tasks:
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
			f.write(task.task + '\n')
	
		f.write(tomorrow.strftime(time_fmt + ', %a') + ':' + '\n\n')
		for task in tomorrow_tasks:
			f.write(task.task + '\n')
	
		f.write('Unscheduled tasks:\n\n')
		for task in unsched_tasks:
			f.write(task.task + '\n')
		
		Logger.info('Corgi: tasks synced to taskpaper file: %s' % how_many_tasks)				
		Logger.info('Corgi: taskpaper sync complete')
		
		f.close()
	
class CaptureBox(BoxLayout):
	corgi = Corgi()
	task_input = ObjectProperty()
	
	def on_submit(self):
		inp = self.task_input.text
		if not inp:
			return
		with open(sync_file, 'a') as sf:
			sf.write('\n' + inp)
		self.corgi.sync_to_org()


class CaptureInput(TextInput):
	
	def keyboard_on_key_down(self, window, keycode, text, modifiers):
		key, key_str = keycode
		
		# check if enter (13) and shift are pressed together
		if key == 13 and 'shift' in modifiers:
			self.parent.on_submit()
			self.text = ''
		
		# Check if just enter was pressed (since it is a multiline)
		elif key == 13 and not modifiers:
			self.parent.on_submit()
			app.stop()
		else:
			super(CaptureInput, self).keyboard_on_key_down(window, 
			                                                keycode, 
			                                                text, 
			                                                modifiers)
	# 	For compatability with dev version of kivy
	def _keyboard_on_key_down(self, window, keycode, text, modifiers):
		key, key_str = keycode
		if key == 13 and 'shift' in modifiers:
			self.parent.on_submit()
			self.text = ''
		elif key == 13 and not modifiers:
			self.parent.on_submit()
			app.stop()
		else:
			super(CaptureInput, self)._keyboard_on_key_down(window, 
			                                                keycode, 
			                                                text, 
			                                                modifiers)


class CorgiApp(App):
	
	def build(self):
		Config.set('graphics', 'width', '700')
		Config.set('graphics', 'height', '50')
		return CaptureBox()


if __name__ == '__main__':
	if not os.path.isfile(sync_file):
		with open(sync_file, 'w+') as f:
			f.write('')
	
	c = Corgi()
	
	command_arg = sys.argv[1] if len(sys.argv) > 1 else None
	
	if command_arg == 'orgsync':
		c.sync_to_org(sync_only=True)
	elif command_arg == 'taskpapersync':
		c.sync_to_taskpaper()
	else:
		app = CorgiApp()
		app.run()

