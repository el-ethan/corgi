#!/usr/bin/python

import os
from datetime import datetime, timedelta
from glob import glob

from config import org_dir


def cleanup_scratch_files():
    files = glob(org_dir + 'xscratch*.org')
    now = datetime.now()
    _delta = timedelta(days=7)
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

    with open(os.getenv('HOME') + '/scratchy.log', 'a') as f:
        f.write('Last run: %s\nFiles removed: %d'
                '\nFiles remaining: %d\n\n' % (now, delete_count, remain_count))

if __name__ == '__main__':
    cleanup_scratch_files()
