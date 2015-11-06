#!/usr/bin/env python
# -*- coding: utf-8 -*- 
__author__ = "ivc_ShherbakovIV"
__date__ = "$Nov 5, 2015 10:53:56 AM$"

from grab import Grab
import json
import logging
from lxml import etree
from lxml.html import fromstring
import re
import requests
import sqlite3
from urllib.parse import urljoin


class TgBot:
    TELEGRAM_BOT_TOKEN = ''
    TELEGRAM_API_ENDPOINT = 'https://api.telegram.org/bot%(token)s/%(method)s'
    TELEGRAM_CHAT_ID = ''

    def send_message(self,text, method='sendMessage'):
        try:
            response = requests.post(
                                     self.TELEGRAM_API_ENDPOINT % {
                                     'token': self.TELEGRAM_BOT_TOKEN,
                                     'method': method,
                                     },
                                     data={
                                     'chat_id': self.TELEGRAM_CHAT_ID,
                                     'text': text,
                                     }
                                     ).content
            json_doc = json.loads(response)
            if not json_doc.get('ok'):
                raise Exception(
                                json_doc.get('description') or 'not OK, ok'
                                )
            return json_doc
        except Exception as e:
            logging.error('API Error :: %s' % str(e))
            return

class AvitoDB:
    dbname = 'avito.db'
    sqlSelect = 'SELECT * FROM history WHERE id=?'
    sqlInsert = "INSERT INTO history VALUES(?)"
        
    def print_db_ame(self):
        print(self.dbname)
        
    def save(self, data):
        con = sqlite3.connect(self.dbname)
        with con:    
            cur = con.cursor()    
            cur.execute(self.sqlInsert, (data, ))
            
    def find(self, id):
        con = sqlite3.connect(self.dbname)
        with con:    
            cur = con.cursor()    
            cur.execute(self.sqlSelect, (id, ))
        data = cur.fetchall()
        if len(data) == 0:
            return False
        else:
            return True

class ModelFind:    
    def __init__(self, cat, keyword):
        self.cat = cat
        self.keyword = keyword
        

class Avito:
    db = AvitoDB()
    tgBot = TgBot()
    url = 'https://avito.ru'

    def __init__(self):
        self.ps4 = ModelFind('/irkutsk/igry_pristavki_i_programmy', ['ps4', ])
        self.wiiu = ModelFind('/irkutsk/igry_pristavki_i_programmy', ['wii u', ])
 
        
    def findPS4(self):
        self.grab(self.ps4)
    def findWIIU(self):
        self.grab(self.wiiu)  
    
    def find(self):
        print(find)
    
    
    def grab(self, model):
        logging.basicConfig(level=logging.DEBUG)
        g = Grab()
        g.setup(proxy='proxy.esrr.oao.rzd:3128', proxy_type='http', proxy_userpwd='ESRR\\ivc_ShherbakovIV:Huqbvajp31337$$$')
        g.go('%s%s?p=1&q=%s' % (self.url, model.cat, model.keyword), log_file='out.html')        
        print(len(g.doc.select('//div[contains(@class, "c-b-0")]')))
        div = g.doc.select('//div[contains(@class, "c-b-0")]')
        for i in div: 
            subject = i.html()
            date = ''
            link = ''
            name = ''
            price = '0'
            id = '0'
            match = re.search(' <div class="date c-2">(.+?)</div>', subject, re.DOTALL | re.MULTILINE)
            if match:
                date = match.group(1).strip()

            match = re.search("""<div class="description"> <h3 class="title"> <a href="(.+?)" title="(.+?)">""", subject, re.DOTALL | re.MULTILINE)
            if match:
                link = match.group(1).strip()
                name = match.group(2).strip()
                match2 = re.search(r"_(\d+?)$", link, re.DOTALL | re.MULTILINE)
                if match2:
                    id = match2.group(1)
            match = re.search(r"([0-9&nbsp;\s]+?\s+?руб\.)", subject, re.DOTALL | re.MULTILINE)
            if match:
                price = match.group(1).strip()

            if not self.db.find(id):
                print("New Item!")
                print(id)
                print(date)
                print(link)
                print(name)
                print(price)
                self.db.save(id)
                self.tgBot.send_message('%s\rЦена: %s\r%s%s' % (name, price, self.url, link))
                print('==================================')
    

t = Avito()
t.findPS4()
#t.findWIIU()

#print(i.select('//*[contains(@class, "date")]')[0].html())
#print(g.doc.select('//div[contains(@class, "c-b-0")]')[1].html())
        