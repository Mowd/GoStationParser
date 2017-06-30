#!/usr/bin/env python2.6
# -*- encoding: utf8 -*-

import sys
import os
import optparse
import difflib
from datetime import datetime

def process_file(target):
    if target == "data":
        title = u"GoStation Update"
        script = "export_v2.py"
        current_filename = "gostation-%s.csv" % datetime.now().strftime("%Y%m%d")
    elif target == "maintenance":
        title = u"GoStation Maintenance"
        script = "export_maintenance.py"
        current_filename = "gostation-maintenance-%s.csv" % datetime.now().strftime("%Y%m%d")
    else:
        return
    current_path = os.path.dirname(os.path.abspath(__file__))
    last_filename = sorted(os.listdir(os.path.join(current_path, target)))[-1]
    last = os.path.join(current_path, target, last_filename)
    current = os.path.join(current_path, current_filename)
    os.system("python %s/%s" % (current_path, script))
    diff = difflib.ndiff(open(last).readlines(), open(current).readlines())
    updated = False
    output = [title]
    try:
        while True:
            str = diff.next()
            if str[0] in ["+", "-"]:
                updated = True
                output.append(str)
    except:
        pass
    finally:
        if len(output) > 1:
            for o in output:
                print o
        if updated:
            os.rename(current,
                      os.path.join(current_path, target, current_filename))
        else:
            os.remove(current)

def main(args):
    '''\
    %prog [options]
    '''
    process_file("data")
    process_file("maintenance")
    return 0

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=main.__doc__)
    options, args = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(args))

