from idref import REFERENCE_CHAMPION, USER_AGENT_LIST

import os
import random
import urllib
import urllib.request

currentDir = os.path.dirname(__file__)


for idx, name in REFERENCE_CHAMPION.items():
    opener = urllib.request.URLopener()
    opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
    dest = os.path.join(
        currentDir,
        "..", "assets", "images", "champion", "icon", f"{name}.png"
    )
    filename, headers = opener.retrieve(
        f"https://lolg-cdn.porofessor.gg/img/d/champion-icons/12.10/120/{idx}.png",
        dest
    )