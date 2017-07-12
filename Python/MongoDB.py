# coding=utf-8
import pymongo
from pprint import *
import sys, getopt
import xml.dom.minidom
import ssl
import os
import fnmatch

class MongoDB(object):

    def parse_uat_result(self, filename):
        client = pymongo.MongoClient("localhost", 27017)
        db = client.mydb
        cidstatus = []
        xmll = open(filename, 'rU')
        xmldoc = xml.dom.minidom.parse(xmll)
        testlist = xmldoc.getElementsByTagName('test')
        for test in testlist:
        # tags = test.getElementsByTagName('tag')
        # for tag in tags:
        #     cid_str = tag.firstChild.nodeValue
        #     if cid_str[:5] == "CID:C":
        #         cid = cid_str[5:]
        #         status = test.getElementsByTagName('status')
        #         cidstatus[cid] = '1' if status[-1].attributes['status'].value == "PASS" else '5'
            name = test.getAttribute("name")
            TagStatus = test.getElementsByTagName('status')[-1]
            status = TagStatus.getAttribute("status")
            starttime = TagStatus.getAttribute("starttime")
            endtime = TagStatus.getAttribute("endtime")
            cidstatus.append({"Test Name": name, "Test Status": status, "StartTime": starttime, "EndTime": endtime})
        for x in cidstatus:
            db.TestCase.insert(x)
        for data in db.TestCase.find().sort('StartTime', pymongo.ASCENDING):
            print data


MongoDB().parse_uat_result('output.xml')
#MongoDB().abc('123')






