import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import os

class SettingsUI:
    def __init__(self, root):
        self.root = root
        self.root.title("DBAR 工具箱 - 设置")
        self.root.geometry("580x500")
        self.root.configure(bg="#f0f0f0")
        
        self.create_widgets()
    
    def create_widgets(self):
        # 标题
        title_label = tk.Label(self.root, text="设置", bg="#f0f0f0", font=('微软雅黑', 16, 'bold'))
        title_label.pack(pady=20)
        
        # 设置框架
        settings_frame = tk.Frame(self.root, bg="#f0f0f0")
        settings_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)
        # 版本
        version_frame = tk.Label(settings_frame, text="版本信息\nDBAR Toolbox v1.0.1~release", bg="#f0f0f0", font=('微软雅黑', 10, 'bold'))
        version_frame.pack()
        # 备份设置
        backup_frame = tk.LabelFrame(settings_frame, text="备份设置", bg="#f0f0f0", font=('微软雅黑', 10, 'bold'))
        backup_frame.pack(fill=tk.X, pady=10)
        
        # 压缩级别
        compression_label = tk.Label(backup_frame, text="压缩级别:", bg="#f0f0f0")
        compression_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.compression_var = tk.StringVar(value="中等")
        compression_options = ["无", "快速", "中等", "最大"]
        compression_menu = ttk.Combobox(backup_frame, textvariable=self.compression_var, values=compression_options, state="readonly", width=15)
        compression_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # 验证备份
        self.verify_var = tk.BooleanVar(value=True)
        verify_check = tk.Checkbutton(backup_frame, text="备份后验证文件完整性", variable=self.verify_var, bg="#f0f0f0")
        verify_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
        
        # 恢复设置
        restore_frame = tk.LabelFrame(settings_frame, text="恢复设置", bg="#f0f0f0", font=('微软雅黑', 10, 'bold'))
        restore_frame.pack(fill=tk.X, pady=10)
        
        # 覆盖确认
        self.confirm_var = tk.BooleanVar(value=True)
        confirm_check = tk.Checkbutton(restore_frame, text="覆盖文件前确认", variable=self.confirm_var, bg="#f0f0f0")
        confirm_check.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        # 创建备份文件夹
        self.create_dir_var = tk.BooleanVar(value=True)
        create_dir_check = tk.Checkbutton(restore_frame, text="自动创建不存在的文件夹", variable=self.create_dir_var, bg="#f0f0f0")
        create_dir_check.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        
        # 界面设置
        ui_frame = tk.LabelFrame(settings_frame, text="界面设置", bg="#f0f0f0", font=('微软雅黑', 10, 'bold'))
        ui_frame.pack(fill=tk.X, pady=10)
        
        # 主题
        theme_label = tk.Label(ui_frame, text="主题:", bg="#f0f0f0")
        theme_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.theme_var = tk.StringVar(value="浅色")
        theme_options = ["浅色", "深色"]
        theme_menu = ttk.Combobox(ui_frame, textvariable=self.theme_var, values=theme_options, state="readonly", width=15)
        theme_menu.grid(row=0, column=1, padx=10, pady=5, sticky="w")
        
        # 按钮
        button_frame = tk.Frame(self.root, bg="#f0f0f0")
        button_frame.pack(pady=20)
        
        save_button = tk.Button(button_frame, text="保存", command=self.save_settings, width=10)
        save_button.pack(side=tk.LEFT, padx=10)
        
        cancel_button = tk.Button(button_frame, text="取消", command=self.root.destroy, width=10)
        cancel_button.pack(side=tk.LEFT, padx=10)
    
    def save_settings(self):
        # 这里添加保存设置的逻辑
        settings = {
            "compression": self.compression_var.get(),
            "verify_backup": self.verify_var.get(),
            "confirm_overwrite": self.confirm_var.get(),
            "create_directories": self.create_dir_var.get(),
            "theme": self.theme_var.get()
        }
        
        # 实际应用中，这里应该将设置保存到配置文件中
        with open("settings.txt", "w",encoding='utf-8') as f:
            f.write(str(settings))
        print("设置已保存:", settings)
        
        # 显示保存成功的消息
        messagebox.showinfo("设置", "设置已保存")
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SettingsUI(root)
    root.mainloop()
