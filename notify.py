#!/usr/bin/env python2.6
# -*- encoding: utf8 -*-

import sys
import optparse
import fileinput
import pycurl
import urllib

def main(args):
    '''\
    %prog [options]
    '''
    station = []
    for line in fileinput.input():
        station.append(line)
    if len(station) > 0:
        if u"GoStation Maintenance" in station[0]:
            title = u"GoStation Maintenance"
        else:
            title = u"GoStation Update"
        c = pycurl.Curl()
        c.setopt(c.URL, 'PATH_TO_URL')
        c.setopt(c.POSTFIELDS, 'title=%s&text=%s' % (urllib.quote(title), urllib.quote("".join(station))))
        c.perform()
        c.close()
    return 0

if __name__ == '__main__':
    parser = optparse.OptionParser(usage=main.__doc__)
    options, args = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(args))

