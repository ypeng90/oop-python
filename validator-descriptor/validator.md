# Input Validator

## Characteristcs and Functionalities

- `BaseValidator` base class provides common attributes and functionalities to all validators:
  - `_min`: lower bound, default to None
  - `_max`: upper bound, default to None
  - `prop_name`: property name
  - `__get__`: get instance or value depending on where it is called from
  - `validate`: validate value, implemented specifically in each subclass
  - `__set__`: call validate(value) and store value in instance if valid
- `IntegerValidator` subclass provides integer-specific implementation:
  - `validate`: validate value as an integer between bounds, if any
- `StringValidator` subclass provides extra string-specific implementation:
  - `_min`: lower bound, enforced as non-negative
  - `validate`: validate value as a string with length between bounds, if any

## Unit Tester

- Implemented with `unittest`
