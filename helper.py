import logging


def get_logger(name):
    logger = logging.getLogger(name)
    logging.basicConfig(
        level="INFO",
        format= "[%(asctime)s] [%(filename)s] [%(funcName)s] [%(lineno)d] ---> %(message)s"  # noqa
    )
    return logger
