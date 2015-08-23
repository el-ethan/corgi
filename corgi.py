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
from kivy.logger import Logger
from kivy.uix.textinput import TextInput
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
	def tasks_to_sync(self):
		with open(sync_file) as sf:
			tasks = sf.readlines()
		return [t.strip() for t in tasks if t.strip() != '']
	
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
	if len(sys.argv) > 1 and sys.argv[1] == 'sync':
		c.sync_to_org(sync_only=True)
	else:
		app = CorgiApp()
		app.run()

