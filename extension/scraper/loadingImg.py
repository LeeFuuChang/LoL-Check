from selenium import webdriver
from bs4 import BeautifulSoup

from idref import USER_AGENT_LIST

import os
import time
import random
import urllib
import urllib.request


def writelog(txt):
    with open(os.path.join(FILE_DIR, "log.txt"), "a") as f:
        f.write(txt+"\n")



FILE_DIR = os.path.dirname(__file__)


driver = webdriver.Chrome(os.path.join(FILE_DIR, "chromedriver.exe"))

for filename in os.listdir(os.path.join(FILE_DIR, "..", "assets", "images", "champion", "icon")):
    champion = filename[:-4]

    writelog(f"Loading Champion: {champion}")
    replacedSpace = champion.replace(" ", "+")
    url = f"https://leagueoflegends.fandom.com/wiki/Voice_cast?file={replacedSpace}_OriginalLoading.jpg"
    driver.get(url)

    t = time.time()
    while(time.time()-t < 3):
        soup = BeautifulSoup(driver.page_source, "lxml")

        wrapper = soup.find("div", class_="media")
        writelog(f"Web containing {champion} loading URL: {wrapper is not None}")
        if wrapper != None:
            break
    if wrapper is None: 
        writelog(f"Fail loading champion {champion}\n\n")
        continue

    t = time.time()
    while(time.time()-t < 3):
        soup = BeautifulSoup(driver.page_source, "lxml")

        wrapper = soup.find("div", class_="media")
        img = wrapper.find("img")
        writelog(f"Web containing {champion} loading IMG: {img is not None}")
        if img != None:
            break
    if img is None: 
        writelog(f"Fail loading champion {champion}\n\n")
        continue
    url = img["src"]
    writelog(f"Found champion {champion} loading URL: {url}")
    writelog(f"Success loading champion {champion}\n\n")

    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
    filename, headers = opener.retrieve(
        url, os.path.join(FILE_DIR, "..", "assets", "images", "champion", "loading", f"{champion}.jpg")
    )
