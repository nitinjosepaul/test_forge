import logging
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

import config
from library.util.log import Log
from library.test.test_executor import TestExecutor
from library.util.log import ScrolledTextWidgetHandler


class ADInstall(tk.Tk):
    scrolled_text_widget = None

    def __init__(self):
        self.log = Log()
        self.test_executor = TestExecutor()
        super().__init__()
        self.title(f"{config.APPLICATION_NAME} {config.APPLICATION_VERSION}")
        self.geometry("700x600")
        self.resizable(False, False)
        self.create_widgets()
        self.thread = None

    def create_widgets(self):
        self.create_main_sections()
        self.create_widgets_test_section()
        self.create_widgets_logs_section()
        self.create_widgets_status_bar_section()

    # noinspection PyAttributeOutsideInit
    def create_main_sections(self):
        self.labelframe_test = tk.LabelFrame(self, text="Test")
        self.labelframe_test.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.labelframe_logs = tk.LabelFrame(self, text="Logs")
        self.labelframe_logs.pack(fill=tk.BOTH, expand=False, padx=5, pady=5)

        self.frame_status_bar = tk.Frame(self, relief=tk.SUNKEN, bd=1, height=30)
        self.frame_status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    # noinspection PyAttributeOutsideInit
    def create_widgets_test_section(self):
        self.frame_configure = ttk.Frame(self.labelframe_test)
        self.frame_configure.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.frame_selected_file = ttk.Frame(self.labelframe_test)
        self.frame_selected_file.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        self.button_select_xml_file = ttk.Button(self.frame_configure,
                                                 text="Select ADInstall xml",
                                                 command=self.on_click_button_select_xml_file)
        self.button_select_xml_file.pack(side=tk.LEFT, padx=5, pady=5)

        self.button_start = ttk.Button(self.frame_configure,
                                       text="Start",
                                       command=self.start_test_thread)
        self.button_start.pack(side=tk.RIGHT, padx=5, pady=5)

        self.dropdown_test_suites = ttk.Combobox(self.frame_configure, values=self.test_executor.get_test_suite_names())

        self.dropdown_test_suites.pack(side=tk.RIGHT, padx=5, pady=5)
        self.dropdown_test_suites.set("Select")

        self.label_target = ttk.Label(self.frame_configure, text="Test Suite :")
        self.label_target.pack(side=tk.RIGHT, padx=5, pady=5)

        self.label_file = ttk.Label(self.frame_selected_file, text="File :")
        self.label_file.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_current_file_name = ttk.Label(self.frame_selected_file, text="<NOT SELECTED>")
        self.label_current_file_name.pack(side=tk.LEFT, pady=5)

    # noinspection PyAttributeOutsideInit
    def create_widgets_logs_section(self):
        self.button_clear = ttk.Button(self.labelframe_logs, text="Clear", command=self.clear_log)
        self.button_clear.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # Create a ScrolledText widget to display the log
        self.scrolled_text_widget = ScrolledText(self.labelframe_logs, state=tk.DISABLED)
        self.scrolled_text_widget.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")

        # Configure different colors for different tags
        self.scrolled_text_widget.tag_configure(tagName='ERROR', foreground='orange')
        # self.scrolled_text_log.tag_configure(tagName='TEST_PASSED', foreground='green')
        # self.scrolled_text_log.tag_configure(tagName='TEST_FAILED', foreground='red')

        # Assign object
        ScrolledTextWidgetHandler.set_value(self.scrolled_text_widget)        # TODO need to change the class name

    # noinspection PyAttributeOutsideInit
    def create_widgets_status_bar_section(self):
        self.execution_status_label = tk.Label(self.frame_status_bar, text="Status: IDLE", anchor="w")
        self.execution_status_label.pack(side=tk.LEFT, padx=5)

        self.adinstall_version_label = tk.Label(self.frame_status_bar, text=f"ADInstall Version: 201.6.04", anchor="e")
        self.adinstall_version_label.pack(side=tk.RIGHT, padx=5)

    def clear_log(self):
        self.scrolled_text_widget.config(state=tk.NORMAL)  # Make the Text widget editable
        self.scrolled_text_widget.delete(1.0, tk.END)  # Delete all text
        self.scrolled_text_widget.config(state=tk.DISABLED)  # Make the Text widget read-only again

    def on_click_button_select_xml_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.label_current_file_name.config(text=file_path)

    def get_selected_test_suite(self):
        selected_test_suite = self.dropdown_test_suites.get()
        if selected_test_suite.lower() == 'select':
            logging.warning("Please select a test suite first")
            return False
        elif selected_test_suite not in self.test_executor.get_test_suite_names():
            logging.warning("Please select a test suite first")
            return False
        return selected_test_suite

    def start_test_thread(self):
        selected_test_suite = self.get_selected_test_suite()
        if selected_test_suite:
            self.button_start.config(state=tk.DISABLED)
            self.thread = threading.Thread(target=self.test_executor.execute_test_suite,
                                           args=(selected_test_suite, self.update_execution_status))
            self.thread.start()
            self.check_thread_status()

    def check_thread_status(self):
        if self.thread.is_alive():
            self.after(100, self.check_thread_status)
        else:
            self.button_start.config(state=tk.NORMAL)

    def update_execution_status(self, status, name=None, execution_time=None):
        if status == config.EXECUTION_STATUS_IDLE:
            self.execution_status_label.config(text=f"Status: {status}")

        elif status == config.EXECUTION_STATUS_RUNNING and name:
            self.execution_status_label.config(text=f"Status: {status} | {name}")

        elif status == config.EXECUTION_STATUS_COMPLETED and execution_time:
            self.execution_status_label.config(text=f"Status: {status} | Duration {execution_time}")
