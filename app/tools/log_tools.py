import logging
import os


def log(level, message, path=''):
    """
        log to file and console
    :param level: log level
    :param message: message
    :param path: log path (only for plugin to use)
    :return:
    """
    """
    Log to multiple locations if multipleLocs is True
    """
    if path != '':
        file_name = os.path.splitext(path)[0]
        logger = logging.getLogger(path)
        path = "log/plugin/%s.log" % path
    else:
        logger = logging.getLogger("general")
        path = "log/general.log"
    logger.setLevel(logging.INFO)
    fh = logging.FileHandler(path)
    formatter = logging.Formatter('%(levelname)s - %(asctime)s - %(name)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    logger.addHandler(console)

    if level == 'info':
        logger.info(message)

    if level == 'error':
        logger.error(message)

    if level == 'debug':
        logger.debug(message)

    if level == 'exception':
        logger.exception(message)

    if level == 'critical':
        logger.critical(message)
