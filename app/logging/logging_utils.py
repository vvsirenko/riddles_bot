import inspect
import logging
import logging.config
import json

with open('./logging/logging_config.json') as file:
    logging_config = json.load(file)

logging.config.dictConfig(logging_config)
default_logger = logging.getLogger()


class LogLevel:
    critical = logging.getLevelName(logging.CRITICAL)
    error = logging.getLevelName(logging.ERROR)
    warning = logging.getLevelName(logging.WARNING)
    info = logging.getLevelName(logging.INFO)
    debug = logging.getLevelName(logging.DEBUG)


class LogLabel:
    run_method = "RUN_METHOD"


class LogCustomMessage:
    run_method = f'user: %(user_name)s user_id: %(user_id)s run_method: %(method)s'


def log(message, params=None, level="INFO"):
    try:
        level_name = logging.getLevelName(level)
        module_name = inspect.currentframe().f_back.f_globals['__name__']
        logger = logging.getLogger(module_name)
        logger.log(level_name, message, params)
    except Exception:
        default_logger.log(
            logging.getLevelName("ERROR"),
            "Failed to write a log. Exception occurred"
        )
