# Bank Account

## Characteristcs and Functionalities

- `TimeZone` class for preferred time zone:
  - `name`: time zone name
  - `offset`: time zone offset computed from given `offset_hours` and `offset_minutes`
  - `__eq__`: ordering
  - `__repr__`: detailed representation
- `Account` base class provides common attributes and functionalities to all accounts:
  - `account_number`: uniquely identifier, passed in the initializer
  - `first_name`: first name, passed in the initializer
  - `last_name`: last name, passed in the initializer
  - `full_name`: full name, computed from `first_name` and `last_name`
  - `timezone`: preferred time zone, e.g. -7 for MST
  - `balance`: balance, non-negative
  - `get_interest_rate`: method to get monthly interest rate, which is uniform across all accounts
  - `set_interest_rate`: method to set monthly interest rate, which is uniform across all accounts
  - `transaction_counter`: counter to generate auto-incremented number
  - `generate_confirmation_code`: method to generate confirmation code composed of:
    - `transaction_code`: "D" for `deposit`, "W" for `withdraw`, "I" for `pay_interest`, and "X" for failed transactions
    - `account_number`
    - timestamp in UTC
    - transaction id: an unqiue number that increments across all accounts and transactions
  - `deposit`: method to deposit with confirmation code generated
  - `withdraw`: method to withdraw with confirmation code generated
  - `pay_interest`: method to pay monthly interest with confirmation code generated

## Unit Tester

- Implemented with `unittest`
