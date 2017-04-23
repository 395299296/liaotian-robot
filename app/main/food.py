from lxml import etree
from random import randint
from os import path
import requests
import json

home_url = 'https://t.dianping.com'
food_url = 'https://t.dianping.com/list/{city}-category_1?pageIndex={page}'
headers = {
	'User-Agent': 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0'
}
class Food():
	def __init__( self ):
		self.contents = []

	def getContent(self, content):
    	d = path.dirname(__file__)
		with open(path.join(d， 'city.json'), 'r', encoding="utf-8") as json_file:
			data = json.load(json_file)
			city = 'shenzhen'
			for x in data:
				if x['name'] in content:
					city = x['pinyin'].lower()
					break;
			url = food_url.format(city=city, page=randint(0,50))
			r = requests.get(url, headers=headers)
			tree = etree.HTML(r.text)
			contentlist = tree.xpath("//div[@class='tg-floor-item-wrap']")
			for i in contentlist:
				a = i.xpath('a[@class="tg-floor-img"]')[0]
				deal_url = a.xpath('@href')[0]
				pic_url = a.xpath('img')[0].attrib['lazy-src-load']
				pic_url = pic_url[0:pic_url.find('%')]
				a = i.xpath('a[@class="tg-floor-title"]')[0]
				title = a.xpath('h3/text()')[0]
				news = {}
				news['type'] = 'news'
				news['title'] = title
				news['pic_url'] = pic_url
				news['content'] = ''
				news['url'] = home_url + deal_url
				self.contents.append(news)

		return self.contents
