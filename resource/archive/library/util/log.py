import os
import logging
import tkinter as tk
import config


class ScrolledTextWidgetHandler(logging.Handler):
    _scrolled_text_widget = None

    def __init__(self):
        super().__init__()

    @classmethod
    def set_value(cls, value):
        cls._scrolled_text_widget = value

    def emit(self, record):
        message = self.format(record)
        # Make the Text widget editable
        ScrolledTextWidgetHandler._scrolled_text_widget.config(state=tk.NORMAL)
        # Insert the new log message
        ScrolledTextWidgetHandler._scrolled_text_widget.insert(tk.END, message + "\n")
        # Make the Text widget read-only again
        ScrolledTextWidgetHandler._scrolled_text_widget.config(state=tk.DISABLED)
        # Scroll to the end of the log
        ScrolledTextWidgetHandler._scrolled_text_widget.see(tk.END)


class Log:

    def __init__(self, console_logging=True):
        # Check if log directory already exists, create if required
        if not os.path.exists(config.log_dir):
            os.makedirs(config.log_dir)

        self.logger = None
        self._initialize_logger()
        self.add_file_handler()
        if console_logging:
            self.add_console_handler()

    def _initialize_logger(self):
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)

    def add_file_handler(self, filename=None):
        if not filename:
            filename = os.path.join(config.log_dir, 'main.log')

        file_handler = logging.FileHandler(filename, mode='w')

        # Set the minimum level for the file handler
        file_handler.setLevel(logging.DEBUG)

        # Create a foramtter and add to file handler
        file_formatter = logging.Formatter('[%(asctime)s] [%(module)s] [%(levelname)s] %(message)s')
        file_handler.setFormatter(file_formatter)

        # Add file handler to logger
        self.logger.addHandler(file_handler)

    def add_console_handler(self):
        console_handler = ScrolledTextWidgetHandler()

        # Set the minimum level for console handler
        console_handler.setLevel(logging.INFO)

        # Create a foramtter and add to console handler
        console_formatter = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_formatter)

        # Add console handler to logger
        self.logger.addHandler(console_handler)