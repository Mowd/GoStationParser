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
    summary = []
    try:
        while True:
            res = diff.next()
            if res[0] in ["+", "-"]:
                if res[0] == "+":
                    s = res.split(",")
                    summary.append("%s,%s" % (s[1], s[2]))
                updated = True
                output.append(res.strip())
    except:
        pass
    finally:
        if len(output) > 1:
            for o in output:
                print o
            print "\n\n"
            print "\n".join(summary)
        if updated:
            os.rename(current,
                      os.path.join(current_path, target, current_filename))
        else:
            os.remove(current)

def main(args):
    '''\
    %prog [options]
    '''
    if args[0] == "data":
        process_file("data")
    if args[0] == "maintenance":
        process_file("maintenance")
    return 0

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=main.__doc__)
    options, args = parser.parse_args()

    if len(args) != 1:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(args))

