import tkinter as tk
from tkinter import ttk
import os

class TkinterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DBAR 工具箱")
        self.root.geometry("480x311")
        
        self.root.configure(bg="#f0f0f0")
        
        self.create_widgets()
    
    def create_widgets(self):
        self.label_2 = tk.Label(self.root, text="欢迎使用DBAR工具，选择一个选项以继续", bg="#f0f0f0",font=('微软雅黑',12))
        self.label_2.place(x=92.296875, y=15.203125)
        def button_1_click():
            try:
                os.system("backupUI.py")
            except Exception as e:
                os.system("backupUI.exe")

        self.button_1 = tk.Button(self.root, text="➡  备份我的文件",command=button_1_click)
        self.button_1.place(x=21.296875, y=81.203125, width=111, height=30)

        def button_2_click():
            try:
                os.system("restoreUI.py")
            except Exception as e:
                os.system("restoreUI.exe")
        self.button_2 = tk.Button(self.root, text="➡   恢复我的文件",command=button_2_click)
        self.button_2.place(x=23.296875, y=145.203125, width=106, height=30)

        self.label_3 = tk.Label(self.root, text="遇到问题？", bg="#f0f0f0")
        self.label_3.place(x=133.296875, y=280)
        def button_3_click():
            try:
                os.system("start msedge https://github.com/infinity-explorer")
            except Exception as e:
                pass

        self.button_3 = tk.Button(self.root, text="点击这里",command=button_3_click)
        self.button_3.place(x=218.296875, y=278.203125, width=100, height=30)
        def button_4_click():
            try:
                os.system("settingsUI.py")
            except Exception as e:
                os.system("settingsUI.exe")

        self.button_4 = tk.Button(self.root, text="⚙",command=button_4_click)
        self.button_4.place(x=422.296875, y=20.203125, width=38, height=30)

        self.canvas_1 = tk.Canvas(self.root, bg="white", bd=1, relief=tk.SOLID)
        self.canvas_1.place(x=182.296875, y=80.203125, width=256, height=180)


if __name__ == "__main__":
    root = tk.Tk()
    app = TkinterApp(root)
    root.mainloop()
