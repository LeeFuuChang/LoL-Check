from selenium import webdriver
from bs4 import BeautifulSoup

from idref import USER_AGENT_LIST

import os
import time
import random
import urllib
import urllib.request

currentDir = os.path.dirname(__file__)

def writelog(txt):
    with open(os.path.join(FILE_DIR, "log.txt"), "a") as f:
        f.write(txt+"\n")

def writeFailed(txt):
    with open(os.path.join(FILE_DIR, "failed.txt"), "a") as f:
        f.write(txt+"\n")


WEB_URL = "https://lol.garena.tw/items"
FILE_DIR = os.path.dirname(__file__)

driver = webdriver.Chrome(os.path.join(FILE_DIR, "chromedriver.exe"))
driver.get(WEB_URL)
time.sleep(30)
t = time.time()
while(time.time()-t < 10):
    soup = BeautifulSoup(driver.page_source, "lxml")

    wrapper = soup.find("div", {"class":"boxs"})
    if wrapper != None:
        break

for box in wrapper.find_all("a", {"class":"box"}):
    imgBox = box.find("div", {"class":"imgBox"})
    url = imgBox.find("img")["src"]
    idx = url.split("/")[-1][:-4]

    print(url)

    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
    filename, headers = opener.retrieve(
        url,
        os.path.join(
            currentDir,
            "..", "assets", "images", "items", f"{idx}.png"
        )
    )