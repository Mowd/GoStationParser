#!/usr/bin/env python2.6
# -*- encoding: utf8 -*-

import sys
import os
import optparse
import urllib2
import json
import codecs
from datetime import datetime


def main(args):
    '''\
    %prog [options]
    '''
    lines = []
    current_path = os.path.dirname(os.path.abspath(__file__))
    response = urllib2.urlopen('https://wapi.gogoro.com/tw/api/vm/construction')
    content = response.read()
    with codecs.open("%s/construction.json" % current_path, "w") as fo:
        fo.write(content)
    data = json.loads(content)
    if data["data"] is not None:
        for d in data["data"]["List"]:
            name = json.loads(d["Name"])
            address = json.loads(d["Address"])
            address = address["List"][1]["Value"].replace(",", u"，")
            start = d["ConstructionStart"]
            end = d["ConstructionEnd"]
            status = d["Status"]
            lines.append(u"%s,%s,%s,%s,%s" %
                (
                 name["List"][1]["Value"],
                 address,
                 start,
                 end,
                 status
                )
            )
    lines = sorted(lines)
    with codecs.open("%s/gostation-maintenance-%s.csv"
                     % (current_path, datetime.now().strftime("%Y%m%d")),
                     "w", "utf-8") as fo:
        fo.write(u"站名,地址,開始時間,結束時間,狀態\r\n")
        fo.write("\r\n".join(lines))
        fo.write("\r\n")
    return 0


if __name__ == '__main__':
    parser = optparse.OptionParser(usage=main.__doc__)
    options, args = parser.parse_args()

    if len(args) != 0:
        parser.print_help()
        sys.exit(1)

    sys.exit(main(args))

