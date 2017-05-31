# -*- coding: utf-8 -*-
import scrapy
from CrawlMeiziTu.items import CrawlmeizituItem
#from CrawlMeiziTu.items import CrawlmeizituItemPage
import time
class MeizituSpider(scrapy.Spider):
    name = "Meizitu"
    #allowed_domains = ["meizitu.com/"]

    start_urls = []
    last_url = []
    with open('..//url.txt', 'r') as fp:
        crawl_urls = fp.readlines()
        for start_url in crawl_urls:
            last_url.append(start_url.strip('\n'))
    start_urls.append("".join(last_url[-1]))


    def parse(self, response):
        selector = scrapy.Selector(response)
        #item = CrawlmeizituItemPage()

        next_pages = selector.xpath('//*[@id="wp_page_numbers"]/ul/li/a/@href').extract()
        next_pages_text = selector.xpath('//*[@id="wp_page_numbers"]/ul/li/a/text()').extract()
        all_urls = []
        if '下一页' in next_pages_text:
            next_url = "http://www.meizitu.com/a/{}".format(next_pages[-2])
            with open('..//url.txt', 'a+') as fp:
                fp.write('\n')
                fp.write(next_url)
                fp.write("\n")
            request = scrapy.http.Request(next_url, callback=self.parse)
            time.sleep(2)
            yield request

        all_info = selector.xpath('//h3[@class="tit"]/a')
        #读取每个图片夹的连接
        for info in all_info:
            links = info.xpath('//h3[@class="tit"]/a/@href').extract()
        for link in links:
            request = scrapy.http.Request(link, callback=self.parse_item)
            time.sleep(1)
            yield request

        # next_link = selector.xpath('//*[@id="wp_page_numbers"]/ul/li/a/@href').extract()
        # next_link_text = selector.xpath('//*[@id="wp_page_numbers"]/ul/li/a/text()').extract()
        # if '下一页' in next_link_text:
        #     nextPage = "http://www.meizitu.com/a/{}".format(next_link[-2])
        #     item['page_url'] = nextPage
        #     yield item

            #抓取每个文件夹的信息
    def parse_item(self, response):
         item = CrawlmeizituItem()
         selector = scrapy.Selector(response)

         image_title = selector.xpath('//h2/a/text()').extract()
         image_url = selector.xpath('//h2/a/@href').extract()
         image_tags = selector.xpath('//div[@class="metaRight"]/p/text()').extract()
         if selector.xpath('//*[@id="picture"]/p/img/@src').extract():
            image_src = selector.xpath('//*[@id="picture"]/p/img/@src').extract()
         else:
            image_src = selector.xpath('//*[@id="maincontent"]/div/p/img/@src').extract()
         if selector.xpath('//*[@id="picture"]/p/img/@alt').extract():
             pic_name = selector.xpath('//*[@id="picture"]/p/img/@alt').extract()
         else:
            pic_name = selector.xpath('//*[@id="maincontent"]/div/p/img/@alt').extract()
         #//*[@id="maincontent"]/div/p/img/@alt
         item['title'] = image_title
         item['url'] = image_url
         item['tags'] = image_tags
         item['src'] = image_src
         item['alt'] = pic_name
         print(item)
         time.sleep(1)
         yield item
