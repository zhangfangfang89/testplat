#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os

import yaml


def yaml_parser():
    # 获取当前文件路径
    print(__file__)
    curPath = os.path.dirname(__file__)
    print(curPath)
    # 获取根路径
    rootPath = os.path.abspath(os.path.join(curPath, '../autotest'))  # 获取myProject，也就是项目的根路径
    print(rootPath)
    dataPath = os.path.join(rootPath, 'config')  # 获取tran.csv文件的路径
    print(dataPath)
    # 获取配置文件的路径 D:/WorkSpace/StudyPractice/Python_Yaml/YamlStudy\config.yaml
    yamlPath = os.path.join(dataPath, 'base.yml')
    print(yamlPath)
    # 加上 ,encoding='utf-8'，处理配置文件中含中文出现乱码的情况。
    with open(yamlPath, 'r', encoding='utf-8') as f:
        cont = f.read()
    x = yaml.safe_load(cont)
    return x;


if __name__ == '__main__':
    x = yaml_parser()
    print(x)
