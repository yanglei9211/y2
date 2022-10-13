import os
import argparse
from configparser import RawConfigParser, SectionProxy


class ProgramArgs:
    def __init__(self, args: argparse.Namespace):
        self.debug = args.debug
        self.host = args.host
        self.port = args.port


class DefaultSetting:
    def __init__(self, section: SectionProxy):
        self.send_error_msg = section['send_error_msg']
        self.msg_robot = section['msg_robot']
        self.token_timeout = section.get('token_timeout', 86400)  # 默认一天
        self.secret_key = section.get('secret_key')


class MongoDBSetting:
    def __init__(self, section: SectionProxy):
        self.mongodb_url = section['mongodb_url']
        self.replica_set = section['replica_set']
        self.w_value = section.get('w_value', 1)
        self.wtimeout = section.get('wtimeout', 5000)


class MqSetting:
    def __init__(self, section: SectionProxy):
        self.mq_host = section['mq_host']
        self.log_mq_name = section['log_mq_name']


class EsSetting:
    def __init__(self, section: SectionProxy):
        self.es_host = section['es_host']


def get_config(debug: int) -> RawConfigParser:
    filename = 'server.conf' if debug else 'prod.conf'
    cf = RawConfigParser()
    if os.path.isfile(filename):
        cf.read(filename)
    else:
        raise IOError(filename + ' does not exist or not file.')
    return cf


_argp = argparse.ArgumentParser()
_argp.add_argument('--debug', default='1', type=int)
_argp.add_argument('--port', default=8000, type=int)
_argp.add_argument('--host', default='0.0.0.0', type=str)
_args = _argp.parse_args()

# 命令行参数
program_args = ProgramArgs(_args)
_cf = get_config(program_args.debug)

# 公共配置
default_setting = DefaultSetting(_cf['default'])

# mongodb配置
mongodb_setting = MongoDBSetting(_cf['mongodb'])

# mq配置
mq_setting = MqSetting(_cf['mq'])

# es配置
es_setting = EsSetting(_cf['es'])

