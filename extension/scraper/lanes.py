from idref import USER_AGENT_LIST

import os
import random
import urllib
import urllib.request


currentDir = os.path.dirname(__file__)


url1 = "https://static.wikia.nocookie.net/leagueoflegends/images/e/ef/Top_icon.png/revision/latest/scale-to-width-down/50?cb=20181117143602"
url2 = "https://static.wikia.nocookie.net/leagueoflegends/images/1/1b/Jungle_icon.png/revision/latest/scale-to-width-down/50?cb=20181117143559"
url3 = "https://static.wikia.nocookie.net/leagueoflegends/images/9/98/Middle_icon.png/revision/latest/scale-to-width-down/50?cb=20181117143644"
url4 = "https://static.wikia.nocookie.net/leagueoflegends/images/9/97/Bottom_icon.png/revision/latest/scale-to-width-down/50?cb=20181117143632"
url5 = "https://static.wikia.nocookie.net/leagueoflegends/images/e/e0/Support_icon.png/revision/latest/scale-to-width-down/50?cb=20181117143601"

urls = [
    [url1,"TOP"],
    [url2,"JUNGLE"],
    [url3,"MID"],
    [url4,"BOTTOM"],
    [url5,"SUPPORT"],
]

for idx, (url, lane) in enumerate(urls):
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
    filename, headers = opener.retrieve(
        url,
        os.path.join(
            currentDir,
            "..", "assets", "images", "lanes", f"{lane}.png"
        )
    )