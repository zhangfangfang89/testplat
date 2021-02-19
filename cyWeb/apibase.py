#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import sys

current_path = os.getcwd()
current_path = os.path.dirname(current_path)
if current_path not in sys.path:
    sys.path.append(current_path)
import requests
import json
import ast
from tools.configparser_tool import ConfigparserUse


class ApiBase(object):
    def __init__(self):
        self.url = ''
        self.headers = {}
        self.payload = {}
        self.resp_json = ''
        self.code = ''
        self.cookies = ''

    def set_url(self, dir_base, url, platForm, *args, **kwargs):
        """

        :param url: 被测的url，可有带主机的
        :return: self.url
        """

        if url.startswith("http://") or url.startswith("https://"):
            self.url = url
        else:
            config = ConfigparserUse(dir_base)
            self.url = config.get_value_string(platForm, 'uil') + url

    def set_headers(self, dir_base, headers, platForm, *args, **kwargs):
        """

        :param header: 头部信息
        :param Content_Length:
        :param platForm:
        :return:
        """
        config = ConfigparserUse(dir_base)
        self.headers = ast.literal_eval(config.get_value_string(platForm, 'headers'))
        # 不同的项目这边的代码会有不同，先写这个通用的
        self.headers.update(headers)

    def set_payload(self, dir_base, data, platForm, *args, **kwargs):
        """

        :param data:
        :param platForm:用于表示接口是pc端还是app端的

        :param type: 用于判断请求方式 ,True:表示非form-data
        :return:
        """
        config = ConfigparserUse(dir_base)
        # 转化为dict
        self.payload = ast.literal_eval(config.get_value_string(platForm, 'payload'))
        # 添加dict
        # 不同的项目这边的代码会有不同，先写这个通用的
        self.payload.update(data)

    def get(self):
        # 该方法比较少用还未完善
        resp_json = requests.get(url=self.url, params=self.payload, headers=self.headers)
        self.code = resp_json.status_code
        if self.code == 200:
            self.resp_json = resp_json.json()

    def post(self):
        """
        :return:
        """
        # 这边方式适合表单提交的情况
        resp_json = requests.get(url=self.url, data=self.payload, headers=self.headers)
        self.code = resp_json.status_code
        if self.code == 200:
            try:
                self.resp_json = resp_json.json()
            except Exception as e:
                raise e

    def dictTostr(self, dict_str):
        """
        用于将字典的key和value 拼接成字符串
        :param dict_str:
        :return:
        """
        dstr = ''
        for key, value in dict_str.items():
            dstr += '{}={};'.format(key, value)
        return dstr
