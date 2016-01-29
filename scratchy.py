#!/usr/bin/python

import os
from datetime import datetime, timedelta
from glob import glob


def cleanup_scratch_files():
    files = glob('/home/ethan/Dropbox/org_files/xscratch*.org')
    now = datetime.now()
    _delta = timedelta(days=3)
    file_count = len(files)
    delete_count = 0
    for f in files[:]:

        filename = os.path.basename(f)
        date_string = filename.strip('xscratch.org')
        dt = datetime.strptime(date_string, '%Y%b%d%H%M%S')
        expiration_date = dt + _delta

        if now > expiration_date:
            os.remove(f)
            delete_count += 1

    remain_count = len(files) - delete_count
    print 'remaining %s' % remain_count
    print 'removed %s' % delete_count

    with open('/home/ethan/scratchy.log', 'a') as f:
        remaining = file_count - delete_count
        f.write('Last run: %s\nFiles removed: %d'
                '\nFiles remaining: %d\n\n' % (now, delete_count, remain_count))

if __name__ == '__main__':
    cleanup_scratch_files()
