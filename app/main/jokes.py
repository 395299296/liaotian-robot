from lxml import etree
from random import randint
import requests

joke_url = 'http://www.qiushibaike.com/hot/page/{page}/'

class Jokes():
    def __init__( self ):
        self.contents = []

    def getContent(self, content):
        r = requests.get(joke_url.format(page=randint(1,35)))
        tree = etree.HTML(r.text)
        contentlist = tree.xpath('//div[contains(@id, "qiushi_tag_")]')

        for i in contentlist:
            a = i.xpath('a[@class="contentHerf"]')[0]
            div = a.xpath('div[@class="content"]')[0]
            span = div.xpath('span')[0]
            self.contents.append({'type':'text', 'content':span.text})

        return self.contents
