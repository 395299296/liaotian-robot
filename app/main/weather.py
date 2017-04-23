import json
import subprocess
from os import path

class Weather():
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
			subprocess.run('scrapy crawl weather -a city=%s' % city, shell=True, cwd='weather')
			with open('weather/weather.txt', 'r', encoding="utf-8") as file_object:
				self.contents.append({'type':'text', 'content':file_object.read()})

		return self.contents
