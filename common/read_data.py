#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
from functools import lru_cache
import yaml
import json
from configparser import ConfigParser
from common.logger import logger

class MyConfigParser(ConfigParser):
    # 重写 configparser 中的 optionxform 函数，解决 .ini 文件中的 键option 自动转为小写的问题
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=defaults)

    def optionxform(self, optionstr):
        return optionstr

class ReadFileData():

    def __init__(self):
        pass

    @lru_cache
    def load_yaml(self, file_path):
        logger.info(f"加载 {file_path} 文件......")
        with open(file_path, encoding='utf-8') as f:
            data = yaml.safe_load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    @lru_cache
    def load_json(self, file_path):
        logger.info(f"加载 {file_path} 文件......")
        with open(file_path, encoding='utf-8') as f:
            data = json.load(f)
        logger.info("读到数据 ==>>  {} ".format(data))
        return data

    @lru_cache
    def load_ini(self, file_path):
        logger.info(f"加载 {file_path} 文件......")
        config = MyConfigParser()
        config.read(file_path, encoding="UTF-8")
        data = dict(config._sections)
        # print("读到数据 ==>>  {} ".format(data))
        return data

class get_data():

    def __init__(self):
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")

    def get_ini_data(self,host_name,name):
        # BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        # data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
        # # print(data_file_path)
        return ReadFileData().load_ini(self.data_file_path)[host_name][name]

    def get_group_data(self,host_name):
        return ReadFileData().load_ini(self.data_file_path)[host_name]

if __name__ == '__main__':
    pass
