# proxy_pool
redis proxy pool


### 该代理池主要由三大模块构成

* 获取模块：需要定时在IP网站进行爬取

* 检测模块：需要定时检测数据库中的代理

* 接口模块：需要用API来提供对外服务的接口

### 存储模块的主要思想

* 使用redis的有序集合，集合中的每一个元素都是不重复的，对于代理池来说，集合的元素就是一个个代理，IP:PORT。
* 有序集合的每一个元素都有一个分数字段，分数是可以重复的，0-100，根据分数对代理进行排序
* 分数为100为可用，检测器会定时循环检测每个代理，可用则为100，不可用则分数-1，一直到0被清除
* 新获取的代理分数为10，如何通过测试，分数为100，否则-1，到0被清除

### 使用方法

* 可以在127.0.0.1:8080查看网站接口

第一步，启动Flask
```python
from schedule import Schedule
s=Schedule()
s.run()
```
如果启动成功，会有如下画面
```python
proxy pool start...
start crawl proxy...
Getter is starting
test is starting...
run....
testing  111.177.167.136:9999
 * Running on http://127.0.0.1:8080/ (Press CTRL+C to quit)
testing  111.177.169.249:9999
testing  111.177.170.186:9999
testing  111.177.173.19:9999
testing  111.177.173.43:9999
```

然后就可以调用代理池的代理了
```python
import requests

PROXY_URL='http://127.0.0.1:8080/random'

def get_proxy():
    response=requests.get(PROXY_URL)
    return response.text

proxy=get_proxy()
proxies={
    'http':"http://"+proxy,
    'https':'https://'+proxy
}

response=requests.get('http://httpbin.org/get',proxies=proxies)
print(response.text)
```
