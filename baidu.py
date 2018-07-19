#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-25 15:25:12
import requests
import random
from pyquery  import PyQuery as pq
from libs.redis.redisdb import Redis
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import _thread
import json
class baidu:
    redis=Redis()
    driver = False
    headers=[
        {
            'User-Agent':'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
        },
        {
            'User-Agent':'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50'
        },
        {
            'User-Agent':'Mozilla/5.0(compatible;MSIE9.0;WindowsNT6.1;Trident/5.0'
        },
        {
            'User-Agent':'Mozilla/4.0(compatible;MSIE8.0;WindowsNT6.0;Trident/4.0)'
        },
        {
            'User-Agent':'Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1'
        },
        {
            'User-Agent':'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11'
        },
        {
            'User-Agent':'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11'
        },
        {
            'User-Agent':'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)'
        },
    ]
    def __init__(self):
        # self.driver = webdriver.PhantomJS()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options) #,executable_path = 'D:\APPS\dir\chromedriver.exe'
        print("ok")
        # pass
    def getHeader(self):
        le=len(self.headers)
        ind=random.randint(0,le-1)
        return self.headers[ind]
    def search(self,keyword):
        url="http://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=0&rsv_idx=1&tn=baidu&wd="+keyword+" 阅读"
        self.redis.addBaiduUrl([url,keyword])
        # html=requests.get(url,headers=self.getHeader())
    def actLink(self):
        while True:
            url=self.redis.getBaiduLink()
            # url=["https://www.baidu.com/link?url=5AYDIIi-uu80t4A5dtegh9mW-rW7taSGPsjxd9yEmwSghfjZ_LjKUgo3k97TX-qTKIlpuJePJgxSK4wG0Nes1K&wd=&eqid=e293e0190006fded000000055b503b7e",1]
            if url!=None:
                url=json.loads(url)
                print(url)
                print("取得链接地址:"+url[0])
                bookName=url[1]
                url=url[0]
                # print(1111111)
                # data=requests.get(url,headers=self.getHeader())
                # print(data.headers)
                # print(data.text)
                self.driver.get(url)
                data = self.driver.page_source
                newUrl=self.driver.current_url
                print("地址转换为:"+newUrl)
                title=self.driver.title
                if self.redis.hadUrl(newUrl)==1:
                    time.sleep(0.1)
                    continue
                self.redis.addHadUrl(newUrl)
                self.redis.addUrlInfo(newUrl,title,data,bookName)
            time.sleep(0.3)
    def actBaidu(self):
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(chrome_options=chrome_options) #,executable_path = 'D:\APPS\dir\chromedriver.exe'
        while True:
            url=self.redis.getBaiduUrl()
            if url!=None:
                
                url=json.loads(url)
                print("取得百度地址:"+str(url[0]))
                # return
                bookName=url[1]
                url=url[0]
                had=self.redis.hadUrl(url)
                if had==1:
                    time.sleep(0.1)
                    continue
                html=requests.get(url,headers=self.getHeader())
                # data=driver.get(url)
                # html = driver.page_source
                if html.status_code!=200:
                    self.redis.addBaiduUrl([url,bookName])
                    time.sleep(0.1)
                    continue
                self.redis.addHadUrl(url)
                
                p=pq(html.text)
                for each in p('a[href^="http://www.baidu.com/link?url="]').items():
                    # self.crawl(each.attr.href, callback=self.detail_page,fetch_type='js',validate_cert = False)
                    if self.redis.hadUrl(each.attr.href)==1:
                        
                        continue
                    self.redis.addBaiduLink([each.attr.href,bookName])
                if "&pn=" in url:
                    continue
                for each in range(30):
                    # print(each.attr.href)
                    urlN=url+"&pn="+str((each+1)*10)
                    if self.redis.hadUrl(urlN)==1:
                        
                        continue
                    self.redis.addBaiduUrl([urlN,bookName])
            time.sleep(1)
                    # self.crawl(each.attr.href, callback=self.index_page,fetch_type='js',validate_cert = False)
    def start(self):
        pass

if __name__=="__main__":
    print("111111")
    baid=baidu()
    baid.search("天涯明月刀")
    _thread.start_new_thread( baid.actBaidu,())
    baid.actLink()

