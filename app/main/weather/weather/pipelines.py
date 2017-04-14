# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeatherPipeline(object):
    def process_item(self, item, spider):
        with open('weather.txt', 'w+', encoding="utf-8") as file:
            city = item['city'][0]
            file.write('城市：' + str(city) + '\n\n')
            date = item['date']
            desc = item['dayDesc']
            dayDesc = desc[1::2]
            nightDesc = desc[0::2]
            dayTemp = item['dayTemp']
            weaitem = zip(date, dayDesc, nightDesc, dayTemp)
            for item in weaitem:
                d = item[0]
                dd = item[1]
                nd = item[2]
                ta = item[3].split('/')
                dt = ta[0]
                if len(ta) > 1:
                    nt = ta[1]
                else:
                    nt = dt
                txt = '日期：{0}\n白天：{1}({2})\n夜晚：{3}({4})\n\n'.format(
                    d,
                    dd,
                    dt,
                    nd,
                    nt
                )
                file.write(txt)
        return item
