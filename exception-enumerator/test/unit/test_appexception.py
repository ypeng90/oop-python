"""
Tests for AppException class
Command line: python -m pytest test/unit
"""

from re import A
import pytest

from app.appexception import GenericException, Timeout, AppException

@pytest.mark.parametrize("message", [None, ""])
def test_throw_default_ok(message):
    with pytest.raises(Timeout) as e:
        AppException.Timeout.throw(message)
        assert e == "Timeout connecting to resource."

@pytest.mark.parametrize("name, code, message", [("Generic", 100, "test"), ("Timeout", 101, "test")])
def test_throw_custom_ok(name, code, message):
    member = getattr(AppException, name)
    with pytest.raises(member.exception) as e:
        member.throw(message)
        assert e == f"{code} - {message}"

@pytest.mark.parametrize("message", [123, ("test",)])
def test_throw_default_invalid(message):
    with pytest.raises(TypeError):
        AppException.Timeout.throw(message)
