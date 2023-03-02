import os
import shutil

from airtest.core.api import connect_device
from airtest.core.helper import G, set_logdir
from airtest.utils.compat import script_log_dir
from airtest.core.settings import Settings as ST
from airtest.report.report import LogToHtml
from airtest.utils.compat import script_log_dir, script_dir_name

from test_unittest.Base.BaseSettings import Entrance_DIR2, ipport, AirResource


def new_aotu_setup(basedir=None, devices=None, logdir=None, project_root=None, compress=None):
    if basedir:
        if os.path.isfile(basedir):
            basedir = os.path.dirname(basedir)
        if basedir not in G.BASEDIR:
            G.BASEDIR.append(basedir)
    if devices:
        for dev in devices:
            connect_device(dev)

    if project_root:
        ST.PROJECT_ROOT = project_root
    if compress:
        ST.SNAPSHOT_QUALITY = compress

def new_loging(logdir):
    if os.path.exists(logdir):
        shutil.rmtree(logdir)
    os.mkdir(logdir)
    ST.LOG_DIR = logdir
    G.LOGGER.set_logfile(os.path.join(ST.LOG_DIR, ST.LOG_FILE))



class DIYLogToHtml(LogToHtml):
    def __init__(self, script_root, log_root="", static_root="", export_dir=None, script_name="", logfile="log.txt", lang="en", plugins=None):
        """
        :param script_root:  script_root  ==>path ===> py文件的上一级目录
        :param log_root:  日志文件夹路径
        :param static_root:  ""
        :param export_dir:  None
        :param script_name:   ====> name  ===> py文件名
        :param logfile:  日志文件  log.txt
        :param lang:  "en"
        :param plugins:None
        """
        self.log = []
        self.script_root = script_root  # py文件的上一级目录
        self.script_name = script_name  # py文件名
        self.log_root = log_root  #  日志文件夹路径
        self.static_root = static_root or AirResource  # report 文件夹
        self.test_result = True
        self.run_start = None
        self.run_end = None
        self.export_dir = export_dir  # None
        self.logfile = os.path.join(log_root, logfile)  # 日志文件  log.txt路径
        self.lang = lang
        self.init_plugin_modules(plugins)

    def DIY_report(self,template_name="log_template.html", output_file=None, record_list=None):
        """
                Generate the report page, you can add custom data and overload it if needed
                :param template_name: default is HTML_TPL  "log_template.html"
                :param output_file: The file name or full path of the output file, default HTML_FILE
                :param record_list: List of screen recording files
                :return:
                """
        if not self.script_name:
            path, self.script_name = script_dir_name(self.script_root)

        if self.export_dir:
            self.script_root, self.log_root = self._make_export_dir()
            # output_file可传入文件名，或绝对路径
            output_file = output_file if output_file and os.path.isabs(output_file) \
                else os.path.join(self.script_root, output_file or "log.html")
            if not self.static_root.startswith("http"):
                self.static_root = "static/"

        if not record_list:
            record_list = [f for f in os.listdir(self.log_root) if f.endswith(".mp4")]  # []
        data = self.report_data(output_file=output_file, record_list=record_list)
        # 将数据 里面指向的绝对路径地址 替换成 ip地址
        #  因为我们现在所有的项目都是放在服务器上  不能通过 file协议访问
        # 所以后期所有的访问资源都要放在静态目录
        # 所以指向地址也要改变成 静态服务器地址
        data['data'] = data['data'].replace(Entrance_DIR2,ipport)
        # print(data)
        return self._render(template_name, output_file, **data)


def DIY_simple_report(filepath, logpath=True, logfile="log.txt", output="log.html"):
    """
    :param filepath:  py文件路径
    :param logpath: 日志文件夹路径
    :param logfile: 日志文件  log.txt
    :param output:   html输出地址  html输出地址
    :return:
    """
    # path py文件的上一级目录  name  py文件名
    path, name = script_dir_name(filepath)
    if logpath is True:
        logpath = os.path.join(path, "log")
    # 实例化rpt对象
    rpt = DIYLogToHtml(path, logpath, logfile=logfile, script_name=name)
    # 调用report方法
    rpt.DIY_report("log_template.html", output_file=output)
