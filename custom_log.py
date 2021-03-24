import datetime
import logging
import sys
import os
import inspect
import random
from logging.handlers import RotatingFileHandler
# default log setting
date_time = datetime.datetime.now().strftime("%Y_%m_%d")
log_name = 'logging_scan_' + date_time + '.log'
logging.basicConfig(level=logging.DEBUG)

# import force all import lib logging level
loggers = [logging.getLogger(name) for name in logging.root.manager.loggerDict]
for logger in loggers:
    logger.setLevel(logging.ERROR)

# create custom logger
auto_logger = logging.getLogger("auto_logger")
# custom_handler = logging.FileHandler(log_name)
custom_handler = RotatingFileHandler(log_name, mode='a', maxBytes=5*1024*1024, backupCount=2, encoding=None, delay=0)


custom_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y/%m/%d %H:%M")
ENV = os.environ.get('ENV', 'test')
if ENV == 'test':
    custom_handler.setLevel(logging.DEBUG)
elif ENV == 'dev':
    custom_handler.setLevel(logging.INFO)
elif ENV == 'sit':
    custom_handler.setLevel(logging.INFO)
elif ENV == 'uat':
    custom_handler.setLevel(logging.INFO)
elif ENV == 'prod':
    custom_handler.setLevel(logging.INFO)
else:
    custom_handler.setLevel(logging.DEBUG)
custom_handler.setFormatter(custom_format)
auto_logger.addHandler(custom_handler)

# uuid setting
random.seed(datetime.datetime.now())
log_id = str("%04d" % random.randint(1, 9999))
local_id = 'eth-' + log_id


def info(input_str):
    func = inspect.currentframe().f_back.f_code
    if func.co_name == '<module>':
        temp_log = "   |" + local_id + '| ' + input_str
    else:
        temp_log = f"   |%s|%s| %s" % (local_id, func.co_name, input_str)
    auto_logger.info(temp_log)
    print(temp_log)


def warning(input_str):
    func = inspect.currentframe().f_back.f_code
    if func.co_name == '<module>':
        temp_log = "|" + local_id + '| ' + input_str
    else:
        temp_log = f"|%s|%s| %s" % (local_id, func.co_name, input_str)
    auto_logger.warning(temp_log)
    print(temp_log)


def error(input_str):
    func = inspect.currentframe().f_back.f_code
    if func.co_name == '<module>':
        temp_log = "  |" + local_id + '| ' + input_str
    else:
        temp_log = f"  |%s|%s| %s" % (local_id, func.co_name, input_str)
    auto_logger.error(temp_log)
    print(temp_log)


def debug(input_str):
    func = inspect.currentframe().f_back.f_code
    if func.co_name == '<module>':
        temp_log = f"  |%s| %s (%s line:%i)" % (local_id, input_str, func.co_filename, func.co_firstlineno)
    else:
        temp_log = f"  |%s|%s| %s (%s line:%i)" % (local_id,
                                                   func.co_name,
                                                   input_str,
                                                   func.co_filename,
                                                   func.co_firstlineno)
    auto_logger.debug(temp_log)
    print(temp_log)


def read():
    temp_list = []
    try:
        path_html = ""
        files = os.listdir(".")
        files.sort()
        for file in files:
            if 'logging_scan' in file:
                path_html = file
        if os.path.isfile(path_html):
            read_file = open(path_html)
            lines = read_file.readlines()
            lines.reverse()

            for line in lines:
                line = line.replace('\n', '')
                temp_list.append(str(line))
            read_file.close()
    except Exception as ex:
        print(ex)
    return temp_list


def demo_function():
    info('log info test')
    warning('log warning test')
    error('log error test')
    debug('log debug test')


# unit test
if __name__ == '__main__':
    exit_code = 0
    try:
        demo_function()
    except Exception as ex_test:
        exit_code = 1
        print(ex_test)
    finally:
        if exit_code == 0:
            print('----------------------')
            print('| azure_vault : PASS |')
            print('----------------------')
        else:
            print('----------------------')
            print('| azure_vault : FAIL |')
            print('----------------------')
        sys.exit(exit_code)



