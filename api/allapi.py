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
