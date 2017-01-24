# coding:utf-8
import sys

reload(sys)
sys.setdefaultencoding('utf8')
#    __author__ = '郭 璞'
#    __date__ = '2017/1/24'
#    __Desc__ = 下载包， 解压包， 拓展文件安装

import urllib2
import re

import os
import zipfile

import shutil

class Downloader:

    def __init__(self, extensionname):
        self.extensionname = extensionname

    def urlOpener(self, targeturl):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.94 Safari/537.36'
        }
        return urllib2.urlopen(urllib2.Request(url=targeturl, headers=headers)).read()

    # 获取指定拓展的所有能用的版本
    def getLinks(self, url, regpattern):
        content = self.urlOpener(targeturl=url)
        reg = re.compile(regpattern)
        return re.findall(reg, content)

    def getDownloadLinks(self):
        versionLinks = self.getLinks("http://windows.php.net/downloads/pecl/releases/{}".format(self.extensionname),
                                     '<A HREF="(/downloads/pecl/releases/{}/.*?)">'.format(self.extensionname))
        for index, item in enumerate(versionLinks):
            print "{} : {}".format(index, item)
        choice = int(raw_input('Please choose the special version you want by number!\n'))
        return versionLinks[choice]

    def getTargetUrl(self):
        userChoice = "http://windows.php.net"+str(self.getDownloadLinks())
        print userChoice
        regpattern = '<A HREF="(/.*?/php_.*?\.zip)">.*?<\/A>'
        targetUrls = self.getLinks(url=userChoice, regpattern=regpattern)

        # 由于正则匹配度写的不好，第一个链接不能正常匹配，因此采用折断方式，去除第一个无效链接
        return targetUrls[1:]

    def folderMaker(self):
        if not os.path.exists(r'./packages/{}'.format(self.extensionname)):
            os.mkdir(r'./packages/{}'.format(self.extensionname))

    def download(self):
        choices = self.getTargetUrl()

        for index, item in enumerate(choices):
            print "{} : {}".format(index, item)
        choice = int(raw_input('Please choose the special version which suitable for your operation system you want by number!\n'))
        userChoice = choices[choice]

        # 对外提供友好的用户提示信息，优化的时候可通过添加进度条形式展现
        print 'Downloading, please wait...'

        # 开启下载模式，进行代码优化的时候可以使用多线程来进行加速
        data = self.urlOpener(targeturl="http://windows.php.net"+str(userChoice))
        # 将下载的资源存放到 本地资源库（先进行文件夹存在与否判断）
        filename = userChoice.split('/')[-1]
        self.folderMaker()
        with open(r'./packages/{}/{}'.format(self.extensionname, filename), 'wb') as file:
           file.write(data)

        print '{} downloaded!'.format(filename)



class UnZiper:

    def __init__(self, extensionname):
        self.extensionname = extensionname

    def folderMaker(self, foldername):
        if not os.path.exists(r'./packages/{}/{}'.format(self.extensionname, foldername)):
            os.mkdir(r'./packages/{}/{}'.format(self.extensionname, foldername))
            print 'Created folder {} succeed!'.format(foldername)

    def unzip(self):
        filelists = [item for item in os.listdir(r'./packages/{}/'.format(self.extensionname)) if item.endswith('.zip')]

        filezip = zipfile.ZipFile(r'./packages/{}/{}'.format(self.extensionname, filelists[0]))
        foldername = filelists[0].split('.')[0]

        self.folderMaker(foldername=foldername)

        print 'Uncompressing files, please wait...'
        for file in filezip.namelist():
            filezip.extract(file, r'./packages/{}/{}/{}'.format(self.extensionname, foldername, file))
        filezip.close()
        print 'Uncompress files succeed!'


class Configurer:

    def __init__(self, extensionname):
        self.extensionname = extensionname
        self.phpExtensionPath = ''
        self.phppath = ''

    def getPhpExtPath(self):
        # 默认系统中仅有一个php版本
        rawpath = [item for item in os.getenv('path').split(';') if item.__contains__('php')][0]
        self.phppath = rawpath
        return rawpath+str('ext\\')

    def getExtensionDllPath(self):

            for root, dirs, files in os.walk(r'./packages/{}/'.format(self.extensionname)):
                extensionfolder = root.split('\\')[-1]
                if extensionfolder.__contains__('dll'):
                    return root.split('\\')[0] + '/' + extensionfolder+'/'+extensionfolder

    # 针对php.ini文件中的相关的拓展选项进行针对性的添加.采用的具体方式是使用临时文件替换的方法
    def iniAppend(self):
        inipath = self.phppath+str('php.ini')
        tmpinipath = self.phppath+str('php-tmp.ini')

        # 要进行替换的新的文件内容
        newcontent = '; Windows Extensions\nextension={}.dll'.format(self.extensionname)
        open(tmpinipath, 'w').write(
            re.sub(r'; Windows Extensions', newcontent, open(inipath).read()))

        # 进行更名操作
        os.rename(inipath, self.phppath+str('php.bak.ini'))
        os.rename(tmpinipath, self.phppath+str('php.ini'))
        print 'Rename Succeed!'


    def configure(self):
        # 打印php拓展目录路径
        extpath = self.getPhpExtPath()+str('php_{}.dll'.format(self.extensionname))
        print extpath
        # 获取到拓展动态链接库及其路径
        extensiondllpath = self.getExtensionDllPath()
        # 将拓展文件添加到php拓展目录中
        shutil.copyfile(extensiondllpath, extpath)

        # 在php.ini文件中添加对应的拓展选项
        self.iniAppend()


        print '{} 拓展已添加，拓展服务将在重启Apache服务器后生效！'.format(self.extensionname)











