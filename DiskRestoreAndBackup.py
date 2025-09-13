import os
import subprocess
import json
from pathlib import Path
from typing import Callable, List, Optional, Dict, Any
from enum import Enum
import logging
import sys
from datetime import datetime
from pathlib import Path
import DiskRestoreAndBackup

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wim_backup")

class WIMOperation(Enum):
    CAPTURE = "capture"
    APPLY = "apply"
    INFO = "info"
    DELETE = "delete"
    APPEND = "append"

class WimBackup:
    def __init__(self, wimlib_path):
        #初始化wim备份库
        self.wimlib_path = "./wimlib/wimlib-imagex.exe"
    
    def checkWimlibAvalible():                 #检查wimlib-imagex.exe是否存在
        if os.path.exists("./wimlib/wimlib-imagex.exe") != True:
            print("没有找到wimlib-imagex.exe,因此程序无法运行")
            sys.exit(1)
        else:
            result = subprocess.run("./wimlib/wimlib-imagex.exe --version",capture_output = True,text = True,check = True)
            print(f"当前wimlib版本：{result.stdout.strip()}")
            #20：04，终于成功了
    
    def writeBackupInformationsToTXT(backupFilePath,sourceFilePath):
        timeStamp = datetime.now().isoformat()
        backupInfo = f"{timeStamp}|{backupFilePath}|{sourceFilePath}"
        txtFileInfo = "backupRecords.txt"
        with open(txtFileInfo, "a")as f:
            f.write(f"{backupInfo}\n")

        with open(txtFileInfo, "r")as f:        #检查是否写入成功
            backupTXTFileInfo = f.readlines()
            if backupTXTFileInfo == "":
                print("备份信息未成功写入文件")
                os.remove(txtFileInfo)
                with open(txtFileInfo, "a")as f:
                    f.write(f"{backupInfo}\n")
            else:
                print("备份信息已成功写入文件")
    
    def creatFullBackup(backupPath):
        backupFileNum = 0
        backupDir = "./wimlib/backup"
        
        while os.path.exists(os.path.join(backupDir,f"backup_{backupFileNum}.wim")):            #如果路径有效则继续增加backupFileNum
            backupFileNum += 1
        
        backupFileName = os.path.join(backupDir, f"backup_{backupFileNum}.wim")
        print(backupFileName)

        command = f"sudo ./wimlib/wimlib-imagex.exe capture {backupPath} {backupFileName}"
        print(command)
        result=os.system(command)
        if result == 0:
            DiskRestoreAndBackup.WimBackup.writeBackupInformationsToTXT(backupFileName,backupPath)
            print(f"文件已经备份为{backupFileName}")
            return True
        else:
            print("备份失败")

class WimRestore:
    def RestoreWim(sourcePath,backupFilePath,autoRecoveryAllBackupFiles:False):
        backupFileNum=0
        backupDir="./wimlib/backup"
        if autoRecoveryAllBackupFiles == False:
            command=f"sudo ./wimlib/wimlib-imagex.exe apply {backupFilePath} {sourcePath}"
            print(command)
            result=os.system(command)
            if result==0:
                print("文件恢复成功")
            else:
                print("文件恢复失败")
        elif autoRecoveryAllBackupFiles==True:
            while True:
                backupFilePath=os.path.join(backupDir,f"backup_{backupFileNum}.wim")
                print(backupFilePath)
                if not os.path.exists(backupFilePath):
                    print("批量恢复已完成")
                    break
                command2=f"sudo ./wimlib/wimlib-imagex.exe apply {backupFilePath} {sourcePath}"
                print(command2)
                result=os.system(command2)
                backupFileNum+=1
