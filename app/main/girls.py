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
                    filters = ['淘宝', '淘女郎', '工作', '勿扰', '拍摄', '拍片', '片']
                    rstr = '|'.join(filters)
                    pattern = re.compile(rstr)
                    for x in intro:
                        if '主页' in x:
                            continue
                        news['content'] += re.sub(pattern, '', x)
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
