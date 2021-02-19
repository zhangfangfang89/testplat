# -*- coding:utf-8 -*-
import os, sys, django

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "drf.settings")
django.setup()
from django.conf import settings

current_path = os.getcwd()
current_path = os.path.dirname(current_path)
if current_path not in sys.path:
    sys.path.append(current_path)

import logging.config
from logging.handlers import RotatingFileHandler

from colorlog import ColoredFormatter
import datetime, time


class LoggerFromfileconfig():

    def __init__(self, logger_name="fileLogger"):
        project_path = settings.BASE_DIR
        dir_tools = os.path.join(project_path, "tools")
        logging.config.fileConfig(os.path.join(dir_tools, "log.ini"))

        self.logger = logging.getLogger(logger_name)

    def outLogDebug(self, message):
        self.logger.debug(message)

    def outLogInfo(self, message):
        self.logger.info(message)

    def outLogError(self, message):
        self.logger.error(message)

    def outLogCritical(self, message):
        self.logger.critical(message)


class Logger():

    def __init__(self, path):

        """初始化"""
        self.log_colors_config = {
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red',
        }
        self.path_old = path
        self.path = path
        self.log_dir = ''

        now_time = datetime.date.today()
        file_name = os.path.exists(os.path.join(self.path, str(now_time)))
        if not file_name:

            self.path = os.path.join(self.path, str(now_time))
            os.system("mkdir {}".format(self.path))
        else:
            try:
                self.path = os.path.join(self.path_old, str(now_time))
                print(self.path)
            except OSError:
                raise

        now_time = "{}".format(time.localtime().tm_hour)
        self.logger = logging.getLogger(__name__)
        self.log_dir = os.path.join(self.path, "{}-log.log".format(now_time))
        self.filehandler = logging.FileHandler(self.log_dir)
        self.rotatingfilehandler = RotatingFileHandler(
            filename=self.log_dir, mode='a', maxBytes=1024 * 1024 * 5,
            backupCount=5,
            encoding='utf-8')
        self.consolehandler = logging.StreamHandler()
        self.logger.setLevel(logging.DEBUG)
        self.formatter = ColoredFormatter(
            '%(log_color)s[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] [%(levelname)s]- %(message)s',
            log_colors=self.log_colors_config)

    def rotateInputLog(self):
        """使用RotatingFileHandler类，滚动备份日志"""

        self.rotatingfilehandler.setLevel(level=logging.DEBUG)
        self.rotatingfilehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.rotatingfilehandler)
        # 写入后关闭
        self.rotatingfilehandler.close()
        return self.logger

    def inputLog(self):
        """将日志写入指定的文件"""

        self.filehandler.setLevel(level=logging.DEBUG)
        self.filehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.filehandler)
        # 写入后关闭
        self.filehandler.close()
        return self.logger

    def outLog(self):
        """控制台输出"""
        self.consolehandler.setLevel(level=logging.WARNING)
        self.consolehandler.setFormatter(self.formatter)
        self.logger.addHandler(self.consolehandler)
        return self.logger

    def removeFileLog(self):
        now_time = datetime.date.today() - datetime.timedelta(days=1)
        file_name = os.path.exists(os.path.join(self.path_old, str(now_time)))
        if file_name:

            try:
                os.popen("rm -rf {}".format(os.path.join(self.path_old, str(now_time))))
            except OSError:
                raise


