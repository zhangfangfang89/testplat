#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os, sys, django, json

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf.settings")
django.setup()

current_path = os.getcwd()
current_path = os.path.dirname(current_path)
if current_path not in sys.path:
    sys.path.append(current_path)
from api.apibase import ApiBase

from tools.log_tool import Logger
from django.conf import settings


def theLog(projectname):
    logger = Logger("{}".format(os.path.join(os.path.join(settings.BASE_DIR, projectname), 'log')))
    print(logger.log_dir)
    return logger


class TestApi(ApiBase):
    """class"""
    
    def getRoleList(self,*args,**wkargs):
        """获取角色列表数据哦哦哦哦"""
        log= theLog('cyWeb')
        self.set_url('/Users/mac/pythonProject/testplat/cyWeb/config/base.ini','/qdi-sales-online-api/staffRole/getRoleList/',platForm='pc')
        self.set_payload('/Users/mac/pythonProject/testplat/cyWeb/config/base.ini',{},platForm='pc')
        self.set_headers('/Users/mac/pythonProject/testplat/cyWeb/config/base.ini',{'Cookie': 'qaqdi_token=d9704ed45a1c42e39cc23cc98481be57'},platForm='pc')
        self.headers.update({ "Cookie":self.cookies})
        try:
            self.get()
            if self.code == 200:
                log.rotateInputLog().info("获取角色列表数据哦哦哦哦接口成功"+json.dumps(self.resp_json))
                return self.resp_json
            else:
                log.rotateInputLog().error("获取角色列表数据哦哦哦哦接口失败，非200！" + json.dumps(self.resp_json))
                raise Exception("获取角色列表数据哦哦哦哦接口失败，非200！")
        except Exception as e:
            log.rotateInputLog().error(e)

        
        

    