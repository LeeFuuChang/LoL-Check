const MAIN = document.querySelector("main");
const TRANSLATION = {
    "NONE": {
        "NA": "無牌位"
    },
    "IRON": {
        "IV": "鐵牌 IV",
        "III": "鐵牌 III",
        "II": "鐵牌 II",
        "I": "鐵牌 I",
    },
    "BRONZE": {
        "IV": "銅牌 IV",
        "III": "銅牌 III",
        "II": "銅牌 II",
        "I": "銅牌 I",
    },
    "SILVER": {
        "IV": "銀牌 IV",
        "III": "銀牌 III",
        "II": "銀牌 II",
        "I": "銀牌 I",
    },
    "GOLD": {
        "IV": "金牌 IV",
        "III": "金牌 III",
        "II": "金牌 II",
        "I": "金牌 I",
    },
    "PLATINUM": {
        "IV": "白金 IV",
        "III": "白金 III",
        "II": "白金 II",
        "I": "白金 I",
    },
    "DIAMOND": {
        "IV": "鑽石 IV",
        "III": "鑽石 III",
        "II": "鑽石 II",
        "I": "鑽石 I",
    },
    "MASTER": {
        "IV": "大師",
        "III": "大師",
        "II": "大師",
        "I": "大師",
        "NA": "大師"
    },
    "GRANDMASTER": {
        "IV": "宗師",
        "III": "宗師",
        "II": "宗師",
        "I": "宗師",
        "NA": "宗師"
    },
    "CHALLENGER": {
        "IV": "菁英",
        "III": "菁英",
        "II": "菁英",
        "I": "菁英",
        "NA": "菁英"
    },
};
const CHAMPION_ID_TO_ENG = {
    0: "NA",
    200: "Bel'Veth",
    266: "Aatrox",
    103: "Ahri",
    84 : "Akali",
    166: "Akshan",
    12 : "Alistar",
    32 : "Amumu",
    34 : "Anivia",
    1  : "Annie",
    523: "Aphelios",
    22 : "Ashe",
    136: "Aurelion Sol",
    268: "Azir",
    432: "Bard",
    53 : "Blitzcrank",
    63 : "Brand",
    201: "Braum",
    51 : "Caitlyn",
    164: "Camille",
    69 : "Cassiopeia",
    31 : "Cho'Gath",
    42 : "Corki",
    122: "Darius",
    131: "Diana",
    119: "Draven",
    36 : "Dr. Mundo",
    245: "Ekko",
    60 : "Elise",
    28 : "Evelynn",
    81 : "Ezreal",
    9  : "Fiddlesticks",
    114: "Fiora",
    105: "Fizz",
    3  : "Galio",
    41 : "Gangplank",
    86 : "Garen",
    150: "Gnar",
    79 : "Gragas",
    104: "Graves",
    887: "Gwen",
    120: "Hecarim",
    74 : "Heimerdinger",
    420: "Illaoi",
    39 : "Irelia",
    427: "Ivern",
    40 : "Janna",
    59 : "Jarvan IV",
    24 : "Jax",
    126: "Jayce",
    202: "Jhin",
    222: "Jinx",
    145: "Kai'Sa",
    429: "Kalista",
    43 : "Karma",
    30 : "Karthus",
    38 : "Kassadin",
    55 : "Katarina",
    10 : "Kayle",
    141: "Kayn",
    85 : "Kennen",
    121: "Kha'Zix",
    203: "Kindred",
    240: "Kled",
    96 : "Kog'Maw",
    7  : "LeBlanc",
    64 : "Lee Sin",
    89 : "Leona",
    876: "Lillia",
    127: "Lissandra",
    236: "Lucian",
    117: "Lulu",
    99 : "Lux",
    54 : "Malphite",
    90 : "Malzahar",
    57 : "Maokai",
    11 : "Master Yi",
    21 : "Miss Fortune",
    62 : "Wukong",
    82 : "Mordekaiser",
    25 : "Morgana",
    267: "Nami",
    75 : "Nasus",
    111: "Nautilus",
    518: "Neeko",
    76 : "Nidalee",
    56 : "Nocturne",
    20 : "Nunu",
    2  : "Olaf",
    61 : "Orianna",
    516: "Ornn",
    80 : "Pantheon",
    78 : "Poppy",
    555: "Pyke",
    246: "Qiyana",
    133: "Quinn",
    497: "Rakan",
    33 : "Rammus",
    421: "Rek'Sai",
    526: "Rell",
    888: "Renata Glasc",
    58 : "Renekton",
    107: "Rengar",
    92 : "Riven",
    68 : "Rumble",
    13 : "Ryze",
    360: "Samira",
    113: "Sejuani",
    235: "Senna",
    147: "Seraphine",
    875: "Sett",
    35 : "Shaco",
    98 : "Shen",
    102: "Shyvana",
    27 : "Singed",
    14 : "Sion",
    15 : "Sivir",
    72 : "Skarner",
    37 : "Sona",
    16 : "Soraka",
    50 : "Swain",
    517: "Sylas",
    134: "Syndra",
    223: "Tahm Kench",
    163: "Taliyah",
    91 : "Talon",
    44 : "Taric",
    17 : "Teemo",
    412: "Thresh",
    18 : "Tristana",
    48 : "Trundle",
    23 : "Tryndamere",
    4  : "Twisted Fate",
    29 : "Twitch",
    77 : "Udyr",
    6  : "Urgot",
    110: "Varus",
    67 : "Vayne",
    45 : "Veigar",
    161: "Vel'Koz",
    711: "Vex",
    254: "Vi",
    234: "Viego",
    112: "Viktor",
    8  : "Vladimir",
    106: "Volibear",
    19 : "Warwick",
    498: "Xayah",
    101: "Xerath",
    5  : "Xin Zhao",
    157: "Yasuo",
    777: "Yone",
    83 : "Yorick",
    350: "Yuumi",
    154: "Zac",
    238: "Zed",
    221: "Zeri",
    115: "Ziggs",
    26 : "Zilean",
    142: "Zoe",
    143: "Zyra"
};
const CHAMPION_ID_TO_TW = {
    0: "",
    200: "貝爾薇斯",
    266: "厄薩斯",
    103: "阿璃",
    84: "阿卡莉",
    166: "埃可尚",
    12: "亞歷斯塔",
    32: "阿姆姆",
    34: "艾妮維亞",
    1: "安妮",
    523: "亞菲利歐",
    22: "艾希",
    136: "翱銳龍獸",
    268: "阿祈爾",
    432: "巴德",
    53: "布里茨",
    63: "布蘭德",
    201: "布郎姆",
    51: "凱特琳",
    164: "卡蜜兒",
    69: "卡莎碧雅",
    31: "科加斯",
    42: "庫奇",
    122: "達瑞斯",
    131: "黛安娜",
    119: "達瑞文",
    36: "蒙多醫生",
    245: "艾克",
    60: "伊莉絲",
    28: "伊芙琳",
    81: "伊澤瑞爾",
    9: "費德提克",
    114: "菲歐拉",
    105: "飛斯",
    3: "加里歐",
    41: "剛普朗克",
    86: "蓋倫",
    150: "吶兒",
    79: "古拉格斯",
    104: "葛雷夫",
    887: "關",
    120: "赫克林",
    74: "漢默丁格",
    420: "伊羅旖",
    39: "伊瑞莉雅",
    427: "埃爾文",
    40: "珍娜",
    59: "嘉文四世",
    24: "賈克斯",
    126: "杰西",
    202: "燼",
    222: "吉茵珂絲",
    145: "凱莎",
    429: "克黎思妲",
    43: "卡瑪",
    30: "卡爾瑟斯",
    38: "卡薩丁",
    55: "卡特蓮娜",
    10: "凱爾",
    141: "慨影",
    85: "凱能",
    121: "卡力斯",
    203: "鏡爪",
    240: "克雷德",
    96: "寇格魔",
    7: "勒布朗",
    64: "李星",
    89: "雷歐娜",
    876: "莉莉亞",
    127: "麗珊卓",
    236: "路西恩",
    117: "露璐",
    99: "拉克絲",
    54: "墨菲特",
    90: "馬爾札哈",
    57: "茂凱",
    11: "易大師",
    21: "好運姐",
    62: "悟空",
    82: "魔鬥凱薩",
    25: "魔甘娜",
    267: "娜米",
    75: "納瑟斯",
    111: "納帝魯斯",
    518: "妮可",
    76: "奈德麗",
    56: "夜曲",
    20: "努努和威朗普",
    2: "歐拉夫",
    61: "奧莉安娜",
    516: "鄂爾",
    80: "潘森",
    78: "波比",
    555: "派克",
    246: "姬亞娜",
    133: "葵恩",
    497: "銳空",
    33: "拉姆斯",
    421: "雷珂煞",
    526: "銳兒",
    888: "睿娜妲．格萊斯克",
    58: "雷尼克頓",
    107: "雷葛爾",
    92: "雷玟",
    68: "藍寶",
    13: "雷茲",
    360: "煞蜜拉",
    113: "史瓦妮",
    235: "姍娜",
    147: "瑟菈紛",
    875: "賽特",
    35: "薩科",
    98: "慎",
    102: "希瓦娜",
    27: "辛吉德",
    14: "賽恩",
    15: "希維爾",
    72: "史加納",
    37: "索娜",
    16: "索拉卡",
    50: "斯溫",
    517: "賽勒斯",
    134: "星朵拉",
    223: "貪啃奇",
    163: "塔莉雅",
    91: "塔隆",
    44: "塔里克",
    17: "提摩",
    412: "瑟雷西",
    18: "崔絲塔娜",
    48: "特朗德",
    23: "泰達米爾",
    4: "逆命",
    29: "圖奇",
    77: "烏迪爾",
    6: "烏爾加特",
    110: "法洛士",
    67: "汎",
    45: "維迦",
    161: "威寇茲",
    711: "薇可絲",
    254: "菲艾",
    234: "維爾戈",
    112: "維克特",
    8: "弗拉迪米爾",
    106: "弗力貝爾",
    19: "沃維克",
    498: "剎雅",
    101: "齊勒斯",
    5: "趙信",
    157: "犽宿",
    777: "犽凝",
    83: "約瑞科",
    350: "悠咪",
    154: "札克",
    238: "劫",
    221: "婕莉",
    115: "希格斯",
    26: "極靈",
    142: "柔依",
    143: "枷蘿"
};
const QUEUE_ID_TO_TW = {
    0: "自定義",
    78: "無限死鬥 (鏡像)",
    400: "一般對戰 (競技)",
    420: "單雙積分",
    430: "一般對戰 (盲選)",
    440: "彈性積分",
    450: "隨機單中",
    830: "電腦 (入門)",
    840: "電腦 (初階)",
    850: "電腦 (中階)",
    900: "阿福快打",
    920: "普羅王傳說",
    950: "夢魘挑戰 (票選)",
    960: "夢魘挑戰",
    1010: "冰雪阿福",
    1020: "無限死鬥",
    1200: "閃電急擊",
    1300: "閃電急擊",
    1400: "法典禁地",
    1900: "阿福快打 (自選)",
    2000: "教學 1",
    2010: "教學 2",
    2020: "教學 3"
};
const MAP_ID_TO_TW = {1: "召喚峽谷", 2: "召喚峽谷", 11: "召喚峽谷", 12: "咆嘯深淵", 14: "咆嘯深淵", 21: "閃電急擊"};





function AddPlayerToDisplay(data){
    let teamContainers = document.querySelectorAll(".team-container");
    let teamContainer = teamContainers[teamContainers.length-1];

    let date = new Date();
    let convertTime = [[12*31*24*60*60, "年"], [31*24*60*60, "個月"], [24*60*60, "天"], [60*60, "小時"], [60, "分鐘"], [1, "秒"]];
    let nowTimeStamp = (
        date.getFullYear()*convertTime[0][0]) + (
        (date.getMonth()+1)*convertTime[1][0]) + (
        date.getDate()*convertTime[2][0]) + (
        (date.getHours()-8)*convertTime[3][0]) + (
        date.getMinutes()*convertTime[4][0]) + (
        date.getSeconds()*convertTime[5][0]
    );
    let playerMatchHistoryHtml = "";
    for(let i=0; i<Math.min(data.recentMatches.length, 10); i++){
        let match = data.recentMatches[i];
        // console.log(nowTimeStamp, match.gameCreationStamp);
        let matchAge = nowTimeStamp - match.gameCreationStamp;
        let formattedAge;
        for(let j=0; j<convertTime.length; j++){
            formattedAge = Math.floor(matchAge / convertTime[j][0]);
            if(formattedAge > 0){
                formattedAge = `${formattedAge}${convertTime[j][1]}`
                break
            };
        };
        let matchCKDA = Math.floor(((match.kills+match.assists)/(match.deaths===0?1:match.deaths))*10);
        playerMatchHistoryHtml += `
		<div class="match-history" data-index-number="${i+1}">
			<div class="detail-wrapper">
				<div class="champion df aic jcc">
					<div class="champion-icon">
						<img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[match.championId]}.png" alt="">
						<div class="champion-level">
							<h4>${match.champLevel}</h4>
						</div>
					</div>
				</div>
				<div class="match-result df aic jcc">
					<div class="match-result-top">
						<div class="match-result-info df jcc">
							<h3 class="${match.win ? "win" : "lose"}c WL">${match.win ? "勝利" : "失敗"}</h3>
							<h3 class="queue-type">${QUEUE_ID_TO_TW[match.queueId]}</h3>
						</div>
					</div>
					<div class="match-result-bottom">
						<div class="spells df aic">
							<img src="assets/images/spells/${match.spell1Id}.png" alt="spell1">
							<img src="assets/images/spells/${match.spell2Id}.png" alt="spell2">
						</div>
					</div>
				</div>
				<div class="player-result df aic jcc">
					<div class="player-result-top">
						<div class="items df aic">
							<div class="item item0">
								<img src="assets/images/items/${match.items[0]}.png" alt="">
							</div>
							<div class="item item1">
								<img src="assets/images/items/${match.items[1]}.png" alt="">
							</div>
							<div class="item item2">
								<img src="assets/images/items/${match.items[2]}.png" alt="">
							</div>
							<div class="item item3">
								<img src="assets/images/items/${match.items[3]}.png" alt="">
							</div>
							<div class="item item4">
								<img src="assets/images/items/${match.items[4]}.png" alt="">
							</div>
							<div class="item item5">
								<img src="assets/images/items/${match.items[5]}.png" alt="">
							</div>
							<div class="item item6">
								<img src="assets/images/items/${match.items[6]}.png" alt="">
							</div>
						</div>
					</div>
					<div class="player-result-bottom df">
						<div class="KDA">
							<h3>${match.kills}<span>/</span>${match.deaths}<span>/</span>${match.assists}</h3>
						</div>
						<div class="cs">
							<h4>${match.totalMinionsKilled}<span>cs</span></h4>
						</div>
						<div class="gold">
							<h4><span>$</span>${match.goldEarned}</h4>
						</div>
					</div>
				</div>
				<div class="match-info">
					<h4 class="map">${MAP_ID_TO_TW[match.mapId]}</h4>
					<h4 class="duration">${`${match.gameDurationM}`.padStart(2, "0")}<span>:</span>${`${match.gameDurationS}`.padStart(2, "0")}</h4>
				</div>
			</div>
			<div class="history-wrapper df aic">
				<div class="champion-wrapper">
					<img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[match.championId]}.png" alt="" class="champion-icon">
				</div>
				<div class="match-info df jcc">
					<div class="info-section section-1 df aic">
						<div class="KDA df aic jcc ${match.win ? "win" : "lose"}b">
                            <h3>${match.kills}<span>/</span>${match.deaths}<span>/</span>${match.assists}</h3>
						</div>
						<div class="mode df aic jcc">
							<h3>${QUEUE_ID_TO_TW[match.queueId]}</h3>
						</div>
					</div>
					<div class="info-section section-2 df jcc">
						<div class="CKDA df aic jcc ${matchCKDA > 10 ? "win" : "lose"}c">
							<h3><span>${matchCKDA/10}</span>KDA</h3>
						</div>
						<div class="age df aic jcc">
							<h3>${formattedAge}<span>前</span></h3>
						</div>
					</div>
				</div>
			</div>
		</div>
		<hr style="width: 100%;">
        `
    }
    return new Promise(
        (resolve, reject)=>{
            teamContainer.insertAdjacentHTML(`beforeend`, `
            <div class="banner-container df aic jcc">
                <div class="banner-layer-1">
                    <div class="banner-layer-2 df aic jcc">
                        <div class="banner-page banner-page-0 df aic jcc" style="display: flex">
                            <div class="rank df aic jcc">
                                <div class="rank-container df aic jcc">
                                    <div class="rank-detail df aic jcc">
                                        <div class="rank-detail-type rank-detail-solo df jcc">
                                            <div class="detail-top rank-detail-solo-img">
                                            <img src="assets/images/ranks/${data.soloRank.tier}.png" alt="">
                                            </div>
                                            <div class="detail-bottom rank-detail-solo-img df aic jcc">
                                                <h3 class="rank-detail-solo-text tc">單雙積分</h3>
                                                <h3 class="rank-detail-solo-tier tc">${TRANSLATION[data.soloRank.tier][data.soloRank.division]}</h3>
                                                <h3 class="rank-detail-solo-stat df aic jcc">
                                                    <div class="tc">${data.soloRank.wins} W</div>
                                                    <div class="tc">${data.soloRank.losses} L</div>
                                                    <div class="tc">${data.soloRank.leaguePoints} LP</div>
                                                </h3>
                                            </div>
                                        </div>
                                        <div class="rank-detail-type rank-detail-flex df jcc">
                                            <div class="detail-top rank-detail-flex-img">
                                                <img src="assets/images/ranks/${data.flexRank.tier}.png" alt="">
                                            </div>
                                            <div class="detail-bottom rank-detail-flex-img df aic jcc">
                                                <h3 class="rank-detail-flex-text tc">彈性積分</h3>
                                                <h3 class="rank-detail-flex-tier tc">${TRANSLATION[data.flexRank.tier][data.flexRank.division]}</h3>
                                                <h3 class="rank-detail-flex-stat df aic jcc">
                                                    <div class="tc">${data.flexRank.wins} W</div>
                                                    <div class="tc">${data.flexRank.losses} L</div>
                                                    <div class="tc">${data.flexRank.leaguePoints} LP</div>
                                                </h3>
                                            </div>
                                        </div>
                                        <div class="rank-detail-type rank-detail-prev df jcc">
                                            <div class="detail-top rank-detail-prev-img">
                                                <img src="assets/images/ranks/${data.soloRank.previousSeasonEndTier}.png" alt="">
                                            </div>
                                            <div class="detail-bottom rank-detail-prev-img df aic jcc">
                                                <h3 class="rank-detail-prev-text tc">上季積分</h3>
                                                <h3 class="rank-detail-prev-tier tc">${TRANSLATION[data.soloRank.previousSeasonEndTier][data.soloRank.previousSeasonEndDivision]}</h3>
                                                <h3 class="rank-detail-prev-stat df aic jcc" style="opacity: 0">
                                                    <div class="tc">N/A</div>
                                                    <div class="tc">N/A</div>
                                                    <div class="tc">N/A</div>
                                                </h3>
                                            </div>
                                        </div>
                                    </div>
                                    <img src="assets/images/ranks/${data.soloRank.tier}.png" alt="">
                                    <h2 class="division df aic jcc">${"IIIV".includes(data.soloRank.division)?data.soloRank.division:"I"}</h2>
                                </div>
                            </div>
                            <div class="account df aic">
                                <h1 class="username df aic jcc">${data.username}</h1>
                                <div class="level df aic">
                                    <div 
                                        class="progress" 
                                        style="background: conic-gradient(
                                            var(--color-3-2) ${Math.floor(data.percentCompleteForNextLevel*3.6)}deg, 
                                            var(--color-3-3) ${Math.floor(data.percentCompleteForNextLevel*3.6)}deg
                                        )"
                                    ></div>
                                    <span>${data.summonerLevel}</span>
                                </div>
                            </div>
                            <div class="mastery">
                                <div class="mastery-display df aic">
                                    <div class="mastery-detail df aic jcc">
                                        <div class="mastery-detail-type mastery-detail-2 df aic">
                                            <div class="mastery-champion-icon df aic">
                                                <img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[data.mastery[1].championId]}.png" alt="">
                                                <div class="mastery-champion-mastery">
                                                    <img src="assets/images/mastery/mastery-${data.mastery[1].championLevel}.png" alt="">
                                                </div>
                                            </div>
                                            <div class="mastery-detail-stats df jcc">
                                                <div class="mastery-detail-champ df aic jcc">
                                                    <h3 class="df aic jcc">${CHAMPION_ID_TO_TW[data.mastery[1].championId]}</h3>
                                                </div>
                                                <div class="mastery-detail-point df aic jcc">
                                                    <div class="mastery-detail-point-icon">
                                                        <img src="assets/images/mastery/icon.png" alt="">
                                                    </div>
                                                    <h3 class="df aic jcc">${data.mastery[1].formattedChampionPoints} 分數</h3>
                                                </div>
                                                <div class="mastery-detail-grade df aic jcc">
                                                    <h3 class="df aic jcc">最高成績：${data.mastery[1].highestGrade}</h3>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mastery-detail-type mastery-detail-1 df aic">
                                            <div class="mastery-champion-icon df aic">
                                                <img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[data.mastery[0].championId]}.png" alt="">
                                                <div class="mastery-champion-mastery">
                                                    <img src="assets/images/mastery/mastery-${data.mastery[0].championLevel}.png" alt="">
                                                </div>
                                            </div>
                                            <div class="mastery-detail-stats df jcc">
                                                <div class="mastery-detail-champ df aic jcc">
                                                    <h3 class="df aic jcc">${CHAMPION_ID_TO_TW[data.mastery[0].championId]}</h3>
                                                </div>
                                                <div class="mastery-detail-point df aic jcc">
                                                    <div class="mastery-detail-point-icon">
                                                        <img src="assets/images/mastery/icon.png" alt="">
                                                    </div>
                                                    <h3 class="df aic jcc">${data.mastery[0].formattedChampionPoints} 分數</h3>
                                                </div>
                                                <div class="mastery-detail-grade df aic jcc">
                                                    <h3 class="df aic jcc">最高成績：${data.mastery[0].highestGrade}</h3>
                                                </div>
                                            </div>
                                        </div>
                                        <div class="mastery-detail-type mastery-detail-3 df aic">
                                            <div class="mastery-champion-icon df aic">
                                                <img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[data.mastery[2].championId]}.png" alt="">
                                                <div class="mastery-champion-mastery">
                                                    <img src="assets/images/mastery/mastery-${data.mastery[2].championLevel}.png" alt="">
                                                </div>
                                            </div>
                                            <div class="mastery-detail-stats df jcc">
                                                <div class="mastery-detail-champ df aic jcc">
                                                    <h3 class="df aic jcc">${CHAMPION_ID_TO_TW[data.mastery[2].championId]}</h3>
                                                </div>
                                                <div class="mastery-detail-point df aic jcc">
                                                    <div class="mastery-detail-point-icon">
                                                        <img src="assets/images/mastery/icon.png" alt="">
                                                    </div>
                                                    <h3 class="df aic jcc">${data.mastery[2].formattedChampionPoints} 分數</h3>
                                                </div>
                                                <div class="mastery-detail-grade df aic jcc">
                                                    <h3 class="df aic jcc">最高成績：${data.mastery[2].highestGrade}</h3>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mastery-2 mastery-champion df aic jcc">
                                        <div class="mastery-champion-icon df aic">
                                            <img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[data.mastery[1].championId]}.png" alt="">
                                            <div class="mastery-champion-mastery">
                                                <img src="assets/images/mastery/mastery-${data.mastery[1].championLevel}.png" alt="">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mastery-1 mastery-champion df aic jcc">
                                        <div class="mastery-champion-icon df aic">
                                            <img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[data.mastery[0].championId]}.png" alt="">
                                            <div class="mastery-champion-mastery">
                                                <img src="assets/images/mastery/mastery-${data.mastery[0].championLevel}.png" alt="">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="mastery-3 mastery-champion df aic jcc">
                                        <div class="mastery-champion-icon df aic">
                                            <img src="assets/images/champion/icon/${CHAMPION_ID_TO_ENG[data.mastery[2].championId]}.png" alt="">
                                            <div class="mastery-champion-mastery">
                                                <img src="assets/images/mastery/mastery-${data.mastery[2].championLevel}.png" alt="">
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
                                    var(--color-3-2) ${data.soloRank.winrate*3.6}deg, 
                                    var(--color-3-4) ${data.soloRank.winrate*3.6}deg
                                )">
                                    <div class="winrate-info df aic jcc">
                                        <h3 class="winrate-info-WR">${data.soloRank.winrate}<span>%</span></h3>
                                        <h3 class="winrate-info-WL">${data.soloRank.wins} W<span>|</span>${data.soloRank.losses} L</h3>
                                    </div>
                                </div>
                                <h3 class="winrate-title">單雙積分</h3>
                            </div>
                            <div class="winrate winrate-flex df aic jcc">
                                <div class="winrate-persent df aic jcc"
                                style="background: conic-gradient(
                                    var(--color-3-2) ${data.flexRank.winrate*3.6}deg, 
                                    var(--color-3-4) ${data.flexRank.winrate*3.6}deg
                                )">
                                    <div class="winrate-info df aic jcc">
                                        <h3 class="winrate-info-WR">${data.flexRank.winrate}<span>%</span></h3>
                                        <h3 class="winrate-info-WL">${data.flexRank.wins} W<span>|</span>${data.flexRank.losses} L</h3>
                                    </div>
                                </div>
                                <h3 class="winrate-title">彈性積分</h3>
                            </div>
                            <div class="winrate-lane df aic">
                                <div class="winrate-lane-type winrate-lane-TOP df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">${data.positions[0].wins} W<span>|</span>${data.positions[0].losses} L</h4>
                                        <h4 class="lane-detail-WR">${data.positions[0].winrate}% 勝率</h4>
                                    </div>
                                    <img src="assets/images/lanes/TOP.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-JUNGLE df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">${data.positions[1].wins} W<span>|</span>${data.positions[1].losses} L</h4>
                                        <h4 class="lane-detail-WR">${data.positions[1].winrate}% 勝率</h4>
                                    </div>
                                    <img src="assets/images/lanes/JUNGLE.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-MID df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">${data.positions[2].wins} W<span>|</span>${data.positions[2].losses} L</h4>
                                        <h4 class="lane-detail-WR">${data.positions[2].winrate}% 勝率</h4>
                                    </div>
                                    <img src="assets/images/lanes/MID.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-BOTTOM df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">${data.positions[3].wins} W<span>|</span>${data.positions[3].losses} L</h4>
                                        <h4 class="lane-detail-WR">${data.positions[3].winrate}% 勝率</h4>
                                    </div>
                                    <img src="assets/images/lanes/BOTTOM.png" alt="" srcset="">
                                </div>
                                <div class="winrate-lane-type winrate-lane-SUPPORT df aic jcc">
                                    <div class="winrate-lane-detail df aic jcc">
                                        <h4 class="lane-detail-WL">${data.positions[4].wins} W<span>|</span>${data.positions[4].losses} L</h4>
                                        <h4 class="lane-detail-WR">${data.positions[4].winrate}% 勝率</h4>
                                    </div>
                                    <img src="assets/images/lanes/SUPPORT.png" alt="" srcset="">
                                </div>
                            </div>
                        </div>
                        <div class="banner-page banner-page-2 df aic jcc" style="display: none">
                            <div class="match-wrapper df aic">
                                ${playerMatchHistoryHtml}
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
            `);
            resolve();
        }
    );
};

async function AddTeamToDisplay(team){
    let newTeamContainer = document.createElement("div");
    newTeamContainer.classList.add("team-container");
    newTeamContainer.classList.add("df");
    newTeamContainer.classList.add("aic");
    newTeamContainer.classList.add("jcc");
    MAIN.appendChild(newTeamContainer);
    for(let i=0; i<team.length; i++){
        await AddPlayerToDisplay(team[i]);
    };
    document.querySelectorAll(".banner-layer-1").forEach(bnr => {
        bnr.addEventListener("mousedown", ()=>{bannerChangePage(event, this)});
    });
};





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





var onMessageHandler = function(message, sender, sendResponse){
    if(message.team) AddTeamToDisplay(message.team);
    sendResponse({success: message.team!==undefined});
};
chrome.runtime.onMessage.addListener(onMessageHandler);