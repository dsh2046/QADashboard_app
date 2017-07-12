#!/usr/bin python
#coding = utf-8
import xml.dom.minidom
from pyh import *

class email(object):
    pass_amount = 0
    fail_amount = 0
    total_amount = 0
    fail_tag = 'pass'

    def makehtml(self, filename):

        page = PyH('My wonderful PyH page')
        dataList = div(id='dataList', style="margin-top: 20px", cl='col-lg-6')
        #page << table(id='failTable', border='1')
        #page << table(id='passTable', border='1', style='margin-top:20px')
        xmll = open(filename, 'rU')
        xmldoc = xml.dom.minidom.parse(xmll)
        testlist = xmldoc.getElementsByTagName('test')
        suite = xmldoc.getElementsByTagName('suite')
        testname = suite[0].getAttribute('name')
        email.total_amount = len(testlist)
        alltags = xmldoc.getElementsByTagName('tag')[-1]
        eachtag = alltags.getElementsByTagName('stat')

        for each in eachtag:
            tagname = each.firstChild.data
            totalpass = tr()
            totalfail = tr()
            pass_amount = 0
            fail_amount = 0

            for test in testlist:
                TagStatus = test.getElementsByTagName('status')[-1]
                status = TagStatus.getAttribute("status")
                tag = test.getElementsByTagName("tag")[0]
                tagname2 = tag.firstChild.data
                name = test.getAttribute("name")
                if tagname2 ==tagname:
                    if status=="PASS":
                        email.pass_amount += 1
                        pass_amount += 1
                        totalpass += tr(td(name,  style="padding:5px")+td('PASS', style='color:green;padding:5px')+td('N/A', style='color:green;padding:5px'))
                    else:
                        email.fail_amount += 1
                        fail_amount += 1
                        logfile = TagStatus.firstChild.data
                        totalfail += tr(td(name, style="padding:5px") + td('FAIL', style='color:red;padding:5px') + td(logfile, style='color:red;padding:5px'))
                        email.fail_tag = 'fail'

            headrow = tr(td(tagname, colspan='3'), style='text-align:center;font-weight:600')
            headrow << span('  (Pass:'+str(pass_amount), style='color:green') + span('   Fail:'+str(fail_amount)+')', style='color:red')
            dataList << table(id=tagname + 'fail', border='1',style='margin-bottom:20px') << headrow + totalfail + totalpass



        page << h4('Hi All:')
        if email.fail_tag =='fail':
            page << i() << span() << h1(testname, style='display:inline-block') + h2('(BUILD FAILED)', style='color:red;display:inline-block')
        else:
            page << i() << span() << h1(testname, style='display:inline-block') + h2('(BUILD SUCCESS)', style='color:green;display:inline-block')

        page << div() << span('Total:  ',email.total_amount, id='total')+span('Pass:  ',email.pass_amount, id='pass', style="color:green;margin-left:20px")+span('Fail:  ',email.fail_amount, id='fail', style="color:red;margin-left:20px")
        dataList.render()
        page << dataList
        page << h4('Thanks~')
        page << h4('Regards')
        page.printOut('demo_1.html')


email().makehtml('../Log/output2.xml')

# mydiv2 = page << div(id='myDiv2')
# mydiv2 << h2('A smaller title') + p('Followed by a paragraph.')
# page << div(id='myDiv3')
# page.myDiv3.attributes['cl'] = 'myCSSclass3'
# page.myDiv3 << p('Another paragraph')


