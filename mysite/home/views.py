from django.shortcuts import render
from django.http import *
from django.db import connection
from django.db import models
from django.core import serializers
from django.views.generic.base import View
from django.core import serializers

from home.models import *
import psycopg2
import json
import os

def dbConn(username):
    conn = psycopg2.connect(database=username, user="postgres", password="12345678", host="localhost", port="5432")
    cur = conn.cursor()
    return cur


class IndexView(View):
    def get(self, request):
        if 'remember' in request.GET:
            request.session['remember'] = request.GET['remember']
        # username = request.session.get('username', 'anybody')
        username = 'admin'
        if username == 'anybody':
            return HttpResponse("<h2>Please login again!!</h2>")
        else:
            try:
                result = product.objects.all()[0]
                detail_table = functional_test_run.objects.all().filter(product_id=int(result.id))
            except:
                result = ''
                detail_table = ''
            result2 = product.objects.all()
            try:
                product_name = request.GET.get('pn', '')
                testtype_name = request.GET.get('ttn', '')
                if product_name == '':
                    return render(request, 'home/pages/index.html', {'side': result2, 'detail': detail_table, 'username': username, 'product_name': result2[0], 'test_type': 'Functional'})
                else:
                    if testtype_name == '':
                        return render(request, 'home/pages/index.html', {'side': result, 'username': username, 'product_name': product_name, 'choose_type': '1'})
                    else:
                        if testtype_name == 'Functional':
                            result = product.objects.all().get(name=product_name)
                            result2 = product.objects.all()
                            detail_table = functional_test_run.objects.all().filter(product_id=int(result.id))
                            return render(request, 'home/pages/index.html', {'side': result2, 'detail': detail_table, 'username': username, 'product_name': product_name, 'test_type': testtype_name})
                        elif testtype_name == 'Performance':
                            result = product.objects.all().get(name=product_name)
                            result2 = product.objects.all()
                            detail_table = performance_test_run.objects.all().filter(product_id=int(result.id))
                            return render(request, 'home/pages/index.html', {'side': result2, 'detail': detail_table, 'username': username, 'product_name': product_name, 'test_type': testtype_name})
            except:
                return render(request, 'home/pages/index.html', {'result': '', 'username': username})


class CompareView(View):
    def get(self, request):
        progress = []
        regress = []
        new_testcase = []
        thisrun_testcaseDic = {}
        lastrun_testcaseDic = {}
        run_id = int(request.GET.get('id', ''))
        # username = request.session.get('username', 'anybody')
        username = 'admin'
        test_type = request.GET.get('test_type', '')

        if test_type == 'Functional':
            product_id = functional_test_run.objects.all().get(id=int(run_id)).product_id
            test_run_time = functional_test_run.objects.all().get(id=int(run_id)).start_time
            test_run = functional_test_run.objects.all().filter(product_id=int(product_id)).order_by('start_time')
            try:
                lastrun_id = functional_test_run.objects.all().filter(start_time__lt=test_run_time).filter(product_id=product_id).order_by('-start_time')[:1].values_list('id')[0][0]
                run_result = functional_results.objects.all().filter(job_id=int(run_id)).values_list()
                lastrun_result = functional_results.objects.all().filter(job_id=int(lastrun_id)).values_list()
                for run in run_result:
                    thisrun_testcase_name = functional_testcase.objects.all().get(id=run[2]).test_name
                    thisrun_testcaseDic[thisrun_testcase_name] = run[3]
                for lastrun in lastrun_result:
                    lastrun_testcase_name = functional_testcase.objects.all().get(id=lastrun[2]).test_name
                    lastrun_testcaseDic[lastrun_testcase_name] = lastrun[3]
                for k, v in thisrun_testcaseDic.items():
                    if k in lastrun_testcaseDic:
                        if 'Pass' in v and 'Fail' in lastrun_testcaseDic[k]:
                            progress.append(k)
                        elif 'Fail' in v and 'Pass' in lastrun_testcaseDic[k]:
                            regress.append(k)
                    else:
                        new_testcase.append(k)

                final_result = {'progress': progress, 'regress': regress, 'new': new_testcase}
                final_result = json.dumps(final_result)
                return HttpResponse(final_result)
            except:
                return HttpResponse('error')

        elif test_type == 'Performance':
            product_id = performance_test_run.objects.all().get(id=int(run_id)).product_id
            test_run_time = performance_test_run.objects.all().get(id=int(run_id)).start_time
            test_run = performance_test_run.objects.all().filter(product_id=int(product_id)).order_by('start_time')
            try:
                lastrun_id = performance_test_run.objects.all().filter(start_time__lt=test_run_time).order_by('-start_time')[:1].values_list('id')[0]
                run_result = performance_results.objects.all().filter(job_id=int(run_id)).values_list()
                lastrun_result = performance_results.objects.all().filter(job_id=lastrun_id).values_list()
                for run in run_result:
                    testcase_name = performance_testcase.objects.all().get(id=run[2]).test_name
                    thisrun_testcaseDic[testcase_name] = run[3]
                for run in lastrun_result:
                    testcase_name = performance_testcase.objects.all().get(id=run[2]).test_name
                    lastrun_testcaseDic[testcase_name] = run[3]
                for k, v in thisrun_testcaseDic.items():
                    if k in lastrun_testcaseDic:
                        if 'Pass' in v and 'Fail' in lastrun_testcaseDic[k]:
                            progress.append(k)
                        elif 'Fail' in v and 'Pass' in lastrun_testcaseDic[k]:
                            regress.append(k)
                    else:
                        new_testcase.append(k)
                final_result = {'progress': progress, 'regress': regress, 'new': new_testcase}
                final_result = json.dumps(final_result)
                return HttpResponse(final_result)
            except:
                return HttpResponse('error')


def table(request):
    if request.method == 'GET' and 'remember' in request.GET:
        request.session['remember'] = request.GET['remember']
    # username = request.session.get('username', 'anybody')
    username = 'admin'
    if username == 'anybody':
        return HttpResponse("<h2>Please login again!!</h2>")
    else:
        # cur = dbConn(username)
        # cur.execute('select * from functional_test_run')
        # result = cur.fetchall()
        try:
            result = functional_test_run.objects.all().all()
            return render(request, 'home/pages/tables.html', {'result': result, 'username': username})
        except:
            return render(request, 'home/pages/tables.html', {'result': '', 'username': username})

def detail(request):
    # if 'username' in request.session:
    # username = request.session.get('username')
    username = 'admin'
    cur = dbConn(username)
    job_id = request.GET['id']
    test_type = request.GET.get('test_type', '')
    if test_type == 'Functional':
        cur.execute('select home_functional_testcase.test_name, home_functional_testcase.test_type, home_functional_results.start_time, home_functional_results.end_time, home_functional_results.test_result, home_functional_results.log_file, home_functional_test_run.total_ran, home_functional_results.area from home_functional_results, home_functional_testcase, home_functional_test_run where home_functional_results.test_id=home_functional_testcase.id and home_functional_results.job_id='+job_id+' and home_functional_test_run.id=home_functional_results.job_id')
        result = cur.fetchall()
        return HttpResponse(json.dumps(result))
    elif test_type == 'Performance':
        cur.execute('select home_performance_testcase.test_name, home_performance_results.start_time, home_performance_results.end_time, home_performance_results.test_result, home_performance_results.log_file, home_performance_test_run.total_ran from home_performance_results, home_performance_testcase, home_performance_test_run.total_ran where home_performance_results.test_id=home_performance_testcase.id and home_performance_results.job_id='+job_id+' and home_performance_test_run.id=home_performance_results.job_id')
        result = cur.fetchall()
        return HttpResponse(json.dumps(result))
    #
    # else:
    #     return HttpResponse('Please Login Again!')

def login(request):
    if request.session.get('remember') == '1':
        return HttpResponseRedirect('/table/')
    else:
        return render(request, 'home/pages/login.html')
    # del request.session['remember']
    # return HttpResponse(request.session.get('remember'))


def login_validate(request):
    username = request.GET['username']
    password = request.GET['password']
    request.session['username'] = username
    conn = psycopg2.connect(database="User_Info", user="postgres", password="12345678", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("select * from account where Username="+"'"+username+"'"+" and Password="+"'"+password+"'")
    if cur.fetchone():
        return HttpResponse('1')
    else:
        return HttpResponse("Doesn't exist")

def logout(request):
    del request.session['username']
    if 'remember' in request.session:
        del request.session['remember']
    return HttpResponseRedirect('/login/')

def getfile(request):
    myFile = request.FILES.get("logfile", None)
    myFile2 = request.FILES.get("reportfile", None)
    myFile3 = request.FILES.get("picfile", None)
    jobname = request.POST.get('jobname', None)
    username = request.POST.get('username', None)

    dir = '/home/samueldeng/AFVersioning/mysite/home/static/Test_Log/'+username+'_Log/'+jobname+'_Log'
    if not os.path.isdir(dir):
        os.makedirs(dir)

    destination = open(os.path.join("/home/samueldeng/AFVersioning/mysite/home/static/Test_Log/"+username+"_Log/"+jobname+'_Log', myFile.name), 'wb+')
    for chunk in myFile.chunks():
        destination.write(chunk)
    destination.close()

    destination = open(os.path.join("/home/samueldeng/AFVersioning/mysite/home/static/Test_Log/"+username+"_Log/"+jobname+'_Log', myFile2.name), 'wb+')
    for chunk in myFile2.chunks():
        destination.write(chunk)
    destination.close()

    destination = open(os.path.join("/home/samueldeng/AFVersioning/mysite/home/static/Test_Log/"+username+"_Log/"+jobname+'_Log', myFile3.name), 'wb+')
    for chunk in myFile3.chunks():
        destination.write(chunk)
    destination.close()
    return HttpResponse('123')








