from kivy.logger import Logger
from kivy.uix.textinput import TextInput


class EmacsTextInput(TextInput):

	def backward_kill_word(self):

		# TODO: can I split on multiple characters? re.split, right?
		split_on_chars = [' ']

		words = [w for w in self.text.split(' ') if w]
		ending = ' ' if len(words) > 1 else ''
		self.text = ' '.join(words[:-1]) + ending

	def keyboard_on_key_down(self, window, keycode, text, modifiers):
		key, key_str = keycode
		Logger.info('modifier -- key: %s -- %s' % (modifiers, key))

		# Check if M-BACKSPACE was pressed
		if key == 8 and 'alt' in modifiers:
			self.backward_kill_word()

		else:
			super(EmacsTextInput, self).keyboard_on_key_down(window, 
			                                                 keycode, 
			                                                 text, 
			                                                 modifiers)

	def _keyboard_on_key_down(self, window, keycode, text, modifiers):
		"""Override behaviour to control effect of enter key"""
		key, key_str = keycode
		Logger.info('modifier -- key: %s -- %s' % (modifiers, key))

		# Check if M-BACKSPACE was pressed
		if key == 8 and 'alt' in modifiers:
			self.backward_kill_word()

		else:
			super(EmacsTextInput, self)._keyboard_on_key_down(window, 
			                                                 keycode, 
			                                                 text, 
			                                                 modifiers)		
