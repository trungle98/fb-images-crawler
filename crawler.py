from threading import Thread

from selenium import webdriver
from time import sleep
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import urllib
import requests
import pickle
import multiprocessing as mp
import pandas as pd
import numpy as np

import os

from selenium.webdriver.remote.webelement import WebElement

import random
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
    def login_using_cookie(self, cookies):
        self.browser.get('https:facebook.com')
        # cookies = pickle.load(open("cookie.pkl", "rb"))
        for cookie in cookies:
            self.browser.add_cookie(cookie)
            print(cookie)
        self.browser.refresh()
        sleep(2)
        
        print("loged in")

    def getPhoto(self, uid):

        sleep(2)
        self.browser.get('https:facebook.com/' + uid + '/photos')
        elm = self.browser.find_elements_by_xpath(
            '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[1]/div[2]/div/div/div[1]/div/div/div/a')

        print("avt=================" + str(len(elm)))

        for e in elm:
            print("in iterior")
            try:
                print("href:" + str(e))
                src = e.get_attribute('href')
                print(src)
                self.browser.get(src)
                sleep(4)
                img_avt = self.browser.find_elements_by_xpath(
                    '/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img')
                for img in img_avt:
                    avatar = img.get_attribute('src')
                    print(f"source avatar======================: {avatar}")
                    print("avatar===========" + str(avatar))
                    response = requests.get(avatar)

                with open(f"img-test/avatar-{uid}.jpg", "wb") as file:
                    file.write(response.content)
                    print(src)
                    self.images.append(f'avatar-{uid}.jpg')
                    self.avatar.append(1)
            except Exception as e:
                print('error when save avt: ' + e)
                break
        sleep(2)
        for i in range(10):
            self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
        sleep(2)
        count = 0
        arr_link = []
        #element = self.browser.find_elements_by_class_name('oajrlxb2')
        element = self.browser.find_elements_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div/div/div/div/div/div[3]')
        for elm in element:

            child_elm = elm.find_elements_by_class_name('oajrlxb2')
            for e in child_elm:
                src = e.get_attribute('href')
                print(src)
                arr_link.append(src)

        for link in arr_link:
            self.browser.get(link)
            sleep(2)
            img = self.browser.find_element_by_xpath('/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div[1]/div/div[1]/div/div[2]/div/div/div/img')
            img_src = img.get_attribute('src')
            response = requests.get(img_src)

            with open(f"img-test/{count}-{uid}.jpg", "wb") as file:
                file.write(response.content)
                print(src)
                self.images.append(f'{count}-{uid}.jpg')
                self.avatar.append('0')
            count += 1
        dict = {'Image': self.images, 'Avatar': self.avatar}
        df = pd.DataFrame(dict)
        df.to_csv(f'img-test/dataset/{uid}.csv')


def readUid():
        data = pd.read_csv('uid/uid2.csv')
        data['uid'] = data['uid'].astype(str)
        newdata = []
        for data in data['uid']:
            uid = data.split(',')
            newdata.append(uid[0])
        return newdata
def removeUid(uids):
    dict = {'uid': uids}
    df = pd.DataFrame(dict)
    df.to_csv(f'uid/uid.csv')

n = 0

# m.login()
# m.getPhoto(uids[0])
# print(uids)
def run_app():
    m = Crawler()
    uids = readUid()
    for i in range(len(uids)):
        uid = random.choice(uids)
        try:  
            print(f"n is: {n}")
            m.login_using_cookie([
{
    "domain": ".facebook.com",
    "expirationDate": 1625917370,
    "hostOnly": False,
    "httpOnly": False,
    "name": "_fbp",
    "path": "/",
    "SameSite": "lax",
    "secure": False,
    "session": False,
    "storeId": "0",
    "value": "fb.1.1616083832341.623865440",
    "id": 1
},
{
    "domain": ".facebook.com",
    "expirationDate": 1649761069.64812,
    "hostOnly": False,
    "httpOnly": False,
    "name": "c_user",
    "path": "/",
    "SameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "100006688606351",
    "id": 2
},
{
    "domain": ".facebook.com",
    "expirationDate": 1676688325.137943,
    "hostOnly": False,
    "httpOnly": True,
    "name": "datr",
    "path": "/",
    "SameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "w9QtYJxyIXA4HC9fTxSCW0J0",
    "id": 3
},
{
    "domain": ".facebook.com",
    "expirationDate": 1626001067.648171,
    "hostOnly": False,
    "httpOnly": True,
    "name": "fr",
    "path": "/",
    "SameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1RINyOyHzAyJS3wNf.AWUo8ZYyBDvdQku2D-tcav_F70Q.BgdBvB.O8.AAA.0.0.BgdCeu.AWXkz74ddOs",
    "id": 4
},
{
    "domain": ".facebook.com",
    "expirationDate": 1618245069.735605,
    "hostOnly": False,
    "httpOnly": False,
    "name": "locale",
    "path": "/",
    "SameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "vi_VN",
    "id": 5
},
{
    "domain": ".facebook.com",
    "hostOnly": False,
    "httpOnly": False,
    "name": "presence",
    "path": "/",
    "SameSite": "unspecified",
    "secure": True,
    "session": True,
    "storeId": "0",
    "value": "C%7B%22t3%22%3A%5B%7B%22i%22%3A%22u.100003848175915%22%7D%5D%2C%22utc3%22%3A1618225503120%2C%22lm3%22%3A%22u.100003848175915%22%2C%22v%22%3A1%7D",
    "id": 6
},
{
    "domain": ".facebook.com",
    "expirationDate": 1681297071.648034,
    "hostOnly": False,
    "httpOnly": True,
    "name": "sb",
    "path": "/",
    "SameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "w9QtYEqs-RlsrCtq_3F-6mPr",
    "id": 7
},
{
    "domain": ".facebook.com",
    "expirationDate": 1618315072.685648,
    "hostOnly": False,
    "httpOnly": True,
    "name": "spin",
    "path": "/",
    "SameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "r.1003605869_b.trunk_t.1618225072_s.1_v.2_",
    "id": 8
},
{
    "domain": ".facebook.com",
    "expirationDate": 1618829869,
    "hostOnly": False,
    "httpOnly": False,
    "name": "wd",
    "path": "/",
    "SameSite": "lax",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "1853x949",
    "id": 9
},
{
    "domain": ".facebook.com",
    "expirationDate": 1649761069.648146,
    "hostOnly": False,
    "httpOnly": True,
    "name": "xs",
    "path": "/",
    "SameSite": "no_restriction",
    "secure": True,
    "session": False,
    "storeId": "0",
    "value": "12%3AAohj6Ynd6qtFYA%3A2%3A1618225070%3A17170%3A6381",
    "id": 10
}
])
            sleep(10)
            m.getPhoto(uid)
            print(f"===============================NUM_OF_UID_BEFORE_REMOVE UID {uid}============================================")
            print(f"========================       {len(uids)}         =======================")
            uids.remove(uid)
            removeUid(uids)
            print(f"===============================NUM_OF_UID_AFTER_REMOVE UID {uid}============================================")
            print(f"========================       {len(uids)}         =======================")
        except Exception as e:
            print(e)

        
number_of_threads = 5
threads = []
run_app()
