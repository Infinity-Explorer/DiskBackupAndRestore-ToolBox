import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from DiskRestoreAndBackup import WimRestore, WIMOperation

class RestoreUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DBAR 工具箱 - 恢复备份")
        self.root.geometry("600x400")
        self.root.configure(bg="#f0f0f0")
        
        # 初始化变量
        self.backup_file = tk.StringVar()
        self.restore_path = tk.StringVar()
        self.selected_backup_index = tk.IntVar()
        self.backup_info = {}  # 存储备份信息
        
        # 初始化恢复对象
        self.restore_obj = None
        
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="恢复备份", bg="#f0f0f0", font=('微软雅黑', 16, 'bold'))
        title_label.pack(pady=20)
        
        # 主框架
        main_frame = tk.Frame(self.root, bg="#f0f0f0")
        main_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        
        # 选择备份文件框架
        backup_file_frame = tk.LabelFrame(main_frame, text="选择备份文件", bg="#f0f0f0", font=('微软雅黑', 10, 'bold'))
        backup_file_frame.pack(fill=tk.X, pady=10)
        
        # 备份文件路径
        backup_path_frame = tk.Frame(backup_file_frame, bg="#f0f0f0")
        backup_path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(backup_path_frame, text="备份文件:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        backup_entry = tk.Entry(backup_path_frame, textvariable=self.backup_file, width=50)
        backup_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_button = tk.Button(backup_path_frame, text="浏览", command=self.browse_backup_file)
        browse_button.pack(side=tk.LEFT, padx=5)
        
        # 备份信息框架
        info_frame = tk.LabelFrame(main_frame, text="备份信息", bg="#f0f0f0", font=('微软雅黑', 10, 'bold'))
        info_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # 备份列表
        
        
        
        
        # 恢复设置框架
        restore_settings_frame = tk.LabelFrame(main_frame, text="恢复设置", bg="#f0f0f0", font=('微软雅黑', 10, 'bold'))
        restore_settings_frame.pack(fill=tk.X, pady=10)
        
        # 恢复路径
        restore_path_frame = tk.Frame(restore_settings_frame, bg="#f0f0f0")
        restore_path_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(restore_path_frame, text="恢复到:", bg="#f0f0f0").pack(side=tk.LEFT, padx=5)
        restore_entry = tk.Entry(restore_path_frame, textvariable=self.restore_path, width=50)
        restore_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        browse_restore_button = tk.Button(restore_path_frame, text="浏览", command=self.browse_restore_path)
        browse_restore_button.pack(side=tk.LEFT, padx=5)
        
        # 恢复选项
        options_frame = tk.Frame(restore_settings_frame, bg="#f0f0f0")
        options_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 按钮框架
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        restore_button = tk.Button(button_frame, text="开始恢复", command=self.start_restore, width=12)
        restore_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(button_frame, text="取消", command=self.root.destroy, width=12)
        cancel_button.pack(side=tk.LEFT, padx=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, length=500, mode='determinate')
        self.progress.pack(pady=10)
        
        # 状态标签
        self.status_label = tk.Label(self.root, text="就绪", bg="#f0f0f0")
        self.status_label.pack()
    
    def browse_backup_file(self):
        """浏览并选择备份文件"""
        file_path = filedialog.askopenfilename(
            title="选择备份文件",
            filetypes=[("WIM 文件", "*.wim"), ("所有文件", "*.*")]
        )
        if file_path:
            self.backup_file.set(file_path)
            self.load_backup_info()
    
    def browse_restore_path(self):
        """浏览并选择恢复路径"""
        folder_path = filedialog.askdirectory(title="选择恢复路径")
        if folder_path:
            self.restore_path.set(folder_path)
        
        # 清空备份信息
        self.backup_info = {}
        
        backup_file = self.backup_file.get()
    
    def on_backup_select(self, event):
        """当用户选择备份时的处理"""
        selected_items = self.backup_tree.selection()
        if selected_items:
            item = self.backup_tree.item(selected_items[0])
            backup_index = item["values"][0]
            self.selected_backup_index.set(int(backup_index))
    
    def start_restore(self):
        """开始恢复过程"""
        backup_file = self.backup_file.get()
        restore_path = self.restore_path.get()
        
        if not backup_file:
            messagebox.showerror("错误", "请选择备份文件")
            return
        
        if not restore_path:
            messagebox.showerror("错误", "请选择恢复路径")
            return
        
        # 确认恢复操作
        confirm = messagebox.askyesno(
            "确认恢复", 
            f"您确定要恢复备份到路径 '{restore_path}' 吗？\n\n" +
            "警告：此操作可能会覆盖现有文件。"
        )
        
        if not confirm:
            return
        
        # 检查目标路径是否存在，不存在则创建
        if not os.path.exists(restore_path):
            try:
                os.makedirs(restore_path)
            except Exception as e:
                messagebox.showerror("错误", f"创建目标目录失败: {str(e)}")
                return
        
        # 禁用按钮，防止重复操作
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                for child in widget.winfo_children():
                    if isinstance(child, tk.Button):
                        child.config(state=tk.DISABLED)
        
        # 更新状态
        self.status_label.config(text="正在初始化恢复...")
        self.progress['value'] = 0
        self.root.update_idletasks()
        
        try:
            # 初始化恢复对象
            if not self.restore_obj:
                self.restore_obj = WimRestore()
            
            self.status_label.config(text="正在恢复备份...")
            
            # 执行恢复
            print(backup_file, restore_path)
            success = WimRestore.RestoreWim(
                restore_path,
                backup_file,
                autoRecoveryAllBackupFiles=False
            )
            
           
            self.status_label.config(text="恢复完成")
            messagebox.showinfo("成功", "备份已成功恢复")
                
        except Exception as e:
            self.status_label.config(text="恢复失败")
            messagebox.showerror("错误", f"恢复过程中出现错误: {str(e)}")
        finally:
            # 恢复按钮状态
            for widget in self.root.winfo_children():
                if isinstance(widget, tk.Frame):
                    for child in widget.winfo_children():
                        if isinstance(child, tk.Button):
                            child.config(state=tk.NORMAL)
    
    def update_progress(self, value):
        """更新进度条"""
        self.progress['value'] = value
        self.status_label.config(text=f"正在恢复备份... {value}%")
        self.root.update_idletasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = RestoreUI(root)
    root.mainloop()

