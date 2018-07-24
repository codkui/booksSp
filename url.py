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

class Url:
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
        pass
    def findUrl(self,html,host):
        p=pq(html)
        for each in p('a[href^="'+host+'"]').items():
                    # self.crawl(each.attr.href, callback=self.detail_page,fetch_type='js',validate_cert = False)
            if self.redis.hadUrl(each.attr.href)==1:
                continue
            self.redis.addUrl(each.attr.href)
    def getUlr(self):
        url=self.redis.getUrl()