import scrapy
from Gitee_redis_master.items import GiteeRedisMasterItem


class GiteeUrlSpider(scrapy.Spider):
    name = "gitee_master"

    allowed_domains = ["gitee.com"]  # 限定域名，只爬取该域名下的网页

    def parse(self, response, **kwargs):
        all_urls = response.xpath(
            "//a[@class='title project-namespace-path']/@href").extract()
        for url in all_urls:
            item = GiteeRedisMasterItem()
            item['url'] = url
            yield item
        for url in all_urls:
            yield scrapy.Request(url, self.parse, dont_filter=True)
        # item = GiteeRedisMasterItem()
        # yield  item