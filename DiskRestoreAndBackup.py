import os
import subprocess
from pathlib import Path
from enum import Enum
import logging
import sys
from datetime import datetime
import hashlib
import re

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("wim_backup")

def __version__():
    return "1.1.2"

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
        with open(backupFilePath, "rb")as f:
            fileHash = hashlib.md5(f.read()).hexdigest()
        backupInfo = f"{timeStamp}|{backupFilePath}|{sourceFilePath}|{fileHash}"
        txtFileInfo = "backupRecords.txt"
        with open(txtFileInfo, "a")as f:
            f.write(f"{backupInfo}\n")

        with open(txtFileInfo, "r")as f:
            backupTXTFileInfo = f.readlines()
            if backupTXTFileInfo == "":
                print("备份信息未成功写入文件")
                os.remove(txtFileInfo)
                with open(txtFileInfo, "a")as f:
                    f.write(f"{backupInfo}\n")
            else:
                print("备份信息已成功写入文件")
    
    def creatFullBackup(backupPath, compressLevel:str):
        backupFileNum = 0
        backupDir = "./wimlib/backup"

        if compressLevel == "default":
            compressLevel = 7
        
        while os.path.exists(os.path.join(backupDir,f"backup_{backupFileNum}.wim")):            #如果路径有效则继续增加backupFileNum
            backupFileNum += 1
        
        backupFileName = os.path.join(backupDir, f"backup_{backupFileNum}.wim")
        print(backupFileName)

        command = f"sudo ./wimlib/wimlib-imagex.exe capture --compress=LZX:{str(compressLevel)} {backupPath} {backupFileName} {backupPath} {backupFileName}" # 设置压缩级别，default=7
        print(command)
        result=os.system(command)
        if result == 0:
            WimBackup.writeBackupInformationsToTXT(backupFileName,backupPath)
            print(f"文件已经备份为{backupFileName}")
            return True
        else:
            print("备份失败")

class WimRestore:
    def RestoreWim(sourcePath,backupFilePath,autoRecoveryAllBackupFiles:bool,autoRestoreBackupsToPath:bool,checkHash:bool):
        backupFileNum=0
        backupDir="./wimlib/backup"

        if checkHash:
            hashCheckResult = WimHashCheck.checkHash(backupFilePath)
            print(hashCheckResult)
            if hashCheckResult == False:
                print("备份文件校验失败")
                return False
            elif hashCheckResult == True:
                if autoRestoreBackupsToPath==True:
                    pathInfo = WimRestore.readBackupInformationsFromTXT(backupFilePath,"sourceFilePath")
                    command2=f"sudo ./wimlib/wimlib-imagex.exe apply {backupFilePath} {pathInfo}"
                    print(command2)
                    result=os.system(command2)
                    if result==0:
                        print("文件恢复成功")
                    else:
                        print("文件恢复失败")
                
                if autoRecoveryAllBackupFiles==True:
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
                    
                else:
                    command3 = f"sudo ./wimlib/wimlib-imagex.exe apply {backupFilePath} {sourcePath}"
                    print(command3)
                    result=os.system(command3)
                    if result==0:
                        print("文件恢复成功")
                    else:
                        print("文件恢复失败")

        else:
            if autoRestoreBackupsToPath==True:
                pathInfo = WimRestore.readBackupInformationsFromTXT(backupFilePath,"sourceFilePath")
                command2=f"sudo ./wimlib/wimlib-imagex.exe apply {backupFilePath} {pathInfo}"
                print(command2)
                result=os.system(command2)
                if result==0:
                    print("文件恢复成功")
                else:
                    print("文件恢复失败")
                
            if autoRecoveryAllBackupFiles==True:
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

            else:
                command4 = f"sudo ./wimlib/wimlib-imagex.exe apply {backupFilePath} {sourcePath}"
                print(command4)
                result=os.system(command4)
                if result==0:
                    print("文件恢复成功")
                else:
                    print("文件恢复失败")
        
        

    def readBackupInformationsFromTXT(backupFile,objectReturn:str):
    # 使用正则表达式从备份文件名中提取信息
        matchObj = re.match(r"(.*)_(\d+).wim", backupFile)
        if matchObj is None:
            print("没有找到匹配的备份文件")
            return
    
        try:
        # 获取备份编号并转换为整数
            backup_number = int(matchObj.group(2))
        
        # 打开备份记录文件
            with open("backupRecords.txt", 'r') as f:
            # 读取所有行
                lines = f.readlines()
            
            # 计算要读取的行号（备份编号 + 1）
                target_line = backup_number + 1
            
            # 检查行号是否有效
                if target_line > len(lines):
                    print(f"错误：请求的行号 {target_line} 超出文件范围（文件共有 {len(lines)} 行）")
                    return
            
            # 获取目标行内容并去除首尾空白字符
                lineInfo = lines[target_line - 1].strip()
                print(lineInfo)
            
            # 使用正则表达式解析行内容
                matchObj = re.match(r"(.*)\|(.*?)\|(.*?)\|(.*)", lineInfo)
                if matchObj is None:
                    print("该备份记录是旧版本DBAR工具所创建的或者它存在问题")
                else:
                # 打印解析出的四个字段
                    print(f"{matchObj.group(1)}")  # 第一个字段
                    print(f"{matchObj.group(2)}")  # 第二个字段
                    print(f"{matchObj.group(3)}")  # 第三个字段
                    print(f"{matchObj.group(4)}")  # 第四个字段

                    if objectReturn == "timeStamp":
                        return matchObj.group(1)
                    elif objectReturn == "backupFilePath":
                        return matchObj.group(2)
                    elif objectReturn == "sourceFilePath":
                        return matchObj.group(3)
                    elif objectReturn == "fileHash":
                        return matchObj.group(4)

        except FileNotFoundError:
            print("错误：backupRecords.txt 文件不存在")
        except ValueError:
            print("错误：备份文件编号格式不正确")
        except Exception as e:
            print(f"发生错误: {e}")

class WimHashCheck(WimRestore):
    
    def checkHash(backupFile):
        with open(backupFile, "rb") as f:
            fileHashNew = hashlib.md5(f.read()).hexdigest()
        
        fileHashOld = WimRestore.readBackupInformationsFromTXT(backupFile,"fileHash")
        if fileHashNew == fileHashOld:
            print("文件哈希值匹配")
            return True
        else:
            print("文件哈希值不匹配")
            return False
