import os
from glob import glob

from datetime import datetime

import pytest

from corgi.org_parse import org_timestamp_to_dt, get_org_tasks
from corgi.sync import sync_to_taskpaper


ORG_FILE_CONTENT = '''
    * TODO task
    * TODO task with deadline
      DEADLINE: <2016-03-31 Thu +1w>
    * TODO task with "home" tag        :home:
    * TODO task with "work" tag        :work:
    '''

@pytest.fixture(scope='function')
def make_test_files(request):
    with open('test_org_file.org', 'w') as f:
        f.write(ORG_FILE_CONTENT)

    def finalizer():
        org_files = glob('*.org')
        taskpaper_files = glob('*.taskpaper')
        files = org_files + taskpaper_files
        for _file in files:
            os.remove(_file)

    request.addfinalizer(finalizer)


class TestParser(object):

    def test_org_timestamp_to_dt(self):
        org_timestamp = '<2013-10-06 Sun 1:18>'
        expected_dt = datetime(2013, 10, 6, 1, 18)
        assert org_timestamp_to_dt(org_timestamp) == expected_dt


@pytest.mark.usefixtures('make_test_files')
class TestSyncToTaskpaper(object):

    def test_files_created_by_tag(self):
        files = ('@work.taskpaper', '@home.taskpaper')

        for path in files:
            assert not os.path.exists(path)
        tasks = get_org_tasks('test_org_file.org')
        sync_to_taskpaper(tasks)

        for path in files:
            assert os.path.exists(path)

        with open(files[0]) as f:
            tasks = f.readlines()
            assert '- task with "work" tag @work\n' in tasks

        with open(files[1]) as f:
            tasks = f.readlines()
            assert '- task with "home" tag @home\n' in tasks
