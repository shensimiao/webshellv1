
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from lib.config import LoggingConfiguration
from lib.utils import BASE_DIR
__all__ = [
    'Logger',
    'logger',
]


def handleException(excType, excValue, traceback, logger):
    logger.error("Uncaught exception", exc_info=(excType, excValue, traceback))

config = LoggingConfiguration()

#Global setup
FILE_LOG_LEVEL = config.log_file_level
FILE_LOG_PATH = config.log_file_path
FILE_NAME = config.log_name
CONSOLE_LOG_LEVEL = config.log_console_level

LOG_PATH = os.path.join(BASE_DIR, FILE_LOG_PATH) # 存放log文件的路径


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }
    #全局配置
    logging.root.setLevel(logging.NOTSET)

    logger = None

    # 日志输出格式
    fmt = '%(asctime)s [%(levelname)s][%(name)s][%(module)s][%(funcName)s] : %(message)s'

    formatter = logging.Formatter(fmt)

    def __init__(self,
                 loggname,
                 console_output_level='debug',
                 file_output_level='info',
                 backup_count=5):

        self.logger = logging.getLogger(loggname)
        self.log_file_name = loggname + '.log'

        self.console_level = self.level_relations[console_output_level]
        self.file_level = self.level_relations[file_output_level]
        self.backup_count = backup_count

    def get_logger(self):

        """ 在logger中添加日志句柄并返回，如果logger已有句柄，则直接返回 """
        if not self.logger.handlers:  #避免重复日志

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(self.formatter)
            console_handler.setLevel(self.console_level)
            self.logger.addHandler(console_handler)

            #每天重新创建一个日志文件，最多保留backup_count份
            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH,self.log_file_name), when='D',
                                                    interval=1, backupCount=self.backup_count, delay=True,
                                                    encoding='utf-8')
            file_handler.setFormatter(self.formatter)
            file_handler.setLevel(self.file_level)
            self.logger.addHandler(file_handler)
        return self.logger


DDoSDLog = Logger(
    loggname=FILE_NAME, console_output_level=CONSOLE_LOG_LEVEL,
    file_output_level=FILE_LOG_LEVEL
)
logger = DDoSDLog.get_logger()
