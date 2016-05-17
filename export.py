#!/usr/bin/env python2.6
# -*- encoding: utf8 -*-

import sys
import os
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
    lines = []
    current_path = os.path.dirname(os.path.abspath(__file__))
    response = urllib2.urlopen('https://wapi.gogoro.com/tw/api/vm/list')
    data = json.load(response)
    for d in data["data"]:
        locname = json.loads(d["LocName"])
        address = json.loads(d["Address"])
        address = address["List"][1]["Value"].replace(",", u"，")
        if d["State"] == 1:
            state = u"已啟用"
        elif d["State"] == 99:
            state = u"建置中"
        else:
            state = u"建置中(其他狀態%s)" % d["State"]
        lines.append(u"%s,%s,%s,%s,%f,%f" %
            (
             locname["List"][1]["Value"],
             address,
             d["AvailableTime"],
             state,
             d["Latitude"],
             d["Longitude"]
            )
        )
    lines = sorted(lines)
    with codecs.open("%s/gostation-%s.csv"
                     % (current_path, datetime.now().strftime("%Y%m%d")),
                     "w", "utf-8") as fo:
        fo.write(u"站名,地址,營業時間,目前狀態,緯度,經度\r\n")
        fo.write("\r\n".join(lines))
    return 0


if __name__ == '__main__':
    parser = optparse.OptionParser(usage=main.__doc__)
    options, args = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(args))

