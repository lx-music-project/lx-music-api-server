# ----------------------------------------
# - mode: python - 
# - author: helloplhm-qwq - 
# - name: log.py - 
# - project: lx-music-api-server - 
# - license: MIT - 
# ----------------------------------------
# This file is part of the "lx-music-api-server" project.
# Do not edit except you know what you are doing.

import logging
import colorlog
import os
from .utils import sanitize_filename
from .variable import debug_mode, log_length_limit

try:
    os.mkdir("logs")
except:
    pass

class flaskLogHelper(logging.Handler):
    # werkzeug日志转接器
    def __init__(self, custom_logger):
        super().__init__()
        self.custom_logger = custom_logger

    def emit(self, record):
        #print(record)
        log_message = self.format(record)
        self.custom_logger.info(log_message)

class log:
    # 主类
    def __init__(self, module_name = 'Not named logger', output_level = 'INFO', filename = ''):
        self._logger = logging.getLogger(module_name)
        if not output_level.upper() in dir(logging):
            raise NameError('Unknown loglevel: '+output_level)
        if not debug_mode:
            self._logger.setLevel(getattr(logging, output_level.upper()))
        else:
            self._logger.setLevel(logging.DEBUG)
        formatter = colorlog.ColoredFormatter(
            '%(log_color)s%(asctime)s|[%(name)s/%(levelname)s]|%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            log_colors={
                'DEBUG': 'cyan',
                'INFO': 'green',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'red,bg_white',
            })
        file_formatter = logging.Formatter(
            '%(asctime)s|[%(name)s/%(levelname)s]|%(message)s',
            datefmt='%Y-%m-%d %H:%M:%S',
            )
        if filename:
            filename = sanitize_filename(filename)
        else:
            filename = './logs/' + module_name + '.log'
        file_handler = logging.FileHandler(filename, encoding='utf-8')
        file_handler.setFormatter(file_formatter)
        file_handler_ = logging.FileHandler("./logs/console_full.log", encoding='utf-8')
        file_handler_.setFormatter(file_formatter)
        self._logger.addHandler(file_handler_)
        self._logger.addHandler(file_handler)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.module_name = module_name
        self._logger.addHandler(console_handler)
        self.debug_ = logging.getLogger(module_name + '_levelChangedMessage')
        debug_handler = logging.StreamHandler()
        debug_handler.setFormatter(formatter)
        self.debug_.addHandler(debug_handler)
        self.debug_.setLevel(logging.DEBUG)

    def debug(self, message, allow_hidden = True):
        if self.module_name == "flask" and "\n" in message:
            if message.startswith("Error"):
                return self._logger.error(message)
            for m in message.split("\n"):
                if "WARNING" in m:
                    self._logger.warning(m)
                else:
                    self._logger.info(m)
            return
        if len(str(message)) > log_length_limit and allow_hidden:
            message = str(message)[:log_length_limit] + "..."
        self._logger.debug(message)

    def log(self, message, allow_hidden = True):
        if self.module_name == "flask" and "\n" in message:
            if message.startswith("Error"):
                return self._logger.error(message)
            for m in message.split("\n"):
                if "WARNING" in m:
                    self._logger.warning(m)
                else:
                    self._logger.info(m)
            return
        if len(str(message)) > log_length_limit and allow_hidden:
            message = str(message)[:log_length_limit] + "..."
        self._logger.info(message)

    def info(self, message, allow_hidden = True):
        if self.module_name == "flask" and "\n" in message:
            if message.startswith("Error"):
                return self._logger.error(message)
            for m in message.split("\n"):
                if "WARNING" in m:
                    self._logger.warning(m)
                else:
                    self._logger.info(m)
            return
        if len(str(message)) > log_length_limit and allow_hidden:
            message = str(message)[:log_length_limit] + "..."
        self._logger.info(message)

    def warning(self, message):
        self._logger.warning(message)

    def error(self, message):
        self._logger.error(message)

    def critical(self, message):
        self._logger.critical(message)

    def set_level(self, loglevel):
        loglevel_upper = loglevel.upper()
        if not loglevel_upper in dir(logging):
            raise NameError('Unknown loglevel: '+loglevel)
        self.debug_.debug('loglevel changed to: '+ loglevel_upper)
        self._logger.setLevel(getattr(logging, loglevel_upper))

    def getLogger(self):
        return self._logger
        
    def addHandler(self, handler):
        self._logger.addHandler(handler)