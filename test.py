# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#    __author__ = '郭 璞'
#    __date__ = '2017/1/24'
#    __Desc__ = 

from handler import *

configurer = Configurer('redis')

path = configurer.getExtensionDllPath()
print path

configurer.configure()

# os.rename(r'./1.ini', 'php----bak.ini')
