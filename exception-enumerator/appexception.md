# Exception Enumerator

## Characteristics and Functionalities

- `GenericException` class for generic exceptions:
- `Timeout` class for timeout exceptions:
- `AppException` class for exception enumerator:
  - `code`: exception code, aliases of `value`
  - `exception`: exception class
  - `message`: exception message, a string
  - `throw`: method to raise exception with code and message

## Tests

Unit tests are implemented with `pytest` for all methods.
