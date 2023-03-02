# -*- coding: utf-8 -*-
"""
@author: ZJ
@email: 1576094876@qq.com
@File : PublicFunction.py
@desc: 
@Created on: 2020/12/4 11:35
"""
import json
import os
import time

import jinja2

from test_unittest.Base.BaseSettings import Report_Data, BaseDIR, StaticDIR


def out_report_data(case_data):
    case_data['run_time'] = round(time.time() - case_data['start_time'],1)
    txtpath = Report_Data + case_data['case_name'] + ".txt"
    with open(txtpath, 'w', encoding='utf-8') as f:
        json.dump(case_data, f, ensure_ascii=False, indent=2)

def render_directory():
    """ 用jinja2渲染html"""
    # template_name "log_template.html
    # output_file  html输出地址
    # template_vars  kwags
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(BaseDIR),
        extensions=(),
        autoescape=True
    )
    report_data_list = []
    template = env.get_template("Template.html")
    report_data_filename_list = os.listdir(Report_Data)
    print(report_data_filename_list)
    i = 0
    sum_time = 0
    for report_data_filename in report_data_filename_list:
        with open(Report_Data+report_data_filename,"r",encoding="utf-8") as f:
            report_data = json.loads(f.read())
            if report_data['test_result'] is True:
                i+=1
            sum_time += report_data['run_time']
            report_data_list.append(report_data)
    detail_info ={}
    detail_info['sum'] = len(report_data_list)
    detail_info['success_num'] = i
    detail_info['error_num'] = detail_info['sum'] -detail_info['success_num']
    detail_info['percent'] = str(round(detail_info['success_num']/detail_info['sum'],4)*100)+"%"
    detail_info['sum_time'] = sum_time
    html = template.render(report_data_list=report_data_list,detail_info=detail_info)

    with open(StaticDIR+"\\result.html", 'w', encoding="utf-8") as f:
        f.write(html)

if __name__ == '__main__':
    render_directory()