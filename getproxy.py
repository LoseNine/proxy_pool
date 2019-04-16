import json
from crawl import getProxyList
from bs4 import BeautifulSoup
import requests

class ProxyMetaclass(type):
    def __new__(cls,name,bases,attrs):
        count=0
        attrs['__CrawlFunc__']=[]
        for k,v in attrs.items():
            if '__crawl__' in k:
                attrs['__CrawlFunc__'].append(k)
                count+=1
        attrs['__CrawlFunc__']=count
        return type.__new__(cls,name,bases,attrs)

class Crawler(object,metaclass=ProxyMetaclass):
    def get_proxies(self):
        proxies=[]
        for proxy in self.crawl():
            print("get proxy successfully :",proxy)
            proxies.append(proxy)
        return proxies

    def crawl(self,targeturl="http://www.xicidaili.com/nn/",n=4):
        Header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"}

        for page in range(1, n):
            url = targeturl + str(page)
            # print url
            html_doc = requests.get(url,headers=Header)

            soup = BeautifulSoup(html_doc.text,'lxml')
            # print soup
            trs = soup.find('table', id='ip_list').find_all('tr')
            for tr in trs[1:]:
                tds = tr.find_all('td')
                # 国家
                if tds[1].find('img') is None:
                    nation = '未知'
                    locate = '未知'
                else:
                    nation = tds[1].find('img')['alt'].strip()
                    locate = tds[4].text.strip()
                ip = tds[1].text.strip()
                port = tds[2].text.strip()
                anony = tds[5].text.strip()
                protocol = tds[6].text.strip()
                speed = tds[7].find('div')['title'].strip()
                time = tds[9].text.strip()
                #print('%s|%s|%s|%s|%s|%s|%s|%s\n' % (nation, ip, port, locate, anony, protocol, speed, time))
                yield ':'.join([ip,port])

