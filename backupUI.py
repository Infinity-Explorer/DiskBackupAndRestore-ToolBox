import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import mainUIByPYQT6 as mainUIModule
from DiskRestoreAndBackup import WimBackup, WIMOperation

class BackupUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DBAR Backup ToolBox")
        self.root.geometry("600x300")
        
        # 创建界面组件
        self.create_widgets()
        
        # 初始化备份对象
        self.backup_obj = None


    
        
    def create_widgets(self):
        # 源路径选择
        tk.Label(self.root, text="源路径:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.source_path = tk.Entry(self.root, width=50)
        self.source_path.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="浏览", command=self.browse_source).grid(row=0, column=2, padx=5, pady=5)
        # 进度条
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.grid(row=4, column=0, columnspan=3, padx=5, pady=10)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="就绪")
        self.status_label.grid(row=5, column=0, columnspan=3, pady=5)
        
        # 备份按钮
        self.backup_button = tk.Button(self.root, text="开始备份", command=self.start_backup)
        self.backup_button.grid(row=6, column=1, pady=10)
        
    def browse_source(self):
        """选择源路径"""
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.source_path.delete(0, tk.END)
            self.source_path.insert(0, folder_selected)
            
    def start_backup(self):
        """开始备份过程"""
        # 获取输入值
        source = self.source_path.get()
        
        # 禁用备份按钮，防止重复操作
        self.backup_button.config(state=tk.DISABLED)
        self.status_label.config(text="正在初始化备份...")

        self.status_label.config(text="正在创建备份...")
            
            # 构建完整的备份文件路径
            
            # 创建完整备份
        result = mainUIModule.MainUI.readSettingsInfoFromTXT("compressLevel")
        if result == "快速":
             global success
             success = WimBackup.creatFullBackup(source, compressLevel="1")
        elif result == "中等":
             success = WimBackup.creatFullBackup(source, compressLevel="default")
        else:
             success = WimBackup.creatFullBackup(source, compressLevel="15")

        if success:
                self.status_label.config(text="备份完成")
                messagebox.showinfo("成功", "备份已成功完成")
                self.backup_button.config(state=tk.NORMAL)
        else:
                self.status_label.config(text="备份失败")
                messagebox.showerror("错误", "备份过程中出现错误")
                self.backup_button.config(state=tk.NORMAL)
                
            
    def update_progress(self, value):
        """更新进度条"""
        self.progress['value'] = value
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = BackupUI(root)
    root.mainloop()
