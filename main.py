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
        data = pd.read_csv('uid/uid2.csv')
        data['uid'] = data['uid'].astype(str)
        newdata = []
        for data in data['uid']:
            uid = data.split('.')
            newdata.append(uid[0])

        return newdata

    def savePhoto(self, uids):

        for uid in uids:

            #self.browser.get('https://www.facebook.com/groups/698980760870684/user/' + uid)
            self.browser.get('https://www.facebook.com/' + uid+'/photos')
            for i in range(5):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
            elements = self.browser.find_elements_by_tag_name('img')
            avt = self.browser.find_elements_by_tag_name('image')
            for a in avt:
                src = a.get_attribute('xlink:href')
                reponse = requests.get(src)

                with open(f"img-test/avatar-{uid}.jpg", "wb") as file:
                    file.write(reponse.content)
                    print(src)
                    img_src = f"img-test/avatar-{uid}.jpg"
                    print(img_src)
                image = face_recognition.load_image_file(img_src)
                face_locations = face_recognition.face_locations(image)
                print("=============face===============")
                print(face_locations)
                if len(face_locations) == 0:
                    os.remove(f"img-test/avatar-{uid}.jpg")
                    print('remove')
                else:
                    break
            count = 0
            try:
                for e in elements:
                    src = e.get_attribute('src')
                    reponse = requests.get(src)
                    if count > 4:
                        break
                    with open(f"img-test/{count}-{uid}.jpg", "wb") as file:
                        file.write(reponse.content)
                        print(src)
                        img_src = f"img-test/{count}-{uid}.jpg"
                        print(img_src)
                    image = face_recognition.load_image_file(img_src)
                    face_locations = face_recognition.face_locations(image)
                    print("=============face===============")
                    print(face_locations)
                    if len(face_locations) == 0:
                        os.remove(f"img-test/{count}-{uid}.jpg")
                        print('remove')
                    else:
                        count += 1
                    write_last_uid(uid)
                uids.remove(uid)
                rewrite_csv(uids)
            except:
                uids.remove(uid)
                rewrite_csv(uids)
                continue
        self.browser.close()

def save_avatar(self, uid):
    self.browser.get('https://www.facebook.com/media/set/?set=a.' + uid + '&type=3')
    elements = self.browser.find_elements_by_tag_name('img')

    for e in elements:
        src = e.get_attribute('src')
        reponse = requests.get(src)

        with open(f"img-test/avatar-{uid}.jpg", "wb") as file:
            file.write(reponse.content)
            print(src)
            img_src = f"img-test/avatar-{uid}.jpg"
            print(img_src)
        # image = face_recognition.load_image_file(img_src)
        # face_locations = face_recognition.face_locations(image)
        # print("=============face===============")
        # print(face_locations)
        # if len(face_locations) == 0:
        #     os.remove(f"img-test/avatar-{uid}.jpg")
        #     print('remove')
        # else:
        #     break

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
    with open('uid/uid-female.csv', 'w') as csvfile:
        # creating a csv writer object
        csvwriter = csv.writer(csvfile)

        # writing the fields
        csvwriter.writerow(["uid"])

        # writing the data rows
        csvwriter.writerows([uids])
m = Crawler()

m.login()
sleep(10)
uid = m.readUid()

m.savePhoto(uid)
