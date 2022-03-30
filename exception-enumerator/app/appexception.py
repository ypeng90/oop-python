"""Exception models"""

from enum import Enum
from tkinter.messagebox import NO


class GenericException(Exception):
    """GenericException base class for all custom exceptions"""
    
    pass


class Timeout(Exception):
    """Timeout base class"""
    
    pass


class AppException(Enum):
    """AppException base class"""
    
    Generic = (100, GenericException, "Application exception.")
    Timeout = (101, Timeout, "Timeout connecting to resource.")
    NotAnInteger = (200, ValueError, "Value must be an integer.")
    NotAList = (201, ValueError, "Value must be a list.")
    
    def __new__(cls, ex_code, ex_class, ex_message):
        """

        Args:
            ex_code (int): exception code
            ex_class (type): exception class
            ex_message (str): exception default message

        Returns:
            AppException: instance
        """
        # create a new instance of cls
        member = object.__new__(cls)
        
        # set up instance attributes
        member._value_ = ex_code
        member.exception = ex_class
        member.message = ex_message
        return member
    
    @property
    def code(self):
        """Aliase of value

        Returns:
            int: exception code
        """
        return self.value
    
    def throw(self, message=None):
        """Raise exception

        Args:
            message (type, optional): exception message. Defaults to None.

        Raises:
            TypeError: message is not a string
            self.exception: exception with code and message
        """
        if message is not None and not isinstance(message, str):
            raise TypeError("Message must be a string.")
        message = message or self.message
        raise self.exception(f"{self.code} - {message}")
