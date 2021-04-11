import _thread
import csv
from _thread import *
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib
import requests
import face_recognition
import os
import pandas as pd
import numpy as np

import os


class Crawler:

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path='chromedriver')

        self.images = []
        self.avatar = []
    def login(self):

        self.browser.get('https:facebook.com')

        txtUser = self.browser.find_element_by_id('email')
        txtUser.send_keys('namthaint8487@gmail.com')

        txtPass = self.browser.find_element_by_id('pass')
        txtPass.send_keys('#nam7thai8@84')

        txtPass.send_keys(Keys.ENTER)
        print("Loged in")
    def readUid(self):
        print('read uid')
        data = pd.read_csv('uid/uid2.csv')
        data['uid'] = data['uid'].astype(str)
        newdata = []
        for data in data['uid']:
            uid = data.split('.')
            newdata.append(uid[0])

        return newdata

    def save_avatar(self, uid):
        print(f'accessed {uid}')
        # self.browser.get('https://www.facebook.com/media/set/?set=a.' + uid + '&type=3')
        self.browser.get('https://www.facebook.com/' + uid + '/photos')
        elements = self.browser.find_elements_by_tag_name('image')

        print(elements)
        try:
            for e in elements:

                src = e.get_attribute('xlink:href')
                reponse = requests.get(src)
                print(f"source avatar======================: {src}")
                with open(f"img-test/avatar-{uid}.jpg", "wb") as file:
                    file.write(reponse.content)
                    print(src)
                    self.images.append(f'avatar-{uid}.jpg')
                    self.avatar.append('1')
        except:
            print('error when save avt')
        for i in range(5):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
        elements = self.browser.find_elements_by_tag_name('img')
        count = 0
        print(elements)
        try:
            for e in elements:
                print(count)
                src = e.get_attribute('src')
                reponse = requests.get(src)
                print(f"source images======================: {src}")
                with open(f"img-test/{count}-{uid}.jpg", "wb") as file:
                    file.write(reponse.content)
                    print(src)
                    self.images.append(src)
                    self.avatar.append('0')
        except:
            print('error when save images')

            count += 1
        dict = {'images': self.images, 'avatar': self.avatar}
        df = pd.DataFrame(dict)
        df.to_csv('dataset.csv')
    def create_folder(self):
        try:
            os.mkdir('img-test')
        except:
            print('error or this folder is created')
m = Crawler()
m.create_folder()
m.login()
sleep(10)
uid = m.readUid()
threads = []
for i in range(len(uid)):
    try:
        m.save_avatar(uid[i])
    except:
        continue
