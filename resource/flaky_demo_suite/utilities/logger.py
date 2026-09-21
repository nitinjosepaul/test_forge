import logging
from pathlib import Path

class LogManager:
    _logger = None
    _custom_file_handlers = {}

    _MAIN_CONSOLE_HANDLER_NAME = "MAIN CONSOLE HANDLER"
    _MAIN_FILE_HANDLER_NAME = "MAIN FILE HANDLER"

    def __init__(self, name='MAIN', main_log_file_path='file.log'):
        if type(self)._logger is None:
            type(self)._logger = logging.getLogger(name)
            type(self)._logger.setLevel(logging.DEBUG)

            # Disable propagation to parent loggers.
            type(self)._logger.propagate = False

            # Add the main console and file handlers
            self._add_main_file_handler(absolute_file_path=main_log_file_path)
            self._add_main_console_handler()

    @staticmethod
    def _formatter():
        return logging.Formatter('[%(asctime)s] [%(name)s | %(module)s.%(funcName)s] [%(levelname)s] %(message)s',
                                           datefmt='%d-%m-%Y %I:%M:%S %p')

    @classmethod
    def _get_handler_by_name(cls, name):
        if cls._logger is None:
            return None

        for handler in cls._logger.handlers:
            if handler.get_name() == name:
                return handler
        else:
            return None

    @classmethod
    def _build_file_handler(cls, name, absolute_file_path, level=logging.INFO, mode='w'):
        file_path = Path(absolute_file_path)
        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(str(file_path), mode=mode)
        file_handler.set_name(name)
        file_handler.setLevel(level)
        file_handler.setFormatter(cls._formatter())
        return file_handler

    @classmethod
    def _add_main_file_handler(cls, absolute_file_path, level=logging.DEBUG):
        if cls._get_handler_by_name(cls._MAIN_FILE_HANDLER_NAME) is not None:
            cls._logger.debug(f"Main file handler {cls._MAIN_FILE_HANDLER_NAME} is already present - "
                              f"not adding file handler again")
        else:
            # Create a file handler
            file_handler = cls._build_file_handler(
                name = cls._MAIN_FILE_HANDLER_NAME,
                absolute_file_path=absolute_file_path,
                level = level,
                mode = 'w')

            # Add file handler to logger
            cls._logger.addHandler(file_handler)
            cls._logger.debug(f"Main file handler {cls._MAIN_FILE_HANDLER_NAME} has been created.")

    @classmethod
    def _add_main_console_handler(cls, level=logging.INFO):
        if cls._get_handler_by_name(cls._MAIN_CONSOLE_HANDLER_NAME) is not None:
            cls._logger.debug(f"Main console handler {cls._MAIN_CONSOLE_HANDLER_NAME} is already present - "
                              f"not adding console handler again")
        else:

            # Create a console handler
            console_handler = logging.StreamHandler()
            console_handler.set_name(cls._MAIN_CONSOLE_HANDLER_NAME)
            console_handler.setLevel(level)

            # Create a formatter and add formatter to console handler
            console_handler.setFormatter(cls._formatter())

            # Add console handler to logger
            cls._logger.addHandler(console_handler)
            cls._logger.debug(f"Main console handler {cls._MAIN_CONSOLE_HANDLER_NAME} has been created.")

    @classmethod
    def get_logger(cls):
        if cls._logger is None:
            raise RuntimeError("LogManager is not initialized. Initialize it in test bootstrap first.")
        return cls._logger

    @classmethod
    def add_file_handler(cls, name, absolute_file_path, level=logging.INFO):
        if cls._logger is None:
            cls()

        if name in (cls._MAIN_CONSOLE_HANDLER_NAME, cls._MAIN_FILE_HANDLER_NAME):
            raise ValueError(f"{name} is reserved for internal handlers")

        if name in cls._custom_file_handlers:
            raise ValueError(f"Custom file handler '{name}' already exists.")

        existing_handler = cls._get_handler_by_name(name)
        if existing_handler is not None:
            raise ValueError(f"A file handler named '{name}' already exists on the logger but was not registered "
                             f"via LogManager. Remove it manually before adding it through LogManager.")

        file_handler = cls._build_file_handler(
                name=name,
                absolute_file_path=absolute_file_path,
                level=level,
                mode="w",
        )
        cls._logger.addHandler(file_handler)
        cls._logger.debug(f"Custom file handler {name} has been created.")
        cls._custom_file_handlers[name] = file_handler

    @classmethod
    def remove_file_handler(cls, name):
        if name in (cls._MAIN_CONSOLE_HANDLER_NAME, cls._MAIN_FILE_HANDLER_NAME):
            raise ValueError(f"{name} is reserved for internal handlers")

        if name not in cls._custom_file_handlers:
            raise ValueError(f"Custom file handler '{name}' does not exist on the logger")

        handler = cls._custom_file_handlers.pop(name)
        cls._logger.debug(f"Custom file handler {name} has been deleted.")
        cls._logger.removeHandler(handler)
        handler.close()

    @classmethod
    def remove_all_custom_file_handlers(cls):
        for name in list(cls._custom_file_handlers.keys()):
            cls.remove_file_handler(name)

# # Test/demo usage kept commented out so importing this module has no side effects.
# logger = LogManager.get_logger()
#
# def function_a():
#     LogManager.add_file_handler("functionA", "functionA.log")
#     logger.debug("Debug Message")
#     logger.info("Info Message")
#     LogManager.remove_file_handler("functionA")
#
#
# def function_b():
#     LogManager.add_file_handler("functionB", "functionB.log")
#     logger.warning("Warning Message")
#     logger.error("Error Message")
#     logger.critical("Critical Message")
#     LogManager.remove_file_handler("functionB")
#
# function_b()
# function_a()