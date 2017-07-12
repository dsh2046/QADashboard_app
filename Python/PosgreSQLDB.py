import psycopg2
import os
import xml.dom.minidom
from PostgreSQL_connect import *
from shutil import copy
import os.path
import requests

from poster.encode import multipart_encode
import urllib2
import sys
from urllib2 import Request, urlopen, URLError, HTTPError
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers


class PosgreSQLDB(object):
    pass_amount = 0
    fail_amount = 0
    runname = ''

    def testcase(self, filename):
        cidstatus = []
        xmll = open(filename, 'rU')
        xmldoc = xml.dom.minidom.parse(xmll)
        testlist = xmldoc.getElementsByTagName('test')
        for test in testlist:
            TagStatus = test.getElementsByTagName('status')[-1]
            status = TagStatus.getAttribute("status")
            if(status=="PASS"):
                PosgreSQLDB.pass_amount += 1
            else:
                PosgreSQLDB.fail_amount += 1
            name = test.getAttribute("name")        # Name of Test
            cur.execute("SELECT * FROM home_functional_testcase WHERE test_name="+"'"+name+"'")
            if(cur.rowcount==0):
                cur.execute("INSERT INTO home_functional_testcase(test_name, test_type, test_comment)VALUES(%s, %s, %s)", (str(name), "123", "TBA"))
            else:
                continue

        conn.commit()

    def testrun(self, filename):
        xmll = open(filename, 'rU')
        xmldoc = xml.dom.minidom.parse(xmll)
        suite = xmldoc.getElementsByTagName('suite')
        start_time = xmldoc.getElementsByTagName('status')[0].getAttribute("starttime")
        end_time = xmldoc.getElementsByTagName('status')[-1].getAttribute("endtime")
        productname = suite[0].getAttribute('name')
        PosgreSQLDB.runname = productname+start_time
        testlist = xmldoc.getElementsByTagName('test')
        test_amount = len(testlist)
        cur.execute("SELECT * FROM home_product WHERE name="+"'"+productname+"'")
        if(cur.rowcount==0):
            cur.execute("INSERT INTO home_product(name)VALUES(%s)", (str(productname),))
        cur.execute("SELECT id FROM home_product WHERE name="+"'"+productname+"'")
        product_id = cur.fetchone()[0]
        cur.execute("INSERT INTO home_functional_test_run(name, product_id, os, test_type, build_info, start_time, "
                    "end_time, total_ran, total_passed, total_failed, status)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,"
                    " %s, %s)",
                    (str(PosgreSQLDB.runname), str(product_id), "linux", "123", "Buinfo", str(start_time), str(end_time),
                     str(test_amount), str(PosgreSQLDB.pass_amount), str(PosgreSQLDB.fail_amount), "1"))
        conn.commit()


        cur.execute("SELECT id FROM home_functional_test_run WHERE name=" + "'" + PosgreSQLDB.runname + "'")
        id = cur.fetchone()[0]
        for test in testlist:
            name = test.getAttribute("name")
            cur.execute("SELECT id FROM home_functional_testcase WHERE test_name=" + "'" + name + "'")
            testcase_id = cur.fetchone()[0]
            TagStatusStart = test.getElementsByTagName('status')[0]
            TagStatus = test.getElementsByTagName('status')[-1]
            status = TagStatus.getAttribute("status")
            startTime = TagStatusStart.getAttribute("starttime")
            endTime = TagStatus.getAttribute("endtime")
            if(status=="FAIL"):
                logfile = TagStatus.firstChild.data
            else:
                logfile = "pass"
            # cur.execute("SELECT * FROM functional_results WHERE job_id=" + "'" + str(id) + "'" + " and test_id=" + "'" + str(testcase_id) + "'")
            #
            #if(cur.rowcount==0):
            cur.execute("INSERT INTO home_functional_results(job_id, test_id, test_result, log_file, start_time, end_time)VALUES(%s, %s, %s, %s, %s, %s)",
                        (str(id), str(testcase_id), str(status), str(logfile), str(startTime), str(endTime)))
            conn.commit()

    def upload(self):
        # dir = '../mysite/home/static/Test_Log/'+PosgreSQLDB.runname+'_Log'
        # file_path = '../Log'
        # if not os.path.isdir(dir):
        #     os.makedirs(dir)

        # for i in os.listdir(file_path):
        #     if os.path.isfile(os.path.join(file_path,i)):
        #         copy(i, dir)
        url = "http://127.0.0.1:8000/getfile/"
        response = requests.post(url, data={'jobname': PosgreSQLDB.runname, 'username': username}, files={'logfile': open('../Log/log.html', 'rb'), 'reportfile': open('../Log/report.html', 'rb'), 'picfile': open('../Log/selenium-screenshot-1.png', 'rb')})


PosgreSQLDB().testcase("../Log/output.xml")
PosgreSQLDB().testrun("../Log/output.xml")
#PosgreSQLDB().upload()


