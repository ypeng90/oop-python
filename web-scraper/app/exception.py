"""Custom Exception Models"""


from http import HTTPStatus
from datetime import datetime
import json
import traceback


class AppException(Exception):
    """AppException base class for all exceptions"""
    
    status = HTTPStatus.INTERNAL_SERVER_ERROR
    
    def __init__(self, *args, client_msg=None):
        """

        Args:
            client_msg (str, optional): message for client. Defaults to None.
        """
        if args:
            super().__init__(*args)
            self._internal_msg = args[0]
        else:
            super().__init__(self.status.phrase)
            self._internal_msg = self.status.phrase
        
        if client_msg is not None:
            self._client_msg = client_msg
        else:
            self._client_msg = self._internal_msg
        
        self._time_utc = datetime.utcnow().isoformat()
    
    @property
    def info(self):
        """Information to client

        Returns:
            str: serialized json object of info to user
        """
        data = {
            "code": self.status.value,
            "message": self._client_msg,
            "category": type(self).__name__,
            "time_utc": self._time_utc
        }
        return json.dumps(data)
    
    @property
    def traceback(self):
        """

        Returns:
            _type_: traceback generator
        """
        return traceback.TracebackException.from_exception(self).format()
    
    def log(self):
        """Log information for debug
        """
        ex = {
            "time_utc": self._time_utc,
            "message": self._internal_msg,
            "category": type(self).__name__,
            "args": self.args[1:],
            "traceback": list(self.traceback)
        }
        # TODO: extend
        print(ex)


class ClientException(AppException):
    """ClientException subclass for exceptions caused by client"""
    
    status = HTTPStatus.BAD_REQUEST


class InvalidInputException(AppException):
    """ClientException subclass for exceptions caused by invalid input"""
    
    status = HTTPStatus.BAD_REQUEST


class NotAuthorizedException(ClientException):
    """NotAuthorizedError subclass for exceptions caused by failed client authentication"""
    
    status = HTTPStatus.UNAUTHORIZED


class NotFoundException(ClientException):
    """NotFoundError subclass for exceptions caused by failed resource lookup"""
    
    status = HTTPStatus.NOT_FOUND


class InternalException(AppException):
    """InternalException subclass for exceptions caused by server"""
    
    status = HTTPStatus.INTERNAL_SERVER_ERROR


class APIException(AppException):
    """APIException subclass for exceptions caused by API errors"""
    
    status = HTTPStatus.NOT_IMPLEMENTED


class DBException(InternalException):
    """APIException subclass for exceptions caused by database errors"""
    
    status = HTTPStatus.SERVICE_UNAVAILABLE


class UIException(InternalException):
    """APIException subclass for exceptions caused by UI errors"""
    
    status = HTTPStatus.GATEWAY_TIMEOUT
