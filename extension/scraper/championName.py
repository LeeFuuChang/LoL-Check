from selenium import webdriver
from bs4 import BeautifulSoup

from idref import REFERENCE

import os
import time
import json


def writelog(txt):
    with open(os.path.join(FILE_DIR, "log.txt"), "a") as f:
        f.write(txt+"\n")



FILE_DIR = os.path.dirname(__file__)


driver = webdriver.Chrome(os.path.join(FILE_DIR, "chromedriver.exe"))

url = f"https://lol.garena.tw/champions"
driver.get(url)

t = time.time()
while(time.time()-t < 3):
    soup = BeautifulSoup(driver.page_source, "lxml")

    boxs = soup.find("div", class_="boxs")
    if boxs != None:
        break

if boxs is None: 
    quit()

new = REFERENCE.copy()

for idx, championENG in REFERENCE.items():
    box = boxs.find("a", href=f"/champions/{championENG}")

    if box is None: 
        print(f"\n\nFail on {championENG}\n\n")
        continue
    championTW = box.find("span", class_="name").text
    print(f"\n\nFound {championENG} => {championTW}\n\n")
    new[idx] = championTW

with open(os.path.join(FILE_DIR, "championNameOutput.json"), "w") as f:
    json.dump(new, f, ensure_ascii=False)
