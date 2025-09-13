import sys
import platform
import os
import multiprocessing
import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                            QHBoxLayout, QPushButton, QLabel, QMessageBox,
                            QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QDesktopServices

class MainUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DBAR 工具箱")
        self.setGeometry(100, 100, 600, 400)
        
        # 创建主窗口部件
        self.main_widget = QWidget()
        self.setCentralWidget(self.main_widget)
        
        # 创建主布局
        self.main_layout = QVBoxLayout()
        self.main_widget.setLayout(self.main_layout)
        
        # 欢迎标签
        self.welcome_label = QLabel("欢迎使用DBAR工具，选择一个选项以继续")
        self.welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.welcome_label.setStyleSheet("font-size: 20px;")
        self.main_layout.addWidget(self.welcome_label)
        
        # 创建按钮区域
        self.button_layout = QHBoxLayout()
        self.main_layout.addLayout(self.button_layout)
        
        # 备份按钮
        self.backup_button = QPushButton("➡  备份我的文件")
        self.backup_button.clicked.connect(self.backup_files)
        self.button_layout.addWidget(self.backup_button)
        self.backup_button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        # 恢复按钮
        self.restore_button = QPushButton("➡   恢复我的文件")
        self.restore_button.clicked.connect(self.restore_files)
        self.button_layout.addWidget(self.restore_button)
        self.restore_button.setStyleSheet("background-color: #4CAF50; color: white;")
        
        # 设置按钮
        self.settings_button = QPushButton("⚙")
        self.settings_button.clicked.connect(self.open_settings)
        self.settings_button.setFixedSize(38, 30)
        self.main_layout.addWidget(self.settings_button, alignment=Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignRight)
        
        # 创建分隔线
        self.separator = QFrame()
        self.separator.setFrameShape(QFrame.Shape.HLine)
        self.separator.setFrameShadow(QFrame.Shadow.Sunken)
        self.main_layout.addWidget(self.separator)
        
        # 创建中间区域
        self.center_frame = QFrame()
        self.center_layout = QVBoxLayout()
        self.center_frame.setLayout(self.center_layout)
        self.center_frame.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.center_frame.setStyleSheet("background-color: white; border: 1px solid #ccc;")
        self.main_layout.addWidget(self.center_frame, stretch=1)
        
        # 添加系统信息
        self.system_info_label = QLabel()
        self.system_info_label.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.center_layout.addWidget(self.system_info_label)
        self.update_system_info()
        
        # 添加定时器更新系统信息
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(5000)  # 每5秒更新一次
        
        # 底部帮助区域
        self.help_layout = QHBoxLayout()
        self.main_layout.addLayout(self.help_layout)
        
        self.help_label = QLabel("遇到问题？")
        self.help_layout.addWidget(self.help_label)
        
        self.help_button = QPushButton("点击这里")
        self.help_button.clicked.connect(self.open_help)
        self.help_layout.addWidget(self.help_button)
        
    def update_system_info(self):
        # 获取系统信息
        system = platform.system()
        release = platform.release()
        version = platform.version()
        processor = platform.processor()
        
        # 获取CPU核心数
        cpu_count = multiprocessing.cpu_count()
        
        # 获取内存信息（简化版）
        try:
            import psutil
            memory = psutil.virtual_memory()
            memory_total = round(memory.total / (1024 ** 3), 2)  # GB
            memory_used = round(memory.used / (1024 ** 3), 2)  # GB
            memory_percent = memory.percent
            memory_available = True
        except ImportError:
            memory_total = "未知"
            memory_used = "未知"
            memory_percent = "未知"
            memory_available = False
        
        # 获取当前时间
        current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建信息文本
        info_text = f"""
        <b>系统信息</b><br>
        操作系统: {system} {release}<br>
        处理器: {processor}<br>
        CPU核心数: {cpu_count}<br>
        当前时间: {current_time}<br><br>
        
        <b>内存信息</b><br>
        """
        
        if memory_available:
            info_text += f"""
        总内存: {memory_total} GB<br>
        已使用: {memory_used} GB<br>
        使用率: {memory_percent}%
        """
        else:
            info_text += "（需要安装psutil库以获取详细信息）"
        
        self.system_info_label.setText(info_text)
        
    def backup_files(self):
        try:
            if not os.path.exists("./backupUI.exe"):
                os.system("backupUI.py")
            else:
                os.system("start ./backupUI.exe")
        except Exception as e:
            QMessageBox.critical(self, "错误", "备份程序未找到，请检查备份程序是否在当前目录下")
            
    def restore_files(self):
        try:
            if not os.path.exists("./restoreUI.exe"):
                os.system("restoreUI.py")
            else:
                os.system("start ./restoreUI.exe")
        except Exception as e:
            QMessageBox.critical(self, "错误", "恢复程序未找到，请检查恢复程序是否在当前目录下")
            
    def open_settings(self):
        try:
            if not os.path.exists("./settingsUI.exe"):
                os.system("settingsUI.py")
            else:
                os.system("start ./settingsUI.exe")
        except Exception as e:
            QMessageBox.critical(self, "错误", "设置程序未找到，请检查设置程序是否在当前目录下")
            
    def open_help(self):
        try:
            QDesktopServices.openUrl(QUrl("https://github.com/Infinity-Explorer/DiskBackupAndRestore-ToolBox"))
        except Exception as e:
            QMessageBox.critical(self, "错误", "无法打开网页，请检查网络连接")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainUI()
    window.show()
    sys.exit(app.exec())
