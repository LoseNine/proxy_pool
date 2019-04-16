TESTER_CYCLE=20
GETTER_CYCLE=20
TESTER_ENABLED=True
GETTER_ENABLED=True
API_ENABLED=True
API_HOST='127.0.0.1'
API_PORT=8080

from multiprocessing import Process
from show import app
from getter import Getter
from verified import TEST
import time

class Schedule:
    def shedule_tester(self,cycle=TESTER_CYCLE):
        """
        定时测试代理
        :param cycle:
        :return:
        """
        tester=TEST()
        while 1:
            print('test is starting...')
            tester.run()
            time.sleep(cycle)

    def schdule_getter(self,cycle=GETTER_CYCLE):
        """定时获取代理"""
        getter=Getter()
        while 1:
            print('start crawl proxy...')
            getter.run()
            time.sleep(cycle)

    def shedule_api(self):
        """开启api"""
        app.run(API_HOST,API_PORT)

    def run(self):
        print('proxy pool start...')
        if TESTER_ENABLED:
            tester_process=Process(target=self.shedule_tester)
            tester_process.start()

        if GETTER_ENABLED:
            getter_process=Process(target=self.schdule_getter)
            getter_process.start()

        if API_ENABLED:
            api_process=Process(target=self.shedule_api)
            api_process.start()

if __name__ == '__main__':
    s=Schedule()
    s.run()