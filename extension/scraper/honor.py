from idref import USER_AGENT_LIST

import os
import random
import urllib
import urllib.request


currentDir = os.path.dirname(__file__)


url0 = "https://static.wikia.nocookie.net/leagueoflegends/images/c/c5/Honor_Level_0.png/revision/latest?cb=20181227192238"
url1 = "https://static.wikia.nocookie.net/leagueoflegends/images/d/d2/Honor_Level_1.png/revision/latest?cb=20181227193006"
url2 = "https://static.wikia.nocookie.net/leagueoflegends/images/4/46/Honor_Level_2.png/revision/latest?cb=20170629212458"
url3 = "https://static.wikia.nocookie.net/leagueoflegends/images/2/21/Honor_Level_3_Flair.png/revision/latest?cb=20180422200256"
url4 = "https://static.wikia.nocookie.net/leagueoflegends/images/6/6a/Honor_Level_4_Flair.png/revision/latest?cb=20180422200233"
url5 = "https://static.wikia.nocookie.net/leagueoflegends/images/0/0e/Honor_Level_5_Flair.png/revision/latest?cb=20180422200148"
name = "mastery-1"

urls = [
    url0,
    url1,
    url2,
    url3,
    url4,
    url5,
]

for idx, url in enumerate(urls):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
    filename, headers = opener.retrieve(
        url,
        os.path.join(
            currentDir,
            "..", "assets", "images", "honor", f"honor-{idx}.png"
        )
    )