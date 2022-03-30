"""Inventory models"""


from app.utilities import validate_integer


class Resource:
    """Base class for all resources"""

    def __init__(self, name, manufacturer, total, allocated):
        """

        Args:
            name (str): resource name
            manufacturer (str): resource manufacturer
            total (int): current total count of resource
            allocated (int): current count of in-use resource

        Note:
            `allocated` cannot exceed `total`
        """
        self._name = name
        self._manufacturer = manufacturer

        validate_integer("total", total, min_value=0)
        self._total = total

        validate_integer(
            "allocated", allocated, 0, total,
            custom_max_message="Allocated count cannot exceed total count."
        )
        self._allocated = allocated

    @property
    def name(self):
        """

        Returns:
            str: resource name
        """
        return self._name

    @property
    def manufacturer(self):
        """

        Returns:
            str: resource manufacturer
        """
        return self._manufacturer

    @property
    def total(self):
        """

        Returns:
            int: current total count of resource
        """
        return self._total

    @property
    def allocated(self):
        """

        Returns:
            int: current count of resources in use
        """
        return self._allocated

    @property
    def category(self):
        """

        Returns:
            str: resource category
        """
        return type(self).__name__.lower()

    @property
    def available(self):
        """

        Returns:
            int: current count of available resource
        """
        return self.total - self.allocated

    def __str__(self):
        return self.name

    def __repr__(self):
        """

        Returns:
            str: detailed representation
        """
        return (
            f"{self.name} ({self.category} - {self.manufacturer}) : "
            f"total={self.total}, allocated={self.allocated}"
        )

    def allocate(self, count):
        """Allocate count of resource items if available

        Args:
            count (int): count of resource to be allocated

        Returns:

        """
        validate_integer(
            "count", count, 1, self.available,
            custom_max_message="Cannot allocate more than available."
        )
        self._allocated += count

    def freeup(self, count):
        """Reset count of allocated resource items, if not more than allocated, 
        to be available

        Args:
            num (int): count of resource to be available

        Returns:

        """
        validate_integer(
            "count", count, 1, self.allocated,
            custom_max_message="Cannot reset more than allocated."
        )
        self._allocated -= count

    def died(self, count):
        """Remove count of allocated resource items, if not more than allocated, 
        from total and allocated

        Args:
            count (int): count of died resource

        Returns:

        """
        validate_integer(
            "count", count, 1, self.allocated,
            custom_max_message="Cannot retire more than allocated."
        )
        self._total -= count
        self._allocated -= count

    def purchased(self, count):
        """Add count of new resource items to total

        Args:
            count (int): count of new resource to be available

        Returns:

        """
        validate_integer("count", count, 1)
        self._total += count


class CPU(Resource):
    """Resource subclass for CPU resources"""

    def __init__(
        self, name, manufacturer, total, allocated,
        cores, socket, power_watts
    ):
        """

        Args:
            name (str): resource name
            manufacturer (str): resource manufacturer
            total (int): current total count of resource
            allocated (int): current count of in-use resource
            cores (int): number of cores
            socket (str): socket type
            power_watts (int): rated wattage
        """
        super().__init__(name, manufacturer, total, allocated)

        validate_integer("cores", cores, 1)
        validate_integer("power_watts", power_watts, 1)

        self._cores = cores
        self._socket = socket
        self._power_watts = power_watts

    @property
    def cores(self):
        """

        Returns:
            int: number of cores
        """
        return self._cores

    @property
    def socket(self):
        """

        Returns:
            str: socket type
        """
        return self._socket

    @property
    def power_watts(self):
        """

        Returns:
            int: rated wattage
        """
        return self._power_watts

    def __repr__(self):
        return f"{self.category}: {self.name} ({self.socket} - x{self.cores})"


class Storage(Resource):
    """Resource subclass for storage devices"""

    def __init__(self, name, manufacturer, total, allocated, capacity_gb):
        """

        Args:
            name (str): resource name
            manufacturer (str): resource manufacturer
            total (int): current total count of resource
            allocated (int): current count of in-use resource
            capacity_gb (int): storage capacity in GB
        """
        super().__init__(name, manufacturer, total, allocated)
        validate_integer("capacity_gb", capacity_gb, 1)
        self._capacity_gb = capacity_gb

    @property
    def capacity_gb(self):
        """

        Returns:
            int: storage capacity in GB
        """
        return self._capacity_gb

    def __repr__(self):
        return f"{self.category}: {self.capacity_gb} GB"


class HDD(Storage):
    """Storage subclass for HDD-type storage"""

    def __init__(
        self, name, manufacturer, total, allocated, capacity_gb,
        size, rpm
    ):
        """

        Args:
            name (str): resource name
            manufacturer (str): resource manufacturer
            total (int): current total count of resource
            allocated (int): current count of in-use resource
            capacity_gb (int): storage capacity in GB
            size (str): device size, 2.5" or 3.5"
            rpm (int): disk rotation speed in rpm
        """
        super().__init__(name, manufacturer, total, allocated, capacity_gb)

        allowed_sizes = ['2.5"', '3.5"']
        if size not in allowed_sizes:
            raise ValueError(
                f"Invalid HDD size. "
                f"Must be one of {', '.join(allowed_sizes)}"
            )
        validate_integer("rpm", rpm, min_value=1_000, max_value=50_000)

        self._size = size
        self._rpm = rpm

    @property
    def size(self):
        """

        Returns:
            str: device size, 2.5" or 3.5"
        """
        return self._size

    @property
    def rpm(self):
        """

        Returns:
            int: disk rotation speed in rpm
        """
        return self._rpm

    def __repr__(self):
        s = super().__repr__()
        return f"{s} ({self.size}, {self.rpm} rpm)"


class SSD(Storage):
    """Storage subclass for SSD-type storage"""

    def __init__(
            self, name, manufacturer, total, allocated, capacity_gb,
            interface
    ):
        """

        Args:
            name (str): resource name
            manufacturer (str): resource manufacturer
            total (int): current total count of resource
            allocated (int): current count of in-use resource
            capacity_gb (int): storage capacity in GB
            interface (str): device interface, e.g. PCIe NVMe 3.0 x4
        """
        super().__init__(name, manufacturer, total, allocated, capacity_gb)

        self._interface = interface

    @property
    def interface(self):
        """

        Returns:
            str: device interface, e.g. PCIe NVMe 3.0 x4
        """
        return self._interface

    def __repr__(self):
        s = super().__repr__()
        return f"{s} ({self.interface})"
