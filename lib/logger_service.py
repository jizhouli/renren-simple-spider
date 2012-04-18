#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Lijingtian (lijt@kuxun.com)
'''
LOGGER USAGE:

from logger_service import logger

logger.debug('test debug')
logger.info('test info')
logger.warn('test warn')
logger.error('test error')
logger.critical('test critical')
'''

# systemic class
import os
import sys
import logging

class Logger(object):
    '''
    '''
    #获取脚本文件的当前路径
    def cur_file_dir(self):
        #获取脚本路径
        path = sys.path[0]
        #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
        if os.path.isdir(path):
            return path
        elif os.path.isfile(path):
            return os.path.dirname(path)

    def __init__(self):
        # log file name
        log_filename = self.cur_file_dir() + '/run.log'
        print 'LOG FILE PATH:'
        print log_filename

        # create logger
        self.logger = logging.getLogger()
        
        # create file handler and not set level
        self.handler = logging.FileHandler(log_filename)
        
        formatter = logging.Formatter("%(asctime)s - %(levelname)s : %(message)s.")
        self.handler.setFormatter(formatter)

        # add handler to logger
        self.logger.addHandler(self.handler)

        # set output level
        #self.logger.setLevel(logging.NOTSET)
        self.logger.setLevel(logging.INFO)
        pass

    def __str__(self):
        pass

    def debug(self, output):
        try:
            print 'DEBUG: ' + output.encode('utf8')
            self.logger.debug(output.encode('utf8'))
        except Exception, e:
            self.logger.error('log output error')
            self.logger.error(str(e))

    def info(self, output):
        try:
            print 'INFO: ' + output.encode('utf8')
            self.logger.info(output.encode('utf8'))
        except Exception, e:
            self.logger.error('log output error')
            self.logger.error(str(e))


    def warn(self, output):
        try:
            print 'WARN: ' + output.encode('utf8')
            self.logger.warn(output.encode('utf8'))
        except Exception, e:
            self.logger.error('log output error')
            self.logger.error(str(e))


    def error(self, output):
        try:
            print 'ERROR: ' + output.encode('utf8')
            self.logger.error(output.encode('utf8'))
        except Exception, e:
            self.logger.error('log output error')
            self.logger.error(str(e))


    def critical(self, output):
        try:
            print 'CRITICAL: ' + output.encode('utf8')
            self.logger.critical(output.encode('utf8'))
        except Exception, e:
            self.logger.error('log output error')
            self.logger.error(str(e))


# Create One Instance of Logger Class
logger = Logger()


