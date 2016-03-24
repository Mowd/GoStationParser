#!/usr/bin/env python2.6
# -*- encoding: utf8 -*-

import sys
import optparse
import urllib2
import json
import codecs
from datetime import datetime
#reload(sys)
#sys.setdefaultencoding('utf-8')

def main(args):
    '''\
    %prog [options]
    '''
    response = urllib2.urlopen('https://wapi.gogoro.com/tw/api/vm/list')
    data = json.load(response)
    with codecs.open("gostation-%s.csv" % datetime.now().strftime("%Y%m%d"), "w", "utf-8") as fo:
        fo.write(u"站名,地址,營業時間,目前狀態,緯度,經度\r\n")
        for d in data["data"]:
            locname = json.loads(d["LocName"])
            address = json.loads(d["Address"])
            fo.write(u"%s,%s,%s,%s,%f,%f\r\n" %
            (locname["List"][1]["Value"],
             address["List"][1]["Value"],
             d["AvailableTime"],
             d["State"],
             d["Latitude"],
             d["Longitude"]
            ))
    return 0


if __name__ == '__main__':
    parser = optparse.OptionParser(usage=main.__doc__)
    options, args = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(args))

