import csv

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
            self.browser.get('https:facebook.com/' + uid + '/photos')
            for i in range(5):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
            elements = self.browser.find_elements_by_tag_name('img')
            count = 0
            for e in elements:
                src = e.get_attribute('src')
                reponse = requests.get(src)
                with open(f"images/{uid}-{count}.jpg", "wb") as file:
                    file.write(reponse.content)
                    print(src)
                    img_src = f"images/{uid}-{count}.jpg"
                    print(img_src)
                image = face_recognition.load_image_file(img_src)
                face_locations = face_recognition.face_locations(image)
                print("=============face===============")
                print(face_locations)
                if len(face_locations) == 0:
                    os.remove(f"images/{uid}-{count}.jpg")
                    print('remove')
                count += 1
                write_last_uid(uid)
            uids.remove(uid)
            rewrite_csv(uids)
        self.browser.close()


def read_last_uid():
    f = open("last_uid.txt", "r")
    print(f.read())
    return str(f.read())

def write_last_uid(uid):
    with open("last_uid.txt", "r") as f:
        lines = f.readlines()
    with open("last_uid.txt", "w") as f:
        for line in lines:
            if line.strip("\n") != "nickname_to_delete":
                f.write(line)
    with open("last_uid.txt", "a") as file:
        file.write(uid)
def rewrite_csv(uids):
    with open('uid.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow("uid")

        # writing the data rows
        csvwriter.writerows(uids)
m = Crawler()

m.login()
sleep(10)
uid = m.readUid()

m.savePhoto(uid)
