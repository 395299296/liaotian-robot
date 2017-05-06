from random import randint
from urllib.parse import quote, unquote
from . import config
import os
import re


rootdir = 'girl/'

class Girls():
    def __init__( self ):
        self.contents = []

    def getContent(self, content):
        for parent,dirnames,filenames in os.walk(rootdir):
            count = len(dirnames)
            if count > 0:
                dirname = dirnames[randint(0,count-1)]
                with open('%s/%s/个人简介.txt' % (rootdir, dirname), 'r', encoding="utf-8") as file_object:
                    news = {}
                    news['type'] = 'news'
                    news['title'] = dirname
                    intro = file_object.readlines()
                    news['content'] = ''
                    for x in intro:
                        if '主页' in x:
                            continue
                        result = getKeyInfo(x, news['content'])
                        if result:
                        	if news['content'][-1] != '\n':
                        		news['content'] += '\n'	
                        	news['content'] += '\n'.join(result)
                        else:
                        	news['content'] += x
                    pic_url = 'http://{domain}/girl/{name}.jpg'.format(domain=config.Domain,name=quote(dirname))
                    files = os.listdir(parent + dirname)
                    n = randint(0,len(files)-1)
                    extname = os.path.splitext(files[n])[1]
                    if extname != '.txt':
                        pic_url = 'http://{domain}/girl/{name}/{jpg}'.format(domain=config.Domain,name=quote(dirname),jpg=files[n])
                    news['pic_url'] = pic_url
                    news['url'] = pic_url
                    self.contents.append(news)

        return self.contents

    def getKeyInfo(self, s, content):
    	result = []
    	if not '三围' in content:
	        pattern = re.compile(r'三围.*?\d{2}\D?\d{2}\D?\d{2}', re.IGNORECASE)
	        sanwei = re.findall(pattern, s)
	        if sanwei:
	            pattern = re.compile(r'\d{2}\D?\d{2}\D?\d{2}', re.IGNORECASE)
	            sanwei = re.findall(pattern, sanwei[0])
	            result.append('三围:'+sanwei[0])

	    if not '手机' in content:
	        pattern = re.compile(r'1\d{10}', re.IGNORECASE)
	        phone = re.findall(pattern, s)
	        if phone:
	            result.append('手机:'+phone[0])

	    if not '手机' in content:
	        pattern = re.compile(r'微信.*?[A-Za-z0-9_]+', re.IGNORECASE)
	        wechat = re.findall(pattern, s)
	        if wechat:
	            pattern = re.compile(r'[A-Za-z0-9_]+', re.IGNORECASE)
	            wechat = re.findall(pattern, wechat[0])
	            result.append('微信:'+wechat[0])

	    if not 'QQ' in content:
	        pattern = re.compile(r'Q.*?[1-9]\\d{4,10}', re.IGNORECASE)
	        qq = re.findall(pattern, s)
	        if qq:
	            pattern = re.compile(r'[1-9]\\d{4,10}', re.IGNORECASE)
	            qq = re.findall(pattern, qq[0])
	            result.append('QQ:'+qq[0])

	    if not '陌陌' in content:
	        pattern = re.compile(r'陌陌.*?[A-Za-z0-9_]+', re.IGNORECASE)
	        momo = re.findall(pattern, s)
	        if momo:
	            pattern = re.compile(r'[A-Za-z0-9_]+', re.IGNORECASE)
	            momo = re.findall(pattern, momo[0])
	            result.append('陌陌:'+momo[0])

	    if not 'Instagram' in content:
	        pattern = re.compile(r'instagram.*?[A-Za-z0-9_]+', re.IGNORECASE)
	        instagram = re.findall(pattern, s)
	        if instagram:
	            pattern = re.compile(r'instagram', re.IGNORECASE)
	            instagram = re.sub(pattern, '', instagram[0])
	            pattern = re.compile(r'[A-Za-z0-9_]+', re.IGNORECASE)
	            instagram = re.findall(pattern, instagram)
	            result.append('Instagram:'+instagram[0])

        return result
