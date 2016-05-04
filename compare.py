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
    last = "data/" + sorted(os.listdir("data"))[-1]
    current = "gostation-%s.csv" % datetime.now().strftime("%Y%m%d")
    os.system("python export.py")
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
            os.rename(current, "data/" + current)
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

