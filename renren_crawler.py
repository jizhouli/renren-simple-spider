#!/usr/bin/env python
# -*- coding: utf-8 -*-
#author: jizhouli@126.com

import os
import sys

import re
import json

import urllib
import urllib2
import cookielib

from lib.logger_service import logger

class RenRenCrawler(object):
    def __init__(self):
        pass

    def set_cookie(self):
        # 设置cookie
        cookie=cookielib.CookieJar()
        opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        urllib2.install_opener(opener)
        logger.info('set cookie')

    def login(self, user, password):
        headers = {
            'Host': 'www.renren.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:10.0.2) Gecko/20100101 Firefox/10.0.2',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-cn,zh;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://www.renren.com/SysHome.do',
            #'Content-Length': '133', # USELESS
            #'Cookie': '_r01_=1; depovince=BJ; jebecookies=f6bce625-6dbc-4f9a-9a29-58a629eac5da|||||; idc=tel; ick=35776a1f-d2e0-4f25-805a-59533875f319; loginfrom=null; feedType=37491_hot; JSESSIONID=abcgo0AVJR7s7fCIqDdBt; anonymid=h15tajwhbuns1e', # USELESS
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
        }
    
        param = {
            'email': user,
            'password': password,
            'icode': '',
            'origURL': 'http://www.renren.com/home',
            'domain': 'renren.com',
            'key_id': '1',
            '_rtk': 'c59b27d3',
        }
    
        url = 'http://renren.com/ajaxLogin/login' 
        
        postdata=urllib.urlencode(param)
        req = urllib2.Request(url, postdata, headers)
        login_response= urllib2.urlopen(req)
        logger.info('login ' + user)
        
        ret =login_response.read()
        #logger.info(ret)
    
        pass

    def get_friends_list(self):
        friends = []
        friends_id = []

        req=urllib2.urlopen('http://friend.renren.com/myfriendlistx.do#item_0')
        ret_html =req.read()
        logger.info('get friends list')

        friends_json = ''
        m = re.search(r'var friends=(.*);', ret_html)
        if m:
            friends_json = m.group(1)
        else:
            logger.info('can`t find friend list')
            return False, friends, friends_id

        # head
        # <type 'unicode'>
        # name
        # <type 'unicode'>
        # mo
        # <type 'bool'>
        # selected
        # <type 'bool'>
        # vip
        # <type 'bool'>
        # groups
        # <type 'list'>
        # id
        # <type 'int'>

        friends = json.loads(friends_json)
        logger.info('friends total:\t' + str(len(friends)))
        for f in friends:
            friends_id.append(f['id'])
            logger.info('name:    \t' + f['name'])
            logger.info('id:      \t' + str(f['id']))
            logger.info('mo:      \t' + str(f['mo']))
            logger.info('vip:     \t' + str(f['vip']))
            logger.info('selected:\t' + str(f['selected']))
            logger.info('groups:  \t')
            for g in f['groups']:
                logger.info('         \t' + g)
            logger.info('')

        logger.info('friends id: ' + str(friends_id))
        return True, friends, friends_id

    def get_maybe_friends_list(self):
        maybe_friends = []
        maybe_friends_id = []

        req=urllib2.urlopen('http://friend.renren.com/myrelationperson.do')
        ret_html =req.read()
        logger.info('get maybe friends list')

        maybe_friends_json = ''
        m = re.search(r'var maybe_groups = (.*);', ret_html)
        if m:
            maybe_friends_json = m.group(1)
        else:
            logger.info('can`t find maybe friend list')
            return False, maybe_friends, maybe_friends_id

        maybe_friends = json.loads(maybe_friends_json)
        logger.info('maybe friends total:\t' + str(len(maybe_friends)))
        for fs in maybe_friends:
            logger.info('name:      \t' + fs['name'])
            logger.info('type:      \t' + fs['type'])
            logger.info('morelink:  \t' + fs['morelink'])
            logger.info('count:     \t' + str(fs['count']))
            for f in fs['people']:
                maybe_friends_id.append(f['id'])
                indent = ' '*4
                logger.info(indent + 'name:     \t' + f['name'])
                logger.info(indent + 'id:       \t' + str(f['id']))
                logger.info(indent + 'gender:   \t' + f['gender'])
                logger.info(indent + 'tinyurl:  \t' + f['tinyurl'])
            logger.info('')

        logger.info('maybe friends id: ' + str(maybe_friends_id))

        return True, maybe_friends, maybe_friends_id

def main():

    if len(sys.argv) != 3:
        logger.info('argument num is invalid - ' + str(len(sys.argv)))
        logger.info(' ')
        logger.info('>> python renren_crawler.py user password')
        sys.exit(1)
    
    logger.info('ren ren crawler, start...')

    user = sys.argv[1]
    password = sys.argv[2]

    # 实例化人人蜘蛛
    renren = RenRenCrawler()

    # 设置cookie启用
    renren.set_cookie()

    # 登陆人人
    renren.login(user, password)

    ## 获取好友列表
    renren.get_friends_list()

    # 获取推荐好友列表
    renren.get_maybe_friends_list()

    logger.info('ren ren crawler, stop.')
    pass

if __name__ == '__main__':
    main()
