# Exception Handler

## Characteristcs and Functionalities

- `AppException` base class provides common attributes and functionalities to all exceptions
  - `status`: status corresponding to a `HTTPStatus` member
  - `_internal_msg`: message to developer
  - `_client_msg`: message to client
  - `_time_utc`: timestamp in UTC when exception is raised
  - `info`: information to client, including:
    - `code`: HTTP status code corresponding to `status`
    - `message`: message to client
    - `category`: exception category
    - `time_utc`: timestamp in UTC when exception is raised
  - `traceback`: exception traceback generator
  - `log`: method to log exception to debug
- `ClientException` subclass for exceptions caused by client
  - `NotAuthorizedException` subclass for exceptions caused by failed client authentication
  - `NotFoundException` subclass for exceptions caused by failed resource lookup
- `InternalException` subclass for exceptions caused by server
  - `APIException` subclass for exceptions caused by API errors
  - `DBException` subclass for exceptions caused by database errors
  - `UIException` subclass for exceptions caused by UI errors

## Unit Tester

- Implemented with `unittest`
