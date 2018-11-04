#*****************************************************************************
# log.py :
# Description :
#       the library for common logging
#
# Maintainer: Motica
#
# History: (optional)
#  2018/11/14 created by Motica
#
#****************************************************************************/
import logging
from settings import *

# Global
LOG_LEVELS = ['CRITICAL', 'ERROR', 'WARNING', 'INFO', 'DEBUG', 'NOTSET']

def get_log_level():
    if LOG_LEVEL in LOG_LEVELS: # Check log level is valid
        return LOG_LEVEL
    else: # set log to 'DEBUG' if log is not valid
        print ('[Error] log level is not correct, set log to default (DEBUG)')
        return 'DEBUG'

class lib_core_log():
    def __init__(self, name):
        level = get_log_level()
        logging.basicConfig(level=level,
                            format = '%(asctime)s [%(name)s] [%(lineno)s] [%(levelname)s] %(message)s',
                            handlers = [logging.FileHandler(name+'.log', 'w', 'utf-8'),]
                            )      
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level))
        # Setup Handler
        ch = logging.StreamHandler()
        ch.setLevel(getattr(logging, level))
        formatter = logging.Formatter(\
            '%(asctime)s [%(name)s] [%(lineno)s] [%(levelname)s] %(message)s')
        ch.setFormatter(formatter)
        # Setup Logger
        self.logger.addHandler(ch)
