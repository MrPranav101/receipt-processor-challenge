import logging
import contextvars

from uuid import uuid4

context_id_var = contextvars.ContextVar('context_id')
request_id_var = contextvars.ContextVar('request_id')


class ContextFilter(logging.Filter):
    def filter(self, record) -> bool:
        record.request_id = request_id_var.get(None)
        return True


def set_request_id(request_id: str = None, generate=False) -> None:
    if generate:
        id = str(uuid4())
        request_id = str(id)
    request_id_var.set(request_id)


def get_logger(
    name: str,
    log_level: str = 'DEBUG',
) -> logging.Logger:
    """
    This is a utility function to return a Logger with a custom StreamHandler object

    Args:
        name (str): Name of the log instance\n
        log_level (str, optional): log level. Defaults to 'DEBUG'.\n
    Returns:
        logging.Logger: a Logger object
    """

    logger = logging.getLogger(name)
    logger.propagate = False
    level = logging.getLevelName(log_level.upper())
    logger.setLevel(level)
    logger.addFilter(ContextFilter())

    # prevent duplicate handlers
    streamhandler_exists = False
    for handler in logger.handlers:
        if type(handler) == logging.StreamHandler:
            streamhandler_exists = True

    if not streamhandler_exists:
        streamHandler = logging.StreamHandler()
        streamFormatter = logging.Formatter('[%(levelname)s]: %(request_id)s || %(asctime)s || %(filename)s:%(lineno)d || %(message)s')
        streamHandler.setFormatter(streamFormatter)
        streamHandler.setLevel(level)
        logger.addHandler(streamHandler)

    return logger
