"""
Tests for Converter classes
Command line: python -m pytest tests/unit/test_converter.py
"""

import pytest
from app.converter import IntConverter, StrAlnumConverter


@pytest.mark.parametrize(
    "input, output",
    [
        (5, 5),
        (-5, -5),
        (5., 5),
        (-5., -5),
        (5.0, 5),
        (-5.0, -5),
        ("5", 5),
        ("-5", -5),
        ("5.", 5),
        ("-5.", -5),
        ("5.0", 5),
        ("-5.0", -5),
        (" -5", -5),
        ("-5 ", -5),
        (" -5 ", -5),
        (5.5, None),
        ("5.5", None),
        (True, None),
        (bool(10), None),
        (1 == 1, None),
        (False, None),
        (bool(0), None),
        (1 == 2, None),
        ("t", None),
        ("true", None),
        ("f", None),
        ("false", None),
        (dict(), None),
    ]
)
def test_intconverter_ok(input, output):
    assert IntConverter(input).value == output

@pytest.mark.parametrize(
    "input, output",
    [
        ("t", 1),
        ("T", 1),
        ("true", 1),
        ("True", 1),
        ("TRUE", 1),
        ("f", 0),
        ("F", 0),
        ("false", 0),
        ("False", 0),
        ("FALSE", 0),
        (True, 1),
        (bool(10), 1),
        (1 == 1, 1),
        (False, 0),
        (bool(0), 0),
        (1 == 2, 0),
    ]
)
def test_intconverter_include_boolean_ok(input, output):
    assert IntConverter(input, include_bool_str=True).value == output

@pytest.mark.parametrize(
    "input, output",
    [
        ("a", "a"),
        (" a", "a"),
        ("a ", "a"),
        (" a ", "a"),
        ("a;", "a"),
        ("a\;", "a"),
        ("&a|", "a"),
        ([], None),
    ]
)
def test_stralnumconverter_ok(input, output):
    assert StrAlnumConverter(input).value == output
