"""
Tests for Resource class
Command line: python -m pytest tests/unit
"""

import pytest

from app.mod import Mod


@pytest.fixture
def mod_values():
    return {
        "modulus": 10,
        "residue": 3
    }

@pytest.fixture
def mod(mod_values):
    return Mod(**mod_values)

@pytest.mark.parametrize("modulus, residue", [(10, 3), (10, -1), (10, 13)])
def test_create_mod_ok(modulus, residue):
    mod = Mod(modulus, residue)
    assert getattr(mod, "modulus") == modulus
    assert getattr(mod, "residue") == residue % modulus

@pytest.mark.parametrize("modulus", ["10", 10.0, (10,)])
def test_create_mod_invalid_modulus_type(mod_values, modulus):
    mod_values["modulus"] = modulus
    with pytest.raises(TypeError):
        Mod(**mod_values)

def test_create_mod_negative_modulus(mod_values):
    mod_values["modulus"] = -10
    with pytest.raises(ValueError):
        Mod(**mod_values)

@pytest.mark.parametrize("residue", ["3", 3.0, (3,)])
def test_create_mod_invalid_residue_type(mod_values, residue):
    mod_values["residue"] = residue
    with pytest.raises(TypeError):
        Mod(**mod_values)

def test_int_ok(mod):
    assert int(mod) == mod.residue

def test_repr_ok(mod_values, mod):
    assert repr(mod) == f"Mod({mod_values['modulus']}, {mod_values['residue']})"

# also test get_residue
# can not use mod in parametrize
@pytest.mark.parametrize("other", [Mod(10, 3), Mod(10, 13), 3])
def test_eq_ok(mod, other):
    assert mod == other

# also test get_residue
@pytest.mark.parametrize("other", [Mod(13, 3), (10, 3)])
def test_eq_invalid(mod, other):
    with pytest.raises(TypeError):
        mod == other

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_lt_ok(mod, other):
    assert mod < other

def test_hash_ok(mod, mod_values):
    assert hash((mod.modulus, mod.residue)) == hash((mod_values["modulus"], mod_values["residue"]))

def test_neg_ok(mod, mod_values):
    neg_mod = -mod
    assert neg_mod.residue == mod_values["modulus"] - mod_values["residue"]

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_add_ok(mod, other):
    result = mod + other
    assert result.residue == 7

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_iadd_ok(mod, other):
    mod += other
    assert mod.residue == 7

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_sub_ok(mod, other):
    result = mod - other
    assert result.residue == 9

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_isub_ok(mod, other):
    mod -= other
    assert mod.residue == 9

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_mul_ok(mod, other):
    result = mod * other
    assert result.residue == 2

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_imul_ok(mod, other):
    mod *= other
    assert mod.residue == 2

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_pow_ok(mod, other):
    result = mod ** other
    assert result.residue == 1

@pytest.mark.parametrize("other", [Mod(10, 4), Mod(10, 14), 4])
def test_ipow_ok(mod, other):
    mod **= other
    assert mod.residue == 1
