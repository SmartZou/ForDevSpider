# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import logging
from scrapy import signals
from scrapy.exceptions import NotConfigured
from elasticsearch import Elasticsearch
from Csdn_redis_slaver.settings import ELASTICSEARCH_HOST


class CsdnRedisSlaverPipeline:
    def __init__(self, idle_number, crawler):
        self.crawler = crawler
        self.idle_number = idle_number
        self.idle_list = []
        self.idle_count = 0
        self.cnt = 0
        self.es_index_name = "csdn_index"
        # self.es_index_type = "csdn_type"
        self.es = Elasticsearch(
            ELASTICSEARCH_HOST,
            sniff_on_start=True,  # 连接前测试
            sniff_on_connection_fail=True,  # 节点无响应刷新节点
            sniff_timeout=60,  # 设置超时时间
            # 除指定Es地址外，其他值均可以使用默认值
        )
        self._index_mappings = {
            "mappings": {
                self.es_index_type: {
                    "properties": {
                        "source":{
                            "type": "text",
                            "index": True,
                        },
                        "title": {
                            "type": "text",
                            "index": True,
                        },
                        "author": {
                            "type": "text",
                            "index": True,
                        },
                        "updated": {
                            "type": "text",
                            "index": True,
                        },
                        "tags": {
                            "type": "text",
                            "index": True,
                        },
                        "content": {
                            "type": "text",
                            "index": True,
                        },
                    }
                }
            }
        }

    @classmethod
    def from_crawler(cls, crawler):
        # 首先检查是否应该启用和提高扩展
        # 否则不配置
        if not crawler.settings.getbool('MYEXT_ENABLED'):
            raise NotConfigured

        # 获取配置中的时间片个数，默认为360个，30分钟
        idle_number = crawler.settings.getint('IDLE_NUMBER', 360)

        # 实例化扩展对象
        ext = cls(idle_number, crawler)

        # 将扩展对象连接到信号， 将signals.spider_idle 与 spider_idle() 方法关联起来。
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.spider_idle, signal=signals.spider_idle)

        # return the extension object
        return ext

    def spider_opened(self, spider):
        logger.info("opened spider %s redis spider Idle, Continuous idle limit： %d", spider.name, self.idle_number)

    def process_item(self, item, spider):
        if self.es.indices.exists(index=self.es_index_name) is not True:
            res = self.es.indices.create(index=self.es_index_name, body=self._index_mappings)
            print('创建index结果:', res)

    def spider_closed(self, spider):  # 获取当前已经连续触发的次数

        logger.info("closed spider %s, idle count %d , Continuous idle count %d",
                    spider.name, self.idle_count, len(self.idle_list))

    def spider_idle(self, spider):
        self.idle_count += 1  # 空闲计数
        self.idle_list.append(time.time())  # 每次触发 spider_idle时，记录下触发时间戳
        idle_list_len = len(self.idle_list)
        # 判断 当前触发时间与上次触发时间 之间的间隔是否大于5秒，如果大于5秒，说明redis 中还有key
        if idle_list_len > 2 and self.idle_list[-1] - self.idle_list[-2] > 6:
            self.idle_list = [self.idle_list[-1]]

        elif idle_list_len > self.idle_number:
            # 连续触发的次数达到配置次数后关闭爬虫
            logger.info('\n continued idle number exceed {} Times'
                        '\n meet the idle shutdown conditions, will close the reptile operation'
                        '\n idle start time: {},  close spider time: {}'.format(self.idle_number,
                                                                                self.idle_list[0], self.idle_list[0]))
            # 执行关闭爬虫操作
            content = "Slaver已关闭,共抓取数据:{0}条.".format(self.cnt)
            # sendmail(receivers=receivers, content=content, subject="Slaver爬虫执行完毕")
            self.crawler.engine.close_spider(spider, 'closespider_pagecount')
