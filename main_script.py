import os

import requests
from bs4 import BeautifulSoup
from difflib import SequenceMatcher
import time
from selenium import webdriver
import cv2
import numpy as np


url_1 = 'https://peviitor.ro/'
url_2 = 'https://www.footyheadlines.com/'


def compare_html(website_1, website_2):
    res_1 = requests.get(website_1).text
    res_2 = requests.get(website_2).text

    if res_1 == res_2:
        return True
    else:
        return False


def compare_text(website_1, website_2):
    res_1 = requests.get(website_1).text
    res_2 = requests.get(website_2).text

    text_1 = str(BeautifulSoup(res_1, 'lxml').getText)
    text_2 = str(BeautifulSoup(res_2, 'lxml').getText)

    diff = SequenceMatcher(None, text_1, text_2)
    similarity = round(diff.ratio() * 100, 2)

    if similarity > 0.94:
        return True
    else:
        return False


def compare_screenshots(website_1, website_2):

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)

    driver.get(website_1)
    time.sleep(2)
    screenshot_1 = driver.get_screenshot_as_png()
    with open('screenshot_1.png', 'wb') as f:
      f.write(screenshot_1)

    driver.get(website_2)
    time.sleep(2)
    screenshot_2 = driver.get_screenshot_as_png()
    with open('screenshot_2.png', 'wb') as f:
      f.write(screenshot_2)

    driver.quit()

    img1 = cv2.imread('screenshot_1.png')
    img2 = cv2.imread('screenshot_1.png')

    img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    def mse(img1, img2):
        h, w = img1.shape
        diff = cv2.subtract(img1, img2)
        err = np.sum(diff ** 2)
        mse = err / (float(h * w))
        return mse, diff

    error, diff = mse(img1, img2)

    os.remove('screenshot_1.png')
    os.remove('screenshot_2.png')

    if error < 0.1:
        return True
    else:
        return False


def compare(web1, web2):

    if compare_html(web1, web2) and compare_text(web1, web2) and compare_screenshots(web1, web2):
        return True
    else:
        return False

print(compare(url_1, url_2))






