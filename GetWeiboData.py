#coding:utf-8
import time
from splinter import Browser
import re
import sys

global browser
browser = Browser('firefox')

def login(username, password):
    global browser
    
    browser.visit('http://weibo.com/login')
    browser.find_by_name('username')[1].fill(username)
    browser.find_by_name('password')[1].fill(password)
    browser.find_by_css('.W_btn_g')[1].click()

def getdata(url, log):
    global browser

    h_log = open(log, 'wb')
    e_title = re.compile(r'&lt;div&gt;&lt;p&gt;(.+?)&lt;span style=\\"color: rgb\(55, 72, 91\);\\"&gt;')
    c_title = re.compile(r'&lt;p style=\\"color: rgb\(167, 167, 167\);\\"&gt; \\"(.+?)\\"&lt;\\/p&gt;')
    p_time = re.compile(r'&lt;span class=\\"time\\"&gt;(.+?)&lt;\\/span&gt;')
    for u in url:
        print u
        time.sleep(1)
        e_list = []
        c_list = []
        browser.visit(u)
        date = p_time.findall(browser.html)[0]
        date = date.split(' ')[0]
        for i in e_title.findall(browser.html):
            e_list.append(i.replace('&amp;', '').replace('nbsp;', '').replace(',', '.'))
        for i in c_title.findall(browser.html):
            c_list.append(i.replace('&amp;', '').replace('nbsp;', '').replace('\\', '').replace(',', '.'))

        for i in xrange(min(len(e_list), len(c_list))):
            o = '%s,%s,%s\n' % (date.encode('gbk', 'ignore'), e_list[i].encode('gbk', 'ignore'), c_list[i].encode('gbk', 'ignore'))
            h_log.write(o)
    browser.quit()


def getList():
    global browser
    url = []
    browser.visit('http://weibo.com/p/1006065582522936/wenzhang')
    p = re.compile(r'(\d+\?mod=zwenzhang)\\"&gt;&lt;')
    for i in p.findall(browser.html):
        u = 'http://weibo.com/p/%s' % i
        #print u
        url.append(u)
    pi = 1
    over = False
    while(over == False):
        pi += 1
        over = True
        time.sleep(5)
        page = 'http://weibo.com/p/1006065582522936/wenzhang?cfs=600&Pl_Core_ArticleList__42_filter=&Pl_Core_ArticleList__42_page=%d#Pl_Core_ArticleList__42' % pi
        #print page
        browser.visit(page)
        for i in p.findall(browser.html):
            u = 'http://weibo.com/p/%s' % i
            #print u
            url.append(u)
            over = False

    #browser.quit()
    return url


if __name__ == '__main__':
    username = ''
    password = ''
    login(username, password)
    time.sleep(5)
    result = getList()
    #result = ['http://weibo.com/p/1001603854301528255366?mod=zwenzhang']
    getdata(result, sys.argv[1])
    #print len(result)
