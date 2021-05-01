# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from Csdn_redis_slaver.settings import UA_list, proxy_api
from random import choice, randint
from twisted.internet.error import TimeoutError, ConnectionRefusedError
import requests

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class CsdnRedisSlaverSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class CsdnRedisSlaverDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def __init__(self):
        self.pre_proxy = ''
        self.proxy_ip = self.get_proxy()

    def get_proxy(self):
        s = 'http://' + requests.get(proxy_api).text
        return s

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        ua = choice(UA_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)
        request.meta['proxy'] = self.proxy_ip
        return None

    def process_response(self, request, response, spider):
        if response.status != 200:
            return request
        return response

    def process_exception(self, request, exception, spider):
        print(type(exception), exception)
        # 连接失败异常
        if isinstance(exception, ConnectionRefusedError):
            # 失效后，把失效ip做记录pre
            self.pre_proxy = request.meta['proxy']
            # 判断当前ip是否失效
            if self.proxy_ip == self.pre_proxy:
                # 失效则获取新的ip
                self.proxy_ip = self.get_proxy()
                print(self.pre_proxy, ' change ', self.proxy_ip)
            # 如果当前ip不是失效ip(已经请求过新的)
            request.meta['proxy'] = self.proxy_ip

        # 超时异常，处理时采用1/10的概率进行更换ip
        if isinstance(exception, TimeoutError):
            opt = randint(0, 8)
            if opt == 1:
                # 失效后，把失效ip做记录pre
                self.pre_proxy = request.meta['proxy']
                # 判断当前ip是否失效
                if self.proxy_ip == self.pre_proxy:
                    # 失效则获取新的ip
                    self.proxy_ip = self.get_proxy()
                    print(self.pre_proxy, ' change ', self.proxy_ip)
                # 如果当前ip不是失效ip(已经请求过新的)
                request.meta['proxy'] = self.proxy_ip
        return request

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
