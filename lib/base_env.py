#!/usr/bin/env python
# -*- coding: utf-8 -*-
#Author: Lijingtian(lijt@kuxun.com)
'''
通用基础环境
'''

import os
import sys
from logger_service import logger

logger.info('base_env loading')

# GLOBAL SETTING VARIABLES

MV_CMD=''
DIR_SEP=''
if os.name == 'nt':
    MV_CMD = 'move'
    DIR_SEP = '\\'
    logger.info('os platform - nt')
elif os.name == 'posix':
    MV_CMD = 'mv'
    DIR_SEP = '/'
    logger.info('os platform - posix')
else:
    logger.error('the system can not be identified, nt or posix is needed. EXIT')
    sys.exit(1)

#获取脚本文件的当前路径
def cur_file_dir():
    #获取脚本路径
    path = sys.path[0]
    #判断为脚本文件还是py2exe编译后的文件，如果是脚本文件，则返回的是脚本的目录，如果是py2exe编译后的文件，则返回的是编译后的文件路径
    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)

logger.info('base_env loaded')
