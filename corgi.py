#!/usr/bin/python
"""corgi (Capture ORG Instantly): a utility for quick capture of notes and 
reminders for org mode.
"""
import os
import psutil
from ConfigParser import RawConfigParser
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

config = RawConfigParser()
config.read('corgi.cfg')

sync_file = config.get('files', 'sync')
org_file = config.get('files', 'org')
# org_file = 'test_org.org'


class Corgi(object):
	
	@property
	def running_emacs(self):
		if 'emacs' in [psutil.Process(p).name() for p in psutil.pids()]:
			return True
		return False
	
	@property
	def org_tasks(self):
		with open(org_file) as org_f:
			tasks = org_f.readlines()
		return tasks
	
	@property
	def sync_tasks(self):
		with open(sync_file) as sf:
			tasks = sf.readlines()
		return tasks
	
	@property
	def confirm_synced(self):
		overlap = [t for t in self.org_tasks if t in self.sync_tasks]
		if len(overlap) == len(self.sync_tasks):
			return True
		return False
		
	def sync_to_org(self):
		if not self.running_emacs and self.sync_tasks:
			with open(org_file, 'a') as org_f:
				for st in self.sync_tasks:
					org_f.write(st)
			assert self.confirm_synced
			with open(sync_file, 'w+') as f:
				f.write('')
				assert not f.read()
		return


class CaptureBox(BoxLayout):
	task_input = ObjectProperty()
	corgi = Corgi()
	
	def on_submit(self):
		task_target_file = sync_file if self.corgi.running_emacs else org_file
		with open(task_target_file, 'a') as f:
			f.write('\n' + '** TODO ' + self.task_input.text)
		
		self.corgi.sync_to_org()
		

class CorgiApp(App):
	
	def build(self):
		Config.set('graphics', 'width', '700')
		Config.set('graphics', 'height', '50')
		return CaptureBox()


if __name__ == '__main__':
	if not os.path.isfile(sync_file):
		with open(sync_file, 'w+') as f:
			f.write('')
	CorgiApp().run()

