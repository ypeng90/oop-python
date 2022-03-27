"""Account models"""

import itertools
import numbers
from datetime import timedelta, datetime
from collections import namedtuple


class TimeZone:
    """Base class for time zones with name and offset"""
    
    def __init__(self, name, offset_hours, offset_minutes):
        """

        Args:
            name (type): time zone name, non-empty
            offset_hours (int): time zone hour offset
            offset_minutes (int): time zone minute offset

        Raises:
            ValueError: name is empty
            ValueError: hour offset is not an integer
            ValueError: minute offset is not an integer in [-59, 59]
            ValueError: calculated offset is not in [-12:00, +14:00]
        """
        if name is None or len(str(name).strip()) == 0:
            raise ValueError("Time zone name cannot be empty.")
        self._name = str(name).strip()
        
        if not isinstance(offset_hours, numbers.Integral):
            raise ValueError("Hours offset must be an integer.")
        if not isinstance(offset_minutes, numbers.Integral) or offset_minutes < -59 or offset_minutes > 59:
            raise ValueError("Minutes offset must be an integer in [-59, 59].")
        # sign of minutes will be set to sign of hours
        offset = timedelta(hours=offset_hours, minutes=offset_minutes)
        # offsets are in [-12:00, 14:00]
        # see https://en.wikipedia.org/wiki/List_of_UTC_time_offsets
        if offset < timedelta(hours=-12, minutes=0) or offset > timedelta(hours=14, minutes=0):
            raise ValueError("Offset must be between -12:00 and +14:00.")
        self._offset_hours = offset_hours
        self._offset_minutes = offset_minutes
        self._offset = offset
    
    @property
    def name(self):
        """

        Returns:
            str: time zone name
        """
        return self._name
    
    @property
    def offset(self):
        """

        Returns:
            timedelta: time zone offset
        """
        return self._offset
    
    def __eq__(self, other):
        """

        Args:
            other (type): other object to be compared

        Returns:
            bool: true only if name, offset_hours, offset_minutes all match
        """
        return (isinstance(other, TimeZone) and 
                self.name == other.name and 
                self._offset_hours == other._offset_hours and
                self._offset_minutes == other._offset_minutes)
    
    def __repr__(self):
        """

        Returns:
            str: detailed representation
        """
        return (f"TimeZone(name='{self.name}', "
                f"offset_hours={self._offset_hours}, "
                f"offset_minutes={self._offset_minutes})")


Confirmation = namedtuple("Confirmation", "account_number, transaction_code, transaction_id, time_utc, time")


class Account:
    """Base class for bank accounts"""
    
    transaction_counter = itertools.count(0)
    _interest_rate = 0.5  # percentage
    
    _transaction_codes = {
        "deposit": "D",
        "withdraw": "W",
        "interest": "I",
        "rejected": "X",
    }
    
    def __init__(self, account_number, first_name, last_name, timezone=None, initial_balance=0):
        """

        Args:
            account_number (type): account number
            first_name (str): first name
            last_name (str): last name
            timezone (TimeZone, optional): preferred time zone. Defaults to None.
            initial_balance (int, optional): initial balance. Defaults to 0.
        """
        self._account_number = account_number
        self.first_name = first_name
        self.last_name = last_name
        
        if timezone is None:
            timezone = TimeZone("UTC", 0, 0)
        self.timezone = timezone
        
        self._balance = Account.validate_real_number(initial_balance, min_value=0)
    
    @property
    def account_number(self):
        """

        Returns:
            str: account number
        """
        return self._account_number
    
    def validate_and_set_name(self, property_name, value, field_title):
        """Validate value and store as value of property_name

        Args:
            property_name (str): property name
            value (type): _description_
            field_title (str): name of field

        Raises:
            ValueError: value is empty
        """
        if len(str(value).strip()) == 0:
            raise ValueError(f"{field_title} cannot be empty.")
        setattr(self, property_name, value)
    
    @property 
    def first_name(self):
        """

        Returns:
            str: first name
        """
        return self._first_name
    
    @first_name.setter
    def first_name(self, value):
        """

        Args:
            value (type): first name
        """
        self.validate_and_set_name("_first_name", value, "First Name")
    
    @property
    def last_name(self):
        """

        Returns:
            str: last name
        """
        return self._last_name
    
    @last_name.setter
    def last_name(self, value):
        """

        Args:
            value (type): last name
        """
        self.validate_and_set_name("_last_name", value, "Last Name")
    
    @property
    def full_name(self):
        """

        Returns:
            str: full name
        """
        return f"{self.first_name} {self.last_name}"
    
    @property
    def timezone(self):
        """

        Returns:
            TimeZone: preferred time zone
        """
        return self._timezone
    
    @timezone.setter
    def timezone(self, value):
        """

        Args:
            value (type): time zone

        Raises:
            ValueError: value is not a TimeZone object
        """
        if not isinstance(value, TimeZone):
            raise ValueError("Time zone must be a valid TimeZone object.")
        self._timezone = value
    
    @property
    def balance(self):
        """

        Returns:
            real: current balance
        """
        return self._balance
    
    @classmethod
    def get_interest_rate(cls):
        """Ensure interest rate is uniformly across all instances and no accidental change

        Returns:
            real: interest rate
        """
        return cls._interest_rate
    
    @classmethod
    def set_interest_rate(cls, value):
        """

        Args:
            value (type): interest rate

        Raises:
            ValueError: value is not a non-negative real number
        """
        if not isinstance(value, numbers.Real) or value < 0:
            raise ValueError("Interest rate must be a non-negative real number.")
        cls._interest_rate = value
    
    @staticmethod
    def validate_real_number(value, min_value=None):
        """Validate value as a real_number no less than min_value if given

        Args:
            value (type): value
            min_value (real, optional): minimal value for lower bound. Defaults to None.

        Raises:
            ValueError: value is not a real number
            ValueError: min_value is not a real number
            ValueError: value is less than min_value

        Returns:
            real: value
        """
        if not isinstance(value, numbers.Real):
            raise ValueError("Value must be a real number.")
        if min_value is not None:
            if not isinstance(min_value, numbers.Real):
                raise ValueError("Min_value must be a real number.")
            if value < min_value:
                raise ValueError(f"Value must be no less than {min_value}.")
        
        return value
    
    def generate_confirmation_code(self, transaction_code):
        """

        Args:
            transaction_code (str): transaction code

        Returns:
            str: confirmation code
        """
        dt_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
        return f"{transaction_code}-{self.account_number}-{dt_str}-{next(Account.transaction_counter)}"
    
    @staticmethod
    def parse_confirmation_code(confirmation_code, preferred_time_zone=None):
        """

        Args:
            confirmation_code (str): confirmation code
            preferred_time_zone (TimeZone, optional): preferred time zone. Defaults to None.

        Raises:
            ValueError: confirmation code does not contain four parts joined by "-"
            ValueError: datetime string in confirmation code is not a valid datetime string
            ValueError: preferred time zone is not a TimeZone object

        Returns:
            Confirmation: Confirmation object
        """
        # X-A100-20190325224918-101
        parts = confirmation_code.split("-")
        if len(parts) != 4:
            raise ValueError("Invalid confirmation code.")
        
        # unpack into separate variables
        transaction_code, account_number, raw_dt_utc, transaction_id = parts
        
        # convert raw_dt_utc to a proper datetime object
        try:
            dt_utc = datetime.strptime(raw_dt_utc, "%Y%m%d%H%M%S")
        except ValueError as e:
            raise ValueError("Invalid transaction datetime.") from e
        
        if preferred_time_zone is None:
            preferred_time_zone = TimeZone("UTC", 0, 0)
        
        if not isinstance(preferred_time_zone, TimeZone):
            raise ValueError("Invalid TimeZone specified.")
        
        dt_preferred = dt_utc + preferred_time_zone.offset
        dt_preferred_str = f"{dt_preferred.strftime('%Y-%m-%d %H:%M:%S')} ({preferred_time_zone.name})"
        
        return Confirmation(account_number, transaction_code, transaction_id, dt_utc.isoformat(), dt_preferred_str)
    
    def deposit(self, value):
        """

        Args:
            value (type): value

        Returns:
            str: confirmation code
        """
        value = Account.validate_real_number(value, min_value=0.01)
        
        transaction_code = Account._transaction_codes["deposit"]
        conf_code = self.generate_confirmation_code(transaction_code)
        
        # deposit only when everything works
        self._balance += value
        
        return conf_code
    
    def withdraw(self, value):
        """

        Args:
            value (type): value

        Returns:
            str: confirmation code
        """
        value = Account.validate_real_number(value, min_value=0.01)
        
        accepted = False
        if self.balance - value < 0:
            # insufficient funds
            transaction_code = Account._transaction_codes["rejected"]
        else:
            transaction_code = Account._transaction_codes["withdraw"]
            accepted = True
        conf_code = self.generate_confirmation_code(transaction_code)
        
        # withdraw only when everything works
        if accepted:
            self._balance -= value
        
        return conf_code
    
    def pay_interest(self):
        """

        Returns:
            str: confirmation code
        """
        # emphasize interest rate is uniformly accross all instances
        interest = self.balance * Account.get_interest_rate() / 100
        
        conf_code = self.generate_confirmation_code(Account._transaction_codes["interest"])
        
        # pay interest only when everything works
        self._balance += interest
        
        return conf_code


