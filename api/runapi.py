# -*- coding:utf-8 -*-
import os, sys

current_path = os.getcwd()
current_path = os.path.dirname(current_path)
if current_path not in sys.path:
    sys.path.append(current_path)

