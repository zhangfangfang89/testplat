#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys

current_path = os.getcwd()
current_path = os.path.dirname(current_path)
if current_path not in sys.path:
    sys.path.append(current_path)

import pymysql


class DbBase(object):
    def __init__(self, ip, username, password, database_name, port=3306):
        try:
            self.conn = pymysql.connect(host=ip, user=username, passwd=password, db=database_name, port=port)

        except BaseException as e:
            raise Exception("创建数据库连接：" + e)
        else:
            self.cursor = self.conn.cursor()

    def select_sql(self, sql):
        try:
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except BaseException as e:
            raise Exception("查询语句" + e)

    def insert_sql(self, sql):

        try:

            self.cursor.execute(sql)
            self.conn.commit()
        except BaseException:
            self.conn.rollback()

    def update_sql(self, sql):
        print('开始update  sql')
        try:
            self.cursor.execute(sql)

            self.conn.commit()
        except BaseException:
            self.conn.rollback()
