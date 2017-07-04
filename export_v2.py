#!/usr/bin/env python2.6
# -*- encoding: utf8 -*-

import sys
import os
import optparse
import urllib2
import json
import codecs
from datetime import datetime

def parseTimeByte(he):
    day_list = [u'一', u'二', u'三', u'四', u'五', u'六', u'日', ];
    availday_list = []
    for day in xrange(0, 7):
        h = he[day * 12: day * 12 + 12]
        b = bin(int(h, 16))[2:].zfill(48)
        time_table = []
        for i in xrange(8, 24):
            time_table.append("%02d:00" % i)
            time_table.append("%02d:30" % i)
        for i in xrange(0, 8):
            time_table.append("%02d:00" % i)
            time_table.append("%02d:30" % i)
        availtime_list = []
        start_time = end_time = ""
        for i in xrange(0, 48):
            if start_time == "" and b[i] == "1":
                start_time = time_table[i]
            if start_time != "" and b[i] == "0":
                end_time = time_table[i]
                availtime_list.append("%s ~ %s" % (start_time, end_time))
                start_time = end_time = ""
        if start_time != "" and end_time == "":
            if len(availtime_list) == 0:
                availtime_list.append("24HR")
            else:
                if b[0] == "0":
                    end_time = time_table[0]
                else:
                    tmp = availtime_list[0].split(" ~ ")
                    availtime_list[0] = "%s ~ %s" % (start_time, tmp[1])
        if len(availtime_list) == 0:
            availtime_list.append(u"公休")
        availday_list.append(u"星期%s：%s" % (
                day_list[day],
                u"，".join(availtime_list)
            )
        )
    first = availday_list[0].split(u"：")[1]
    merge = True
    for i in availday_list:
        if first != i.split(u"：")[1]:
            merge = False
            break
    if merge:
        availday_list = [first]
    return availday_list

def main(args):
    '''\
    %prog [options]
    '''
    lines = []
    current_path = os.path.dirname(os.path.abspath(__file__))
    response = urllib2.urlopen('https://webapi.gogoro.com/api/vm/list')
    #response = urllib2.urlopen('https://webapi.gogoro.com/api/opencharger/list')
    data = json.load(response)
    for d in data:
        locname = json.loads(d["LocName"])
        address = json.loads(d["Address"])
        address = address["List"][1]["Value"].replace(",", u"，")
        state = u"已啟用"
        if "State" in d:
            if d["State"] == 1:
                state = u"已啟用"
            elif d["State"] == 99:
                state = u"建置中"
            else:
                state = u"建置中(其他狀態%s)" % d["State"]
        availday_list = parseTimeByte(d["AvailableTimeByte"])
        lines.append(u"%s,%s,%s,%s,%f,%f,%s" %
            (
             locname["List"][1]["Value"],
             address,
             u"，".join(availday_list),
             state,
             d["Latitude"],
             d["Longitude"],
             d["StorePhoto"][0]
            )
        )
    lines = sorted(lines)
    with codecs.open("%s/gostation-%s.csv"
                     % (current_path, datetime.now().strftime("%Y%m%d")),
                     "w", "utf-8") as fo:
        fo.write(u"站名,地址,營業時間,目前狀態,緯度,經度,gx_media_links\r\n")
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

