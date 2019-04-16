from store import RedisClient
from getproxy import Crawler

POOL_UPPER_THRESHOLD=10000

class Getter:
    def __init__(self):
        self.redis=RedisClient()
        self.crawler=Crawler()

    def is_over_threshold(self):
        """
        判断是否达到了代理池限制
        :return:
        """
        if self.redis.count()>=POOL_UPPER_THRESHOLD:
            return True
        else:
            return False

    def run(self):
        print('Getter is starting')
        if not self.is_over_threshold():
            proxies=self.crawler.get_proxies()
            for proxy in proxies:
                self.redis.add(proxy)