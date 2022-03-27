"""Validator models"""


import numbers


class BaseValidator:
    """Base class for validators"""
    
    def __init__(self, min_=None, max_=None):
        """

        Args:
            min_ (int, optional): minimal value for lower bound. Defaults to None.
            max_ (int, optional): maximal value for upper bound. Defaults to None.
        """
        self._min = min_
        self._max = max_
    
    def __set_name__(self, owner_class, prop_name):
        """Set property name

        Args:
            owner_class (type): owner class
            prop_name (str): property name
        """
        self.prop_name = prop_name
    
    def __get__(self, instance, owner_class):
        """Get instance or value depending on where it is called from

        Args:
            instance (type): instance from which it is called
            owner_class (type): class from which it is called

        Returns:
            type: instance if called from class
            str: value if called from instance
        """
        if instance is None:
            return self
        else:
            return instance.__dict__.get(self.prop_name, None)
    
    def validate(self, value):
        """Validate value, implemented specifically in each subclass

        Args:
            value (type): value type
        """
        pass
    
    def __set__(self, instance, value):
        """Call validate(value) and store value in instance if valid

        Args:
            instance (type): instance where it is called from
            value (type): value type
        """
        self.validate(value)
        instance.__dict__[self.prop_name] = value


class IntegerValidator(BaseValidator):
    def validate(self, value):
        """Validate value as an integer between bounds, if any

        Args:
            value (type): value type

        Raises:
            ValueError: value is not an integer
            ValueError: value is less than lower bound
            ValueError: value is larger than upper bound
        """
        if not isinstance(value, numbers.Integral):
            raise ValueError(f"{self.prop_name} must be an integer.")
        if self._min is not None and value < self._min:
            raise ValueError(f"{self.prop_name} must be >= {self._min}.")
        if self._max is not None and value > self._max:
            raise ValueError(f"{self.prop_name} must be <= {self._max}.")


class StringValidator(BaseValidator):
    def __init__(self, min_, max_):
        """Enforce min_ as non-negative

        Args:
            min_ (int or None): minimal value for lower bound. Enforced as non-negative.
            max_ (int or None): maximal value for upper bound.
        """
        min_ = max(min_ or 0, 0)
        super().__init__(min_, max_)
    
    def validate(self, value):
        """Validate value as a string with length between bounds, if any

        Args:
            value (type): value type

        Raises:
            ValueError: value is not a string
            ValueError: value is shorter than lower bound
            ValueError: value is longer than upper bound
        """
        if not isinstance(value, str):
            raise ValueError(f"{self.prop_name} must be a string.")
        if self._min is not None and len(value) < self._min:
            raise ValueError(f"{self.prop_name} must be >= {self._min} chars.")
        if self._max is not None and len(value) > self._max:
            raise ValueError(f"{self.prop_name} must be <= {self._max} chars.")
