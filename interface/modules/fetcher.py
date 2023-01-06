from .constants import *
from . import functions
from .data import *
import os
from tkinter import messagebox
from threading import Thread

import requests as rq
from urllib3.exceptions import InsecureRequestWarning
rq.packages.urllib3.disable_warnings(InsecureRequestWarning)




class Fetcher:
    storage = "C:\\LoL-Check"
    credict_path = os.path.join("C:\\LoL-Check\\credit.txt")

    def Fetch(self, route):
        if not self.ClientData.IsFilled(): return FAILED_JSON_RETURN.copy()
        try:
            res = rq.get(
                f"{self.ClientData.RiotClientAccessUrl}/{route}", auth=(
                    "riot", f"{self.ClientData.RiotUserAccessToken}"
                ), verify=False
            ).json()
            res = {
                "success" : True,
                "res" : res
            }
        except:
            return FAILED_JSON_RETURN.copy()
        return res



    def __init__(self, root):
        self.root = root

        self.LoLPath = ""
        self.AssertGamePath()

        self.ClientData = ClientData()



    def ValidGamePath(self, path):
        return os.path.exists(os.path.join(path, "lol.version"))



    def SaveGamePath(self, path):
        self.LoLPath = path
        if not os.path.exists(self.storage): os.mkdir(self.storage)
        with open(self.credict_path, "w", encoding="utf-8") as f:
            f.write(self.LoLPath)



    def AssertGamePath(self, callback=lambda s:s):
        print("Start AssertGamePath")
        if not os.path.exists(self.storage): os.mkdir(self.storage)
        flag = False
        for i in range(2):
            if os.path.exists(self.credict_path) and not flag:
                with open(self.credict_path, "r", encoding="utf-8") as f:
                    self.LoLPath = f.read()
                if( not self.ValidGamePath(self.LoLPath) ): flag = True
                else: break
            else:
                messagebox.showinfo("提示", "首次開啟初始化中，請稍後")
                self.SaveGamePath(functions.FindLoLPath())
                break
        callback(self.LoLPath)
        print("Ended AssertGamePath")



    def Initialize(self):
        print("Start Initializing Fetcher")
        LatestClientLog = None
        for file in functions.listdir(f"{self.LoLPath}\\Game\\Logs\\LeagueClient Logs\\"):
            if CLIENT_LOG_FILETYPE in file:
                LatestClientLog = file
                break
        print(f"latestClientLog: {LatestClientLog}")

        with open(LatestClientLog, "r", encoding="utf-8") as f:
            log = f.read()
        log = log.split("Application Version:")[1]
        vsn = int(log[:functions.indexOf(log, ".")])
        print(f"ClientAccessVersion: {vsn}")

        idx = functions.indexOf(log, RIOT_BASE_URL)
        RiotClientAccessUrl = log[idx : functions.indexOf(log, "/", idx+len(RIOT_BASE_URL))]
        RiotUserAccessToken = RiotClientAccessUrl[len(RIOT_BASE_URL) : functions.indexOf(RiotClientAccessUrl, "@")]
        RiotClientAccessUrl = RiotClientAccessUrl[:len(HTTPS)] + RiotClientAccessUrl[functions.indexOf(RiotClientAccessUrl, "@")+1:]
        print(f"RiotClientAccessUrl: {RiotClientAccessUrl}")
        print(f"RiotUserAccessToken: {RiotUserAccessToken}")

        self.ClientData.CurrentSeason = vsn
        self.ClientData.RiotClientAccessUrl = RiotClientAccessUrl
        self.ClientData.RiotUserAccessToken = RiotUserAccessToken
        if self.ClientData.IsFilled(): Thread(target=self.root.UpdateLocal).start()
        print("Ended Initializing Fetcher")



    def LoadPlayer(self, username, puuid):
        if not self.LoLPath: self.AssertGamePath()
        if username is None or puuid is None: return FAILED_JSON_RETURN.copy()

        # Account data
        data = self.Fetch(f"lol-summoner/v1/summoners?name={username}")
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        accountId = data["accountId"]
        summonerId = data["summonerId"]
        summonerLevel = data["summonerLevel"]
        percentCompleteForNextLevel = data["percentCompleteForNextLevel"]

        # Rank data
        data = self.Fetch(f"lol-ranked/v1/ranked-stats/{puuid}")
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        soloRank = {
            "previousSeasonEndTier" : data["queueMap"]["RANKED_SOLO_5x5"]["previousSeasonEndTier"],
            "previousSeasonEndDivision" : data["queueMap"]["RANKED_SOLO_5x5"]["previousSeasonEndDivision"],
            "tier" : data["queueMap"]["RANKED_SOLO_5x5"]["tier"],
            "division" : data["queueMap"]["RANKED_SOLO_5x5"]["division"],
            "leaguePoints" : data["queueMap"]["RANKED_SOLO_5x5"]["leaguePoints"],
            "losses" : 0,
            "wins" : 0,
            "winrate" : 0
        }
        flexRank = {
            "tier" : data["queueMap"]["RANKED_FLEX_SR"]["tier"],
            "division" : data["queueMap"]["RANKED_FLEX_SR"]["division"],
            "leaguePoints" : data["queueMap"]["RANKED_FLEX_SR"]["leaguePoints"],
            "losses" : 0,
            "wins" : 0,
            "winrate" : 0
        }

        # Career data
        positions = [
            {
                "winrate" : 0,
                "wins" : 0,
                "losses" : 0
            },
            {
                "winrate" : 0,
                "wins" : 0,
                "losses" : 0
            },
            {
                "winrate" : 0,
                "wins" : 0,
                "losses" : 0
            },
            {
                "winrate" : 0,
                "wins" : 0,
                "losses" : 0
            },
            {
                "winrate" : 0,
                "wins" : 0,
                "losses" : 0
            }
        ]
        roles = ["TOP","JUNGLE","MID","BOTTOM","SUPPORT"]
        for i in range(len(roles)):
            data = self.Fetch(f"lol-career-stats/v1/summoner-stats/{puuid}/{self.ClientData.CurrentSeason}/rank5solo/{roles[i]}")
            if not data["success"]: continue
            else: data = data["res"]
            if data.get("errorCode", False): continue
            data = data["seasonSummary"][f"{self.ClientData.CurrentSeason}"]["rank5solo"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"]
            positions[i]["wins"] += int(data["victory"])
            positions[i]["losses"] += int(data["defeat"])
            soloRank["wins"] += int(data["victory"])
            soloRank["losses"] += int(data["defeat"])
            soloRank["winrate"] = int( (soloRank["wins"] / 
                (1 if((soloRank["wins"]+soloRank["losses"]) == 0)else (soloRank["wins"]+soloRank["losses"]))
            ) * 100)
            positions[i]["winrate"] = int( (positions[i]["wins"] /
                (1 if((positions[i]["wins"]+positions[i]["losses"]) == 0)else (positions[i]["wins"]+positions[i]["losses"]))
            ) * 100)
        for i in range(len(roles)):
            data = self.Fetch(f"lol-career-stats/v1/summoner-stats/{puuid}/{self.ClientData.CurrentSeason}/rank5flex/{roles[i]}")
            if not data["success"]: continue
            else: data = data["res"]
            if data.get("errorCode", False): continue
            data = data["seasonSummary"][f"{self.ClientData.CurrentSeason}"]["rank5flex"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"]
            positions[i]["wins"] += int(data["victory"])
            positions[i]["losses"] +=int( data["defeat"])
            flexRank["wins"] += int(data["victory"])
            flexRank["losses"] +=int( data["defeat"])
            flexRank["winrate"] = int( (flexRank["wins"] /
                (1 if((flexRank["wins"]+flexRank["losses"]) == 0)else (flexRank["wins"]+flexRank["losses"]))
            ) * 100)
            positions[i]["winrate"] = int( (positions[i]["wins"] /
                (1 if((positions[i]["wins"]+positions[i]["losses"]) == 0)else (positions[i]["wins"]+positions[i]["losses"]))
            ) * 100)

        # Mastery data
        data = self.Fetch(f"lol-collections/v1/inventories/{summonerId}/champion-mastery")
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        data.sort(key=lambda champ:-champ["championPoints"])
        data.extend([
            {
                "championId": 0,
                "championLevel": 0,
                "championPoints": 0,
                "formattedChampionPoints": "0",
                "highestGrade": "NA"
            },
            {
                "championId": 0,
                "championLevel": 0,
                "championPoints": 0,
                "formattedChampionPoints": "0",
                "highestGrade": "NA"
            },
            {
                "championId": 0,
                "championLevel": 0,
                "championPoints": 0,
                "formattedChampionPoints": "0",
                "highestGrade": "NA"
            }
        ])
        mastery = [
            {
                "championId": data[0]["championId"],
                "championLevel": data[0]["championLevel"],
                "championPoints": data[0]["championPoints"],
                "formattedChampionPoints": data[0]["formattedChampionPoints"],
                "highestGrade": data[0]["highestGrade"]
            },
            {
                "championId": data[1]["championId"],
                "championLevel": data[1]["championLevel"],
                "championPoints": data[1]["championPoints"],
                "formattedChampionPoints": data[1]["formattedChampionPoints"],
                "highestGrade": data[1]["highestGrade"]
            },
            {
                "championId": data[2]["championId"],
                "championLevel": data[2]["championLevel"],
                "championPoints": data[2]["championPoints"],
                "formattedChampionPoints": data[2]["formattedChampionPoints"],
                "highestGrade": data[2]["highestGrade"]
            }
        ]

        # Match data
        recentMatches = []
        data = self.Fetch(f"lol-match-history/v1/products/lol/{puuid}/matches?begIndex=&endIndex=10")
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        data = data["games"]["games"]
        timeNm = [12*31*24*60*60, 31*24*60*60, 24*60*60, 60*60, 60, 1]
        for i in range(min(len(data), 10)):
            recentMatches.append({
                "gameCreationStamp" : sum([
                    int(t)*timeNm[idx] for idx, t in enumerate(
                        data[i]["gameCreationDate"][:19].replace("T", "-").replace(":", "-").split("-")
                    )
                ]),
                "gameDurationM" : data[i]["gameDuration"]//60,
                "gameDurationS" : data[i]["gameDuration"]%60,
                "mapId" : data[i]["mapId"],
                "queueId" : data[i]["queueId"],
                "championId" : data[i]["participants"][0]["championId"],
                "champLevel" : data[i]["participants"][0]["stats"]["champLevel"],
                "spell1Id" : data[i]["participants"][0]["spell1Id"],
                "spell2Id" : data[i]["participants"][0]["spell2Id"],
                "assists" : data[i]["participants"][0]["stats"]["assists"],
                "deaths" : data[i]["participants"][0]["stats"]["deaths"],
                "kills" : data[i]["participants"][0]["stats"]["kills"],
                "goldEarned" : data[i]["participants"][0]["stats"]["goldEarned"],
                "totalMinionsKilled" : data[i]["participants"][0]["stats"]["totalMinionsKilled"],
                "win" : data[i]["participants"][0]["stats"]["win"],
                "items" : [
                    data[i]["participants"][0]["stats"]["item0"],
                    data[i]["participants"][0]["stats"]["item1"],
                    data[i]["participants"][0]["stats"]["item2"],
                    data[i]["participants"][0]["stats"]["item3"],
                    data[i]["participants"][0]["stats"]["item4"],
                    data[i]["participants"][0]["stats"]["item5"],
                    data[i]["participants"][0]["stats"]["item6"],
                ]
            })


        result = {
            "isEqual" : lambda other: other["username"] == username,
            "username" : username,
            "puuid" : puuid,
            "accountId" : accountId,
            "summonerId" : summonerId,
            "summonerLevel" : summonerLevel,
            "percentCompleteForNextLevel" : percentCompleteForNextLevel,
            "soloRank" : soloRank,
            "flexRank" : flexRank,
            "mastery" : mastery,
            "positions" : positions,
            "recentMatches" : recentMatches,
            "success" : True
        }
        # print(result)
        return result



    def LoadPlayerFromLogString(self, logString):
        looking = ""
        currentIdx = 0
        isLocal = "**LOCAL**" in logString

        looking = "'"
        currentIdx = functions.indexOf(logString, looking)
        username =  logString[currentIdx+len(looking) : functions.indexOf(logString, "'", currentIdx+1)] if(currentIdx>0)else None

        looking = "Champion("
        currentIdx = functions.indexOf(logString, looking)
        champion =  logString[currentIdx+len(looking) : functions.indexOf(logString, ")", currentIdx+1)] if(currentIdx>0)else None

        looking = "TeamBuilderRole("
        currentIdx = functions.indexOf(logString, looking)
        role =  logString[currentIdx+len(looking) : functions.indexOf(logString, ")", currentIdx+1)] if(currentIdx>0)else None
        if(role is not None and role == "UTILITY"): role = "SUPPORT"

        looking = "PUUID("
        currentIdx = functions.indexOf(logString, looking)
        puuid =  logString[currentIdx+len(looking) : functions.indexOf(logString, ")", currentIdx+1)] if(currentIdx>0)else None

        result = self.LoadPlayer(username, puuid)
        if not result["success"]: return FAILED_JSON_RETURN.copy()
        result["champion"] = champion
        result["isLocal"] = isLocal
        result["role"] = role

        return result



    def LoadPlayerFromSummonerId(self, summonerId):
        data = self.Fetch(f"lol-summoner/v1/summoners/{summonerId}")
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        if data.get("errorCode", False): return FAILED_JSON_RETURN.copy()
        username = data["displayName"]
        puuid = data["puuid"]

        result = self.LoadPlayer(username, puuid)
        if not result["success"]: return FAILED_JSON_RETURN.copy()

        return result


    def LoadPlayerFromUsername(self, username):
        data = self.Fetch(f"lol-summoner/v1/summoners?name={username}")
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        if data.get("errorCode", False): return FAILED_JSON_RETURN.copy()
        username = data["displayName"]
        puuid = data["puuid"]

        result = self.LoadPlayer(username, puuid)
        if not result["success"]: return FAILED_JSON_RETURN.copy()

        return result
        

    def SearchChampionSelectTeam(self):
        data = self.Fetch("lol-gameflow/v1/gameflow-phase")
        if not data["success"]: 
            self.Initialize()
            return FAILED_JSON_RETURN.copy()
        elif data["res"] != "ChampSelect":
            return FAILED_JSON_RETURN.copy()

        data = self.Fetch(f"lol-summoner/v1/current-summoner")
        if not data["success"]: 
            self.Initialize()
            return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        if data.get("errorCode"): 
            self.Initialize()
            return FAILED_JSON_RETURN.copy()

        data = self.Fetch(f"lol-champ-select/v1/session")
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        if data.get("errorCode"): 
            self.root.DisplayingChampionSelectGameId = -1
            return FAILED_JSON_RETURN.copy()
        teamSummoners = {
            "success" : True,
            "gameId" : data["gameId"],
            "myTeam" : []
        }
        for i in range(len(data["myTeam"])):
            teamSummoners["myTeam"].append({
                "summonerId" : data["myTeam"][i]["summonerId"],
                "role" : data["myTeam"][i]["assignedPosition"]
            })
        TeamOrder = []
        for i in range(len(teamSummoners["myTeam"])):
            result = self.LoadPlayerFromSummonerId(
                teamSummoners["myTeam"][i]["summonerId"]
            )
            if not result["success"]: continue
            result["role"] = teamSummoners["myTeam"][i]["role"]
            TeamOrder.append(result)
        TeamOrder.sort(key=lambda player:ROLE_ORDER.get(player["role"].upper(), 0))
        return {
            "success" : True,
            "gameId" : teamSummoners["gameId"],
            "A" : TeamOrder
        }



    def SearchLastestGameLog(self):
        data = self.Fetch(f"lol-summoner/v1/current-summoner")
        if not data["success"]: 
            self.Initialize()
            return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        if data.get("errorCode"): 
            self.Initialize()
            return FAILED_JSON_RETURN.copy()

        if not self.ClientData.IsFilled(): return FAILED_JSON_RETURN.copy()

        log_dir = functions.listdir(f"{self.LoLPath}\\Game\\Logs\\GameLogs\\")[0]
        print("Latest Game Dir:", log_dir)
        with open(os.path.join(log_dir, f"{os.path.split(log_dir)[1]}_r3dlog.txt"), "r", encoding="utf-8") as f:
            log_data = f.read()
        return {
            "success": True,
            "res": log_data
        }



    def SearchLastestGameA(self, log_data=None):
        if not log_data: 
            data = self.SearchLastestGameLog()
            if not data["success"]: return FAILED_JSON_RETURN.copy()
            else: log_data = data["res"]

        OrderLogStrings = []
        ChaosLogStrings = []

        current_idx = 0
        ALogStrings = []
        APlayers = []

        for i in range(5):
            current_idx = functions.indexOf(log_data, f"TeamOrder {i}) ")
            if(current_idx >= 0): OrderLogStrings.append(log_data[current_idx : functions.indexOf(log_data, "\n", current_idx)])

        for i in range(5):
            current_idx = functions.indexOf(log_data, f"TeamChaos {i}) ")
            if(current_idx >= 0): ChaosLogStrings.append(log_data[current_idx : functions.indexOf(log_data, "\n", current_idx)])

        if sum([ "LOCAL" in logString for logString in OrderLogStrings ]):
            ALogStrings = OrderLogStrings
        elif sum([ "LOCAL" in logString for logString in ChaosLogStrings ]):
            ALogStrings = ChaosLogStrings

        for idx, logString in enumerate(ALogStrings):
            print(f"Load A{idx}")
            res = self.LoadPlayerFromLogString( logString )
            if( res["success"] ):
                APlayers.append(res)
                print("OK")
            else:
                print("Failed")

        APlayers.sort(key=lambda player : ROLE_ORDER[player.get("role", "NONE")])

        return {
            "success": True,
            "res": APlayers
        }


    def SearchLastestGameB(self, log_data=None):
        if not log_data: 
            data = self.SearchLastestGameLog()
            if not data["success"]: return FAILED_JSON_RETURN.copy()
            else: log_data = data["res"]

        OrderLogStrings = []
        ChaosLogStrings = []

        current_idx = 0
        BLogStrings = []
        BPlayers = []

        for i in range(5):
            current_idx = functions.indexOf(log_data, f"TeamOrder {i}) ")
            if(current_idx >= 0): OrderLogStrings.append(log_data[current_idx : functions.indexOf(log_data, "\n", current_idx)])

        for i in range(5):
            current_idx = functions.indexOf(log_data, f"TeamChaos {i}) ")
            if(current_idx >= 0): ChaosLogStrings.append(log_data[current_idx : functions.indexOf(log_data, "\n", current_idx)])

        if sum([ "LOCAL" in logString for logString in OrderLogStrings ]):
            BLogStrings = ChaosLogStrings
        elif sum([ "LOCAL" in logString for logString in ChaosLogStrings ]):
            BLogStrings = OrderLogStrings

        for idx, logString in enumerate(BLogStrings):
            print(f"Load B{idx}")
            res = self.LoadPlayerFromLogString( logString )
            if( res["success"] ):
                BPlayers.append(res)
                print("OK")
            else:
                print("Failed")

        BPlayers.sort(key=lambda player : ROLE_ORDER[player.get("role", "NONE")])

        return {
            "success": True,
            "res": BPlayers
        }


    def SearchLatestGameAll(self):
        data = self.SearchLastestGameLog()
        if not data["success"]: return FAILED_JSON_RETURN.copy()
        else: log_data = data["res"]

        dataA = self.SearchLastestGameA(log_data)
        A = [] if(not dataA["success"])else dataA["res"]
        dataB = self.SearchLastestGameA(log_data)
        B = [] if(not dataB["success"])else dataB["res"]

        return {
            "success" : True,
            "A":A,
            "B":B
        }



    def LoadLocalPlayer(self):
        if not self.LoLPath: self.AssertGamePath()
        if not self.ClientData.IsFilled(): return FAILED_JSON_RETURN.copy()

        data = self.Fetch(f"lol-summoner/v1/current-summoner")
        if not data["success"]: 
            self.Initialize()
            return FAILED_JSON_RETURN.copy()
        else: data = data["res"]
        if data.get("errorCode"): 
            self.Initialize()
            return FAILED_JSON_RETURN.copy()

        puuid = data.get("puuid", None)
        username = data.get("displayName", None)
        if puuid is None or username is None: return FAILED_JSON_RETURN.copy()

        soloRank = {
            "losses": 0,
            "wins": 0,
            "winrate": 0
        }
        flexRank = {
            "losses": 0,
            "wins": 0,
            "winrate": 0
        }
        positions = [{
            "losses": 0,
            "wins": 0,
            "winrate": 0
        },{
            "losses": 0,
            "wins": 0,
            "winrate": 0
        },{
            "losses": 0,
            "wins": 0,
            "winrate": 0
        },{
            "losses": 0,
            "wins": 0,
            "winrate": 0
        },{
            "losses": 0,
            "wins": 0,
            "winrate": 0
        }]
        roles = ["TOP","JUNGLE","MID","BOTTOM","SUPPORT"]
        for i in range(len(roles)):
            data = self.Fetch(f"lol-career-stats/v1/summoner-stats/{puuid}/{self.ClientData.CurrentSeason}/rank5solo/{roles[i]}")
            if not data["success"]: continue
            else: data = data["res"]
            if data.get("errorCode", False): continue

            data = data["seasonSummary"][f"{self.ClientData.CurrentSeason}"]["rank5solo"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"]

            positions[i]["wins"] += int(data["victory"])
            positions[i]["losses"] += int(data["defeat"])
            positions[i]["winrate"] = int( (positions[i]["wins"] / 
                (1 if(positions[i]["wins"]+positions[i]["losses"]==0)else (positions[i]["wins"]+positions[i]["losses"]))
            ) * 100 )

            soloRank["wins"] += int(data["victory"])
            soloRank["losses"] += int(data["defeat"])
            soloRank["winrate"] = int( (soloRank["wins"] / 
                (1 if(soloRank["wins"]+soloRank["losses"]==0)else (soloRank["wins"]+soloRank["losses"]))
            ) * 100 )
        for i in range(len(roles)):
            data = self.Fetch(f"lol-career-stats/v1/summoner-stats/{puuid}/{self.ClientData.CurrentSeason}/rank5flex/{roles[i]}")
            if not data["success"]: continue
            else: data = data["res"]
            if data.get("errorCode", False): continue

            data = data["seasonSummary"][f"{self.ClientData.CurrentSeason}"]["rank5flex"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"]

            positions[i]["wins"] += int(data["victory"])
            positions[i]["losses"] += int(data["defeat"])
            positions[i]["winrate"] = int( (positions[i]["wins"] / 
                (1 if(positions[i]["wins"]+positions[i]["losses"]==0)else (positions[i]["wins"]+positions[i]["losses"]))
            ) * 100 )

            flexRank["wins"] += int(data["victory"])
            flexRank["losses"] += int(data["defeat"])
            flexRank["winrate"] = int( (flexRank["wins"] / 
                (1 if(flexRank["wins"]+flexRank["losses"]==0)else (flexRank["wins"]+flexRank["losses"]))
            ) * 100 )

        return {
            "success": True,
            "username": username,
            "puuid": puuid,
            "soloRank": soloRank,
            "flexRank": flexRank,
            "positions": positions
        }





