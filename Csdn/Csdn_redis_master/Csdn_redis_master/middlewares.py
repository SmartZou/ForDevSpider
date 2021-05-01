# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

from random import choice

from Csdn_redis_master.settings import UA_list


class CsdnRedisMasterDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def process_request(self, request, spider):
        ua = choice(UA_list)
        if ua:
            request.headers.setdefault('User-Agent', ua)

