from idref import REFERENCE_CHAMPION, USER_AGENT_LIST

import os
import random
import urllib
import urllib.request

currentDir = os.path.dirname(__file__)


name = "Bel'Veth"


opener = urllib.request.URLopener()
opener.addheader('User-Agent', random.choice(USER_AGENT_LIST))
dest = os.path.join(
    currentDir,
    "..", "assets", "images", "champion", "loading", f"{name}.jpg"
)
filename, headers = opener.retrieve(
    f"https://static.wikia.nocookie.net/leagueoflegends/images/d/d1/Bel%27Veth_OriginalLoading.jpg/revision/latest?cb=20220524235558",
    dest
)