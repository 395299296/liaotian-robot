from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from weather.items import WeatherItem

class WeatherSpider(Spider):
    name = "weather"

    def __init__(self, city=None, *args, **kwargs):
        super(WeatherSpider, self).__init__(*args, **kwargs)
        self.allowed_domains = ["sina.com.cn"]
        self.start_urls = [
            "http://weather.sina.com.cn/%s/" % city
        ]

    def parse(self, response):
        item = WeatherItem()
        item['city'] = response.xpath('//*[@id="slider_ct_name"]/text()').extract()
        tenDay = response.xpath('//*[@id="blk_fc_c0_scroll"]');
        item['date'] = tenDay.css('p.wt_fc_c0_i_date::text').extract()
        item['dayDesc'] = tenDay.css('img.icons0_wt::attr(title)').extract()
        item['dayTemp'] = tenDay.css('p.wt_fc_c0_i_temp::text').extract()
        return item