#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

current_path = os.getcwd()
current_path = os.path.dirname(current_path)
if current_path not in sys.path:
    sys.path.append(current_path)
import configparser, os


class ConfigparserUse(object):
    def __init__(self, p):
        self.configobj = configparser.ConfigParser()
        self.dir = p

    def get_keys(self, session):
        self.configobj.read(self.dir, encoding="utf-8")
        option_list = self.configobj.options(session)
        print(option_list)
        return option_list

    def get_value_string(self, session, key):
        self.configobj.read(self.dir, encoding="utf-8")
        if self.configobj.has_option(session, key):
            return self.configobj.get(session, key)
        else:
            return None

    def get_value_int(self, session, key) -> int:
        self.configobj.read(self.dir, encoding="utf-8")
        if self.configobj.has_option(session, key):
            return self.configobj.getint(session, key)
        else:
            return None

    def set_value(self, session, key, value):
        # self.configobj.write(self.dir)
        if not self.configobj.has_section(session):
            self.configobj.add_section(session)
        if not self.configobj.has_option(session, key):
            self.configobj.set(session, key, value)
            f = open(self.dir, "w+")
            self.configobj.write(f)  # 写进文件
            f.close()
        

if __name__ == "__main__":
    c = ConfigparserUse()
    c.get_keys("db")
