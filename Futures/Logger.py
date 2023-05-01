import logging
from logging import handlers
from datetime import datetime
import os


class Logger(object):
    level_relations = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR, 'crit': logging.CRITICAL}  #日志级别关系映射

    def __init__(self, logname, level='info', fmt='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s'):

        self.logger = logging.getLogger(logname)
        now = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        format_str = logging.Formatter(fmt)
        self.logger.setLevel(self.level_relations.get(level))
        console = logging.StreamHandler()  # console out
        console.setFormatter(format_str)
        handler = logging.FileHandler(f'./Logs/{logname}-{now}.log', encoding='utf-8')
        handler.setFormatter(format_str)
        self.logger.addHandler(handler)
        self.logger.addHandler(console)
