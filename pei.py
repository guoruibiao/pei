# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#    __author__ = '郭 璞'
#    __date__ = '2017/1/24'
#    __Desc__ = 大管家

from handler import *

extensionname = 'xrange'

# downloader = Downloader(extensionname)
# downloader.download()
#
# zipper = UnZiper(extensionname)
# zipper.unzip()

configurer = Configurer(extensionname)
configurer.configure()
