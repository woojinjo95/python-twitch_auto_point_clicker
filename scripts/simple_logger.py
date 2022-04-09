import logging


def simple_logger(name='main'):
    logger = logging.getLogger(name)
    log_format = "[%(asctime)s]%(levelname)s %(message)s"
    formatter = logging.Formatter(log_format)

    streamhandler = logging.StreamHandler()
    streamhandler.setFormatter(formatter)
    streamhandler.setLevel(logging.INFO)
    filehandler = logging.FileHandler(filename=f'{name}.log', encoding='utf-8')
    filehandler.setFormatter(formatter)
    filehandler.setLevel(logging.DEBUG)

    logger.setLevel(logging.DEBUG)
    logger.addHandler(streamhandler)
    logger.addHandler(filehandler)
    return logger
