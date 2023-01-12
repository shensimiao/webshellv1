from __future__ import absolute_import, division, with_statement

import os
import configparser
from ast import literal_eval
from lib.utils import BASE_DIR

from typing import Union

CONFIG_FILE = os.path.join(BASE_DIR, 'conf/mysql.conf')

if not os.path.exists(CONFIG_FILE):
    raise FileNotFoundError("Not found : {}".format(CONFIG_FILE))

__all__ = [
    'Config',
    'LoggingConfiguration',
    'DbConfiguration',

]


class Config(object):

    def __init__(self):
        self.config_file = CONFIG_FILE
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def write(self) -> None:
        with open(self.config_file, 'w+') as f:
            self.config.write(f)

    def get(self, section, option) -> Union[str, None]:
        if self.config.has_option(section, option):
            return self.config.get(section, option).strip('"').strip("'")
        return None

    def add_section(self, section) -> bool:
        if not self.config.has_section(section):
            self.config.add_section(section)
            self.write()
            return True
        return False

    def remove_section(self, section) -> bool:
        if self.config.has_section(section):
            self.config.remove_section(section)
            self.write()
            return True
        return False

    def add_option(self, section, option, value) -> bool:
        if self.config.has_section(section) and not self.config.has_option(section, option):
            self.config.set(section, option, value)
            self.write()
            return True
        return False

    def remove_option(self, section, option) -> bool:
        if self.config.has_option(section, option):
            self.config.remove_option(section, option)
            self.write()
            return True
        return False


config = Config()


class LoggingConfiguration(object):
    _section = 'log'
    log_console_level = config.get(_section, 'log_console_level') or "info"
    log_file_level = config.get(_section, 'log_file_level') or "info"
    log_file_path = os.path.join(BASE_DIR, config.get(_section, 'log_file_path')
                                 or "logs/")
    log_name = config.get(_section, 'log_name') or "webshell"


class DbConfiguration(object):
    _section = 'mysql'
    host = config.get(_section, 'host')
    port = config.get(_section, 'port')
    username = config.get(_section, 'user')
    password = config.get(_section, 'passwd')
    db_host = config.get(_section, 'db_host')
    db_username = config.get(_section, 'db_user')
    db_password = config.get(_section, 'db_passwd')
    db = config.get(_section, 'db')
    charset = config.get(_section, 'charset') or 'utf-8'
    pool_size = config.get(_section, 'pool_size')
    pool_recycle = config.get(_section, 'pool_recycle')
    autocommit = eval(config.get(_section, 'autocommit')) or False
    old_time = eval(config.get(_section, 'old_time')) or 6
