#!/usr/bin/python
import psycopg2
import csv
import time
import os
import re
import ConfigParser


date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
cwd = os.getcwd()
Run_Info = {'run_name': 'Product_A_run1', 'product_name': 'Product_A', 'os': 'Linux', 'test_type': 0, 'build_info': 'NA',
        'start_time': date, 'end_time': date, 'total': 16, 'status': 0, 'log_file': 'http://www.google.com', 'test_comment': 'NA', 'area': 'Area1'}


class resultsUpload:
    def __init__(self, config_file_path):
        cf = ConfigParser.ConfigParser()
        cf.read(config_file_path)
        self.host = cf.get("baseconf", "host")
        self.port = cf.get("baseconf", "port")
        self.user = cf.get("baseconf", "user")
        self.pwd = cf.get("baseconf", "password")
        self.db = cf.get("baseconf", "db_name")

    def connectDB(self):
        conn = psycopg2.connect(database=self.db, user=self.user, password=self.pwd, host=self.host, port=self.port)
        cur = conn.cursor()
        return conn, cur

    def upload(self, x, csv_path, chosen_csv=''):
        pass_amount, fail_amount, csv_amount, chosen_csv_exist = 0, 0, 0, 0

        array = self.connectDB()
        conn = array[0]
        cur = array[1]

    # For each CSV file, add Test Case into DB first and count Pass/Fail.
        for each_csvfiles in os.listdir(csv_path):
            if each_csvfiles.endswith(".csv"):
                csv_amount += 1
                if chosen_csv != '' and chosen_csv in each_csvfiles or chosen_csv == '':
                    chosen_csv_exist += 1
                    each_csvfiles = os.path.join(csv_path, each_csvfiles)
                    with open(each_csvfiles, 'rb') as csvfile:
                        test_type = re.findall(r'\w+(?=_test.csv)', each_csvfiles)[0]
                        reader = csv.DictReader(csvfile)
                        for row in reader:
                            if row['Result'] == 'Pass':
                                pass_amount += 1
                            else:
                                fail_amount += 1
                            cur.execute("SELECT * FROM home_functional_testcase WHERE test_name='{0}'".format(str(row['Test_Name'])))
                            if cur.rowcount == 0:
                                cur.execute("INSERT INTO home_functional_testcase(test_name, test_type, test_comment)VALUES(%s, %s, %s)", (str(row['Test_Name']), str(test_type), str(x['test_comment'])))


    # Add 'Products' into DB
        cur.execute("select * from home_product WHERE name='{0}'".format(str(x['product_name'])))
        if cur.rowcount == 0:
            cur.execute("INSERT INTO home_product(name)VALUES(%s)", (str(x['product_name']),))

    # Add 'Test Run' into DB
        cur.execute("select * from home_functional_test_run where name='{0}'".format(str(x['run_name'])))
        if cur.rowcount == 0:
            cur.execute("SELECT id FROM home_product WHERE name='{0}'".format(str(x['product_name'])))
            product_id = cur.fetchone()[0]
            cur.execute("INSERT INTO home_functional_test_run(name, product_id, os, test_type, build_info, start_time, "
                        "end_time, total_ran, total_passed, total_failed, status)VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s,"
                        " %s, %s)",
                        (str(x['run_name']), str(product_id), str(x['os']), str(x['test_type']), str(x['build_info']), str(x['start_time']),
                         str(x['end_time']), str(x['total']), str(pass_amount), str(fail_amount), str(x['status'])))

    # Add 'Results' into DB
        for each_csvfiles in os.listdir(csv_path):
            if each_csvfiles.endswith(".csv"):
                if chosen_csv != '' and chosen_csv in each_csvfiles or chosen_csv == '':
                    each_csvfiles = os.path.join(csv_path, each_csvfiles)
                    with open(each_csvfiles, 'rb') as csvfile:
                        reader = csv.DictReader(csvfile)
                        cur.execute("SELECT id FROM home_functional_test_run WHERE name='{0}'".format(str(x['run_name'])))
                        run_id = cur.fetchone()[0]
                        for row in reader:
                            cur.execute("SELECT id FROM home_functional_testcase WHERE test_name='{0}'".format(str(row['Test_Name'])))
                            testcase_id = cur.fetchone()[0]
                            cur.execute("select * from home_functional_results where job_id='{0}' and test_id='{1}'".format(str(run_id), str(testcase_id)))
                            if cur.rowcount == 0:
                                cur.execute("INSERT INTO home_functional_results(job_id, test_id, test_result, log_file, start_time, end_time, area)VALUES(%s, %s, %s, %s, %s, %s, %s)",
                                            (str(run_id), str(testcase_id), str(row['Result']), str(x['log_file']), str(x['start_time']), str(x['end_time']), str(x['area'])))
        if csv_amount == 0:
            print 'No csv found!'
        elif chosen_csv_exist == 0:
            print 'Chosen csv does not exist!'
        else:
            print 'Upload succeeded!'

        conn.commit()
        cur.close()
        conn.close()

if __name__ == '__main__':
    resultsUpload(cwd + '/db_config.ini').upload(Run_Info, cwd)





