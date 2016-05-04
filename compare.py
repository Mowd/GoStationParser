#!/usr/bin/env python2.6
# -*- encoding: utf8 -*-

import sys
import os
import optparse
import difflib
from datetime import datetime

def main(args):
    '''\
    %prog [options]
    '''
    current_path = os.path.dirname(os.path.abspath(__file__))
    last_filename = sorted(os.listdir(os.path.join(current_path, "data")))[-1]
    last = os.path.join(current_path, "data", last_filename)
    current_filename = "gostation-%s.csv" % datetime.now().strftime("%Y%m%d")
    current = os.path.join(current_path, current_filename)
    os.system("python %s/export.py" % current_path)
    diff = difflib.ndiff(open(current).readlines(), open(last).readlines())
    updated = False
    try:
        while True:
            str = diff.next()
            if str[0] in ["+", "-"]:
                updated = True
                print str
    except:
        pass
    finally:
        if updated:
            os.rename(current,
                      os.path.join(current_path, "data", current_filename))
        else:
            os.remove(current)
    return 0

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=main.__doc__)
    options, args = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(args))

