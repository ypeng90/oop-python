"""Value Converter Models"""


import decimal
from loguru import logger
import re

logger.add("logs/default.log")


class ValueConverter:
    """Base class
    """
    def __init__(self, value):
        """

        Args:
            value (type): input value
        """
        self.value = value
    
    @property
    def value(self):
        """

        Returns:
            type: converted value
        """
        return self._value
    
    def _set_value(self, value):
        """Convert value to desired type, implemented in subclasses

        Args:
            value (type): input value
        """
        pass
    
    @value.setter
    def value(self, value):
        """

        Args:
            value (type): input value
        """
        self._set_value(value)


class IntConverter(ValueConverter):
    """Convert value to integer
    
    Convert non-boolean value to Decimal object and check if Decimal == int(Decimal). 
    If include_bool_str is True, also check if value is boolean value or any of "t", 
    "true", "f", "false" or related.
    
    Args:
        ValueConverter (type): base class
    """
    def __init__(self, value, *, include_bool_str=False):
        """

        Args:
            value (type): input value
            include_bool_str (bool, optional): convert boolean to integer. Defaults to False.
        """
        self._include_bool_str = include_bool_str
        super().__init__(value)
    
    @logger.catch
    def _set_value(self, value):
        """Convert non-boolean value to Decimal object and check if Decimal == int(Decimal). 
        If include_bool_str is True, also check if value is boolean value or any of "t", 
        "true", "f", "false" or related.

        Args:
            value (type): input value
        """
        self._value = None
        if self._include_bool_str:
            if isinstance(value, str):
                temp = value.strip().casefold()
                if temp in ("t", "true"):
                    self._value = 1
                    return
                if temp in ("f", "false"):
                    self._value = 0
                    return
        try:
            if not self._include_bool_str and isinstance(value, bool):
                raise TypeError
            d = decimal.Decimal(value)
        except (TypeError, decimal.InvalidOperation):
            logger.debug(f"{type(self).__name__} : {value}")
        except:
            logger.exception(f"{type(self).__name__} : {value}")
        else:
            if d == int(d):
                self._value = int(d)


class StrAlnumConverter(ValueConverter):
    """Convert value to string with only alphabetical characters and numbers
    
    Strip and replace all special characters with "".
    
    Args:
        ValueConverter (type): base class
    """
    def __init__(self, value):
        """

        Args:
            value (type): input value
        """
        super().__init__(value)
    
    def _set_value(self, value):
        """Strip and replace all special characters with "".

        Args:
            value (type): input value
        """
        if isinstance(value, str):
            self._value = re.sub("[^A-Za-z0-9]+", "", value.strip())
        else:
            self._value = None
