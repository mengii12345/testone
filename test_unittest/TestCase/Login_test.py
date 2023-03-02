# -*- encoding=utf8 -*-
__author__ = "meng"

import logging
import unittest


from airtest.report.report import simple_report
from airtest.core.api import *

from test_unittest.Base.PublicFunction import out_report_data
from test_unittest.Base.new_auto_setup import new_aotu_setup, new_loging, DIY_simple_report
from test_unittest.Base.BaseSettings import Picture, Report, LogsDIR, ipport_REPORT_DIR


class TestFind(unittest.TestCase):

    def get_parameter(logname,describe):
        def outer(fun):
            def inner(self,*args,**kwargs):
                new_loging(LogsDIR + logname)
                try:
                    arg = fun(self,*args,**kwargs)
                    case_data = {}
                    case_data['case_name'] = logname
                    case_data['case_create'] = "mwf"
                    # case_data['case_author'] = "meng"
                    case_data['case_desc'] = describe
                    case_data['test_result'] = True
                    case_data['filepath'] = __file__
                    case_data['start_time'] = time.time()
                    case_data['start_time_str'] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(case_data['start_time']))
                except Exception as e:
                    print("抛出异常：", e)
                    log(e, desc="报错信息", snapshot=True)
                    raise
                finally:
                    DIY_simple_report(__file__, logpath=LogsDIR + logname, output=Report + logname+".html")
                    case_data["htmlpath"] = ipport_REPORT_DIR + case_data['case_name'] + ".html"
                    out_report_data(case_data)
                    sleep(3)
                return arg
            return inner
        return outer


    @classmethod
    def setUpClass(self):

        logger = logging.getLogger("airtest")
        logger.setLevel(logging.ERROR)
        from poco.drivers.android.uiautomation import AndroidUiautomationPoco
        self.poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)
        new_aotu_setup(__file__,devices=["android://127.0.0.1:5037/a98223e6?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH"])
        print("开始测试------")
        clear_app("com.netease.cloudmusic")
        start_app("com.netease.cloudmusic")
    @classmethod
    def tearDownClass(self):
        # clear_app("com.netease.cloudmusic")
        stop_app("com.netease.cloudmusic")

    # def test_stop_app(self):
    #     stop_app("com.netease.cloudmusic")
    # @pytest.mark.first
    @get_parameter("登录",'登录测试')
    def test_login(self):
        # if not cli_setup():
        #     auto_setup(__file__, logdir=r"G:\new airtest\WY\login.log", devices=[
        #         "android://127.0.0.1:5037/a98223e6?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH"])
        # new_loging(LogsDIR+"login.log")
        # try:
            assert_exists(Template(Picture+"tpl1676122438062.png", record_pos=(0.006, -0.555), resolution=(1080, 1920)), "111")
            self.poco(text="同意").click()
            assert_exists(Template(Picture+"tpl1676122852853.png", record_pos=(-0.262, -0.731), resolution=(1080, 1920)),
                          "进入权限申请")
            self.poco("com.android.packageinstaller:id/permission_allow_button").click()
            wait(Template(Picture+"tpl1676122924519.png", record_pos=(-0.003, 0.257), resolution=(1080, 1920)))
            self.poco(text="立即体验").click()
            wait(Template(Picture+"tpl1676123013315.png", record_pos=(0.002, 0.503), resolution=(1080, 1920)))
            self.poco(text="同意并继续").click()
            wait(Template(Picture+"tpl1676123165604.png", record_pos=(-0.257, -0.736), resolution=(1080, 1920)))
            self.poco(text="始终允许").click()
            assert_exists(Template(Picture+"tpl1676123240149.png", record_pos=(-0.004, 0.812), resolution=(1080, 1920)), "登录完成")
        # except Exception as e:
        #     print("抛出异常：", e)
        #     log(e, desc="报错信息", snapshot=True)
        #     raise
        # finally:
        #     simple_report(__file__,logpath=LogsDIR+"login.log",output=Report+"login.html")
        #     sleep(3)

    # @pytest.mark.second
    @get_parameter("搜索","搜索测试")
    def test_search(self):
        # new_loging(LogsDIR+"search.log")
        # if not cli_setup():
        #     auto_setup(__file__, logdir=r"G:\new airtest\WY\search.log", devices=[
        #         "android://127.0.0.1:5037/a98223e6?cap_method=MINICAP&&ori_method=MINICAPORI&&touch_method=MINITOUCH"])
        while not self.poco(text="每日推荐").exists():
            keyevent("BACK")
        # try:
        self.poco("com.netease.cloudmusic:id/searchBar").click()
        assert_exists(Template(Picture+"tpl1676124643903.png", record_pos=(0.007, -0.748), resolution=(1080, 1920)),
                          "进入搜索页面")
        text("乌梅子酱")
        assert_exists(Template(Picture+"tpl1676124813213.png", record_pos=(-0.221, 0.462), resolution=(1080, 1920)), "找到歌曲")
        touch(Template(Picture+"tpl1676127961895.png", record_pos=(-0.052, 0.486), resolution=(1080, 1920)))

        assert_exists(Template(Picture+"tpl1676127487981.png", record_pos=(0.01, 0.472), resolution=(1080, 1920)), "成功进入播放")

        # except Exception as e:
        #     print("抛出异常：",e)
        #     log(e,desc="报错信息",snapshot=True)
        #     raise
        # finally:
        #     simple_report(__file__, logpath=LogsDIR+"search.log", output=Report+"test_search.html")


if __name__ == '__main__':
    unittest.main()
# login()


