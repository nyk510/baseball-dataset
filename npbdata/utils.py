# coding: utf-8
"""
write about this python script
"""

__author__ = "nyk510"

from logging import getLogger, StreamHandler, Formatter, FileHandler


def get_logger(name, log_level="DEBUG", output_file=None, handler_level="INFO"):
    """
    :param str name:
    :param str log_level:
    :param str | None output_file:
    :param str handler_level: handler がログを送出する level
    :return: logger
    """
    logger = getLogger(name)

    formatter = Formatter("[%(levelname)s %(name)s] %(asctime)s: %(message)s")

    handler = StreamHandler()
    logger.setLevel(log_level)
    handler.setLevel(handler_level)

    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if output_file:
        file_handler = FileHandler(output_file)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(handler_level)
        logger.addHandler(file_handler)

    return logger
