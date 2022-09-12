class ClientData:
    CurrentSeason = 0
    RiotClientAccessUrl = ""
    RiotUserAccessToken = ""
    def IsFilled(self):
        return (
            self.CurrentSeason != 0
        ) and (
            self.RiotClientAccessUrl != ""
        ) and (
            self.RiotUserAccessToken != ""
        )