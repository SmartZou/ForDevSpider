import redis
import scrapy
from scrapy.exceptions import DontCloseSpider
from Csdn_redis_slaver.settings import REDIS_HOST, REDIS_PORT
from scrapy_redis.spiders import RedisSpider
from bs4 import BeautifulSoup
from Csdn_redis_slaver.items import CsdnRedisSlaverItem


class CsdnSlaverSpider(RedisSpider):
    name = 'csdn_slaver'
    redis_key = 'csdn'

    # 初始化
    def __init__(self, *args, **kwargs):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT)

    def parse(self, response):
        item = CsdnRedisSlaverItem()
        # 获取文章来源
        item['source'] = response.url
        # 获取文章标题
        item['title'] = response.xpath(
            "//h1[@class='title-article']/text()").extract_first()
        # 获取文章作者
        item['author'] = response.xpath(
            "//a[@class='follow-nickName ']/text()").extract_first()
        # 获取更新时间
        item['updated'] = response.xpath(
            "//span[@class='time']/text()").extract_first()
        # 获取文章标签
        item['tags'] = response.xpath(
            "//a[@class='tag-link']/text()").extract_first()
        # 获取内容
        contTmp = response.xpath(
            "//div[@class='htmledit_views']").extract_first()
        # print(contTmp)contTmp
        # 解析内容
        # bs = BeautifulSoup(contTmp, 'html5lib')
        # for a in bs.stripped_strings:
        #     print(repr(a))
        # 解析内容
        # item['content'] = contTmp
        # 内容来源网站
        item['webSource'] = "CSDN"
        yield item
