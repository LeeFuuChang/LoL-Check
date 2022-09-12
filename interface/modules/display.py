from datetime import datetime
from .constants import *







class HTMLDisplay:
    _start = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Document</title>
        <link rel="stylesheet" href="https://www.leefuuchang.in/projects/LoL-Check/assets/css/display/display.css">
    </head>
    <script>
    function bannerChangePage(e){
        if( !e ) e = window.event;
        console.log("DOWN");
        let banner, i;
        for(i=0; i<e.path.length; i++){
            if( !e.path[i].classList )continue;
            if(e.path[i].classList.contains("banner-layer-1")){
                banner = e.path[i];
                break;
            };
        };
        let bannerPages = banner.querySelectorAll(".banner-page");
        let pageIndicators = banner.querySelectorAll(".page-indicator");
        let currentPageNum = parseInt(banner.querySelector(".page-indicator.active").ariaLabel);
        let x=e.pageX-banner.offsetLeft;

        pageIndicators.forEach(idr=>{
            idr.classList.remove("active");
        });
        bannerPages.forEach(pg=>{
            pg.style.display = "none";
        });

        let newPageNum;
        if( x/banner.offsetWidth < 0.5 ){
            // clicked left side of the banner
            console.log("Click Left", currentPageNum);
            newPageNum = currentPageNum===0 ? (
                pageIndicators.length-1 ) : ( currentPageNum-1
            )
        }else{
            // clicked right side of the banner
            console.log("Click Right", currentPageNum);
            newPageNum = currentPageNum===pageIndicators.length-1 ? (
                0 ) : ( currentPageNum+1
            )
        };
        console.log(newPageNum);
        pageIndicators[newPageNum].classList.add("active");
        bannerPages[newPageNum].style.display = "flex";
    };
    </script>
    <body>
        <main>
            <div class="team-container df aic jcc">
    """
    _end = """
            </div>
        </main>
    </body>
    </html>
    """
    def __init__(self):
        self.ResetTemplate()


    def ResetTemplate(self):
        self.template = f"{self.__class__._start}"


    def GetResult(self):
        return self.template + self.__class__._end


    def AddTeamToDisplay(self, team):
        for player in team[:5]:
            self.AddPlayerToDisplay(player)


    def AddPlayerToDisplay(self, data):
        # Player History Matches
        date = datetime.utcnow()
        convertTime = [[12*31*24*60*60, "年"], [31*24*60*60, "個月"], [24*60*60, "天"], [60*60, "小時"], [60, "分鐘"], [1, "秒"]]
        nowTimeStamp = (
            date.year*convertTime[0][0]) + (
            date.month*convertTime[1][0]) + (
            date.day*convertTime[2][0]) + (
            date.hour*convertTime[3][0]) + (
            date.minute*convertTime[4][0]) + (
            date.second*convertTime[5][0]
        )
        playerMatchHistoryHtml = ""
        for i in range( min(len(data["recentMatches"]), 10) ):
            match = data["recentMatches"][i]
            matchAge = nowTimeStamp - match["gameCreationStamp"]
            for j in range(len(convertTime)):
                formattedAge = int(matchAge / convertTime[j][0])
                if(formattedAge > 0):
                    formattedAge = f"{formattedAge}{convertTime[j][1]}"
                    break
            matchCKDA = round((match["kills"]+match["assists"]) / ( 1 if(match["deaths"]==0) else match["deaths"] ), 1)
            playerMatchHistoryHtml += f"""
                <div class="match-history" data-index-number="{i+1}">
                    <div class="detail-wrapper">
                        <div class="champion df aic jcc">
                            <div class="champion-icon">
                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[match["championId"]]}.png" alt="">
                                <div class="champion-level">
                                    <h4>{match["champLevel"]}</h4>
                                </div>
                            </div>
                        </div>
                        <div class="match-result df aic jcc">
                            <div class="match-result-top">
                                <div class="match-result-info df jcc">
                                    <h3 class="{"win" if(match["win"])else "lose"}c WL">{"勝利" if(match["win"])else "失敗"}</h3>
                                    <h3 class="queue-type">{QUEUE_ID_TO_TW[match["queueId"]]}</h3>
                                </div>
                            </div>
                            <div class="match-result-bottom">
                                <div class="spells df aic">
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/spells/{match["spell1Id"]}.png" alt="spell1">
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/spells/{match["spell2Id"]}.png" alt="spell2">
                                </div>
                            </div>
                        </div>
                        <div class="player-result df aic jcc">
                            <div class="player-result-top">
                                <div class="items df aic">
                                    <div class="item item0">
                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/items/{match["items"][0]}.png" alt="">
                                    </div>
                                    <div class="item item1">
                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/items/{match["items"][1]}.png" alt="">
                                    </div>
                                    <div class="item item2">
                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/items/{match["items"][2]}.png" alt="">
                                    </div>
                                    <div class="item item3">
                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/items/{match["items"][3]}.png" alt="">
                                    </div>
                                    <div class="item item4">
                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/items/{match["items"][4]}.png" alt="">
                                    </div>
                                    <div class="item item5">
                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/items/{match["items"][5]}.png" alt="">
                                    </div>
                                    <div class="item item6">
                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/items/{match["items"][6]}.png" alt="">
                                    </div>
                                </div>
                            </div>
                            <div class="player-result-bottom df">
                                <div class="KDA">
                                    <h3>{match["kills"]}<span>/</span>{match["deaths"]}<span>/</span>{match["assists"]}</h3>
                                </div>
                                <div class="cs">
                                    <h4>{match["totalMinionsKilled"]}<span>cs</span></h4>
                                </div>
                                <div class="gold">
                                    <h4><span>$</span>{match["goldEarned"]}</h4>
                                </div>
                            </div>
                        </div>
                        <div class="match-info">
                            <h4 class="map">{MAP_ID_TO_TW[match["mapId"]]}</h4>
                            <h4 class="duration">{(f'{match["gameDurationM"]:0>2}')}<span>:</span>{(f'{match["gameDurationS"]:0>2}')}</h4>
                        </div>
                    </div>
                    <div class="history-wrapper df aic">
                        <div class="champion-wrapper">
                            <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[match["championId"]]}.png" alt="" class="champion-icon">
                        </div>
                        <div class="match-info df jcc">
                            <div class="info-section section-1 df aic">
                                <div class="KDA df aic jcc {"win" if(match["win"])else "lose"}b">
                                    <h3>{match["kills"]}<span>/</span>{match["deaths"]}<span>/</span>{match["assists"]}</h3>
                                </div>
                                <div class="mode df aic jcc">
                                    <h3>{QUEUE_ID_TO_TW[match["queueId"]]}</h3>
                                </div>
                            </div>
                            <div class="info-section section-2 df jcc">
                                <div class="CKDA df aic jcc {"win" if(matchCKDA > 2)else "lose"}c">
                                    <h3><span>{matchCKDA}</span>KDA</h3>
                                </div>
                                <div class="age df aic jcc">
                                    <h3>{formattedAge}<span>前</span></h3>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                <hr style="width: 100%;">
            """

        fullPlayerDisplay = f"""
            <div class="banner-container df aic jcc">
                <div class="banner-layer-1" onmousedown="bannerChangePage(event)">
                    <div class="banner-layer-2 df aic jcc">
                        <div class="banner-page banner-page-0 df aic jcc" style="display: flex">
                            <div class="rank df aic jcc">
                                <div class="rank-container df aic jcc">
                                    <div class="rank-detail df aic jcc">
                                        <div class="rank-detail-type rank-detail-solo df jcc">
                                            <div class="detail-top rank-detail-solo-img">
                                            <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/ranks/{data["soloRank"]["tier"]}.png" alt="">
                                            </div>
                                            <div class="detail-bottom rank-detail-solo-img df aic jcc">
                                                <h3 class="rank-detail-solo-text tc">單雙積分</h3>
                                                <h3 class="rank-detail-solo-tier tc">{TRANSLATION[data["soloRank"]["tier"]][data["soloRank"]["division"]]}</h3>
                                                <h3 class="rank-detail-solo-stat df aic jcc">
                                                    <div class="tc">{data["soloRank"]["wins"]} W</div>
                                                    <div class="tc">{data["soloRank"]["losses"]} L</div>
                                                    <div class="tc">{data["soloRank"]["leaguePoints"]} LP</div>
                                                </h3>
                                            </div>
                                        </div>
                                        <div class="rank-detail-type rank-detail-flex df jcc">
                                            <div class="detail-top rank-detail-flex-img">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/ranks/{data["flexRank"]["tier"]}.png" alt="">
                                            </div>
                                            <div class="detail-bottom rank-detail-flex-img df aic jcc">
                                                <h3 class="rank-detail-flex-text tc">彈性積分</h3>
                                                <h3 class="rank-detail-flex-tier tc">{TRANSLATION[data["flexRank"]["tier"]][data["flexRank"]["division"]]}</h3>
                                                <h3 class="rank-detail-flex-stat df aic jcc">
                                                    <div class="tc">{data["flexRank"]["wins"]} W</div>
                                                    <div class="tc">{data["flexRank"]["losses"]} L</div>
                                                    <div class="tc">{data["flexRank"]["leaguePoints"]} LP</div>
                                                </h3>
                                            </div>
                                        </div>
                                        <div class="rank-detail-type rank-detail-prev df jcc">
                                            <div class="detail-top rank-detail-prev-img">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/ranks/{data["soloRank"]["previousSeasonEndTier"]}.png" alt="">
                                            </div>
                                            <div class="detail-bottom rank-detail-prev-img df aic jcc">
                                                <h3 class="rank-detail-prev-text tc">上季積分</h3>
                                                <h3 class="rank-detail-prev-tier tc">{TRANSLATION[data["soloRank"]["previousSeasonEndTier"]][data["soloRank"]["previousSeasonEndDivision"]]}</h3>
                                                <h3 class="rank-detail-prev-stat df aic jcc" style="opacity: 0">
                                                    <div class="tc">N/A</div>
                                                    <div class="tc">N/A</div>
                                                    <div class="tc">N/A</div>
                                                </h3>
                                            </div>
                                        </div>
                                    </div>
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/ranks/{data["soloRank"]["tier"]}.png" alt="">
                                    <h2 class="division df aic jcc">{data["soloRank"]["division"] if(data["soloRank"]["division"] in "IIIV")else "I"}</h2>
                                </div>
                            </div>
                            <div class="account df aic">
                                <h1 class="username df aic jcc">{data["username"]}</h1>
                                <div class="level df aic">
                                    <div 
                                        class="progress" 
                                        style="background: conic-gradient(
                                            var(--color-3-2) {int(data["percentCompleteForNextLevel"]*3.6)}deg, 
                                            var(--color-3-3) {int(data["percentCompleteForNextLevel"]*3.6)}deg
                                        )"
                                    ></div>
                                    <span>{data["summonerLevel"]}</span>
                                </div>
                            </div>
                            <div class="mastery">
                                <div class="mastery-display df aic">
                                    <div class="mastery-detail df aic jcc">
                                        <div class="mastery-detail-type mastery-detail-2 df aic">
                                            <div class="mastery-champion-icon df aic">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[data["mastery"][1]["championId"]]}.png" alt="">
                                                <div class="mastery-champion-mastery">
                                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/mastery-{data["mastery"][1]["championLevel"]}.png" alt="">
                                                </div>
                                            </div>
                                            <div class="mastery-detail-stats df jcc">
                                                <div class="mastery-detail-champ df aic jcc">
                                                    <h3 class="df aic jcc">{CHAMPION_ID_TO_TW[data["mastery"][1]["championId"]]}</h3>
                                                </div>
                                                <div class="mastery-detail-point df aic jcc">
                                                    <div class="mastery-detail-point-icon">
                                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/icon.png" alt="">
                                                    </div>
                                                    <h3 class="df aic jcc">{data["mastery"][1]["formattedChampionPoints"]} 分數</h3>
                                                </div>
                                                <div class="mastery-detail-grade df aic jcc">
                                                    <h3 class="df aic jcc">最高成績：{data["mastery"][1]["highestGrade"]}</h3>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mastery-detail-type mastery-detail-1 df aic">
                                            <div class="mastery-champion-icon df aic">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[data["mastery"][0]["championId"]]}.png" alt="">
                                                <div class="mastery-champion-mastery">
                                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/mastery-{data["mastery"][0]["championLevel"]}.png" alt="">
                                                </div>
                                            </div>
                                            <div class="mastery-detail-stats df jcc">
                                                <div class="mastery-detail-champ df aic jcc">
                                                    <h3 class="df aic jcc">{CHAMPION_ID_TO_TW[data["mastery"][0]["championId"]]}</h3>
                                                </div>
                                                <div class="mastery-detail-point df aic jcc">
                                                    <div class="mastery-detail-point-icon">
                                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/icon.png" alt="">
                                                    </div>
                                                    <h3 class="df aic jcc">{data["mastery"][0]["formattedChampionPoints"]} 分數</h3>
                                                </div>
                                                <div class="mastery-detail-grade df aic jcc">
                                                    <h3 class="df aic jcc">最高成績：{data["mastery"][0]["highestGrade"]}</h3>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mastery-detail-type mastery-detail-3 df aic">
                                            <div class="mastery-champion-icon df aic">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[data["mastery"][2]["championId"]]}.png" alt="">
                                                <div class="mastery-champion-mastery">
                                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/mastery-{data["mastery"][2]["championLevel"]}.png" alt="">
                                                </div>
                                            </div>
                                            <div class="mastery-detail-stats df jcc">
                                                <div class="mastery-detail-champ df aic jcc">
                                                    <h3 class="df aic jcc">{CHAMPION_ID_TO_TW[data["mastery"][2]["championId"]]}</h3>
                                                </div>
                                                <div class="mastery-detail-point df aic jcc">
                                                    <div class="mastery-detail-point-icon">
                                                        <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/icon.png" alt="">
                                                    </div>
                                                    <h3 class="df aic jcc">{data["mastery"][2]["formattedChampionPoints"]} 分數</h3>
                                                </div>
                                                <div class="mastery-detail-grade df aic jcc">
                                                    <h3 class="df aic jcc">最高成績：{data["mastery"][2]["highestGrade"]}</h3>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mastery-2 mastery-champion df aic jcc">
                                        <div class="mastery-champion-icon df aic">
                                            <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[data["mastery"][1]["championId"]]}.png" alt="">
                                            <div class="mastery-champion-mastery">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/mastery-{data["mastery"][1]["championLevel"]}.png" alt="">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mastery-1 mastery-champion df aic jcc">
                                        <div class="mastery-champion-icon df aic">
                                            <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[data["mastery"][0]["championId"]]}.png" alt="">
                                            <div class="mastery-champion-mastery">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/mastery-{data["mastery"][0]["championLevel"]}.png" alt="">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mastery-3 mastery-champion df aic jcc">
                                        <div class="mastery-champion-icon df aic">
                                            <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/champion/icon/{CHAMPION_ID_TO_ENG[data["mastery"][2]["championId"]]}.png" alt="">
                                            <div class="mastery-champion-mastery">
                                                <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/mastery/mastery-{data["mastery"][2]["championLevel"]}.png" alt="">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="banner-page banner-page-1 df aic" style="display: none">
                            <div class="winrate winrate-solo df aic jcc">
                                <div class="winrate-persent df aic jcc"
                                style="background: conic-gradient(
                                    var(--color-3-2) {data["soloRank"]["winrate"]*3.6}deg, 
                                    var(--color-3-4) {data["soloRank"]["winrate"]*3.6}deg
                                )">
                                    <div class="winrate-info df aic jcc">
                                        <h3 class="winrate-info-WR">{data["soloRank"]["winrate"]}<span>%</span></h3>
                                        <h3 class="winrate-info-WL">{data["soloRank"]["wins"]} W<span>|</span>{data["soloRank"]["losses"]} L</h3>
                                    </div>
                                </div>
                                <h3 class="winrate-title">單雙積分</h3>
                            </div>
                            <div class="winrate winrate-flex df aic jcc">
                                <div class="winrate-persent df aic jcc"
                                style="background: conic-gradient(
                                    var(--color-3-2) {data["flexRank"]["winrate"]*3.6}deg, 
                                    var(--color-3-4) {data["flexRank"]["winrate"]*3.6}deg
                                )">
                                    <div class="winrate-info df aic jcc">
                                        <h3 class="winrate-info-WR">{data["flexRank"]["winrate"]}<span>%</span></h3>
                                        <h3 class="winrate-info-WL">{data["flexRank"]["wins"]} W<span>|</span>{data["flexRank"]["losses"]} L</h3>
                                    </div>
                                </div>
                                <h3 class="winrate-title">彈性積分</h3>
                            </div>
                            <div class="winrate-lane df aic">
                                <div class="winrate-lane-type winrate-lane-TOP df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">{data["positions"][0]["wins"]} W<span>|</span>{data["positions"][0]["losses"]} L</h4>
                                        <h4 class="lane-detail-WR">{data["positions"][0]["winrate"]}% 勝率</h4>
                                    </div>
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/lanes/TOP.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-JUNGLE df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">{data["positions"][1]["wins"]} W<span>|</span>{data["positions"][1]["losses"]} L</h4>
                                        <h4 class="lane-detail-WR">{data["positions"][1]["winrate"]}% 勝率</h4>
                                    </div>
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/lanes/JUNGLE.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-MID df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">{data["positions"][2]["wins"]} W<span>|</span>{data["positions"][2]["losses"]} L</h4>
                                        <h4 class="lane-detail-WR">{data["positions"][2]["winrate"]}% 勝率</h4>
                                    </div>
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/lanes/MID.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-BOTTOM df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">{data["positions"][3]["wins"]} W<span>|</span>{data["positions"][3]["losses"]} L</h4>
                                        <h4 class="lane-detail-WR">{data["positions"][3]["winrate"]}% 勝率</h4>
                                    </div>
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/lanes/BOTTOM.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-SUPPORT df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">{data["positions"][4]["wins"]} W<span>|</span>{data["positions"][4]["losses"]} L</h4>
                                        <h4 class="lane-detail-WR">{data["positions"][4]["winrate"]}% 勝率</h4>
                                    </div>
                                    <img src="https://www.leefuuchang.in/projects/LoL-Check/assets/images/lanes/SUPPORT.png" alt="" srcset="">
                                </div>
                            </div>
                        </div>
                        <div class="banner-page banner-page-2 df aic jcc" style="display: none">
                            <div class="match-wrapper df aic">
                                {playerMatchHistoryHtml}
                            </div>
                        </div>
                        <div class="banner-footer df jcc">
                            <div class="page-indicators df aic">
                                <a class="page-indicator active" aria-label="0"></a>
                                <a class="page-indicator" aria-label="1"></a>
                                <a class="page-indicator" aria-label="2"></a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            """
        self.template += fullPlayerDisplay







