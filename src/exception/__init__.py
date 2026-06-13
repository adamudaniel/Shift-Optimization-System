import os
import sys
import logging

def error_message_detail(error: Exception, error_detail: sys) -> str:
    # extracting the traceback details from the exception information
    _, _, exc_tb = error_detail.exc_info()

    if exc_tb is not None:
        # getting the filename where the exception occurred
        file_name = exc_tb.tb_frame.f_code.co_filename
        # create the formatted error message with filename, line number, and error message

        # getting the line number where the exception occurred
        line_number = exc_tb.tb_lineno
    else:
        file_name = "Unknown File"
        line_number = "Unknown Line"


    error_message = f"Error occurred in python script name [{file_name}] line number [{line_number}] error message [{str(error)}]"

    logging.error(error_message)  # Log the error message

    return error_message

class CustomException(Exception):
    def __init__(self, error_message: str, error_detail: sys):
        super().__init__(error_message)
        self.error_message = error_message_detail(error_message, error_detail)

    def __str__(self):
        # return the error message in proper format when the exception is printed
        return self.error_message