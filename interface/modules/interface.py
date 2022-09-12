from .constants import *
from PIL import ImageTk
import tkinter as tk





class SearchSummoner(tk.Canvas):
    def __init__(self, root, parent, x, y, w, h, offset_x, offset_y, image, bg, fg, bdg, func):
        self.root = root
        self.parent = parent
        self.x, self.y = x, y
        self.w, self.h = w, h
        super().__init__(
            self.parent,
            width = self.w,
            height = self.h,
            background = bg,
            highlightcolor = bdg,
            bd = -2,
            borderwidth = 0, 
            highlightthickness = 0
        )
        self.place(x=self.x, y=self.y)
        self.image = ImageTk.PhotoImage(image = image)
        self.create_image(0, 0,anchor=tk.NW, image=self.image)

        self.placeholder = "搜尋召喚師"

        self.entry = tk.Entry(self, bg=bg, fg=fg, highlightcolor=bg, borderwidth=0, highlightthickness=-2, insertbackground=fg)
        self.entry.insert(0, self.placeholder)
        self.entry.place(x=offset_x, y=offset_y, width=self.w-offset_x-offset_y-offset_y-offset_y, height=self.h-offset_y-offset_y)
        self.entry.bind("<Return>", lambda e:func(e.widget.get()))
        self.entry.bind("<FocusIn>", self.FocusIn)
        self.entry.bind("<FocusOut>", self.FocusOut)


    def set(self, val):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, val)


    def get(self):
        return self.entry.get()


    def FocusIn(self, e):
        if self.get() == self.placeholder:
            self.entry.delete(0, tk.END)


    def FocusOut(self, e):
        if not self.get():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.placeholder)





class SettingButton(tk.Button):
    def __init__(self, root, parent, x, y, w, h, image, bg, func):
        self.image = ImageTk.PhotoImage(image = image)
        self.root = root
        self.parent = parent
        self.x, self.y = x, y
        self.w, self.h = w, h
        super().__init__(
            self.parent, 
            image = self.image,
            bg = bg,
            activebackground = bg,
            borderwidth = 0,
            highlightthickness = 0,
            relief = "flat", 
            cursor = "hand2",
            command = func
        )
        self.place(x=self.x, y=self.y, width=self.w, height=self.h)





class ManualSearchButton(tk.Button):
    def __init__(self, root, parent, x, y, w, h, image, bg, abg, func):
        self.image = ImageTk.PhotoImage(image = image)
        self.root = root
        self.parent = parent
        self.x, self.y = x, y
        self.w, self.h = w, h
        super().__init__(
            self.parent,
            image = self.image,
            bg = bg,
            activebackground = abg,
            borderwidth = 0,
            highlightthickness = 0,
            relief = "flat", 
            cursor = "hand2",
            command = func
        )
        self.place(x=self.x, y=self.y, width=self.w, height=self.h)





class LaneButton(tk.Button):
    def EnterEffect(e):
        self = e.widget
        w = self.HoverLevel.winfo_width()
        h = self.HoverLevel.winfo_height()
        self.HoverLevel.deiconify()
        x = (self.root.winfo_x()+self.winfo_x()+self.w)-int(w/2)
        y = (self.root.winfo_y()+self.winfo_y()+self.h)-int(h)
        self.HoverLevel.attributes("-topmost", True)
        self.HoverLevel.geometry(f"{w}x{h}+{x}+{y}")


    def LeaveEffect(e):
        e.widget.HoverLevel.withdraw()


    def __init__(self, root, parent, x, y, w, h, image, bg, bdg, fg, win=0, loss=0):
        self.image = ImageTk.PhotoImage(image = image)
        self.root = root
        self.parent = parent
        self.x, self.y = x, y
        self.w, self.h = w, h
        super().__init__(
            self.parent, 
            image = self.image,
            bg = bg,
            activebackground = bg,
            borderwidth = 0,
            highlightthickness = 0,
            relief = "flat", 
            cursor = "hand2"
        )
        self.bind("<Enter>", self.__class__.EnterEffect)
        self.bind("<Leave>", self.__class__.LeaveEffect)
        self.place(x=self.x, y=self.y, width=self.w, height=self.h)

        self.HoverLevel = tk.Toplevel(parent)
        self.HoverLevel.geometry(f"{WIN_WIDTH//2}x{WIN_HEIGHT//4}")
        self.HoverLevel.overrideredirect(1)
        self.HoverLevel.withdraw()

        self.HoverCanvas = tk.Canvas(self.HoverLevel, bd=-2, bg=bg)
        self.HoverCanvas.create_rectangle(2, 2, (WIN_WIDTH//2)-2, (WIN_HEIGHT//4)-2, fill=bg, outline=bdg, width=2)
        self.HoverCanvas.place(x=0, y=0)

        self.HoverWinVar = tk.StringVar()
        self.HoverWin = tk.Label(self.HoverLevel, textvariable=self.HoverWinVar, bg=bg, fg=fg)
        self.HoverWin.pack(pady=3)
        self.SetWin(win)

        self.HoverLossVar = tk.StringVar()
        self.HoverLoss = tk.Label(self.HoverLevel, textvariable=self.HoverLossVar, bg=bg, fg=fg)
        self.HoverLoss.pack()
        self.SetLoss(loss)

        self.HoverWinrateVar = tk.StringVar()
        self.HoverWinrate = tk.Label(self.HoverLevel, textvariable=self.HoverWinrateVar, bg=bg, fg=fg)
        self.HoverWinrate.pack()
        self.SetWinrate( int(win / (1 if(loss+win==0)else (loss+win)) ) )


    def SetWin(self, val):
        self.HoverWinVar.set(f"{val} W")


    def SetLoss(self, val):
        self.HoverLossVar.set(f"{val} L")


    def SetWinrate(self, val):
        self.HoverWinrateVar.set(f"{val} % 勝率")


    def Set(self, vW, vL, vR):
        self.SetWin(vW)
        self.SetLoss(vL)
        self.SetWinrate(vR)





class RankWinrateChart(tk.Canvas):
    def PieChart(canvas, x, y, r, w, bg, data):
        def drawArc(canvas, x, y, r, ds, de, color):
            return canvas.create_arc((x-r, y-r, x+r, y+r), start=-ds+90, extent=-de, fill=color, outline=color)
        flag = False
        items = []
        total = sum([d[0] for d in data])
        for i in range(len(data)):
            data[i][0] = int(360 * data[i][0] / (1 if(total==0)else total) )
            if data[i][0] == 360: flag = data[i]
        if not flag:
            for i in range(len(data)):
                items.append( drawArc(
                    canvas=canvas,
                    x=x, y=y, r=r,
                    ds=0 if(i==0)else sum([d[0] for d in data[:i]]),
                    de=data[i][0],
                    color=data[i][1]
                ))
        else:
            items.append(canvas.create_oval(x-r, y-r, x+r, y+r, fill=flag[1]))
        items.append(canvas.create_oval(x-r+w, y-r+w, x+r-w, y+r-w, fill=bg))
        return items


    def __init__(self, root, parent, x, y, s, title, bg, fg):
        self.root = root
        self.parent = parent
        self.x, self.y = x, y
        self.w, self.h = s, s
        self.bg = bg
        self.fg = fg
        super().__init__(
            self.parent,
            width = self.w,
            height = self.h,
            background = self.bg,
            bd = -2, 
            borderwidth = 0, 
            highlightthickness = 0
        )
        self.place(x=self.x, y=self.y)
        self.ChartItems = self.__class__.PieChart(self, self.w//2, (self.h//5)*2, (self.h//5)*2, self.h//12, self.bg, [
            [50, "#0a96aa"], [50, "#863041"]
        ])
        self.create_text(
            self.w//2, (self.h//10)*9, text=title, font=("Inter", "16", "bold"), fill=self.fg
        )
        self.Winrate = self.create_text(
            self.w//2, (self.h//5)*2 - (self.h//15), text=f"載入中", font=("Inter", "20", "bold"), fill=self.fg
        )
        self.WL = self.create_text(
            self.w//2, (self.h//5)*2 + (self.h//10), text=f"載入中", font=("Inter", "10", "bold"), fill=self.fg
        )


    def Update(self, win, loss):
        for item in self.ChartItems:
            self.delete(item)
        self.delete(self.Winrate)
        self.delete(self.WL)
        self.ChartItems = self.__class__.PieChart(self, self.w//2, (self.h//5)*2, (self.h//5)*2, self.h//12, self.bg, [
            [win, "#0a96aa"], [loss, "#863041"]
        ])
        self.Winrate = self.create_text(
            self.w//2, (self.h//5)*2 - (self.h//15), text=f"{ int( ( win / (1 if(win+loss==0)else (win+loss) ) * 100 )) } %", font=("Inter", "20", "bold"), fill=self.fg
        )
        self.WL = self.create_text(
            self.w//2, (self.h//5)*2 + (self.h//10), text=f"{win} W | {loss} L", font=("Inter", "10", "bold"), fill=self.fg
        )


    def show(self):
        self.place(x=self.x, y=self.y)


    def hide(self):
        self.place_forget()





class RankWinrateSection(tk.Frame):
    def __init__(self, root, parent, x, y, w, h, bg, fg, data, prevImg, nextImg):
        self.root = root
        self.parent = parent
        self.x, self.y = x, y
        self.w, self.h = w, h
        super().__init__(
            self.parent, 
            width = self.w, 
            height = self.h, 
            bg = bg
        )
        self.prevImage = ImageTk.PhotoImage(image = prevImg)
        self.prevButton = tk.Button(self, image=self.prevImage, bg=bg, activebackground=bg, borderwidth=0, highlightthickness=0, relief="flat", command=self.prev, width=30, height=50)
        self.prevButton.place(x=0, y=(self.h-50)//2)
        self.nextImage = ImageTk.PhotoImage(image = nextImg)
        self.nextButton = tk.Button(self, image=self.nextImage, bg=bg, activebackground=bg, borderwidth=0, highlightthickness=0, relief="flat", command=self.next, width=30, height=50)
        self.nextButton.place(x=self.w-30, y=(self.h-50)//2)
        self.place(x=self.x, y=self.y)
        self.chartSize = min(self.w, self.h)
        self.chartOffset = (
            (self.w-self.chartSize)//2,
            (self.h-self.chartSize)//2
        )
        self.idx = 0
        self.charts = []
        self.storage = {}
        for i in range(len(data)):
            chart = RankWinrateChart(self.root, self, self.chartOffset[0], self.chartOffset[1], self.chartSize, data[i], bg, fg)
            chart.place_forget()
            self.charts.append(chart)
            self.storage[data[i]] = chart
        if( len(self.charts)>self.idx ): self.charts[self.idx].show()


    def get(self, name):
        return self.storage.get(name, None)


    def next(self):
        self.charts[self.idx].hide()
        self.idx = (self.idx+1)%len(self.charts)
        self.charts[self.idx].show()


    def prev(self):
        self.charts[self.idx].hide()
        self.idx = (len(self.charts)-1) if(self.idx==0)else self.idx-1
        self.charts[self.idx].show()





class ImageButton(tk.Button):
    def __init__(self, root, parent, x, y, w, h, image, bg, abg, func):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.root = root
        self.parent = parent
        self.image = ImageTk.PhotoImage(image = image)
        super().__init__(
            self.parent, image = self.image, borderwidth = 0, 
            highlightthickness = 0, relief = "flat", command = func,
            bg = bg, activebackground = abg, cursor = "hand2"
        )
        self.place(x=self.x, y=self.y, width=self.w, height=self.h)





class BorderedEntry(tk.Frame):
    def __init__(self, root, parent, x, y, w, h, bd, bg, bdg, fg, placeholder, func):
        self.x, self.y = x, y
        self.w, self.h = w, h
        self.root = root
        self.parent = parent
        super().__init__(
            self.parent, width=self.w, height=self.h, bg=bdg, bd=0
        )
        self.placeholder = placeholder

        self.entry = tk.Entry(self, bd=0, highlightthickness=0, bg=bg, fg=fg, insertbackground=fg)
        self.entry.place(x=bd[2], y=bd[0], width=self.w-bd[2]-bd[3], height=self.h-bd[0]-bd[1])
        self.entry.insert(0, self.placeholder)
        self.place(x=self.x, y=self.y)

        self.entry.bind("<FocusIn>", self.FocusIn)
        self.entry.bind("<FocusOut>", self.FocusOut)
        self.entry.bind("<Return>", lambda e:func(e.widget.get()))


    def set(self, val):
        self.entry.delete(0, tk.END)
        self.entry.insert(0, val)


    def get(self):
        return self.entry.get()


    def FocusIn(self, e):
        if self.get() == self.placeholder:
            self.entry.delete(0, tk.END)


    def FocusOut(self, e):
        if not self.get():
            self.entry.delete(0, tk.END)
            self.entry.insert(0, self.placeholder)

























