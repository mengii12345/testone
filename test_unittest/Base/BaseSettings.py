import os

BaseDIR = os.path.dirname(os.path.dirname(__file__))
# BaseDIR = os.path.dirname(__file__)
BaseDataDIR = os.path.join(BaseDIR,"TestData\\")
EntranceDIR = os.path.join(BaseDIR,"Entrance\\")
StaticDIR = os.path.join(EntranceDIR,"static\\")

Report = os.path.join(StaticDIR,"Report\\")
Report_Data = os.path.join(Report,"ReportData\\")
LogsDIR = os.path.join(StaticDIR,"Logs\\")
TestData = os.path.join(StaticDIR,"TestData\\")
Picture = os.path.join(TestData,"picture\\")

USERNAME = 'meng'
PSAAWORD = "123"
Entrance_DIR2 = EntranceDIR.replace("/","\\").replace("\\","\\\\")
import socket
# 获取本机计算机名称
hostname = socket.gethostname()
# 获取本机ip
ip = socket.gethostbyname(hostname)
ipport = "http://"+ip+":5000/"
# ipport = "http://testapp.cn1.utools.club/"

ipport_REPORT_DIR = ipport+"static/Report/"

AirResource = ipport+"static/AirResource/"

if __name__=="__main__":
    print(BaseDIR)
    print(BaseDataDIR)
    print(StaticDIR)