from tempfile import NamedTemporaryFile
from threading import Thread
from modules import *
from tkinter import messagebox
import tkinter as tk
import webbrowser
from PIL import Image as ImgOpener
from base64 import b64decode
from io import BytesIO
import images
import os




class Main(tk.Tk):
    UpdateClientGap = 3600

    WindowUpdateGap = 30

    StuckResetTime = 180

    OnPage1 = True

    UpdateLocalGap = 180
    UpdatingLocal = False
    UpdatingLocalStuckCounter = 0

    ChampionSelectGap = 2
    DisplayingChampionSelectGameId = -1
    UpdatingChampionSelect = False
    UpdatingChampionSelectStuckCounter = 0

    ManualDisplayingOrder = False
    ManualDisplayingOrderStuckCounter = 0

    ManualDisplayingChaos = False
    ManualDisplayingChaosStuckCounter = 0

    SearchingUser = False
    SearchingUserStuckCounter = 0


    def __init__(self, x, y, w, h):
        super().__init__()
        self.title("LoL Check")
        self.resizable(False, False)
        self.attributes("-topmost", True)
        self.protocol("WM_DELETE_WINDOW", lambda : os._exit(0))
        self.tk.call('wm', 'iconphoto', self._w, ImageTk.PhotoImage(image=ImgOpener.open(BytesIO(b64decode(images.Icon_byte)))))

        self.x, self.y = x, y
        self.w, self.h = w, h
        self.geometry(f"{w}x{h}+{x}+{y}")

        self.HtmlDisplay = HTMLDisplay()
        self.Fetcher = Fetcher(self)
        self.Fetcher.Initialize()

        self.BuildPage1()
        self.BuildPage2()
        if self.OnPage1: self.GUIpage1.place(x=0, y=0)
        else: self.GUIpage2.place(x=0, y=0)

        self.InitializeUI()



    def InitializeUI(self):
        self.UpdateLocalThread()



    def WindowUpdate(self):
        if self.UpdatingLocal:
            self.UpdatingLocalStuckCounter += self.WindowUpdateGap
            if self.UpdatingLocalStuckCounter >= self.StuckResetTime:
                self.UpdatingLocal = False
                self.UpdatingLocalStuckCounter = 0
        else:
            self.UpdatingLocalStuckCounter = 0

        if self.UpdatingChampionSelect:
            self.UpdatingChampionSelectStuckCounter += self.WindowUpdateGap
            if self.UpdatingChampionSelectStuckCounter >= self.StuckResetTime:
                self.UpdatingChampionSelect = False
                self.UpdatingChampionSelectStuckCounter = 0
        else:
            self.UpdatingChampionSelectStuckCounter = 0

        if self.ManualDisplayingOrder:
            self.ManualDisplayingOrderStuckCounter += self.WindowUpdateGap
            if self.ManualDisplayingOrderStuckCounter >= self.StuckResetTime:
                self.ManualDisplayingOrder = False
                self.ManualDisplayingOrderStuckCounter = 0
        else:
            self.ManualDisplayingOrderStuckCounter = 0

        if self.ManualDisplayingChaos:
            self.ManualDisplayingChaosStuckCounter += self.WindowUpdateGap
            if self.ManualDisplayingChaosStuckCounter >= self.StuckResetTime:
                self.ManualDisplayingChaos = False
                self.ManualDisplayingChaosStuckCounter = 0
        else:
            self.ManualDisplayingChaosStuckCounter = 0

        if self.SearchingUser:
            self.SearchingUserStuckCounter += self.WindowUpdateGap
            if self.SearchingUserStuckCounter >= self.StuckResetTime:
                self.SearchingUser = False
                self.SearchingUserStuckCounter = 0
        else:
            self.ManualDisplayingChaosStuckCounter = 0

        self.after(self.WindowUpdateGap*1000, self.WindowUpdate)



    def ClientUpdateThread(self):
        Thread(target=self.Fetcher.Initialize()).start()
        self.after(self.UpdateClientGap*1000, self.ClientUpdateThread)



    def UpdateLocal(self):
        if not self.OnPage1: return
        if self.UpdatingLocal: return
        print("Start UpdateLocal")
        self.UpdatingLocal = True
        res = self.Fetcher.LoadLocalPlayer()
        if not res["success"]: 
            self.UpdatingLocal = False
            print("Ended UpdateLocal-1")
            return

        self.GUIwinrate.get("單雙積分").Update(res["soloRank"]["wins"], res["soloRank"]["losses"])
        self.GUIwinrate.get("彈性積分").Update(res["flexRank"]["wins"], res["flexRank"]["losses"])

        self.GUITopLane.Set(    res["positions"][0]["wins"], res["positions"][0]["losses"], res["positions"][0]["winrate"])
        self.GUIJungleLane.Set( res["positions"][1]["wins"], res["positions"][1]["losses"], res["positions"][1]["winrate"])
        self.GUIMidLane.Set(    res["positions"][2]["wins"], res["positions"][2]["losses"], res["positions"][2]["winrate"])
        self.GUIBottomLane.Set( res["positions"][3]["wins"], res["positions"][3]["losses"], res["positions"][3]["winrate"])
        self.GUISupportLane.Set(res["positions"][4]["wins"], res["positions"][4]["losses"], res["positions"][4]["winrate"])

        self.UpdatingLocal = False
        print("Ended UpdateLocal-0")

    def UpdateLocalThread(self):
        Thread(target=self.UpdateLocal).start()
        self.after(self.UpdateLocalGap*1000, self.UpdateLocalThread)



    def UpdateChampionSelect(self):
        if self.UpdatingChampionSelect: return
        print("Start UpdateChampionSelect")
        self.UpdatingChampionSelect = True
        res = self.Fetcher.SearchChampionSelectTeam()
        if not res["success"]: 
            self.UpdatingChampionSelect = False
            print("Ended UpdateChampionSelect-1")
            return
        if res["gameId"] == self.DisplayingChampionSelectGameId: 
            self.UpdatingChampionSelect = False
            print("Ended UpdateChampionSelect-2")
            return
        self.DisplayingChampionSelectGameId = ( res["gameId"] if(res.get("gameId", None))else -1 )
        self.HtmlDisplay.ResetTemplate()
        self.HtmlDisplay.AddTeamToDisplay(res["A"])
        html = self.HtmlDisplay.GetResult()
        self.HtmlDisplay.ResetTemplate()
        self.Display(html)
        self.UpdatingChampionSelect = False
        print("Ended UpdateChampionSelect-0")

    def ChampionSelectThread(self):
        Thread(target=self.UpdateChampionSelect).start()
        self.after(self.ChampionSelectGap*1000, self.ChampionSelectThread)



    def ManualDisplayOrder(self):
        if not self.OnPage1: return
        if self.ManualDisplayingOrder: return print("Already ManualDisplayOrder")
        self.ManualDisplayingOrder = True
        flag = False
        for i in range(2):
            if not flag:
                print("Start ManualDisplayOrder-1")
                res = self.Fetcher.SearchChampionSelectTeam()
                if( not res["success"] ): flag = True
                else: players = res["A"]
            else:
                print("Start ManualDisplayOrder-2")
                res = self.Fetcher.SearchLastestGameA()
                if( not res["success"] ): 
                    self.ManualDisplayingOrder = False
                    print("Ended ManualDisplayOrder-1")
                    return
                else: players = res["res"]
        self.HtmlDisplay.ResetTemplate()
        self.HtmlDisplay.AddTeamToDisplay( players )
        html = self.HtmlDisplay.GetResult()
        self.HtmlDisplay.ResetTemplate()
        self.Display(html)
        self.ManualDisplayingOrder = False
        print("Ended ManualDisplayOrder-0")

    def ManualDisplayOrderThread(self):
        Thread(target=self.ManualDisplayOrder).start()



    def ManualDisplayChaos(self):
        if not self.OnPage1: return
        if self.ManualDisplayingChaos: return print("Already ManualDisplayChaos")
        self.ManualDisplayingChaos = True
        print("Start ManualDisplayChaos")
        res = self.Fetcher.SearchLastestGameB()
        if( not res["success"] ): 
            self.ManualDisplayingChaos = False
            print("Ended ManualDisplayChaos-1")
            return
        else: players = res["res"]
        self.HtmlDisplay.ResetTemplate()
        self.HtmlDisplay.AddTeamToDisplay( players )
        html = self.HtmlDisplay.GetResult()
        self.HtmlDisplay.ResetTemplate()
        self.Display(html)
        self.ManualDisplayingChaos = False
        print("Ended ManualDisplayChaos-0")

    def ManualDisplayChaosThread(self):
        Thread(target=self.ManualDisplayChaos).start()



    def SearchUser(self, username):
        if self.SearchingUser: return
        print("Start SearchingUser")
        self.SearchingUser = True
        res = self.Fetcher.LoadPlayerFromUsername(username)
        if not res["success"]: 
            print("Ended SearchingUser")
            self.SearchingUser = False
            messagebox.showinfo("提示", "查無此召喚師")
            return 
        self.HtmlDisplay.ResetTemplate()
        self.HtmlDisplay.AddTeamToDisplay([res, ])
        html = self.HtmlDisplay.GetResult()
        self.HtmlDisplay.ResetTemplate()
        self.Display(html)
        self.SearchingUser = False
        print("Ended SearchingUser")

    def SearchUserThread(self, username):
        Thread(target=lambda : self.SearchUser(username)).start()



    def BuildPage1(self):
        self.GUIpage1 = tk.Frame(self, width=self.w, height=self.h, bg="#18141f")

        self.GUISearch1 = SearchSummoner(self, self.GUIpage1, 20, 12, 130, 18, 18, 1, 
            ImgOpener.open(BytesIO(b64decode(images.Search_byte))), 
            "#18141f", "#e4dac8", "#785a28", self.SearchUserThread
        )

        self.GUISetting1 = SettingButton(self, self.GUIpage1, 155, 8, 26, 26, ImgOpener.open(BytesIO(b64decode(images.Settings_byte))), "#18141f", self.SwitchPage)

        self.GUIOrder = ManualSearchButton(self, self.GUIpage1,  20, 45, 75, 40, ImgOpener.open(BytesIO(b64decode(images.Order_byte))), "#18141f", "#18141f", self.ManualDisplayOrderThread)
        self.GUIChaos = ManualSearchButton(self, self.GUIpage1, 105, 45, 75, 40, ImgOpener.open(BytesIO(b64decode(images.Chaos_byte))), "#18141f", "#18141f", self.ManualDisplayChaosThread)

        self.GUIwinrate = RankWinrateSection(self, self.GUIpage1, 0, 100, 200, 150, "#18141f", "#f0e6d2", ["單雙積分", "彈性積分"], ImgOpener.open(BytesIO(b64decode(images.prev_byte))), ImgOpener.open(BytesIO(b64decode(images.next_byte))))

        self.GUITopLane     = LaneButton(self, self.GUIpage1,  30, 265, 20, 20, ImgOpener.open(BytesIO(b64decode(images.Top_byte))),     "#18141f", "#c8a459", "#cdbe91")
        self.GUIJungleLane  = LaneButton(self, self.GUIpage1,  60, 265, 20, 20, ImgOpener.open(BytesIO(b64decode(images.Jungle_byte))),  "#18141f", "#c8a459", "#cdbe91")
        self.GUIMidLane     = LaneButton(self, self.GUIpage1,  90, 265, 20, 20, ImgOpener.open(BytesIO(b64decode(images.Mid_byte))),     "#18141f", "#c8a459", "#cdbe91")
        self.GUIBottomLane  = LaneButton(self, self.GUIpage1, 120, 265, 20, 20, ImgOpener.open(BytesIO(b64decode(images.Bottom_byte))),  "#18141f", "#c8a459", "#cdbe91")
        self.GUISupportLane = LaneButton(self, self.GUIpage1, 150, 265, 20, 20, ImgOpener.open(BytesIO(b64decode(images.Support_byte))), "#18141f", "#c8a459", "#cdbe91")





    def BuildPage2(self):
        self.GUIpage2 = tk.Frame(self, width=self.w, height=self.h, bg="#18141f")

        self.GUISearch2 = SearchSummoner(self, self.GUIpage2, 20, 12, 130, 18, 18, 1, 
            ImgOpener.open(BytesIO(b64decode(images.Search_byte))), 
            "#18141f", "#e4dac8", "#785a28", self.SearchUserThread
        )

        self.GUISetting2 = SettingButton(self, self.GUIpage2, 155, 8, 26, 26, ImgOpener.open(BytesIO(b64decode(images.Settings_byte))), "#18141f", self.SwitchPage)

        self.TutorialButton = ImageButton(self, self.GUIpage2, 20, 60, 160, 30, 
            ImgOpener.open(BytesIO(b64decode(images.Tutorial_byte))), 
            "#18141f", "#18141f", lambda : webbrowser.open(TUTORIAL_URL)
        )

        def LoLPathInputFunc(s):
            if self.Fetcher.ValidGamePath(s):
                self.Fetcher.SaveGamePath(s)
                messagebox.showinfo("提示", "儲存成功")
            else:
                messagebox.showinfo("提示", "無效路徑")
                self.Fetcher.LoLPath = ""
                self.LoLPathInput.set(self.LoLPathInput.placeholder)
        self.LoLPathInput = BorderedEntry(self, self.GUIpage2, 20, 120, 130, 30, (2, 2, 2, 2), "#18141f", "#c8a459", "#e4dac8", "英雄聯盟檔案位置", LoLPathInputFunc)
        self.LoLPathInput.set(self.Fetcher.LoLPath)

        def LoLPathAutoFunc():
            messagebox.showinfo("提示", "已開始搜尋檔案位置，請稍後")
            self.Fetcher.AssertGamePath(self.LoLPathInput.set)
        self.LoLPathAuto = ImageButton(self, self.GUIpage2, 150, 120, 30, 30, 
            ImgOpener.open(BytesIO(b64decode(images.AutoPath_byte))), 
            "#18141f", "#18141f", LoLPathAutoFunc
        )





    def SwitchPage(self):
        self.OnPage1 = not self.OnPage1
        if self.OnPage1:
            self.GUIpage1.place(x=0, y=0)
            self.GUIpage2.place_forget()
        else:
            self.GUIpage1.place_forget()
            self.GUIpage2.place(x=0, y=0)





    def Display(self, html):
        with NamedTemporaryFile('w', delete=False, suffix='.html', encoding='UTF-8') as f:
            url = 'file:\\\\' + f.name
            f.write(html)
        webbrowser.open(url)





    def run(self):
        self.after(self.UpdateClientGap*1000, self.ClientUpdateThread)
        self.after(self.WindowUpdateGap*1000, self.WindowUpdate)
        self.after(self.UpdateLocalGap*1000, self.UpdateLocalThread)
        self.after(self.ChampionSelectGap*1000, self.ChampionSelectThread)
        self.mainloop()
        
        






Main(500, 300, WIN_WIDTH, WIN_HEIGHT).run()