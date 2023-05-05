import logging


class Log(object):
    def __init__(self, level="DEBUG"):
        self.log = logging.getLogger('猴面雀')
        self.log.setLevel(level)
        self.log_format = "%(asctime)s : <%(module)s>  [%(levelname)s]  %(message)s"

    def console_handle(self, level="DEBUG"):
        console_handle = logging.StreamHandler()
        # console_handle.setLevel(level)
        console_handle.setFormatter(self.get_formatter()[0])
        return console_handle

    def file_handle(self, level="DEBUG"):
        file_handler = logging.FileHandler("Data/Paissa.log", mode='a', encoding='utf-8')
        # file_handler.setLevel(level)
        file_handler.setFormatter(self.get_formatter()[1])
        return file_handler

    def get_formatter(self):
        console_fmt = logging.Formatter(fmt=self.log_format)
        file_fmt = logging.Formatter(fmt=self.log_format)
        return console_fmt, file_fmt

    def get_log(self):
        self.log.addHandler(self.console_handle())
        self.log.addHandler(self.file_handle())
        return self.log


logger = Log().get_log()
