from idref import USER_AGENT_LIST

import os
import random
import urllib
import urllib.request


currentDir = os.path.dirname(__file__)


url1 = "https://static.wikia.nocookie.net/leagueoflegends/images/9/95/Cleanse.png/revision/latest?cb=20180514002812"
url2 = "https://static.wikia.nocookie.net/leagueoflegends/images/4/4a/Exhaust.png/revision/latest?cb=20180514003128"
url3 = "https://static.wikia.nocookie.net/leagueoflegends/images/7/74/Flash.png/revision/latest?cb=20180514003149"
url4 = "https://static.wikia.nocookie.net/leagueoflegends/images/a/ab/Ghost.png/revision/latest?cb=20180514003209"
url5 = "https://static.wikia.nocookie.net/leagueoflegends/images/6/6e/Heal.png/revision/latest?cb=20180514003319"
url6 = "https://static.wikia.nocookie.net/leagueoflegends/images/0/05/Smite.png/revision/latest?cb=20180514003641"
url7 = "https://static.wikia.nocookie.net/leagueoflegends/images/e/e8/Teleport.png/revision/latest?cb=20180514003653"
url8 = "https://static.wikia.nocookie.net/leagueoflegends/images/d/d7/Clarity.png/revision/latest?cb=20180514002750"
url9 = "https://static.wikia.nocookie.net/leagueoflegends/images/f/f4/Ignite.png/revision/latest?cb=20180514003345"
url10 = "https://static.wikia.nocookie.net/leagueoflegends/images/c/cc/Barrier.png/revision/latest?cb=20180514002510"
url11 = "https://static.wikia.nocookie.net/leagueoflegends/images/4/4d/Mark.png/revision/latest?cb=20180514003608"

urls = [
    [url1,"1", "Cleanse"],
    [url2,"3", "Exhaust"],
    [url3,"4", "Flash"],
    [url4,"6", "Ghost"],
    [url5,"7", "Heal"],
    [url6,"11", "Smite"],
    [url7,"12", "Teleport"],
    [url8,"13", "Clarity"],
    [url9,"14", "Ignite"],
    [url10,"21", "Barrier"],
    [url11,"32", "Mark"],
    [url11,"39", "Mark"],
]

for idx, (url, spellId, name) in enumerate(urls):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
    filename, headers = opener.retrieve(
        url,
        os.path.join(
            currentDir,
            "..", "assets", "images", "spells", f"{spellId}.png"
        )
    )
    filename, headers = opener.retrieve(
        url,
        os.path.join(
            currentDir,
            "..", "assets", "images", "spells", f"{name}.png"
        )
    )