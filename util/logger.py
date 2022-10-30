import os
import time
from functools import wraps

from loguru import logger as _logger

# def init_logger():
#     basedir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#
#     # print(f"log basedir{basedir}")  # /xxx/python_code/FastAdmin/backend/app
#     # 定位到log日志文件
#     log_path = os.path.join(basedir, 'logs')
#
#     if not os.path.exists(log_path):
#         os.mkdir(log_path)
#
#     log_path_error = os.path.join(log_path, f'{time.strftime("%Y-%m-%d")}_error.log')

# 日志简单配置
# 具体其他配置 可自行参考 https://github.com/Delgan/loguru
# logger.add(log_path_error, rotation="12:00", retention="5 days", enqueue=True)

class Logging(object):
    def __new__(cls):
        # if not cls._instance:
        #     cls._instance = super(Loggings, cls).__new__(cls, *args, **kwargs)
        # return cls._instance
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logging, cls).__new__(cls)
        return cls.instance
    info = _logger.info
    # @classmethod
    # def info(cls, msg):
    #     return _logger.info(msg)

    @classmethod
    def debug(cls, msg):
        return _logger.debug(msg)

    @classmethod
    def warning(cls, msg):
        return _logger.warning(msg)

    @classmethod
    def error(cls, msg):
        # LoggingMq().send_msg(msg)
        return _logger.error(msg)



def async_logger_time_cost(tar_func):
    @wraps(tar_func)
    async def wrap_func(*args, **kwargs):
        st = time.time()
        res = await tar_func(*args, **kwargs)
        time_cost = time.time() - st
        time_cost *= 1000
        time_cost = "%.2f" % time_cost
        if 'request' in kwargs:
            r = kwargs['request']
            _logger.info("{}: {}:   cost {}ms".format(r.method, r.url.path, time_cost))
        else:
            _logger.info("function {} cost {} ms".format(tar_func.__name__, time_cost))
        return res
    return wrap_func


def logger_time_cost(tar_func):
    @wraps(tar_func)
    def wrap_func(*args, **kwargs):
        st = time.time()
        res = tar_func(*args, **kwargs)
        time_cost = time.time() - st
        time_cost *= 1000
        time_cost = "%.2f" % time_cost
        if 'request' in kwargs:
            r = kwargs['request']
            _logger.info("{}: {}:   cost {}ms".format(r.method, r.url.path, time_cost))
        else:
            _logger.info("function {} cost {} ms".format(tar_func.__name__, time_cost))
        return res
    return wrap_func


def setup_logging():
    Logging()
