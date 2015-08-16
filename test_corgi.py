from mock import patch, DEFAULT
from corgi import Corgi

class TestCogi:
	
	def test_confirm_sync(self):
		with patch.multiple('main.Corgi', org_tasks=DEFAULT, sync_tasks=DEFAULT):
			corgi = Corgi()
			corgi.sync_tasks = [1, 2]
			corgi.org_tasks = [1, 3, 4]
			assert corgi.confirm_synced is False
			
			corgi.sync_tasks = [1, 2]
			corgi.org_tasks = [1, 2, 3, 4]
			assert corgi.confirm_synced is True
	
	def test_sync_to_org(self):
		pass