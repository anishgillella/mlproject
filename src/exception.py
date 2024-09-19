import sys

# Importing the logger from the logger module to log exceptions
from src.logger import logging

# Defining a custom exception class inheriting from the base Exception class
class CustomException(Exception):
    def __init__(self, error_message, error_detail: sys):
        """
        Initialize the CustomException with an error message and error details.
        
        :param error_message: The error message string to be displayed.
        :param error_detail: A sys module reference to extract detailed information about the error.
        """
        super().__init__(error_message)  # Initialize the base class with the error message
        self.error_message = CustomException.get_detailed_error_message(
            error_message, error_detail
        )

    @staticmethod
    def get_detailed_error_message(error_message, error_detail: sys):
        """
        Static method to generate a detailed error message.
        
        :param error_message: The main error message.
        :param error_detail: A sys module reference to get exception details.
        :return: A formatted error message string with detailed error info.
        """
        _, _, exc_tb = error_detail.exc_info()  # Get the traceback object from the sys module
        file_name = exc_tb.tb_frame.f_code.co_filename  # Get the filename where the exception occurred
        line_number = exc_tb.tb_lineno  # Get the line number where the exception occurred
        error_message = f"Error occurred in script: [{file_name}] at line number: [{line_number}] error message: [{error_message}]"
        return error_message

    def __str__(self):
        """
        Override the __str__ method to return the custom error message.
        
        :return: The detailed error message.
        """
        return self.error_message
