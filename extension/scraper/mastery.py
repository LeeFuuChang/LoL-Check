from idref import USER_AGENT_LIST

import os
import random
import urllib
import urllib.request


currentDir = os.path.dirname(__file__)


url1 = "https://static.wikia.nocookie.net/leagueoflegends/images/d/d8/Champion_Mastery_Level_1_Flair.png/revision/latest?cb=20150312005229"
url2 = "https://static.wikia.nocookie.net/leagueoflegends/images/4/4d/Champion_Mastery_Level_2_Flair.png/revision/latest?cb=20150312005244"
url3 = "https://static.wikia.nocookie.net/leagueoflegends/images/e/e5/Champion_Mastery_Level_3_Flair.png/revision/latest?cb=20150312005319"
url4 = "https://static.wikia.nocookie.net/leagueoflegends/images/b/b6/Champion_Mastery_Level_4_Flair.png/revision/latest?cb=20200113041829"
url5 = "https://static.wikia.nocookie.net/leagueoflegends/images/9/96/Champion_Mastery_Level_5_Flair.png/revision/latest?cb=20200113041512"
url6 = "https://static.wikia.nocookie.net/leagueoflegends/images/b/be/Champion_Mastery_Level_6_Flair.png/revision/latest?cb=20200113041636"
url7 = "https://static.wikia.nocookie.net/leagueoflegends/images/7/7a/Champion_Mastery_Level_7_Flair.png/revision/latest?cb=20200113041615"
name = "mastery-1"

urls = [
    url1,
    url2,
    url3,
    url4,
    url5,
    url6,
    url7,
]

for idx, url in enumerate(urls):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
    filename, headers = opener.retrieve(
        url,
        os.path.join(
            currentDir,
            "..", "assets", "images", "mastery", f"mastery-{idx+1}.png"
        )
    )