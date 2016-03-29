import os
from ConfigParser import RawConfigParser

config = RawConfigParser()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config.read(BASE_DIR + '/.corgi')

time_fmt = config.get('formats', 'time')

# Any tags in this list will not show up in mobile task list
filter_tags = config.get('tags', 'ignore').split(',')

# This is where tasks are initially added from mobile and corgi capture
sync_file = config.get('files', 'sync')
# This is the file tasks are synced to and from from
org_file = config.get('files', 'org')
# This is the file where mobile tasks show up
taskpaper_file = config.get('files', 'taskpaper')

corgi_home = config.get('paths', 'corgi_home')

prefixes = {
    'level1': '* TODO ',
    'level2': '** TODO ',
    'level3': '*** TODO '
}

default_prefix = prefixes['level2']
