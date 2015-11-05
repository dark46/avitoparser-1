# To change this license header, choose License Headers in Project Properties.
# To change this template file, choose Tools | Templates
# and open the template in the editor.

__author__ = "ivc_ShherbakovIV"
__date__ = "$Nov 5, 2015 10:53:56 AM$"

from lxml.html import fromstring
import requests
import sqlite3
from urllib.parse import urljoin

class AvitoDB:
    dbname = ''
    sqlSelect = 'SELECT * FROM history WHERE id=?'
    sqlInsert = "INSERT INTO history VALUES(?)"
    def __init__(self, c):
        self.dbname = c
        
    def print_db_ame(self):
        print(self.dbname)
        
    def save(self, data):
        con = sqlite3.connect(self.dbname)
        with con:    
            cur = con.cursor()    
            cur.execute(self.sqlInsert, data)
            commit()
            
    def find(self, id):
        con = sqlite3.connect(self.dbname)
        with con:    
            cur = con.cursor()    
            cur.execute(self.sqlSelect, id)
            commit()
        data = cur.fetchall()
        if len(data) == 0:
            return False
        else:
            print("find")
            return True

class ModelFind:    
    def __init__(self, cat, keyword):
        self.cat = cat
        self.keyword = keyword
        

class Avito:
    dbname = 'avito.db'
    url = 'http://avito.ru'

    def __init__(self):
        self.ps4 = ModelFind('/irkutsk/igry_pristavki_i_programmy', ['ps4',])
        print(self.ps4.cat)
        print(self.ps4.keyword)    
    
    def getPhone(url):
        headers = {'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 5.1; ru; rv:1.9.0.13) Gecko/2009073022 Firefox/3.0.13'}
        session = requests.session()
        resp = session.get(url, headers=headers)
        html = fromstring(resp.content)
        href = html.xpath("//a[@id='showPhoneBtn']/@href")[0]
        url = urljoin(resp.url, href)
        resp = session.get(url)
        html = fromstring(resp.content)
        phone = html.xpath("//li[@class='para m_item_phone']/a/text()")[0]
        return phone
    
    def grab(self,model):
        print("grab")
    

t=Avito()
t.grab('123')
    

        
    
    
        