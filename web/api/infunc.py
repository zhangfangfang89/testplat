# -*- coding:utf-8 -*-
import os, sys

current_path = os.getcwd()
current_path = os.path.dirname(current_path)
if current_path not in sys.path:
    sys.path.append(current_path)

import datetime
import random
import inspect
import math
class InfuncAll(object):

    def getNowDate(self):
         pass

    def getRandomDigist(self,prefix=None,num=None,*args,**kwargs):
        """
        返回有指定开头和指定长度的随机数字字符串
        :param prefix:
        :param num:
        :param args:
        :param kwargs:
        :return:
        """
        random_s = ""
        random_s = str(prefix)+math.ceil(random.random()*1000000) if prefix else math.ceil(random.random()*1000000)
        random_s = str(prefix)+math.ceil(random.random()*10*int(num)) if prefix and num else math.ceil(random.random()*1000000)
        return  random_s



