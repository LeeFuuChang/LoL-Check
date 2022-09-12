const PAGE_1 = document.querySelector("#card-page1");
const PAGE_2 = document.querySelector("#card-page2");
const TUTORIAL_URL = "https://hackmd.io/@Cracked-Head-Coder/LoL-Check";
var GameFilesLocation = "";
const os = {
    __Process__ : (result, root) => {
        result = result.split("<script>addRow(\"");
        let data = {dir:[], file:[]};
        for(let i=1; i<result.length; i++){
            let temp = result[i].split(",");
            let path = `${root}/${temp[0].slice(0, temp[0].length-1)}`;
            let isDir = parseInt(temp[2]);
            if(isDir){
                data.dir.push(path);
            }else{
                data.file.push(path);
            }
        };
        return new Promise((resolve, reject)=>{return resolve(data)});
    },
    listdir : async (path) => {
        let result = {success:false};
        try {
            await fetch(
                `file:///${path}`,
                {method:"GET"}
            ).then(res => {
                return res.text();
            }).then(text => {
                os.__Process__(text, path).then(res => {
                    result.success = true;
                    result.dir = res.dir;
                    result.file = res.file;
                });
            });
        } catch (e) {
            console.log(e);
            console.log(path);
        };
        return new Promise((resolve, reject)=>{return resolve(result)});
    }
};
async function FindGarenaGameStorage(){
    let result="", target="Garena/Games", flag=false;
    for(let i=0; i<26; i++){
        let now = [], next = [];
        rootChr = String.fromCharCode(65+i);

        await os.listdir(`${rootChr}:`).then(res=>{
            if( !res.success ) return;
            for(let j=0; j<res.dir.length; j++){
                if(res.dir[j].includes(".")) continue;
                if(res.dir[j].includes(" ")) continue;
                now.push(encodeURI(res.dir[j]));
            };
        });

        while(now.length != 0){
            console.log(rootChr);
            for(let j=0; j<now.length; j++){
                if(decodeURI(now[j]).includes(target)){
                    flag = true;
                    result = now[j];
                    break;
                };
                await os.listdir(now[j]).then(res=>{
                    for(let k=0; k<res.dir.length; k++){
                        if(res.dir[k].includes(".")) continue;
                        if(res.dir[k].includes(" ")) continue;
                        next.push(encodeURI(res.dir[k]));
                    };
                });
            };
            if(flag) break;
            now = next;
            next = [];
        };
        if(flag) break;
    };
    await os.listdir(result).then(res => {result = res.dir[0];});
    result = result.includes(target) ? result : "失敗";
    return new Promise((resolve, reject)=>{return resolve(decodeURI(result))});
};



const HTTPS = "https://"
const CURRENT_SEASON = 12;
const CLIENT_LOG_FILETYPE = "LeagueClientUx.log";
const RIOT_BASE_URL = "https://riot:";
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

    // try{
    //     await fetch(
    //         `${RiotClientAccessUrl}/riotclient/auth-token`,
    //         {
    //             method:"GET",
    //             headers: {
    //                 'Content-Type': 'application/json',
    //                 'Authorization': `Basic ${btoa(`riot:${RiotUserAccessToken}`)}`,
    //             }
    //         }
    //     ).then(res => {
    //         return res.text();
    //     }).then(token => {
    //         console.log(token)
    //     });
    // }catch(e){
    //     console.log(e);
    // };

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
        GameFilesLocation !== ""
    ) && (
        RiotUserAccessToken !== ""
    ) && (
        RiotClientAccessUrl !== ""
    ) && (
        LatestClientLog !== ""
    );
};
async function LoadPlayer(){
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



function SendMessage(message){

};
















PAGE_1.querySelector(".setting").addEventListener("click", ()=>{
    PAGE_1.style.display = "none";
    PAGE_2.style.display = "flex";
});
PAGE_1.querySelector("#get-A").addEventListener("click", ()=>{
    if(GameFilesLocation === ""){
        alert("請先設定英雄聯盟路徑");
        chrome.storage.local.get(["GameFilesLocation"], async function(items){
            if(items["GameFilesLocation"] === undefined){
                document.querySelector("#filepath").value = "";
                GameFilesLocation = ""
            }else{
                document.querySelector("#filepath").value = items["GameFilesLocation"];
                GameFilesLocation = items["GameFilesLocation"];
            };
        });
        return;
    };
    chrome.runtime.sendMessage("ManualDisplayOrder", ()=>{
        alert("請稍後，已開始搜尋隊友數據");
    });
});
PAGE_1.querySelector("#get-B").addEventListener("click", ()=>{
    if(GameFilesLocation === ""){
        alert("請先設定英雄聯盟路徑");
        chrome.storage.local.get(["GameFilesLocation"], async function(items){
            if(items["GameFilesLocation"] === undefined){
                document.querySelector("#filepath").value = "";
                GameFilesLocation = ""
            }else{
                document.querySelector("#filepath").value = items["GameFilesLocation"];
                GameFilesLocation = items["GameFilesLocation"];
            };
        });
        return;
    };
    chrome.runtime.sendMessage("ManualDisplayChaos", ()=>{
        alert("請稍後，已開始搜尋對手數據");
    });
});
PAGE_1.querySelector("#next").addEventListener("click", ()=>{
    let winrate = PAGE_1.querySelector(".winrate");
    let pages = winrate.querySelectorAll(".page");
    let first = winrate.removeChild(pages[0]);
    winrate.appendChild(first);
});
PAGE_1.querySelector("#prev").addEventListener("click", ()=>{
    let winrate = PAGE_1.querySelector(".winrate");
    let pages = winrate.querySelectorAll(".page");
    let last = winrate.removeChild(pages[pages.length-1]);
    winrate.insertBefore(last, pages[0]);
});
PAGE_2.querySelector(".setting").addEventListener("click", ()=>{
    PAGE_1.style.display = "flex";
    PAGE_2.style.display = "none";
});
PAGE_2.querySelector("#tutorial").addEventListener("click", ()=>{
    window.open(TUTORIAL_URL, "_blank");
});
PAGE_2.querySelector("#autopath").addEventListener("click", ()=>{
    FindGarenaGameStorage().then(res => {
        GameFilesLocation = res;
        PAGE_2.querySelector("#filepath").value = res;
		chrome.storage.local.set({
            "GameFilesLocation": res
        }, () => {});
    });
});
PAGE_2.querySelector("#filepath").addEventListener("input", (e)=>{
    GameFilesLocation = e.target.value;
    chrome.storage.local.set({
        "GameFilesLocation": e.target.value
    }, () => {});
});
PAGE_2.querySelector("#openfileurl").addEventListener("click", ()=>{
    chrome.tabs.create({ 'url': 'chrome://extensions/?options=' + chrome.runtime.id });
});
PAGE_2.querySelector("#openlocalfile").addEventListener("click", ()=>{
    chrome.tabs.create({ 'url': 'chrome://flags/#allow-insecure-localhost' });
});



window.addEventListener("load", ()=>{
    chrome.storage.local.get([
        "GameFilesLocation", "LocalSummoner"
    ], async function(items){
		if(items["GameFilesLocation"] === undefined){
            document.querySelector("#filepath").value = "";
		}else{
            document.querySelector("#filepath").value = items["GameFilesLocation"];
            GameFilesLocation = items["GameFilesLocation"];
		};
		if(items["LocalSummoner"] === undefined){
            await LoadPlayer().then(res => {
                if( !res.success ) return;
                chrome.storage.local.set({
                    "LocalSummoner": res
                }, () => {});
                let laneDetails = document.querySelectorAll(".lane-detail");
                for(let i=0; i<laneDetails.length; i++){
                    laneDetails[i].querySelector(".lane-detail-W").innerHTML = `${res.positions[i].wins} 勝`;
                    laneDetails[i].querySelector(".lane-detail-L").innerHTML = `${res.positions[i].losses} 敗`;
                    laneDetails[i].querySelector(".lane-detail-WR").innerHTML = `${res.positions[i].winrate}% 勝率`;
                };
                let solo = document.querySelector("#solo").querySelector(".info");
                solo.querySelector("h3").innerHTML = `${res.soloRank.winrate}<span>%</span>`;
                solo.querySelector("h4").innerHTML = `${res.soloRank.wins} W<span>|</span>${res.soloRank.losses} L`;
                let flex = document.querySelector("#flex").querySelector(".info");
                flex.querySelector("h3").innerHTML = `${res.flexRank.winrate}<span>%</span>`;
                flex.querySelector("h4").innerHTML = `${res.flexRank.wins} W<span>|</span>${res.flexRank.losses} L`;
            });
		}else{
            let laneDetails = document.querySelectorAll(".lane-detail");
            for(let i=0; i<laneDetails.length; i++){
                laneDetails[i].querySelector(".lane-detail-W").innerHTML = `${items["LocalSummoner"].positions[i].wins} 勝`;
                laneDetails[i].querySelector(".lane-detail-L").innerHTML = `${items["LocalSummoner"].positions[i].losses} 敗`;
                laneDetails[i].querySelector(".lane-detail-WR").innerHTML = `${items["LocalSummoner"].positions[i].winrate}% 勝率`;
            };
            let solo = document.querySelector("#solo").querySelector(".info");
            solo.querySelector("h3").innerHTML = `${items["LocalSummoner"].soloRank.winrate}<span>%</span>`;
            solo.querySelector("h4").innerHTML = `${items["LocalSummoner"].soloRank.wins} W<span>|</span>${items["LocalSummoner"].soloRank.losses} L`;
            let flex = document.querySelector("#flex").querySelector(".info");
            flex.querySelector("h3").innerHTML = `${items["LocalSummoner"].flexRank.winrate}<span>%</span>`;
            flex.querySelector("h4").innerHTML = `${items["LocalSummoner"].flexRank.wins} W<span>|</span>${items["LocalSummoner"].flexRank.losses} L`;
		};
	});
});