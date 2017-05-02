from .lyric import sample
import re

class Lyrics():
    def __init__( self ):
        self.contents = []

    def getContent(self, content):
        if content.startswith('歌词'):
            r = re.compile(r'[^\u4e00-\u9fa5]') #过滤非中文内容
            c = r.sub('',content).strip()
            c = c[2:] #过滤歌词俩字
            if not c:
                c = '亲爱的'
            self.contents.append({'type':'text', 'content':sample.sample(c)})
        return self.contents
