const HTTPS = "https://"
const CURRENT_SEASON = 12;
const CLIENT_LOG_FILETYPE = "LeagueClientUx.log";
const RIOT_BASE_URL = "https://riot:";


const UpdateGap = 2;


const ROLE_ORDER = {
    "NONE":0,
    "TOP":1,
    "JUNGLE":2,
    "MIDDLE":3,
    "BOTTOM":4,
    "SUPPORT":5,
    "UTILITY":5
}


var GameFilesLocation = "";
// var RiotClientAccessHeader = new Headers();
var RiotUserAccessToken = "";
var RiotClientAccessUrl = "";
var LatestClientLog = "";
var CurrentlyDisplayingGameId = -1;


async function Initialize(){
    if(GameFilesLocation === ""){
        console.log("Not Ready");
        chrome.storage.local.get(["GameFilesLocation"], async function(items){
            if(items["GameFilesLocation"] === undefined){
                GameFilesLocation = ""
            }else{
                GameFilesLocation = items["GameFilesLocation"];
            };
        });
        return;
    };
    try{
        await fetch(
            `file:///${GameFilesLocation}/Game/Logs/LeagueClient Logs/`,
            {method:"GET"}
        ).then(res => {
            return res.text();
        }).then(files => {
            let log_files = files.split("<script>addRow(\"").slice(1).map(fn => fn.split("\"")[0]).filter(fn => fn.includes(CLIENT_LOG_FILETYPE));
            log_files.sort((a, b) => {
                let atimes = a.replace("T", "-").split("_")[0].split("-").map(t => parseInt(t));
                let btimes = b.replace("T", "-").split("_")[0].split("-").map(t => parseInt(t));
                return(
                    atimes[0]*12*31*24*60*60 + atimes[1]*31*24*60*60 + atimes[2]*24*60*60 + btimes[3]*60*60 + btimes[4]*60 + btimes[5]
                ) - (
                    btimes[0]*12*31*24*60*60 + btimes[1]*31*24*60*60 + btimes[2]*24*60*60 + btimes[3]*60*60 + btimes[4]*60 + btimes[5]
                );
            });
            LatestClientLog = log_files[log_files.length-1];
        });
        console.log(`latestClientLog: ${LatestClientLog}`);
    }catch(e){
        console.log(e);
    };

    try{
        await fetch(
            `file:///${GameFilesLocation}/Game/Logs/LeagueClient Logs/${LatestClientLog}`,
            {method:"GET"}
        ).then(res => {
            return res.text();
        }).then(log => {
            let i = log.indexOf(RIOT_BASE_URL);
            RiotClientAccessUrl = log.slice(i, log.indexOf("/", i+RIOT_BASE_URL.length));
            RiotUserAccessToken = RiotClientAccessUrl.slice(RIOT_BASE_URL.length, RiotClientAccessUrl.indexOf("@"));
            RiotClientAccessUrl = RiotClientAccessUrl.slice(0, HTTPS.length) + RiotClientAccessUrl.slice(RiotClientAccessUrl.indexOf("@")+1);
        });
        console.log(`RiotClientAccessUrl: ${RiotClientAccessUrl}`);
        console.log(`RiotUserAccessToken: ${RiotUserAccessToken}`);
    }catch(e){
        console.log(e);
    };

    try{
        await fetch(
            `${RiotClientAccessUrl}/riotclient/auth-token`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.text();
        }).then(token => {
            console.log(token)
        });
    }catch(e){
        console.log(e);
    };

    await LoadLocalSummoner().then(res => {
        if( !res.success ) return;
        chrome.storage.local.set({
            "LocalSummoner": res
        }, () => {});
    });

    return new Promise((resolve, reject)=>{
        resolve({
            success :(
                GameFilesLocation !== ""
            ) && (
                RiotClientAccessUrl !== ""
            ) && (
                LatestClientLog !== ""
            )
        })
    });
};


function IsReadyToSearch(){
    return (
        GameFilesLocation !== undefined
    ) && (
        RiotUserAccessToken !== undefined
    ) && (
        RiotClientAccessUrl !== undefined
    ) && (
        LatestClientLog !== undefined
    ) && (
        GameFilesLocation !== ""
    ) && (
        RiotUserAccessToken !== ""
    ) && (
        RiotClientAccessUrl !== ""
    ) && (
        LatestClientLog !== ""
    );
};
function AssertReadyToSearch(time, gap){
    let iter = Math.floor(time/gap)
    return new Promise((resolve, reject) => {
        let intv = setInterval(async ()=>{
            await Initialize().then(res => {
                if( IsReadyToSearch() ) resolve(clearInterval(intv));
            });
            if( iter === 0 ) reject(clearInterval(intv));
            iter--;
        }, gap);
    });
};



async function LoadLocalSummoner(){
    if( !IsReadyToSearch() ) return {success: false};


    // Account data
    let username, puuid;
    try{
        await fetch(
            `${RiotClientAccessUrl}/lol-summoner/v1/current-summoner`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.json();
        }).then(data => {
            puuid = data["puuid"];
            username = data["displayName"];
        });
    }catch(e){
        console.log(e);
    };


    if( puuid === undefined || username === undefined) return {success: false};


    // Rank data
    let soloRank = {
        losses : 0,
        wins : 0,
        winrate : 0
    };
    let flexRank = {
        losses : 0,
        wins : 0,
        winrate : 0
    };
    let positions = [
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        }
    ];
    try{
        let roles = ["TOP","JUNGLE","MID","BOTTOM","SUPPORT"];
        for(let i=0; i<roles.length; i++){
            await fetch(
                `${RiotClientAccessUrl}/lol-career-stats/v1/summoner-stats/${puuid}/${CURRENT_SEASON}/rank5solo/${roles[i]}`,
                {
                    method:"GET",
                    headers: {
                        'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                    }
                }
            ).then(res => {
                return res.json();
            }).then(data => {
                if(data["errorCode"] != undefined) return;
                data = data["seasonSummary"][`${CURRENT_SEASON}`]["rank5solo"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"];
                positions[i].wins += data["victory"];
                positions[i].losses += data["defeat"];
                soloRank.wins += data["victory"];
                soloRank.losses += data["defeat"];
                soloRank.winrate = Math.floor((soloRank.wins / ( 
                    (soloRank.wins+soloRank.losses) === 0 ? 1 : (soloRank.wins+soloRank.losses) 
                )) * 100);
                positions[i].winrate = Math.floor((positions[i].wins / ( 
                    (positions[i].wins+positions[i].losses) === 0 ? 1 : (positions[i].wins+positions[i].losses) 
                )) * 100);
            });
        };
        for(let i=0; i<roles.length; i++){
            await fetch(
                `${RiotClientAccessUrl}/lol-career-stats/v1/summoner-stats/${puuid}/${CURRENT_SEASON}/rank5flex/${roles[i]}`,
                {
                    method:"GET",
                    headers: {
                        'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                    }
                }
            ).then(res => {
                return res.json();
            }).then(data => {
                if(data["errorCode"] != undefined) return;
                data = data["seasonSummary"][`${CURRENT_SEASON}`]["rank5flex"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"];
                positions[i].wins += data["victory"];
                positions[i].losses += data["defeat"];
                flexRank.wins += data["victory"];
                flexRank.losses += data["defeat"];
                flexRank.winrate = Math.floor((flexRank.wins / ( 
                    (flexRank.wins+flexRank.losses) === 0 ? 1 : (flexRank.wins+flexRank.losses) 
                )) * 100);
                positions[i].winrate = Math.floor((positions[i].wins / ( 
                    (positions[i].wins+positions[i].losses) === 0 ? 1 : (positions[i].wins+positions[i].losses) 
                )) * 100);
            });
        };
    }catch(e){
        console.log(e);
    };


    let result = {
        success : true,
        username : username,
        puuid : puuid,
        soloRank : soloRank,
        flexRank : flexRank,
        positions : positions
    };
    return new Promise((resolve, reject)=>{resolve(result)});
};


async function LoadPlayer(username, puuid){
    if( puuid === undefined || username === undefined) return {success: false};

    // Account data
    let accountId, summonerId, summonerLevel, percentCompleteForNextLevel;
    try{
        await fetch(
            `${RiotClientAccessUrl}/lol-summoner/v1/summoners?name=${username}`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.json();
        }).then(data => {
            accountId = data["accountId"];
            summonerId = data["summonerId"];
            summonerLevel = data["summonerLevel"];
            percentCompleteForNextLevel = data["percentCompleteForNextLevel"];
        });
    }catch(e){
        console.log(e);
    };

    // Rank data
    let soloRank, flexRank;
    try{
        await fetch(
            `${RiotClientAccessUrl}/lol-ranked/v1/ranked-stats/${puuid}`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.json();
        }).then(data => {
            soloRank = {
                previousSeasonEndTier : data["queueMap"]["RANKED_SOLO_5x5"]["previousSeasonEndTier"],
                previousSeasonEndDivision : data["queueMap"]["RANKED_SOLO_5x5"]["previousSeasonEndDivision"],
                tier : data["queueMap"]["RANKED_SOLO_5x5"]["tier"],
                division : data["queueMap"]["RANKED_SOLO_5x5"]["division"],
                leaguePoints : data["queueMap"]["RANKED_SOLO_5x5"]["leaguePoints"],
                losses : 0,
                wins : 0,
                winrate : 0
            };
            flexRank = {
                tier : data["queueMap"]["RANKED_FLEX_SR"]["tier"],
                division : data["queueMap"]["RANKED_FLEX_SR"]["division"],
                leaguePoints : data["queueMap"]["RANKED_FLEX_SR"]["leaguePoints"],
                losses : 0,
                wins : 0,
                winrate : 0
            };
        });
    }catch(e){
        console.log(e);
    };

    // Career
    let positions = [
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        },
        {
            winrate : 0,
            wins : 0,
            losses : 0
        }
    ];
    try{
        let roles = ["TOP","JUNGLE","MID","BOTTOM","SUPPORT"];
        for(let i=0; i<roles.length; i++){
            await fetch(
                `${RiotClientAccessUrl}/lol-career-stats/v1/summoner-stats/${puuid}/${CURRENT_SEASON}/rank5solo/${roles[i]}`,
                {
                    method:"GET",
                    headers: {
                        'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                    }
                }
            ).then(res => {
                return res.json();
            }).then(data => {
                if(data["errorCode"] != undefined) return;
                data = data["seasonSummary"][`${CURRENT_SEASON}`]["rank5solo"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"];
                positions[i].wins += data["victory"];
                positions[i].losses += data["defeat"];
                soloRank.wins += data["victory"];
                soloRank.losses += data["defeat"];
                soloRank.winrate = Math.floor((soloRank.wins / ( 
                    (soloRank.wins+soloRank.losses) === 0 ? 1 : (soloRank.wins+soloRank.losses) 
                )) * 100);
                positions[i].winrate = Math.floor((positions[i].wins / ( 
                    (positions[i].wins+positions[i].losses) === 0 ? 1 : (positions[i].wins+positions[i].losses) 
                )) * 100);
            });
        };
        for(let i=0; i<roles.length; i++){
            await fetch(
                `${RiotClientAccessUrl}/lol-career-stats/v1/summoner-stats/${puuid}/${CURRENT_SEASON}/rank5flex/${roles[i]}`,
                {
                    method:"GET",
                    headers: {
                        'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                    }
                }
            ).then(res => {
                return res.json();
            }).then(data => {
                if(data["errorCode"] != undefined) return;
                data = data["seasonSummary"][`${CURRENT_SEASON}`]["rank5flex"]["positionSummaries"][roles[i]]["positionSummary"]["stats"]["CareerStats.js"];
                positions[i].wins += data["victory"];
                positions[i].losses += data["defeat"];
                flexRank.wins += data["victory"];
                flexRank.losses += data["defeat"];
                flexRank.winrate = Math.floor((flexRank.wins / ( 
                    (flexRank.wins+flexRank.losses) === 0 ? 1 : (flexRank.wins+flexRank.losses) 
                )) * 100);
                positions[i].winrate = Math.floor((positions[i].wins / ( 
                    (positions[i].wins+positions[i].losses) === 0 ? 1 : (positions[i].wins+positions[i].losses) 
                )) * 100);
            });
        };
    }catch(e){
        console.log(e);
    };

    // Mastery data
    let mastery;
    try{
        await fetch(
            `${RiotClientAccessUrl}/lol-collections/v1/inventories/${summonerId}/champion-mastery`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.json();
        }).then(data => {
            data.sort((a, b)=>{b.championPoints-a.championPoints});
            data.concat(
                [null, null, null].map((_)=>{
                    return {
                        "championId": 0,
                        "championLevel": 0,
                        "championPoints": 0,
                        "formattedChampionPoints": "0",
                        "highestGrade": "NA"
                    }
                })
            );
            mastery = [
                {
                    "championId": data[0].championId,
                    "championLevel": data[0].championLevel,
                    "championPoints": data[0].championPoints,
                    "formattedChampionPoints": data[0].formattedChampionPoints,
                    "highestGrade": data[0].highestGrade
                },
                {
                    "championId": data[1].championId,
                    "championLevel": data[1].championLevel,
                    "championPoints": data[1].championPoints,
                    "formattedChampionPoints": data[1].formattedChampionPoints,
                    "highestGrade": data[1].highestGrade
                },
                {
                    "championId": data[2].championId,
                    "championLevel": data[2].championLevel,
                    "championPoints": data[2].championPoints,
                    "formattedChampionPoints": data[2].formattedChampionPoints,
                    "highestGrade": data[2].highestGrade
                }
            ]
        });
    }catch(e){
        console.log(e);
    };

    // Match data
    let recentMatches = [];
    try{
        await fetch(
            `${RiotClientAccessUrl}/lol-match-history/v1/products/lol/${puuid}/matches?begIndex=&endIndex=10`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.json();
        }).then(data => {
            data = data.games.games;
            let dateNm = [12*31*24*60*60, 31*24*60*60, 24*60*60], timeNm = [60*60, 60, 1];
            for(let i=0; i<Math.min(data.length, 10); i++){
                let temp = data[i]["gameCreationDate"].slice(0, 19).split("T");
                recentMatches.push({
                    gameCreationStamp : temp[0].split("-").map((s, idx)=>{
                        return parseInt(s)*dateNm[idx]
                    }).concat(temp[1].split(":").map((s, idx)=>{
                        return parseInt(s)*timeNm[idx]
                    })).reduce((a, b) => a + b, 0),
                    gameDurationM : Math.floor(data[i]["gameDuration"]/60),
                    gameDurationS : data[i]["gameDuration"]%60,
                    mapId : data[i]["mapId"],
                    queueId : data[i]["queueId"],
                    championId : data[i]["participants"][0]["championId"],
                    champLevel : data[i]["participants"][0]["stats"]["champLevel"],
                    spell1Id : data[i]["participants"][0]["spell1Id"],
                    spell2Id : data[i]["participants"][0]["spell2Id"],
                    assists : data[i]["participants"][0]["stats"]["assists"],
                    deaths : data[i]["participants"][0]["stats"]["deaths"],
                    kills : data[i]["participants"][0]["stats"]["kills"],
                    goldEarned : data[i]["participants"][0]["stats"]["goldEarned"],
                    totalMinionsKilled : data[i]["participants"][0]["stats"]["totalMinionsKilled"],
                    win : data[i]["participants"][0]["stats"]["win"],
                    items : [
                        data[i]["participants"][0]["stats"]["item0"],
                        data[i]["participants"][0]["stats"]["item1"],
                        data[i]["participants"][0]["stats"]["item2"],
                        data[i]["participants"][0]["stats"]["item3"],
                        data[i]["participants"][0]["stats"]["item4"],
                        data[i]["participants"][0]["stats"]["item5"],
                        data[i]["participants"][0]["stats"]["item6"],
                    ]
                });
            };
        });
    }catch(e){
        console.log(e);
    };


    let result = {
        isEqual : (other)=>{return other.username === username},
        username : username,
        puuid : puuid,
        accountId : accountId,
        summonerId : summonerId,
        summonerLevel : summonerLevel,
        percentCompleteForNextLevel : percentCompleteForNextLevel,
        soloRank : soloRank,
        flexRank : flexRank,
        mastery : mastery,
        positions : positions,
        recentMatches : recentMatches,
        success : true
    };
    console.log(result);
    return new Promise(
        (resolve, reject) => {
            setInterval(()=>{
                if(result.success){
                    resolve(result);
                }
            }, 500)
        }
    );
};


async function LoadPlayerFromLogString(logString){
    let looking = "";
    let currentIdx = 0;

    let isLocal = logString.includes("**LOCAL**");

    looking = "'";
    currentIdx = logString.indexOf(looking);
    let username = currentIdx>0 ? logString.slice(currentIdx+looking.length, logString.indexOf("'", currentIdx+1)) : undefined;

    looking = "Champion(";
    currentIdx = logString.indexOf(looking);
    let champion = currentIdx>0 ? logString.slice(currentIdx+looking.length, logString.indexOf(")", currentIdx+1)) : undefined;

    looking = "TeamBuilderRole(";
    currentIdx = logString.indexOf(looking);
    let role = currentIdx>0 ? logString.slice(currentIdx+looking.length, logString.indexOf(")", currentIdx+1)) : undefined;
    if(role !== undefined && role == "UTILITY") role = "SUPPORT";

    looking = "PUUID(";
    currentIdx = logString.indexOf(looking);
    let puuid = currentIdx>0 ? logString.slice(currentIdx+looking.length, logString.indexOf(")", currentIdx+1)) : undefined;

    let result = {success:false};
    await LoadPlayer(username, puuid).then(data=>{result = data});
    result.champion = champion;
    result.isLocal = isLocal;

    return new Promise(
        (resolve, reject) => {
            setInterval(()=>{
                if(result.success){
                    resolve(result);
                }
            }, 500)
        }
    );
};


async function LoadPlayerFromSummonerId(summonerId){
    let username, puuid;
    try{
        await fetch(
            `${RiotClientAccessUrl}/lol-summoner/v1/summoners/${summonerId}`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.json();
        }).then(data => {
            username = data["displayName"];
            puuid = data["puuid"];
        });
    }catch(e){
        console.log(e);
    };

    let result = {success:false};
    await LoadPlayer(username, puuid).then(data=>{result = data});
    return new Promise(
        (resolve, reject) => {
            setInterval(()=>{
                if(result.success){
                    resolve(result);
                }
            }, 500)
        }
    );
};


async function LoadPlayerWithPuuid(puuid){

    let result;
    await LoadPlayer(username, puuid).then(data=>{result = data});

    return new Promise((resolve, reject)=>{resolve(result)});
};


async function SearchChampionSelectTeam(){
    let teamSummoners = {success:false};
    try{
        await fetch(
            `${RiotClientAccessUrl}/lol-champ-select/v1/session`,
            {
                method:"GET",
                headers: {
                    'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
                }
            }
        ).then(res => {
            return res.json();
        }).then(data => {
            if(data["errorCode"] != undefined){
                teamSummoners = {success:false};
                return;
            };
            let myTeam = [];
            for(let i=0; i<data["myTeam"].length; i++){
                myTeam.push({
                    summonerId : data["myTeam"][i]["summonerId"],
                    role : data["myTeam"][i]["assignedPosition"]
                });
            };
            return new Promise((resolve, reject) => {
                setInterval(()=>{
                    if( myTeam.length == data["myTeam"].length ){
                        teamSummoners = {
                            success : true,
                            gameId : data["gameId"],
                            myTeam : myTeam
                        };
                        resolve(teamSummoners);
                    };
                }, 500);
            });
        });
    }catch(e){
        console.log(e);
    };

    if( !teamSummoners.success ) return new Promise((resolve, reject)=>{
        resolve({success : false});
    });

    let TeamOrder = [];
    for(let i=0; i<teamSummoners.myTeam.length; i++){
        await LoadPlayerFromSummonerId( teamSummoners.myTeam[i].summonerId ).then(res => {
            if(res.success){
                res.role = teamSummoners.myTeam[i].role;
                TeamOrder.push(res);
            };
        });
    };

    return new Promise((resolve, reject)=>{
        setInterval(()=>{
            if( TeamOrder.length == teamSummoners.myTeam.length ){
                TeamOrder.sort((a, b)=>{return ROLE_ORDER[a.role] - ROLE_ORDER[b.role]});
                resolve({success : true, A : TeamOrder, gameId : teamSummoners.gameId});
            };
        }, 500);
    });
};


async function SearchLatestGameAll(){
    let TeamOrder = [];
    let TeamChaos = [];
    if( !IsReadyToSearch() ) return {success : false};
    try{
        let log_dir = "";
        await fetch(
            `file:///${GameFilesLocation}/Game/Logs/GameLogs/`,
            {method:"GET"}
        ).then(res => {
            return res.text();
        }).then(dirs => {
            let log_dirs = dirs.split("<script>addRow(\"").slice(1).map(fn => fn.split("\"")[0]);
            log_dirs.sort((a, b) => {
                let atimes = a.replace("T", "-").split("-").map(t => parseInt(t));
                let btimes = b.replace("T", "-").split("-").map(t => parseInt(t));
                return(
                    atimes[0]*12*31*24*60*60 + atimes[1]*31*24*60*60 + atimes[2]*24*60*60 + btimes[3]*60*60 + btimes[4]*60 + btimes[5]
                ) - (
                    btimes[0]*12*31*24*60*60 + btimes[1]*31*24*60*60 + btimes[2]*24*60*60 + btimes[3]*60*60 + btimes[4]*60 + btimes[5]
                );
            });
            log_dir = log_dirs[log_dirs.length-1];
        });

        let current_idx = 0, result = {success:false}, TOp = -1, TCp = -1;
        await fetch(
            `file:///${GameFilesLocation}/Game/Logs/GameLogs/${log_dir}/${log_dir}_r3dlog.txt`,
            {method:"GET"}
        ).then(res => {
            return res.text();
        }).then(log_data => {
            current_idx = log_data.indexOf("TeamOrder 4) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TO 4");
                if(TOp<0) TOp = 5;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamOrder.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamOrder 3) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TO 3");
                if(TOp<0) TOp = 4;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamOrder.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamOrder 2) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TO 2");
                if(TOp<0) TOp = 3;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamOrder.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamOrder 1) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TO 1");
                if(TOp<0) TOp = 2;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamOrder.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamOrder 0) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TO 0");
                if(TOp<0) TOp = 1;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamOrder.push(res);
                });
            }else{
                TOp = 0;
            };


            current_idx = log_data.indexOf("TeamChaos 4) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TC 4");
                if(TCp<0) TCp = 5;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamChaos.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamChaos 3) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TC 3");
                if(TCp<0) TCp = 4;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamChaos.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamChaos 2) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TC 2");
                if(TCp<0) TCp = 3;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamChaos.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamChaos 1) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TC 1");
                if(TCp<0) TCp = 2;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamChaos.push(res);
                });
            };

            current_idx = log_data.indexOf("TeamChaos 0) ");
            if(log_data[current_idx] !== undefined){
                console.log("Load TC 0");
                if(TCp<0) TCp = 1;
                LoadPlayerFromLogString( log_data.slice(current_idx, log_data.indexOf("\n", current_idx)) ).then(res => {
                    if(res.success) TeamChaos.push(res);
                });
            }else{
                TCp = 0;
            };


            return new Promise(
                (resolve, reject) => {
                    setInterval(()=>{
                        if((TOp >= 0 && TCp >= 0) && (TeamOrder.length == TOp && TeamChaos.length == TCp)){
                            TeamOrder.sort((a, b)=>{return ROLE_ORDER[a.role] - ROLE_ORDER[b.role]});
                            TeamChaos.sort((a, b)=>{return ROLE_ORDER[a.role] - ROLE_ORDER[b.role]});
                            resolve({A:TeamOrder, B:TeamChaos});
                        }
                    }, 500)
                }
            );
        }).then(res => {
            let OisL=false, CisL=false;
            for(let i=0; i<res.A.length; i++){
                console.log(res.A[i]);
                if(res.A[i].isLocal) OisL = true;
            };
            for(let i=0; i<res.B.length; i++){
                console.log(res.B[i]);
                if(res.B[i].isLocal) CisL = true;
            };
            console.log(OisL, CisL);
            if( OisL ){
                console.log(TeamOrder, TeamChaos);
                result = {
                    success : true,
                    A:TeamOrder,
                    B:TeamChaos
                };
                return new Promise((resolve, reject)=>{
                    resolve(result);
                });
            }else if( CisL ){
                console.log(TeamOrder, TeamChaos);
                result = {
                    success : true,
                    A:TeamChaos,
                    B:TeamOrder
                };
                return new Promise((resolve, reject)=>{
                    resolve(result);
                });
            }else{
                console.log(TeamOrder);
                console.log(TeamChaos);
                return new Promise((resolve, reject)=>{
                    resolve({success : false});
                });
            };
        });
        return new Promise((resolve, reject)=>{
            resolve(result);
        });
    }catch(e){
        console.log(e);
    };
    return new Promise((resolve, reject)=>{
        resolve({success : false});
    });
};



function SendToDisplay(team){
    return new Promise((resolve, reject) => {
        chrome.tabs.create(
            {url: chrome.runtime.getURL("display.html")},
            function(tab) {
                var updateHandler = function(tabId, onchange) {
                    if(tabId === tab.id && onchange.status === "complete"){
                        chrome.tabs.sendMessage(tabId, {team: team}, (res)=>{
                            if( res === undefined || !res.success ) reject({success : res.success});
                            else resolve({success : res.success});
                        });
                    };
                };
                chrome.tabs.onUpdated.addListener(updateHandler);
                chrome.tabs.sendMessage(tab.id, {team: team}, (res)=>{
                    if( res !== undefined || !res.success ) reject({success : res.success});
                    else resolve({success : res.success});
                });
            }
        );
    });
};



async function ManualDisplayOrder(){
    if( !IsReadyToSearch() ){
        await AssertReadyToSearch(10000, 500);
        console.log("ManualDisplayOrder Ready");
    };
    let flag = false;
    console.log("Start ManualDisplayOrder-1");
    await SearchChampionSelectTeam().then(res => {
        console.log(res, 1);
        if( !res.success ) return;
        else{
            SendToDisplay(res.A);
            CurrentlyDisplayingGameId = res.gameId;
            flag = true;
        }
    });
    if( flag ) return;
    console.log("Start ManualDisplayOrder-2");
    await SearchLatestGameAll().then(res => {
        console.log(res, 2);
        if( !res.success ) return;
        else{
            SendToDisplay(res.A);
            CurrentlyDisplayingGameId = res.gameId;
        }
    });
};
async function ManualDisplayChaos(){
    if( !IsReadyToSearch() ){
        await AssertReadyToSearch(10000, 500);
        console.log("ManualDisplayChaos Ready");
    };
    console.log("Start ManualDisplayChaos");
    await SearchLatestGameAll().then(res => {
        console.log(res);
        if( !res.success ) return;
        else{
            SendToDisplay(res.B);
            CurrentlyDisplayingGameId = res.gameId;
        }
    });
};
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if(message === "ManualDisplayOrder"){
        ManualDisplayOrder();
        sendResponse();
    }else if(message === "ManualDisplayChaos"){
        ManualDisplayChaos();
        sendResponse();
    }
});



async function Loop(){
    console.log("Loop");
    if( !IsReadyToSearch() ) return Initialize();

    // Auto Search Team
    await SearchChampionSelectTeam().then(res => {
        if( !res.success ) return;
        console.log(CurrentlyDisplayingGameId, res.gameId)
        if( CurrentlyDisplayingGameId == res.gameId ) return;
        SendToDisplay(res.A).then(response => {
            if(response.success) CurrentlyDisplayingGameId = res.gameId;
        });
    });
};
setInterval(Loop, UpdateGap*1000);
async function UpdateLocal(){
    console.log("Update Local");
    if( !IsReadyToSearch() ) return Initialize();

    // Update Local Summoner
    await LoadLocalSummoner().then(res => {
        if( !res.success ) return Initialize();
        chrome.storage.local.set({
            "LocalSummoner": res
        }, () => {});
    });
};
setInterval(UpdateLocal, UpdateGap*30000);