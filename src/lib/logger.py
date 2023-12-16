import logging

_STREAM_HANDLER_NAME = "STREAM_HANDLER_NAME"


def get_default_logger(name: str, log_level: int | None = None) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(log_level or logging.DEBUG)
    logger.propagate = False
    contains_stream_handler = any(
        el.name == _STREAM_HANDLER_NAME for el in logger.handlers
    )
    if contains_stream_handler:
        return logger
    handler = logging.StreamHandler()
    handler.set_name(_STREAM_HANDLER_NAME)
    handler.setFormatter(
        logging.Formatter(fmt="[%(asctime)s:%(levelname)s:%(name)s] %(message)s"),
    )
    logger.addHandler(handler)
    return logger
