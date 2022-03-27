import logging


def simple_logger(name='main'):
    logger = logging.getLogger(name)
    log_format = "[%(asctime)s] %(message)s"
    formatter = logging.Formatter(log_format)

    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)
    filehandler = logging.FileHandler(filename='main.log', encoding='utf-8')
    filehandler.setFormatter(formatter)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(streamhandler)
    logger.addHandler(filehandler)
    return logger
