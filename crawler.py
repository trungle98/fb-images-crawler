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
        self.images = []
        self.avatar = []
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
            avt = self.browser.find_elements_by_tag_name('image')

            print(avt)
            try:
                for e in avt:
                    src = e.get_attribute('xlink:href')
                    reponse = requests.get(src)
                    print(f"source avatar======================: {reponse}")
                    with open(f"images/avatar-{uid}.jpg", "wb") as file:
                        file.write(reponse.content)
                        print(src)
                        self.images.append(f'avatar-{uid}.jpg')
                        self.avatar.append('1')
            except:
                print('error when save avt')
                continue
            for i in range(2):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)

            elements  = self.browser.find_elements_by_class_name('opwvks06')
            count = 0
            print(f'element==========={elements}')
            for e in elements:
                src = e.get_attribute('src')
                print(src)
                response = requests.get(src)

                with open(f"images/{count}-{uid}.jpg", "wb") as file:
                    file.write(response.content)
                    self.images.append(f'{count}-{uid}.jpg')
                    self.avatar.append('0')
                count+=1
            dict = {'images': self.images, 'avatar': self.avatar}
            df = pd.DataFrame(dict)
            df.to_csv('dataset.csv')


m = Crawler()
m.login()
sleep(10)
uid = m.readUid()

m.savePhoto(uid)
