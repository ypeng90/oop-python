# Modular Arithmetic

## Characteristics and Functionalities

- `Mod` class for modular arithmetic:
  - `modulus`: modulus, postive integer passed in initializer
  - `residue`: residue, non-negative integer computed from passed value in initializer
  - `__int__`: method to implement `int()`
  - `__repr__`: method to implement `repr()`
  - `__eq__`: method to check equality based on `residue`
  - `__lt__`: method to check ordering based on `residue`
  - `__hash__`: method to compute hash value based on `modulus` and `residue`
  - `__neg__`: method to negate `residue`
  - `__add__`: method to add residue values of self and other to create a new Mod object
  - `__iadd__`: method to add residue values of self and other to modify residue of self
  - `__sub__`: method to subtract residue values of other from that of self to create a new Mod object
  - `__isub__`: method to subtract residue values of other from that of self to modify residue of self
  - `__mul__`: method to multiply residue values of self and other to create a new Mod object
  - `__imul__`: method to multiply residue values of self and other to modify residue of self
  - `__pow__`: method to raise residue values of self to power of that of other to create a new Mod object
  - `__ipow__`: method to raise residue values of self to power of that of other to modify residue of self

## Tests

Unit tests are implemented with `pytest` for all methods.
