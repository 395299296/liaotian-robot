from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from movie.items import MovieItem

class MovieSpider(Spider):
    name = "movie"
    allowed_domains = ["dytt8.net"]
    start_urls = [
        "http://www.dytt8.net"
    ]

    def parse(self, response):
        selector = Selector(response)
        contentlist = selector.xpath('//td[@class="inddline"]')
        for i in contentlist:
            a = i.xpath('a/text()').extract()
            if '最新电影下载' in a:
                link = i.xpath('a/@href').extract()
                if len(link) >= 2:
                    yield Request(self.start_urls[0] + link[1],callback=self.parse_item)

    def parse_item(self, response):
        selector = Selector(response)
        title = selector.xpath('//div[@class="title_all"]/h1/font/text()')
        link = selector.xpath('//td[@bgcolor="#fdfddf"]/a/@href')
        if len(title) > 0 and len(link) > 0:
            item = MovieItem()
            item['movie_title'] = title[0].extract()
            item['movie_link'] = link[0].extract()
            yield item