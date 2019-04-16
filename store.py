MAX_SCORE=100
MIN_SCORE=0
INITIAL_SOCRE=10
REDIS_HOST='localhost'
REDIS_PORT=6379
REDIS_PASSWORD=None
REDIS_KEY='proxies'

import redis
from random import choice

class RedisClient:
    def __init__(self,host=REDIS_HOST,port=REDIS_PORT,password=REDIS_PASSWORD):
        """
        初始化
        :param host: redis地址
        :param port: redis端口
        :param password: redis密码
        """
        self.db=redis.StrictRedis(host=host,port=port,password=password)

    def add(self,proxy,score=INITIAL_SOCRE):
        """
        添加代理到redis，并且设置分数为最高
        :param proxy: 代理
        :param score: 分数
        :return: 添加结果
        """
        if not self.db.zscore(REDIS_KEY,proxy):
            return self.db.zadd(REDIS_KEY,score,proxy)

    def random(self):
        """
        随机获取代理，首先尝试获取最高分，如果失败则按照排名获取，否则异常
        :return: 随机代理
        """
        result=self.db.zrangebyscore(REDIS_KEY,MAX_SCORE,MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result=self.db.zrevrange(REDIS_KEY,0,100)
            if len(result):
                return choice(result)
            else:
                raise NotImplementedError

    def decrease(self,proxy):
        """
        代理分数减一，分数小鱼最小值则移除
        :param proxy: 代理
        :return: 修改后的代理分数
        """
        score=self.db.zscore(REDIS_KEY,proxy)
        if score and score>MIN_SCORE:
            print("proxy ",proxy," score -1")
            return self.db.zincrby(REDIS_KEY,proxy,-1)
        else:
            print("proxy ",proxy," score drop")
            return self.db.zrem(REDIS_KEY,proxy)

    def exist(self,proxy):
        """
        判断是否存在
        :param proxy: 代理
        :return: 代理是否存在
        """
        return not self.db.zscore(REDIS_KEY,proxy)==None

    def max(self,proxy):
        """
        将代理设置为MAX_SCORE
        :param proxy: 代理
        :return: 设置结果
        """
        print("proxy ",proxy," can use is setted ",MAX_SCORE)
        return self.db.zadd(REDIS_KEY,MAX_SCORE,proxy)

    def count(self):
        """
        获取数量
        :return:数量
        """
        return self.db.zcard(REDIS_KEY)

    def all(self):
        """
        获取全部代理
        :return: 全部代理列表
        """
        return self.db.zrangebyscore(REDIS_KEY,MIN_SCORE,MAX_SCORE)