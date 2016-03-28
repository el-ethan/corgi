import os
from glob import glob

from datetime import datetime

import pytest

from corgi.org_parse import org_timestamp_to_dt, get_org_tasks, dt_to_org_timestamp
from corgi.sync import sync_to_taskpaper


ORG_FILE_CONTENT = '''
    * TODO task
    * TODO task with deadline
      DEADLINE: <2016-03-31 Thu +1w>
    * TODO task with "home" tag        :home:
    * TODO task with "work" tag        :work:
    '''

def task_in_file(task, filename):
    with open(filename) as f:
        task_list = f.readlines()

    return task in task_list

@pytest.fixture(scope='function')
def test_tasks(request):

    filepath = 'test_org_file.org'

    with open(filepath, 'w') as f:
        f.write(ORG_FILE_CONTENT)

    tasks = get_org_tasks(filepath)

    def finalizer():
        org_files = glob('*.org')
        taskpaper_files = glob('*.taskpaper')
        files = org_files + taskpaper_files
        for _file in files:
            os.remove(_file)

    request.addfinalizer(finalizer)
    return tasks


class TestParser(object):

    def test_org_timestamp_to_dt(self):
        org_timestamp = '<2013-10-06 Sun 1:18>'
        expected_dt = datetime(2013, 10, 6, 1, 18)
        assert org_timestamp_to_dt(org_timestamp) == expected_dt

    def test_dt_to_org_timestamp(self):
        expected_org_timestamp = '<2013-10-06 Sun 1:18>'
        dt = datetime(2013, 10, 6, 1, 18)
        assert dt_to_org_timestamp(dt, show_time=True) == expected_org_timestamp

@pytest.mark.usefixtures('test_tasks')
class TestSyncToTaskpaper(object):

    def test_files_created_by_tag(self, test_tasks):
        files = ('@work.taskpaper', '@home.taskpaper')

        for path in files:
            assert not os.path.exists(path)
        
        sync_to_taskpaper(test_tasks)

        for path in files:
            assert os.path.exists(path)

        assert task_in_file('- task with "work" tag @work\n', files[0])
        assert task_in_file('- task with "home" tag @home\n', files[1])

    def test_today_and_tomorrow_file(self, test_tasks):
        files = ('today.taskpaper', 'tomorrow.taskpaper')
        sync_to_taskpaper(test_tasks)
        for path in files:
            assert os.path.exists(path)

        assert task_in_file('- task for today \n', files[0])
        assert task_in_file('- task for tomorrow \n', files[1])
