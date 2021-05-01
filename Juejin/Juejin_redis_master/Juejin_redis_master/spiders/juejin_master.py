import scrapy
from Juejin_redis_master.items import JuejinRedisMasterItem


class JuejinUrlSpider(scrapy.Spider):
    name = "juejin_master"

    allowed_domains = ["juejin.cn"]  # 限定域名，只爬取该域名下的网页

    def parse(self, response, **kwargs):

        all_urls = response.xpath(
            "//a/@href").extract()

        recommend_urls = []
        # for i in all_urls:
        #     if i[:21] == "https://blog.csdn.net":
        #         recommend_urls.append(i)

        for i in all_urls:
            tmp = str(i[8:]).split('/')
            if 'post' in tmp and len(tmp)==2:
                recommend_urls.append(i)

        for url in recommend_urls:
            item = JuejinRedisMasterItem()
            item['url'] = url
            yield item
        for url in recommend_urls:
            yield scrapy.Request(url, self.parse, dont_filter=True)
        # item = GiteeRedisMasterItem()
        # yield  item
