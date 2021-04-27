import re

import scrapy
from Csdn_redis_master.items import CsdnRedisMasterItem


class CsdnUrlSpider(scrapy.Spider):
    name = "csdn_master"

    allowed_domains = ["blog.csdn.net"]  # 限定域名，只爬取该域名下的网页

    # start_urls = [  # 开始爬取的链接
    #     "https://blog.csdn.net/u011718690/article/details/114558541"
    # ]

    def parse(self, response, **kwargs):
        # // *[ @ id = "mainBox"] / main / div[8] / div[2] / div / div[2] / a
        all_urls = response.xpath(
            "//a/@href").extract()
        recommend_urls = []
        # for i in all_urls:
        #     if i[:21] == "https://blog.csdn.net":
        #         recommend_urls.append(i)

        for i in all_urls:
            tmp = str(i[8:]).split('/')
            if 'article' in tmp and 'details' in tmp and 'blog.csdn.net' in tmp:
                recommend_urls.append(i)
        for recommend_url in recommend_urls:
            item = CsdnRedisMasterItem()
            item['url'] = recommend_url
            yield item
        for recommend_url in recommend_urls:
            yield scrapy.Request(recommend_url, self.parse, dont_filter=True)

    # def get_hot(self, response):
    #     hot_urls = response.xpath(
    #         "//div[@class='aside-content']/ul[@class='hotArticle-list']/li/a/@href").extract()
    #     for hot_url in hot_urls:
    #         yield scrapy.http.Request(hot_url, self.get_new, dont_filter=True)
    #
    # def get_new(self, response):
    #     new_urls = response.xpath(
    #         "//div[@class=aside-content]/ul[@class='inf_list']/li/a/@href").extract()
    #
    #     for url in new_urls:
    #         item = CsdnRedisMasterItem()
    #         item['url'] = url
    #         yield item

    # 未去重版
    # def parse(self, response):
    #     # 全部链接
    #     all_urls = []
    #     # 最新文章
    #     new_urls = response.xpath(
    #         "//div[@class=aside-content]/ul[@class='inf_list']/li/a/@href").extract()
    #     # 热门文章
    #     hot_urls = response.xpath(
    #         "//div[@class='aside-content']/ul[@class='hotArticle-list']/li/a/@href").extract()
    #     # 相关推荐
    #     recommend_urls = response.xpath(
    #         "//div[@class='content-box']/div/div[@class='title-box']/a/@href").extract()
    #
    #     all_urls += new_urls
    #     all_urls += hot_urls
    #     all_urls += recommend_urls
    #
    #     for url in all_urls:
    #         item = CsdnRedisMasterItem()
    #         item['url'] = url
    #         yield item, scrapy.Request(url=url, callback=self.parse, dont_filter=True)
