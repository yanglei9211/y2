class BaseError(Exception):
    """
    基类，不要直接raise
    """
    def __init__(self, msg_fmt_str, *args, **kwargs):
        self.message = msg_fmt_str % args
        self.fmt_str = msg_fmt_str
        self.args = args

        # error_id 用以分类错误，以在处理时提供简单依据
        self.error_id = kwargs.get('error_id', self.__class__.__name__)
        # 期望的http状态码, web server 使用
        self.http_status_code = kwargs.get('http_status_code', None)

    def __str__(self):
        return '{}: {}'.format(self.error_id, self.message)

    def __unicode(self):
        return u'{}: {}'.format(self.error_id, self.message)


class DTError(BaseError):
    # 接口用,用于系统执行发生异常,正常返回,code=-1,告知已检测到的错误信息
    def __init__(self, *args, **kwargs):
        super(DTError, self).__init__(*args, **kwargs)
        # self.http_status_code = self.http_status_code or 200
        self.http_status_code = 200


class InterError(BaseError):
    # 内部调用错误,调用其他服务时发生异常,正常返回,code=-1,告知已检测到的错误信息
    def __init__(self, *args, **kwargs):
        super(InterError, self).__init__(*args, **kwargs)
        # self.http_status_code = self.http_status_code or 200
        self.http_status_code = 200
