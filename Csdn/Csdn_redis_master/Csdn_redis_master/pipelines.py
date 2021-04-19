# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import redis
from Csdn_redis_master.settings import REDIS_HOST, REDIS_PORT


class CsdnRedisMasterPipeline(object):
    @classmethod
    def from_settings(cls, settings):
        return cls(settings)

    def __init__(self, settings):
        # 记录爬取了多少条数据
        self.cnt = 0
        # 链接redis
        self.r = redis.Redis(REDIS_HOST, REDIS_PORT)
        # 参数设定
        self.settings = settings

    def open_spider(self, spider):
        start_url = "https://blog.csdn.net/qq_29175897/article/details/108759706"
        print("启动csdn爬虫,statr_url:", start_url)
        spider.start_urls = [start_url]

    def process_item(self, item, spider):
        redis_name = 'csdn'
        self.r.lpush(redis_name, item['url'])
        self.cnt += 1
        return item

    def close_spider(self, spider):
        content = "Master已关闭,共抓取url:{0}条.".format(self.cnt)
        print(content)
