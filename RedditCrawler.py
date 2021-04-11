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

    def savePhoto(self,link):

            self.browser.get(link)
            for i in range(500):
                self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                sleep(2)
            elements = self.browser.find_elements_by_class_name('ImageBox-image')
            count = 0
            for e in elements:
                try:
                    src = e.get_attribute('src')
                    reponse = requests.get(src)

                    with open(f"images-fat-2/{count}.jpg", "wb") as file:
                        file.write(reponse.content)
                        print(src)
                        img_src = f"images-fat-2/{count}.jpg"
                        print(img_src)
                    # image = face_recognition.load_image_file(img_src)
                    # face_locations = face_recognition.face_locations(image)
                    # print("=============face===============")
                    # print(face_locations)
                    # if len(face_locations) == 0:
                    #     os.remove(f"images-fat-2/{count}.jpg")
                    #     print('remove')
                    # else:
                    #     count += 1
                    count += 1
                except:
                    print("error when saving file")


m = Crawler()

m.savePhoto('https://www.reddit.com/r/progresspics/top/?t=all')
