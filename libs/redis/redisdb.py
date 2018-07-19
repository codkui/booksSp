#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2018-06-25 15:25:12
import redis
import json

class Redis:
    con=False
    def __init__(self):
        pool = redis.ConnectionPool(host='127.0.0.1',port=6379)
        self.con = redis.Redis(connection_pool=pool)
    def addHost(self,bookName):
        self.con.hset("allHosts",bookName,1)
    def hadHost(self,bookName):
        return self.con.hget("allHosts",bookName)
    def delHost(self,bookName):
        return self.con.hdel("allHosts",bookName)
    def addUrl(self,url):
        print("增加url："+url)
        b=url.replace("://","")
        inx=b.find("/")
        host=url[:inx+4]
        self.con.rpush("url_"+host,url)
        if self.hadHost(host)==1:
            pass
        else:
            self.addHost(host)
    def getUrl(self,host):
        return self.con.brpop("url_"+host)
    def addHadUrl(self,url):
        print("已取url："+url)
        self.con.hset("allHadUrl",url,1)
    def hadUrl(self,url):
        self.con.hget("allHadUrl",url)
    def addUrlInfo(self,url,title,html,bookName=""):
        print("缓存url："+url)
        b=url.replace("://","")
        inx=b.find("/")
        host=url[:inx+4]
        self.con.hmset("urlinfo_"+url,{url:url,html:html,title:title,bookName:bookName,host:host})
    def getUrlInfo(self,url):
        return self.con.hgetall("urlinfo"+url)
    def addBaiduUrl(self,url):
        print("百度url："+url[0])
        self.con.rpush("baiduUrlList",json.dumps(url))
    def getBaiduUrl(self):
        a=self.con.brpop("baiduUrlList")
        if a:
            a=a[1]
        return a
    def addBaiduLink(self,url):
        print("百链url："+url[0])
        self.con.rpush("baiduLinkList",json.dumps(url))
    def getBaiduLink(self):
        a=self.con.brpop("baiduLinkList")
        if a:
            a=a[1]
        return a
    def test(self):
        self.con.set("name","cok")
        print(self.con.get("name"))
        self.addHost("天龙八部")
        print(self.hadHost("天龙八部"))

if __name__=="__main__":
    d=Redis()
    d.test()