import os
from ConfigParser import RawConfigParser

config = RawConfigParser()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

config.read(BASE_DIR + '/.corgi')

time_fmt = config.get('formats', 'time')

# Any tags in this list will not show up in mobile task list
filter_tags = config.get('tags', 'ignore').split(',')

# This is the file tasks are synced to and from from
org_file = config.get('paths', 'org_file')
org_dir = config.get('paths', 'org_dir')
corgi_home = config.get('paths', 'corgi_home')

# This is where tasks are initially added from mobile and corgi capture
sync_file = os.path.join(corgi_home, 'to_sync.txt')

prefixes = {
    'level1': '* TODO ',
    'level2': '** TODO ',
    'level3': '*** TODO '
}

default_prefix = prefixes['level2']
