#!/usr/bin/python
# coding: utf-8

wb = 'http://weike.cflo.com.cn/play.asp?vodid=170766&e=5&from=singlemessage&isappinstalled=0'

#import mechanize
#import cookielib
#import socket
import urllib
import urllib2
import requests
import bs4
import re
import random
from random import choice

##solving unreadable code
import sys
import time
#import chardet

##get proxy ip
def get_ip():
    url = "http://www.xicidaili.com/nn"
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Referer":"http://www.xicidaili.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.3"
                }
    req = requests.get(url,headers=headers)
    soup = bs4.BeautifulSoup(req.text, 'html.parser')
    data = soup.table.find_all("td")
    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>') #ip pattern
    port_compile = re.compile(r'<td>(\d+)</td>')            #port pattern
    ip = re.findall(ip_compile,str(data))
    port = re.findall(port_compile,str(data))
    return [":".join(i) for i in zip(ip,port)]

##imitate a GET request
def GET(url,ip_list=[]):
    try:
        ip = choice(ip_list)
    except:
        return False
    else:
        proxies = { "http":ip,}
        headers = { "Accept":"*/*",
                    "Accept-Encoding":"gzip, deflate, sdch",
                    "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                    "Referer":wb,
                    "User-Agent":choice(ua_list),
                    }
    
    try:
        req = requests.get(url,timeout=100,headers=headers,proxies=proxies)
#        print req
        res = req.text
        if not re.findall(u'评价成功！',res) and not re.match(r'[\d]{4,}',res):
            ip_list.remove(ip)
            print "This ip is redirected"
        else:
            print req
#        res_data = urllib2.urlopen(req) #file
#        res = res_data.read().decode('gbk','ignore').encode('utf-8')
#        print res
    except requests.exceptions.RequestException as error:  
        print type(error)
        if not ip_list:
            print "There is no ip"
            sys.exit()
        #delete invalid ip
        elif ip in ip_list:
            ip_list.remove(ip)
        #repeat GET request
        GET(url,ip_list)
    else:
        print 'url=[%s]\nip=[%s], wb=[%s]\nproxy ip_list remains %s' %(url,ip,res,len(ip_list))        
            
protocol,rest = urllib.splittype(wb)
host,rest = urllib.splithost(rest)
for info in re.split(r'[\?&]',rest):
    if re.match('vodid',info):
        id = info.split('=')[-1]
        id_score = id+'_5'
        print 'id=%s' %(id)
    elif re.match(r'e=[\d]',info):
        xiangmu = info.split('=')[-1]
        print 'xiangmu=%s' %(xiangmu)

ua_list=[
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0"
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
    ]
ip_list=[]

for i in range(5000):
    #refresh ip list every 1000-times
    if i % 50 == 0:
        ip_list.extend(get_ip())
    #launch 
    url_tmp1 = '/js_useradopt.asp?vodid='+id+'&xiangmu='+xiangmu+'&nzz='+str(random.random())
    url_adopt = protocol+"://"+host+url_tmp1
    url_tmp2 = '/js_support.asp?vodid='+id_score+'&xiangmu='+xiangmu+'&nxxx='+str(random.random())
    url_support = protocol+"://"+host+url_tmp2
    GET(url_support,ip_list)
    GET(url_adopt,ip_list)
    time_str = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    print 'voter#%d, %s' % (i, time_str)
