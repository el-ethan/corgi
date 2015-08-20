#!/usr/bin/python
"""corgi (Capture ORG Instantly): a utility for quick capture of notes and 
reminders for org mode.
"""
from kivy.logger import Logger
import os
import sys
import psutil
from ConfigParser import RawConfigParser
from kivy.app import App
from kivy.config import Config
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ObjectProperty

config = RawConfigParser()
config.read('/home/ethan/Dropbox/development/corgi/corgi.cfg')

sync_file = config.get('files', 'sync')
org_file = config.get('files', 'org')
prefix = '** TODO '

class Corgi(object):
	
	@property
	def running_emacs(self):
		if 'emacs' in [psutil.Process(p).name() for p in psutil.pids()]:
			return True
		return False
	
	@property
	def sync_tasks(self):
		with open(sync_file) as sf:
			tasks = sf.readlines()
		return [t.strip() for t in tasks if t.strip() != '']
	
	@property
	def confirm_synced(self):
		with open(org_file) as of:
			_of = of.read()
			synced_tasks = [t for t in self.sync_tasks if t in _of]
		if sorted(synced_tasks) == sorted(self.sync_tasks):
			return True
		return False
		
	def sync_to_org(self, sync_only=False):
		should_sync = True if sync_only or not self.running_emacs else False
		if should_sync and self.sync_tasks:
			with open(org_file, 'a') as org_f:
				for task in self.sync_tasks:
					org_f.write(prefix + task + '\n')
			assert self.confirm_synced
			with open(sync_file, 'w+') as f:
				f.write('')
				assert not f.read()
				
			Logger.info('***** Sync completed *****')
			return 
		reason = 'nothing to sync' if not self.sync_tasks else 'Emacs is running'
		Logger.warning('Not synced:%s' % reason)		
		return


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
	if len(sys.argv) > 1 and sys.argv[1] == 'sync':
		c.sync_to_org(sync_only=True)
	else:
		CorgiApp().run()

