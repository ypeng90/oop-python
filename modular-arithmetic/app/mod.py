from functools import total_ordering
import operator


@total_ordering
class Mod:
    """Mod class to store residue and modulus"""
    
    def __init__(self, modulus, residue):
        """

        Args:
            modulus (type): modulus
            residue (type): raw residue

        Raises:
            TypeError: modulus is not an integer
            ValueError: modulus is positive
            TypeError: value is not an integer
        """
        if not isinstance(modulus, int):
            raise TypeError("Modulus can only be an integer.")
        if modulus <= 0:
            raise ValueError("Modulus can only be positive.")
        if not isinstance(residue, int):
            raise TypeError("Value can only be an integer.")

        self._modulus = modulus
        self._residue = residue % modulus
    
    @property
    def modulus(self):
        """

        Returns:
            int: modulus
        """
        return self._modulus
    
    @modulus.setter
    def modulus(self, value):
        """

        Args:
            value (int): value
        """
        self._modulus = value
    
    @property
    def residue(self):
        """

        Returns:
            int: residue
        """
        return self._residue
    
    @residue.setter
    def residue(self, value):
        """

        Args:
            value (int): value
        """
        self._residue = value
    
    def __int__(self):
        """

        Returns:
            int: residue
        """
        return self.residue
    
    def __repr__(self):
        """

        Returns:
            str: detailed representation
        """
        return f"Mod({self._modulus}, {self._residue})"
    
    def _get_residue(self, other):
        """Get residue from other Mod object or integer value

        Args:
            other (type): other

        Raises:
            TypeError: other is not a Mod object or an integer

        Returns:
            int: residue
        """
        if isinstance(other, Mod) and self.modulus == other.modulus:
            return other.residue
        if isinstance(other, int):
            return other % self.modulus
        raise TypeError("Incompatible types: Mod object with same modulus, or integer.")
    
    def __eq__(self, other):
        """Equality based on residue

        Args:
            other (type): other

        Returns:
            bool: True if two residues equal
        """
        other_residue = self._get_residue(other)
        return other_residue == self.residue
    
    def __lt__(self, other):
        """Ordering based on residue

        Args:
            other (type): other

        Returns:
            bool: True if residue of self is less than that of other
        """
        # raising TypeError instead of returning NotImplemented would result in 
        # Python not trying reflection, which is ok since using @total_ordering
        other_residue = self._get_residue(other)
        return self.residue < other_residue
    
    def __hash__(self):
        """

        Returns:
            int: hash value
        """
        return hash((self.modulus, self.residue))
    
    def __neg__(self):
        """

        Returns:
            Mod: a Mod object
        """
        return Mod(self.modulus, -self.residue)
    
    def _perform_operation(self, other, op, *, in_place=False):
        """Universal operations

        Args:
            other (type): other
            op (function): operator
            in_place (bool, optional): in-place modification. Defaults to False.

        Returns:
            Mod: a Mod object
        """
        other_residue = self._get_residue(other)
        new_residue = op(self.residue, other_residue)
        if in_place:
            self.residue = new_residue % self.modulus
            return self
        return Mod(self.modulus, new_residue)
    
    def __add__(self, other):
        """

        Returns:
            Mod: a new Mod object
        """
        return self._perform_operation(other, operator.add)
    
    def __iadd__(self, other):
        """

        Returns:
            Mod: a modified Mod object
        """
        return self._perform_operation(other, operator.add, in_place=True)
    
    def __sub__(self, other):
        """

        Returns:
            Mod: a new Mod object
        """
        return self._perform_operation(other, operator.sub)
    
    def __isub__(self, other):
        """

        Returns:
            Mod: a modified Mod object
        """
        return self._perform_operation(other, operator.sub, in_place=True)
    
    def __mul__(self, other):
        """

        Returns:
            Mod: a new Mod object
        """
        return self._perform_operation(other, operator.mul)
    
    def __imul__(self, other):
        """

        Returns:
            Mod: a modified Mod object
        """
        return self._perform_operation(other, operator.mul, in_place=True)
    
    def __pow__(self, other):
        """

        Returns:
            Mod: a new Mod object
        """
        return self._perform_operation(other, operator.pow)
    
    def __ipow__(self, other):
        """

        Returns:
            Mod: a modified Mod object
        """
        return self._perform_operation(other, operator.pow, in_place=True)

