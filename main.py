from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib
import requests


import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bf
import os

class Crawler:

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='chromedriver.exe')

    def login(self):

        self.browser.get('https:facebook.com')

        txtUser = self.browser.find_element_by_id('email')
        txtUser.send_keys('namthaint8487@gmail.com')

        txtPass = self.browser.find_element_by_id('pass')
        txtPass.send_keys('#nam7thai8@84')

        txtPass.send_keys(Keys.ENTER)

    def readUid(self):
        data = pd.read_csv('uid.csv')
        data['uid'] = data['uid'].astype(str)
        newdata = []
        for data in data['uid']:
            uid = data.split('.')
            newdata.append(uid[0])

        return newdata


    def savePhoto(self, uids):

        for uid in uids:
            sleep(4)
            self.browser.get('https:facebook.com/'+uid+'/photos')
            for i in range(2):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
            break
        elements  = self.browser.find_elements_by_tag_name('img')
        count = 0
        for e in elements:
            src = e.get_attribute('src')
            reponse = requests.get(src)
            with open(f"images/{uid}-{count}.jpg", "wb") as file:
                file.write(reponse.content)
                print(src)
            count+=1
        self.browser.close()

m = Crawler()
m.login()
sleep(10)
uid = m.readUid()

m.savePhoto(uid)