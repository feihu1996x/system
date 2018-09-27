import unittest
from  BSTestRunner import BSTestRunner
import time,logging
import sys
path='D:\\kyb_testProject\\'
sys.path.append(path)

test_dir='../test_case'
report_dir='../reports'

discover=unittest.defaultTestLoader.discover(test_dir,pattern='test_login.py')

now=time.strftime('%Y-%m-%d %H_%M_%S')
report_name=report_dir+'/'+now+' test_report.html'

with open(report_name,'wb') as f:
    runner=BSTestRunner(stream=f,title='Kyb Test Report',description='kyb Android app test report')
    logging.info('start run test case...')
    runner.run(discover)